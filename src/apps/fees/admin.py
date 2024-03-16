from django.contrib import admin
from .models import Fee, FeePaymentHistory


class FeePaymentHistoryAdmin(admin.TabularInline):
    model = FeePaymentHistory
    extra = 1
    fields = ["amount_paid", "collected_by", "pay_date", "fee_type"]
    verbose_name = "Payment history"
    can_delete = False
    
class FeeAdmin(admin.ModelAdmin):
    list_display = ["pkid", "amount", "fee_type", "target", "is_complete", "recieved_by", "student"]
    inlines = [
        FeePaymentHistoryAdmin
    ]


admin.site.register(Fee, FeeAdmin)

