from django.contrib import admin
from django.db.models.functions import TruncDay, TruncSecond
from .models import *
import json
from django.core.serializers.json import DjangoJSONEncoder
import logging
from django.db.models import Count, F, Avg
from datetime import timedelta, datetime
from rangefilter.filters import DateTimeRangeFilter
from pytz import timezone

db_logger = logging.getLogger('db')


# Register your models here.
class MissiondeviceAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'serial_number', 'camera_serial_number', 'primary_sensor', 'extended_sensor', 'communication_type',
        'mobile_service_company', 'weight', 'production_year')


class CameraAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'serial_number', 'maximum_angle_roll', 'minimum_angle_roll', 'maximum_angle_pitch', 'minimum_angle_pitch',
        'maximum_angle_yaw', 'minimum_angle_yaw', 'zoom_magnification', 'night_vision', 'protocol')


class MissiondeviceDataLogAdmin(admin.ModelAdmin):
    # date_hierarchy = "date"
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'missiondevice_data_log_id', 'format_date', 'latitude', 'longitude', 'roll', 'pitch', 'yaw', 'camera_roll',
        'camera_pitch', 'camera_yaw', 'camera_zoom', 'pressure', 'temperature', 'voltage', 'kite_helium_pressure',
        'etc_senser', 'rssi', 'missiondevice_serial_number')
    list_filter = ('missiondevice_serial_number', ('date', DateTimeRangeFilter),)

    def format_date(self, obj):
        obj.date = obj.date + timedelta(hours=9)
        return obj.date.strftime('%Y-%m-%d %H:%M:%S')

    format_date.admin_order_field = 'date'
    format_date.short_description = 'Date'

    def get_rangefilter_date_default(self, request):
        current_date = datetime.today()
        past_date = current_date - timedelta(hours=1)
        return past_date, current_date

    def changelist_view(self, request, extra_context=None):
        try:
            response = super().changelist_view(request, extra_context=extra_context)
            queryset = response.context_data["cl"].queryset
            # print(queryset)

            if request.GET.get("date__range__lte_0") is not None:
                current_date = request.GET.get("date__range__lte_0") + " " + request.GET.get("date__range__lte_1")
                past_date = request.GET.get("date__range__gte_0") + " " + request.GET.get("date__range__gte_1")
                # print(past_date, current_date)
            else:
                current_date = datetime.today()
                past_date = current_date - timedelta(hours=1)

            queryset = queryset.filter(date__range=(past_date, current_date))
            date = queryset.annotate(hour=TruncSecond("date")).values("hour").annotate(y=F("camera_yaw")).order_by(
                "-hour")
            extra_context = {
                "date": json.dumps(list(date), cls=DjangoJSONEncoder),
                # "column_keys": column_keys,
                # "column_values": column_values
            }

            # print(MissiondeviceDataLog.objects.annotate(hour=TruncMinute("date")).values("hour"))
            # column_mode = queryset.values("camera_roll").values('missiondevice_serial_number').annotate(
            #     camera_roll=F("camera_roll"))
            # print("x: ", date)
            # print("y: ", column_mode)

            # column_keys = list()
            # column_values = list()
            # for item in column_mode:
            #     column_keys.append(list(item.keys())[1])
            #     column_values.append(item.get('camera_roll'))
            # print(column_keys)
            # extra_context = dict(
            #     date=date,
            #     column_keys=column_keys,
            #     column_values=column_values
            # )
        except Exception as e:
            print(e)
            db_logger.exception(e)

            # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


class PoiAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = ('poi_id', 'site', 'latitude', 'longitude', 'altitude', 'zoom_level')


admin.site.register(Poi, PoiAdmin)
admin.site.register(Missiondevice, MissiondeviceAdmin)
admin.site.register(Camera, CameraAdmin)
admin.site.register(MissiondeviceDataLog, MissiondeviceDataLogAdmin)
