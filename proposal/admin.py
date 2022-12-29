from django.contrib import admin
from proposal.models import *

# Register your models here.

@admin.register(Proposal, ProposalStatus, ProposalStatusKepsek, ProposalStatusBendahara)
class ProposalAdmin(admin.ModelAdmin):
    pass
# Register your models here.
