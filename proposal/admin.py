from django.contrib import admin
from proposal.models import ProposalUstadz, ProposalSantri

# Register your models here.

@admin.register(ProposalUstadz, ProposalSantri)
class TampilanAdmin(admin.ModelAdmin):
    pass
# Register your models here.
