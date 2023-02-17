from .serializers import DetectionSerializer
from .models import Detection
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import logging
from django.core.mail.message import EmailMessage
from server import settings
from accounts.models import User
from rest_framework.authtoken.models import Token
import datetime

db_logger = logging.getLogger('db')


class DetectionView(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            token = request.headers['Authorization'].split()
            if len(token) == 2:
                token_key = token[1]
            else:
                db_logger.exception("Token Null")
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            try:
                token = Token.objects.get(key=token_key)
                # print(token.user)
            except Token.DoesNotExist as e:
                db_logger.exception(e)
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            if token.user != 'AnonyMousUser':
                user = User.objects.get(username=token.user)
                image = request.FILES['image']
                # print(image)
                # print(user.email)
                # print(image.name, image.read(), image.content_type)
                # smtp사용해서 메일보내는 코드
                detection_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                subject = "[화재 알림] 금일 {}경 산불 발생".format(detection_time)
                to = [user.email]
                message = "금일 {}경 산불 발생".format(detection_time)
                try:
                    # mail = EmailMessage(subject=subject, body=message, to=to, from_email=settings.EMAIL_HOST_USER)
                    # mail.attach(image.name, image.read(), image.content_type)
                    # mail.send()
                    serializer.save(user=request.user)

                except:
                    db_logger.exception("Mail Attachment error")

            return Response(status=status.HTTP_201_CREATED)
        else:
            db_logger.exception(status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
