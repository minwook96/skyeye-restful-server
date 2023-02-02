from django.db import models
from mission_device.models import Missiondevice
from helikite.models import Helikite
from winch.models import Winch


# Create your models here.
class Site(models.Model):
    site_id = models.IntegerField(primary_key=True, help_text='auto increment PK')
    name = models.CharField(unique=True, max_length=100, blank=True, null=True, help_text='장소명')
    installation_date = models.DateField(blank=True, null=True, help_text='설치 날짜')
    helikite_serial_number = models.OneToOneField(Helikite, models.DO_NOTHING, db_column='helikite_serial_number',
                                                  blank=True, null=True, help_text='설치된 헬리카이트 일련번호')
    gcs_serial_number = models.CharField(unique=True, max_length=100, blank=True, null=True, help_text='gcs')
    missiondevice_serial_number = models.OneToOneField(Missiondevice, models.DO_NOTHING,
                                                       db_column='missiondevice_serial_number', blank=True, null=True,
                                                       help_text='설치된 임무장비 일련번호')
    winch_serial_number = models.OneToOneField(Winch, models.DO_NOTHING, db_column='winch_serial_number', blank=True,
                                               null=True, help_text='설치된 윈치 일련번호')

    class Meta:
        managed = False
        db_table = 'site'
