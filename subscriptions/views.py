from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from videos.permissions import IsAdminOrReadOnly

from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        queryset = Plan.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset


class SubscriptionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return self.request.user.subscriptions.select_related("plan")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def current(self, request):
        subscription = self.get_queryset().active().first()
        if subscription is None:
            return Response(
                {"detail": "No active subscription."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(self.get_serializer(subscription).data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        subscription = self.get_object()

        if subscription.status == Subscription.Status.PENDING:
            subscription.status = Subscription.Status.CANCELED
            subscription.save(update_fields=["status"])
        elif subscription.status == Subscription.Status.ACTIVE:
            subscription.auto_renew = False
            subscription.save(update_fields=["auto_renew"])
        else:
            return Response(
                {"detail": "This subscription cannot be canceled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(self.get_serializer(subscription).data)