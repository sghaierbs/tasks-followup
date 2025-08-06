from django.contrib import admin
from .models import TrackableStatus, TrackableUrgency, TrackableClassification
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import messages

# Register your models here.

admin.site.register(TrackableStatus)
admin.site.register(TrackableUrgency)
admin.site.register(TrackableClassification)

