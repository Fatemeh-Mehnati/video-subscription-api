from django.db import models

# Create your models here.
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class Plan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    duration_days = models.PositiveIntegerField(default=30)
    level = models.PositiveSmallIntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("level",)

    def __str__(self):
        return f"{self.name} (level {self.level})"


class SubscriptionQuerySet(models.QuerySet):
    def active(self):
        return self.filter(
            status=Subscription.Status.ACTIVE,
            end_at__gt=timezone.now(),
        )


class Subscription(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        CANCELED = "canceled", "Canceled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.PROTECT, related_name="subscriptions"
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    auto_renew = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SubscriptionQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)

    def activate(self):
        now = timezone.now()
        self.status = self.Status.ACTIVE
        self.start_at = now
        self.end_at = now + timedelta(days=self.plan.duration_days)
        self.save(update_fields=["status", "start_at", "end_at"])

    def __str__(self):
        return f"{self.user} - {self.plan.name} ({self.status})"