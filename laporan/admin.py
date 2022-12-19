from django.contrib import admin
from laporan.models import Report, UploadImage
# Register your models here.

@admin.register(Report, UploadImage)
class TampilanAdmin(admin.ModelAdmin):
    pass