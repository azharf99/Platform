from django.db import models


# Create your models here.


class UserLog(models.Model):
    user = models.CharField(max_length=200)
    action_flag = models.CharField(max_length=200)
    app = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s %s" % (self.user, self.action_flag, self.app)
