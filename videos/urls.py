from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, VideoViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("videos", VideoViewSet, basename="video")

urlpatterns = router.urls