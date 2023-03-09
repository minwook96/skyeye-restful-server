from django.contrib import admin
from .models import *
from django.db.models.functions import TruncDay, TruncHour, TruncSecond, TruncMinute
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F, Avg
from mission_device.models import MissiondeviceDataLog
from winch.models import WinchDataLog
from datetime import date, timedelta, datetime
import logging

db_logger = logging.getLogger('db')


# Register your models here.
class SiteAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'site_id', 'name', 'installation_date', 'helikite_serial_number', 'gcs_serial_number',
        'missiondevice_serial_number', 'winch_serial_number')


class SiteSettingsConfigAdmin(admin.ModelAdmin):
    list_display = (
        'site', 'missiondevice_altitude_high', 'missiondevice_altitude_low', 'missiondevice_voltage_high',
        'missiondevice_voltage_low', 'winch_tetherline_length_high', 'winch_tetherline_length_low',
        'winch_tetherline_angle_high', 'winch_tetherline_angle_low', 'winch_tetherline_tension_high',
        'winch_tetherline_tension_low', 'winch_wind_speed_high', 'winch_wind_speed_low')


origin_index = admin.site.index  # 원래의 index view 함수를 저장해 놓음


def index(request, extra_context=None):  # 사용자 정의 index 선언
    try:
        if request.GET is not None:
            print(request.GET.get('date__month'))
            print(request.GET.get('date__year'))

        current_date = datetime.today()
        past_date = current_date - timedelta(days=7)
        past_time = current_date - timedelta(hours=1)
        # print(future_date)

        temperature = MissiondeviceDataLog.objects.filter(date__range=(past_date, current_date)).annotate(
            day=TruncHour("date")).values("day").annotate(y=Avg("temperature")).order_by("-day")
        camera_roll = MissiondeviceDataLog.objects.filter(date__range=(past_time, current_date),
                                                          missiondevice_serial_number="test1").annotate(
            day=TruncSecond("date")).values("day").annotate(y=F("camera_roll")).order_by("-day")
        camera_pitch = MissiondeviceDataLog.objects.filter(date__range=(past_time, current_date),
                                                           missiondevice_serial_number="test1").annotate(
            day=TruncSecond("date")).values("day").annotate(y=F("camera_pitch")).order_by("-day")
        camera_yaw = MissiondeviceDataLog.objects.filter(date__range=(past_time, current_date),
                                                         missiondevice_serial_number="test1").annotate(
            day=TruncSecond("date")).values("day").annotate(y=F("camera_yaw")).order_by("-day")
        # print(camera_yaw)
        winch = WinchDataLog.objects.filter(date__range=(past_time, current_date)).annotate(
            day=TruncSecond("date")).values("day").annotate(y=F("wind_speed")).order_by("-day")
        extra_context = {
            "temperature": json.dumps(list(temperature), cls=DjangoJSONEncoder),
            "camera_roll": json.dumps(list(camera_roll), cls=DjangoJSONEncoder),
            "camera_pitch": json.dumps(list(camera_pitch), cls=DjangoJSONEncoder),
            "camera_yaw": json.dumps(list(camera_yaw), cls=DjangoJSONEncoder),
            "date2": json.dumps(list(winch), cls=DjangoJSONEncoder)

        }
    except Exception as e:
        print(e)
        db_logger.exception(e)
    return origin_index(request, extra_context)  # 원래의 index view 기능을 수행


admin.site.index = index  # admin index가 요청이 되면 원래의 index view 함수가 아닌 사용자 지정 함수가 수행
admin.site.register(Site, SiteAdmin)
admin.site.register(SiteSettingsConfig, SiteSettingsConfigAdmin)
