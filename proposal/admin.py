from django.contrib import admin
from proposal.models import Proposal, ProposalStatus, ProposalStatusKepsek, ProposalStatusBendahara, ProposalInventaris, ProposalInventarisStatus, ProposalInventarisStatusKepsek, ProposalInventarisStatusBendahara

# Register your models here.

@admin.register(Proposal, ProposalStatus, ProposalStatusKepsek, ProposalStatusBendahara, ProposalInventaris, ProposalInventarisStatus, ProposalInventarisStatusKepsek, ProposalInventarisStatusBendahara)
class ProposalAdmin(admin.ModelAdmin):
    pass
# Register your models here.
