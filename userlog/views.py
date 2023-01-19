from django.shortcuts import render
from userlog.models import UserLog

# Create your views here.

def index(request):
    logs = UserLog.objects.all().order_by('-created_at')
    context = {
        'logs': logs,
    }
    return render(request, 'user-log.html', context)
