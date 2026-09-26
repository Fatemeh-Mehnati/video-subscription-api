from rest_framework import serializers

from subscriptions.models import Plan

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source="subscription.plan.name", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id", "plan_name", "amount", "status",
            "authority", "ref_id", "created_at", "paid_at",
        )


class InitiatePaymentSerializer(serializers.Serializer):
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.filter(is_active=True)
    )


class VerifyPaymentSerializer(serializers.Serializer):
    authority = serializers.CharField(max_length=64)