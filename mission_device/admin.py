from django.contrib import admin
from .models import *


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
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'missiondevice_data_log_id', 'date', 'latitude', 'longitude', 'roll', 'pitch', 'yaw',
        'camera_roll', 'camera_pitch', 'camera_yaw', 'pressure', 'temperature', 'voltage', 'kite_helium_pressure',
        'etc_senser', 'rssi', 'missiondevice_serial_number')


admin.site.register(Missiondevice, MissiondeviceAdmin)
admin.site.register(Camera, CameraAdmin)
admin.site.register(MissiondeviceDataLog, MissiondeviceDataLogAdmin)
