from django.contrib import admin

# Register your models here.
from timeline.models import Event

admin.site.register(Event)