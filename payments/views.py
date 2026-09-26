from django.shortcuts import render

# Create your views here.
from django.db import transaction
from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from subscriptions.models import Subscription

from .gateway import get_gateway
from .models import Payment
from .serializers import (
    InitiatePaymentSerializer,
    PaymentSerializer,
    VerifyPaymentSerializer,
)
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return self.request.user.payments.select_related("subscription__plan")

    @action(detail=False, methods=["post"])
    def initiate(self, request):
        serializer = InitiatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = serializer.validated_data["plan_id"]

        if request.user.subscriptions.active().exists():
            return Response(
                {"detail": "You already have an active subscription."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            subscription = Subscription.objects.create(user=request.user, plan=plan)
            payment = Payment.objects.create(
                user=request.user,
                subscription=subscription,
                amount=plan.price,
            )

        payment_url = get_gateway().request_payment(payment)
        return Response(
            {
                "payment_id": payment.id,
                "authority": payment.authority,
                "amount": payment.amount,
                "payment_url": payment_url,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"])
    def verify(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authority = serializer.validated_data["authority"]

        try:
            payment = Payment.objects.select_related("subscription__plan").get(
                authority=authority, user=request.user
            )
        except Payment.DoesNotExist:
            return Response(
                {"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if payment.status == Payment.Status.SUCCESS:
            return Response(
                {"detail": "This payment has already been verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ok, ref_id = get_gateway().verify_payment(payment)

        if not ok:
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])
            return Response(
                {"detail": "Payment failed."}, status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            payment.status = Payment.Status.SUCCESS
            payment.ref_id = ref_id
            payment.paid_at = timezone.now()
            payment.save(update_fields=["status", "ref_id", "paid_at"])
            payment.subscription.activate()

        return Response(PaymentSerializer(payment).data)


@api_view(["GET"])
@permission_classes([AllowAny])
def mock_gateway(request):
    authority = request.query_params.get("authority", "")
    return JsonResponse(
        {
            "message": "This is a fake bank page. Copy the authority below and "
                       "send it to /api/payments/verify/ to complete the payment.",
            "authority": authority,
        }
    )