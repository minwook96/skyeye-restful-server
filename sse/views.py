from django.http import JsonResponse, HttpResponse
from django_eventstream import send_event, get_current_event_id
from rest_framework import status


def messages(request, channels_id):
    if request.method == 'GET':
        event_count = get_current_event_id(['channels-{}'.format(channels_id)])
        print("channels_id: ", channels_id)
        print("event_count: ", event_count)

        text = request.GET['text']
        print(text)

        send_event('channels-{}'.format(channels_id), 'message', text)
        return HttpResponse(text, content_type='application/json')
    elif request.method == 'POST':
        try:  # Apache 에서 문제 발생 원인 파악 X
            access_token = request.headers['Authorization']
            print(access_token)
            text = request.POST['text']
            print(text)
            send_event('channels-{}'.format(channels_id), 'message', text)
            return JsonResponse({'message': 'SEND_SUCCESS'}, status=status.HTTP_200_OK)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=status.HTTP_401_UNAUTHORIZED)

        # text = request.POST['text']
        # print(text)
        # send_event('channels-{}'.format(channels_id), 'message', text)
        # return JsonResponse({'message': 'SEND_SUCCESS'}, status=status.HTTP_200_OK)
