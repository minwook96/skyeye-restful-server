from django.contrib import admin
from .models import *
from django.db.models.functions import TruncDay, TruncHour
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F, Avg
from mission_device.models import MissiondeviceDataLog
from winch.models import WinchDataLog
from datetime import date, timedelta


# Register your models here.
class SiteAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'site_id', 'name', 'installation_date', 'helikite_serial_number', 'gcs_serial_number',
        'missiondevice_serial_number', 'winch_serial_number')


origin_index = admin.site.index  # 원래의 index view 함수를 저장해 놓음


def index(request, extra_context=None):  # 사용자 정의 index 선언
    try:
        current_date = date.today()
        future_date = current_date - timedelta(days=7)
        mission_device = MissiondeviceDataLog.objects.filter(date__range=(future_date, current_date)).annotate(
            day=TruncDay("date")).values("day").annotate(y=Avg("temperature")).order_by("-day")
        # print()
        winch = WinchDataLog.objects.filter(date__range=(future_date, current_date)).annotate(
            day=TruncDay("date")).values("day").annotate(
            y=Avg("tetherline_angle")).order_by("-day")
        extra_context = {
            "date1": json.dumps(list(mission_device), cls=DjangoJSONEncoder),
            "date2": json.dumps(list(winch), cls=DjangoJSONEncoder)

        }
    except Exception as e:
        print(e)
    return origin_index(request, extra_context)  # 원래의 index view 기능을 수행


admin.site.index = index  # admin index가 요청이 되면 원래의 index view 함수가 아닌 사용자 지정 함수가 수행
admin.site.register(Site, SiteAdmin)
