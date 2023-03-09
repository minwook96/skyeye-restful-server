from django.contrib import admin
from .models import *
from django.db.models.functions import TruncDay, TruncHour, TruncMinute, TruncSecond
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F, Avg
from datetime import timedelta, datetime
from rangefilter.filters import DateTimeRangeFilter


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
        'winch_data_log_id', 'format_date', 'latitude', 'longitude', 'main_power_voltage', 'tetherline_voltage',
        'main_power_electric_current', 'tetherline_electric_current', 'mechanical_brake_operation',
        'electronic_brake_operation', 'tetherline_length', 'tetherline_angle', 'tetherline_tension', 'pressure',
        'temperature', 'wind_direction', 'wind_speed', 'rain', 'rssi', 'winch_serial_number')
    list_filter = ('winch_serial_number', ('date', DateTimeRangeFilter),)

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

            if request.GET.get("date__range__lte_0") is not None:
                current_date = request.GET.get("date__range__lte_0") + " " + request.GET.get("date__range__lte_1")
                past_date = request.GET.get("date__range__gte_0") + " " + request.GET.get("date__range__gte_1")
                # print(past_date, current_date)
            else:
                current_date = datetime.today()
                past_date = current_date - timedelta(hours=1)

            # print(queryset)
            queryset = queryset.filter(date__range=(past_date, current_date))
            date = queryset.annotate(hour=TruncSecond("date")).values("hour").annotate(y=F("wind_speed")).order_by(
                "-hour")
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
