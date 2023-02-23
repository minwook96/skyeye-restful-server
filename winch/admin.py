from django.contrib import admin
from .models import *
from django.db.models.functions import TruncDay, TruncHour, TruncMinute
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F, Avg


# Register your models here.
class WinchAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'serial_number', 'primary_sensor', 'extended_sensor', 'tetherline_length', 'tetherline_limit_tension',
        'production_year')


class WinchDataLogAdmin(admin.ModelAdmin):
    date_hierarchy = "date"

    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'winch_data_log_id', 'date', 'latitude', 'longitude', 'main_power_voltage', 'tetherline_voltage',
        'main_power_electric_current', 'tetherline_electric_current', 'mechanical_brake_operation',
        'electronic_brake_operation', 'tetherline_length', 'tetherline_angle', 'tetherline_tension', 'pressure',
        'temperature', 'wind_direction', 'wind_speed', 'rain', 'rssi', 'winch_serial_number')
    list_filter = ('date', 'winch_serial_number',)

    def changelist_view(self, request, extra_context=None):
        try:
            response = super().changelist_view(request, extra_context=extra_context)
            queryset = response.context_data["cl"].queryset
            # print(queryset)
            date = queryset.annotate(hour=TruncHour("date")).values("hour").annotate(
                y=Avg("tetherline_angle")).order_by("-hour")
            # column_mode = queryset.values("camera_roll").values('missiondevice_serial_number').annotate(
            #     camera_roll=F("camera_roll"))
            # print("x: ", date)
            # print("y: ", column_mode)
            # chart_data = self.chart_data(queryset)

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
            extra_context = {
                "date": json.dumps(list(date), cls=DjangoJSONEncoder),
                # "column_keys": column_keys,
                # "column_values": column_values
            }
            # Serialize and attach the chart data to the template context
            # as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
            # extra_context = extra_context or {"chart_data": as_json}
        except Exception as e:
            print(e)
            # db_logger.exception(e)

            # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Winch, WinchAdmin)
admin.site.register(WinchDataLog, WinchDataLogAdmin)
