from django.contrib import admin

# Register your models here.
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "status", "ref_id", "created_at", "paid_at")
    list_filter = ("status",)
    readonly_fields = ("authority", "ref_id", "paid_at")