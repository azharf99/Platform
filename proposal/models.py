from django.db import models
from ekskul.models import Extracurricular, Teacher
# Create your models here.

class Proposal(models.Model):
    ekskul = models.ForeignKey(Extracurricular, on_delete=models.CASCADE)
    pengaju = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
