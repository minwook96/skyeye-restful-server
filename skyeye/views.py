from rest_framework import status
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
import logging

db_logger = logging.getLogger('db')


# Create your views here.
class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("사이트", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            db_logger.exception(status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            if request.GET.get('winch_serial_number') is not None:
                winch_serial_number = request.GET.get('winch_serial_number')
                if Site.objects.filter(winch_serial_number=winch_serial_number).exists():
                    data = Site.objects.get(winch_serial_number=winch_serial_number)
                    serializer = SiteSerializer(data)
                    return Response(serializer.data["missiondevice_serial_number"], status=status.HTTP_200_OK)
                else:
                    db_logger.exception(status.HTTP_404_NOT_FOUND)
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif request.GET.get('missiondevice_serial_number') is not None:
                missiondevice_serial_number = request.GET.get('missiondevice_serial_number')
                if Site.objects.filter(missiondevice_serial_number=missiondevice_serial_number).exists():
                    data = Site.objects.get(missiondevice_serial_number=missiondevice_serial_number)
                    serializer = SiteSerializer(data)
                    return Response(serializer.data["winch_serial_number"], status=status.HTTP_200_OK)
                else:
                    db_logger.exception(status.HTTP_404_NOT_FOUND)
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif request.GET.get('gcs_serial_number') is not None:
                missiondevice_serial_number = request.GET.get('gcs_serial_number')
                if Site.objects.filter(missiondevice_serial_number=missiondevice_serial_number).exists():
                    data = Site.objects.get(missiondevice_serial_number=missiondevice_serial_number)
                    serializer = SiteSerializer(data)
                    print(serializer.data)
                    return Response(serializer.data["site_id"], status=status.HTTP_200_OK)
                else:
                    db_logger.exception(status.HTTP_404_NOT_FOUND)
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                db_logger.exception(status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
