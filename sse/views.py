from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from .models import *
from rest_framework.response import Response
import json
from django.db.models import Q
from django.db import transaction, IntegrityError
from django_eventstream import send_event, get_current_event_id
from django.core.serializers.json import DjangoJSONEncoder


def messages(request, channels_id):
    if request.method == 'GET':
        event_count = get_current_event_id(['channels-{}'.format(channels_id)])
        print("channels_id: ", channels_id)
        print("event_count: ", event_count)
        # try:
        #     room = ChatRoom.objects.get(eid=room_id)
        #     cmsgs = ChatMessage.objects.filter(
        #         room=room).order_by('-date')[:50]
        #     msgs = [msg.to_data() for msg in cmsgs]
        # except ChatRoom.DoesNotExist:
        #     msgs = []
        # mfrom = request.GET['from']
        text = request.GET['text']

        text = json.dumps({'data': text}, cls=DjangoJSONEncoder)

        body = json.dumps(
            {
                'messages': text,
                'last-event-id': event_count
            },
            cls=DjangoJSONEncoder)
        send_event('channels-{}'.format(channels_id), 'message', text)
        return HttpResponse(body, content_type='application/json')
    elif request.method == 'POST':
        print("POST")
        # try:
        #     room = ChatRoom.objects.get(eid=room_id)
        # except ChatRoom.DoesNotExist:
        #     try:
        #         room = ChatRoom(eid=room_id)
        #         room.save()
        #     except IntegrityError:
        #         # someone else made the room. no problem
        #         room = ChatRoom.objects.get(eid=room_id)

        mfrom = request.POST['from']
        text = request.POST['text']
        print(mfrom, text)
        text = json.dumps({'data': text}, cls=DjangoJSONEncoder)

        send_event('channels-{}'.format(channels_id), 'message', text, 'from', mfrom)
        # with transaction.atomic():
        # msg = ChatMessage(room=room, user=mfrom, text=text)
        # msg.save()
        # send_event('room-{}'.format(room_id), 'message', msg.to_data())
        # body = json.dumps(msg.to_data(), cls=DjangoJSONEncoder) + '\n'
        # return HttpResponse(body, content_type='application/json')
    else:
        return HttpResponseNotAllowed(['POST'])
