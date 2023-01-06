from django.contrib import admin
from django_eventstream.models import *

# Register your models here.
admin.site.register(Event)
admin.site.register(EventCounter)