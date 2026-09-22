from rest_framework import serializers

from .models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ("id", "name", "price", "duration_days", "level", "is_active")


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.filter(is_active=True),
        source="plan",
        write_only=True,
    )

    class Meta:
        model = Subscription
        fields = (
            "id", "plan", "plan_id", "status",
            "start_at", "end_at", "auto_renew", "created_at",
        )
        read_only_fields = ("status", "start_at", "end_at", "created_at")

    def validate(self, attrs):
        user = self.context["request"].user
        if user.subscriptions.active().exists():
            raise serializers.ValidationError(
                "You already have an active subscription."
            )
        return attrs