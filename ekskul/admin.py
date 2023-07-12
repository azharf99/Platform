from django.contrib import admin
from ekskul.models import User, Student, StudentOrganization,Extracurricular, Teacher

# Register your models here.

@admin.register(User, Student, StudentOrganization,Extracurricular, Teacher)
class AdminUmum(admin.ModelAdmin):
    pass