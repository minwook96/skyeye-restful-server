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

import calendar

db_logger = logging.getLogger('db')


# Register your models here.
class SiteAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'site_id', 'name', 'installation_date', 'helikite_serial_number', 'gcs_serial_number',
        'missiondevice_serial_number', 'winch_serial_number')


origin_index = admin.site.index  # 원래의 index view 함수를 저장해 놓음


def check_date(year, month, day, time):
    target_date = year + "-" + month
    past_date = datetime.strptime(target_date, '%Y-%m')
    if day is None:
        day = 1
        last_day = calendar.monthrange(past_date.year, past_date.month)[1]
        last_date = past_date.replace(day=last_day)
        date_list = [past_date, last_date]
    elif day is not None and len(time) == 0:
        target_date = year + "-" + month + "-" + day
        past_date = datetime.strptime(target_date, '%Y-%m-%d')
        date_list = [past_date, past_date + timedelta(days=1)]
    elif len(time) > 0:
        str_first_time = year + "-" + month + "-" + day + " " + time[0] + ":" + time[1]
        first_time = datetime.strptime(str_first_time, '%Y-%m-%d %H:%M')
        str_second_time = year + "-" + month + "-" + day + " " + time[2] + ":" + time[3]
        second_time = datetime.strptime(str_second_time, '%Y-%m-%d %H:%M')
        date_list = [first_time, second_time]
    return date_list


def index(request, extra_context=None):  # 사용자 정의 index 선언
    try:
        if request.GET is not None:
            # 버튼 선택 안했으면 None 출력
            # print(request.GET.get('date__month')) # 3
            # print(request.GET.get('date__year')) # 2023
            date_day = request.GET.get('date__day')
            date_month = request.GET.get('date__month')
            date_year = request.GET.get('date__year')

            is_time_exist = False
            first_time = request.GET.get('date__range__gte_1')
            second_time = request.GET.get('date__range__lte_1')
            date_time = []
            if first_time is not None:
                is_time_exist = True
                date_time.append(first_time.split(':')[0])
                date_time.append(first_time.split(':')[1])
                date_time.append(second_time.split(':')[0])
                date_time.append(second_time.split(':')[1])
                # print(date_time)

        # 선택한 임무장비 / 기본값 'test1'
        site_id = request.GET.get('options')
        print(site_id)
        if site_id is None:
            # get_serial = Missiondevice.objects.values('serial_number')[1].values()
            # get_serial = list(get_serial)[0]
            # print(get_serial) # test1
            missiondevice_serial_number = 'test1'
            winch_serial_number = 'test1'
        else:
            missiondevice_serial_number = Site.objects.filter(site_id=site_id).values("missiondevice_serial_number")
            winch_serial_number = Site.objects.filter(site_id=site_id).values("winch_serial_number")
            missiondevice_serial_number = missiondevice_serial_number[0]["missiondevice_serial_number"]
            winch_serial_number = winch_serial_number[0]["winch_serial_number"]
            # print(missiondevice_serial_number, winch_serial_number)

        current_date = datetime.today()
        past_date = current_date - timedelta(days=7)
        past_time = current_date - timedelta(hours=1)
        # print(future_date)

        past_date = past_date.replace(month=1, day=1)

        # 버튼 안눌렀으면 [1월 1일, 현재날짜] / 눌렀으면 [해당월 1일, 마지막일]
        date_list = [past_date, current_date]
        if date_year is not None:
            date_list = check_date(date_year, date_month, date_day, date_time)

        # 온도 => 일주일전
        # temperature = MissiondeviceDataLog.objects.filter(date__range=(past_date, current_date)).annotate(
        #     day=TruncHour("date")).values("day").annotate(y=Avg("temperature")).order_by("-day")

        # 카메라 롤,피치,요, 윈치 => 1시간전
        if is_time_exist is False:
            temperature = MissiondeviceDataLog.objects.filter(date__range=(date_list[0], date_list[1]),
                                                              missiondevice_serial_number=missiondevice_serial_number).annotate(
                day=TruncHour("date")).values("day").annotate(y=Avg("temperature")).order_by("-day")
            camera_roll = MissiondeviceDataLog.objects.filter(date__range=(past_time, current_date),
                                                              missiondevice_serial_number=missiondevice_serial_number).annotate(
                day=TruncSecond("date")).values("day").annotate(y=F("camera_roll")).order_by("-day")
            camera_pitch = MissiondeviceDataLog.objects.filter(date__range=(past_time, current_date),
                                                               missiondevice_serial_number=missiondevice_serial_number).annotate(
                day=TruncSecond("date")).values("day").annotate(y=F("camera_pitch")).order_by("-day")
            camera_yaw = MissiondeviceDataLog.objects.filter(date__range=(past_time, current_date),
                                                             missiondevice_serial_number=missiondevice_serial_number).annotate(
                day=TruncSecond("date")).values("day").annotate(y=F("camera_yaw")).order_by("-day")
            # print(camera_yaw)
            winch = WinchDataLog.objects.filter(date__range=(past_time, current_date),
                                                winch_serial_number=winch_serial_number).annotate(
                day=TruncSecond("date")).values("day").annotate(y=F("wind_speed")).order_by("-day")
        else:
            temperature = MissiondeviceDataLog.objects.filter(date__range=(date_list[0], date_list[1])).annotate(
                day=TruncMinute("date")).values("day").annotate(y=Avg("temperature")).order_by("-day")
            camera_roll = MissiondeviceDataLog.objects.filter(date__range=(date_list[0], date_list[1]),
                                                              missiondevice_serial_number=missiondevice_serial_number).annotate(
                day=TruncSecond("date")).values("day").annotate(y=F("camera_roll")).order_by("-day")
            camera_pitch = MissiondeviceDataLog.objects.filter(date__range=(date_list[0], date_list[1]),
                                                               missiondevice_serial_number=missiondevice_serial_number).annotate(
                day=TruncSecond("date")).values("day").annotate(y=F("camera_pitch")).order_by("-day")
            camera_yaw = MissiondeviceDataLog.objects.filter(date__range=(date_list[0], date_list[1]),
                                                             missiondevice_serial_number=missiondevice_serial_number).annotate(
                day=TruncSecond("date")).values("day").annotate(y=F("camera_yaw")).order_by("-day")
            # print(camera_yaw)
            winch = WinchDataLog.objects.filter(date__range=(date_list[0], date_list[1]),
                                                winch_serial_number=winch_serial_number).annotate(
                day=TruncSecond("date")).values("day").annotate(y=F("wind_speed")).order_by("-day")
        site_name = Site.objects.values('site_id', 'name')
        # print(site_name)
        extra_context = {
            "temperature": json.dumps(list(temperature), cls=DjangoJSONEncoder),
            "camera_roll": json.dumps(list(camera_roll), cls=DjangoJSONEncoder),
            "camera_pitch": json.dumps(list(camera_pitch), cls=DjangoJSONEncoder),
            "camera_yaw": json.dumps(list(camera_yaw), cls=DjangoJSONEncoder),
            "date2": json.dumps(list(winch), cls=DjangoJSONEncoder),
            "date": json.dumps(list(date_list), cls=DjangoJSONEncoder),
            "site_name": json.dumps(list(site_name), cls=DjangoJSONEncoder),
        }
    except Exception as e:
        print(e)
        db_logger.exception(e)
    return origin_index(request, extra_context)  # 원래의 index view 기능을 수행


admin.site.index = index  # admin index가 요청이 되면 원래의 index view 함수가 아닌 사용자 지정 함수가 수행
admin.site.register(Site, SiteAdmin)
