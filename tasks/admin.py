from django.contrib import admin

# Register your models here.
from .models import Task  # Replace with your model name

admin.site.register(Task)