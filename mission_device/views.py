from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class MissionDeviceViewSet(viewsets.ModelViewSet):
    queryset = Missiondevice.objects.all()
    serializer_class = MissionDeviceSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("임무장비", serializer.data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("카메라", serializer.data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class MissionDeviceDataLogViewSet(viewsets.ModelViewSet):
    queryset = MissiondeviceDataLog.objects.all()
    serializer_class = MissionDeviceDataLogSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("임무장비 로그 데이터", serializer.data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        data = MissiondeviceDataLog.objects.last()
        serializer = MissionDeviceDataLogSerializer(data)
        print("임무장비 데이터 GCS 전송", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
