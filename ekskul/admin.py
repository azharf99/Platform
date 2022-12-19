from django.contrib import admin
from ekskul.models import *

# Register your models here.

@admin.register(User, Student, StudentOrganization,Extracurricular, Teacher)
class AdminUmum(admin.ModelAdmin):
    pass