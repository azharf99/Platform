from django.contrib import admin
from nilai.models import Penilaian

# Register your models here.

@admin.register(Penilaian)
class TampilanAdmin(admin.ModelAdmin):
    pass