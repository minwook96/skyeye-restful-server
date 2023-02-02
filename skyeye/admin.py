from django.contrib import admin
from .models import *


# Register your models here.
class SiteAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'site_id', 'name', 'installation_date', 'helikite_serial_number', 'gcs_serial_number',
        'missiondevice_serial_number', 'winch_serial_number')


admin.site.register(Site, SiteAdmin)
