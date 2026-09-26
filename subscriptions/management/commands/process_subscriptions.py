from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from subscriptions.models import Subscription


class Command(BaseCommand):
    help = "Expire ended subscriptions and renew the ones with auto_renew enabled."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would happen without changing anything.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        now = timezone.now()

        ended = Subscription.objects.filter(
            status=Subscription.Status.ACTIVE, end_at__lte=now
        ).select_related("plan")

        expired_count = 0
        renewed_count = 0

        for subscription in ended:
            if subscription.auto_renew and subscription.plan.is_active:
                if not dry_run:
                    with transaction.atomic():
                        subscription.start_at = subscription.end_at
                        subscription.end_at = subscription.end_at + timedelta(
                            days=subscription.plan.duration_days
                        )
                        subscription.save(update_fields=["start_at", "end_at"])
                renewed_count += 1
            else:
                if not dry_run:
                    subscription.status = Subscription.Status.EXPIRED
                    subscription.save(update_fields=["status"])
                expired_count += 1

        prefix = "[dry-run] " if dry_run else ""
        self.stdout.write(
            self.style.SUCCESS(
                f"{prefix}Renewed: {renewed_count}, Expired: {expired_count}"
            )
        )