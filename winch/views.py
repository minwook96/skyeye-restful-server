from rest_framework import status
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response


# Create your views here.
class WinchViewSet(viewsets.ModelViewSet):
    queryset = Winch.objects.all()
    serializer_class = WinchSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("윈치", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)

        return Response(status=status.HTTP_200_OK)


class WinchDataLogViewSet(viewsets.ModelViewSet):
    queryset = WinchDataLog.objects.all()
    serializer_class = WinchDataLogSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("윈치 로그 데이터", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        data = WinchDataLog.objects.last()
        serializer = WinchDataLogSerializer(data)

        print("윈치 데이터 GCS 전송", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
