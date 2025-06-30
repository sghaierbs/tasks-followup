from django.contrib import admin
from .models import TrackableStatus, TrackableUrgency, TrackableClassification

# Register your models here.

admin.site.register(TrackableStatus)
admin.site.register(TrackableUrgency)
admin.site.register(TrackableClassification)
