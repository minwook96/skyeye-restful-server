from django.contrib import admin
from .models import *


# Register your models here.
class WinchAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'serial_number', 'primary_sensor', 'extended_sensor', 'tetherline_length', 'tetherline_limit_tension',
        'production_year')


class WinchDataLogAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'winch_data_log_id', 'date', 'latitude', 'longitude', 'main_power_voltage', 'tetherline_voltage',
        'main_power_electric_current', 'tetherline_electric_current', 'mechanical_brake_operation',
        'electronic_brake_operation', 'tetherline_length', 'tetherline_angle', 'tetherline_tension', 'pressure',
        'temperature', 'wind_direction', 'wind_speed', 'rain', 'rssi', 'winch_serial_number')


admin.site.register(Winch, WinchAdmin)
admin.site.register(WinchDataLog, WinchDataLogAdmin)
