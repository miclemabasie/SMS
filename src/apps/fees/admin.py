from django.contrib import admin
from .models import Fee

class FeeAdmin(admin.ModelAdmin):
    list_display = ["amount", "fee_type", "target", "is_complete", "recieved_by", "student"]


admin.site.register(Fee, FeeAdmin)
