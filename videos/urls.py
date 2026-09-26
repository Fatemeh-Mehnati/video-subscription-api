from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    FavoriteViewSet,
    RealtimeTestView,
    VideoViewSet,
    WatchHistoryViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("videos", VideoViewSet, basename="video")
router.register("favorites", FavoriteViewSet, basename="favorite")
router.register("watch-history", WatchHistoryViewSet, basename="watch-history")

comment_list = CommentViewSet.as_view({"get": "list", "post": "create"})
comment_detail = CommentViewSet.as_view(
    {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = router.urls + [
    path("videos/<int:video_pk>/comments/", comment_list, name="comment-list"),
    path(
        "videos/<int:video_pk>/comments/<int:pk>/",
        comment_detail,
        name="comment-detail",
    ),
    path("realtime-test/", RealtimeTestView.as_view(), name="realtime-test"),
]