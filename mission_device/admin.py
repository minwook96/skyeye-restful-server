from django.contrib import admin
from django.db.models.functions import TruncDay, TruncHour, TruncMinute

from .models import *
import json
from django.core.serializers.json import DjangoJSONEncoder
import logging
from django.db.models import Count, F, Avg

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
    date_hierarchy = "date"
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'missiondevice_data_log_id', 'date', 'latitude', 'longitude', 'roll', 'pitch', 'yaw', 'camera_roll',
        'camera_pitch', 'camera_yaw', 'camera_zoom', 'pressure', 'temperature', 'voltage', 'kite_helium_pressure',
        'etc_senser', 'rssi', 'missiondevice_serial_number')
    list_filter = ('date', 'missiondevice_serial_number',)

    def chart_data(self, queryset):
        return (
            queryset.annotate(day=TruncDay("date"))
            .values("day")
            .annotate(y=Count("temperature"))
            .order_by("-day")
        )

    def changelist_view(self, request, extra_context=None):
        try:
            response = super().changelist_view(request, extra_context=extra_context)
            queryset = response.context_data["cl"].queryset
            # print(queryset)
            date = queryset.annotate(hour=TruncHour("date")).values("hour").annotate(y=Avg("temperature")).order_by("-hour")
            column_mode = queryset.values("camera_roll").values('missiondevice_serial_number').annotate(
                camera_roll=F("camera_roll"))
            # print("x: ", date)
            # print("y: ", column_mode)
            chart_data = self.chart_data(queryset)

            column_keys = list()
            column_values = list()
            for item in column_mode:
                column_keys.append(list(item.keys())[1])
                column_values.append(item.get('camera_roll'))
            # print(column_keys)
            # extra_context = dict(
            #     date=date,
            #     column_keys=column_keys,
            #     column_values=column_values
            # )
            extra_context = {
                "date": json.dumps(list(date), cls=DjangoJSONEncoder),
                "column_keys": column_keys,
                "column_values": column_values
            }
            # Serialize and attach the chart data to the template context
            as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
            # extra_context = extra_context or {"chart_data": as_json}
        except Exception as e:
            print(e)
            # db_logger.exception(e)

            # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Missiondevice, MissiondeviceAdmin)
admin.site.register(Camera, CameraAdmin)
admin.site.register(MissiondeviceDataLog, MissiondeviceDataLogAdmin)
