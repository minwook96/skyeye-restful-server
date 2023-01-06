from django.db import models


# Create your models here.
class Missiondevice(models.Model):
    serial_number = models.CharField(primary_key=True, max_length=100, help_text='임무장치 일련번호')
    camera_serial_number = models.OneToOneField("Camera", models.DO_NOTHING, db_column='camera_serial_number',
                                                blank=True, null=True, help_text='카메라 일련번호')
    primary_sensor = models.CharField(max_length=100, blank=True, null=True, help_text='기본 센서')
    extended_sensor = models.CharField(max_length=100, blank=True, null=True, help_text='확장 센서')
    communication_type = models.CharField(max_length=100, blank=True, null=True, help_text="통신방식")
    mobile_service_company = models.CharField(max_length=100, blank=True, null=True, help_text='통신사')
    weight = models.FloatField(blank=True, null=True, help_text='무게')
    production_year = models.TextField(blank=True, null=True,
                                       help_text='제작 년도(1901-2155)')  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'missiondevice'


class Camera(models.Model):
    serial_number = models.CharField(primary_key=True, max_length=100, help_text='카메라 일련번호')
    maximum_angle_roll = models.IntegerField(blank=True, null=True, help_text='Roll 최대각')
    minimum_angle_roll = models.IntegerField(blank=True, null=True, help_text='Roll 최소각')
    maximum_angle_pitch = models.IntegerField(blank=True, null=True, help_text='Pitch 최대각')
    minimum_angle_pitch = models.IntegerField(blank=True, null=True, help_text='Pitch 최소각')
    maximum_angle_yaw = models.IntegerField(blank=True, null=True, help_text='Yaw 최대각')
    minimum_angle_yaw = models.IntegerField(blank=True, null=True, help_text='Yaw 최소각')
    zoom_magnification = models.IntegerField(blank=True, null=True, help_text='무게')
    night_vision = models.IntegerField(blank=True, null=True, help_text='나이트 비전 가능 여부')
    protocol = models.IntegerField(blank=True, null=True, help_text='프로토콜 타입')

    class Meta:
        managed = False
        db_table = 'camera'


class MissiondeviceDataLog(models.Model):
    missiondevice_data_log_id = models.AutoField(primary_key=True, help_text='auto increment PK')
    missiondevice_serial_number = models.ForeignKey(Missiondevice, models.DO_NOTHING,
                                                    db_column='missiondevice_serial_number', blank=True, null=True,
                                                    help_text='임무장치 일련번호')
    date = models.DateTimeField(blank=True, null=True, help_text='날짜')
    latitude = models.FloatField(blank=True, null=True, help_text='위도')
    longitude = models.FloatField(blank=True, null=True, help_text='경도')
    kite_roll = models.FloatField(blank=True, null=True, help_text='카이트 Roll')
    kite_pitch = models.FloatField(blank=True, null=True, help_text='카이트 Pitch')
    kite_yaw = models.FloatField(blank=True, null=True, help_text='카이트 Yaw')
    camera_roll = models.FloatField(blank=True, null=True, help_text='카메라 Roll')
    camera_pitch = models.FloatField(blank=True, null=True, help_text='카메라 Pitch')
    camera_yaw = models.FloatField(blank=True, null=True, help_text='카메라 Yaw')
    pressure = models.IntegerField(blank=True, null=True, help_text='기압')
    temperature = models.FloatField(blank=True, null=True, help_text='온도')
    voltage = models.FloatField(blank=True, null=True, help_text='전압')
    kite_helium_pressure = models.IntegerField(blank=True, null=True, help_text='카이트 내 헬륨 압력')
    etc_senser = models.FloatField(blank=True, null=True, help_text='기타센서값')
    rssi = models.IntegerField(db_column='RSSI', blank=True, null=True,
                               help_text='무선통신 수신감도')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'missiondevice_data_log'
