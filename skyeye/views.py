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
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    db_logger.exception(status.HTTP_404_NOT_FOUND)
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif request.GET.get('missiondevice_serial_number') is not None:
                missiondevice_serial_number = request.GET.get('missiondevice_serial_number')
                print(missiondevice_serial_number)
                if Site.objects.filter(missiondevice_serial_number=missiondevice_serial_number).exists():
                    data = Site.objects.get(missiondevice_serial_number=missiondevice_serial_number)
                    serializer = SiteSerializer(data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    db_logger.exception(status.HTTP_404_NOT_FOUND)
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif request.GET.get('gcs_serial_number') is not None:
                gcs_serial_number = request.GET.get('gcs_serial_number')
                if Site.objects.filter(gcs_serial_number=gcs_serial_number).exists():
                    data = Site.objects.get(gcs_serial_number=gcs_serial_number)
                    serializer = SiteSerializer(data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    db_logger.exception(status.HTTP_404_NOT_FOUND)
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                data = Site.objects.all()
                serializer = SiteSerializer(data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SiteSettingsConfigViewSet(viewsets.ModelViewSet):
    queryset = SiteSettingsConfig.objects.all()
    serializer_class = SiteSettingsConfigSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print("사이트 설정", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            db_logger.exception(status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # def list(self, request, *args, **kwargs):
    #     try:
    #         if request.GET.get('site') is not None:
    #             site = request.GET.get('site')
    #             if SiteSettingsConfig.objects.filter(site=site).exists():
    #                 data = SiteSettingsConfig.objects.get(site=site)
    #                 serializer = SiteSerializer(data)
    #                 return Response(serializer.data, status=status.HTTP_200_OK)
    #             else:
    #                 db_logger.exception(status.HTTP_404_NOT_FOUND)
    #                 return Response(status=status.HTTP_404_NOT_FOUND)
    #         else:
    #             data = Site.objects.all()
    #             serializer = SiteSerializer(data, many=True)
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         db_logger.exception(e)
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
