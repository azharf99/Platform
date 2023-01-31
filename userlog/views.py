from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from userlog.models import UserLog


# Create your views here.

@login_required(login_url='/login/')
def index(request):
    logs = UserLog.objects.all().order_by('-created_at')[:50]
    context = {
        'logs': logs,
    }
    return render(request, 'user-log.html', context)
