from django.views import generic
from proposal.models import *


class CalendarView(generic.ListView):
    model = Proposal
    template_name = 'timeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Proposal.objects.all().order_by('tanggal_final')
