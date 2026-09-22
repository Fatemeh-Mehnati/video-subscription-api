from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "price", "duration_days", "is_active")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "status", "start_at", "end_at", "auto_renew")
    list_filter = ("status", "plan")
    actions = ("activate_selected",)

    @admin.action(description="Activate selected subscriptions")
    def activate_selected(self, request, queryset):
        for subscription in queryset.select_related("plan"):
            subscription.activate()
        self.message_user(request, f"{queryset.count()} subscription(s) activated.")