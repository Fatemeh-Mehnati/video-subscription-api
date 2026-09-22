from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class CanWatchVideo(BasePermission):
    message = "Your subscription does not allow access to this video."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        subscription = (
            request.user.subscriptions.active().select_related("plan").first()
        )
        if subscription is None:
            self.message = "You need an active subscription to watch videos."
            return False

        return subscription.plan.level >= obj.required_level