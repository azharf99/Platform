from django.contrib import admin
from inventaris.models import Inventory, InventoryStatus, Invoice
# Register your models here.

@admin.register(Inventory, InventoryStatus, Invoice)
class TampilanAdmin(admin.ModelAdmin):
    pass