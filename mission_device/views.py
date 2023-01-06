from rest_framework import viewsets
from rest_framework.decorators import action
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

        print("aaaaaaaaaa", serializer)

    # @action(detail=True, methods=['GET'], name='Bookmark')
    # def bookmark(self, request, pk=None):
    #     if self.request.user.is_authenticated:
    #         stylist = Missiondevice.objects.get(pk=pk)
    #         if self.request.user.bookmarks.filter(pk=pk).count() == 1:
    #             self.request.user.bookmarks.remove(pk)
    #             stylist.like_count -= 1
    #         else:
    #             self.request.user.bookmarks.add(pk)
    #             stylist.like_count += 1
    #         self.request.user.save()
    #         stylist.save()
    #         return Response("OK", status=status.HTTP_200_OK)
    #
    #     return Response("Not Authenticated", status=status.HTTP_401_UNAUTHORIZED)


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class MissionDeviceDataLogViewSet(viewsets.ModelViewSet):
    queryset = MissiondeviceDataLog.objects.all()
    serializer_class = MissionDeviceDataLogSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # serializer.save(self.request.data)
            print("임무장치 로그 데이터", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(201)