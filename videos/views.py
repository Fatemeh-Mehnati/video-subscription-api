from django.shortcuts import render

# Create your views here.
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .filters import VideoFilter
from .models import Category, Video
from .permissions import CanWatchVideo, IsAdminOrReadOnly
from .serializers import CategorySerializer, VideoSerializer
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from .models import Comment, Favorite, Rating, WatchHistory
from .serializers import (
    CommentSerializer,
    FavoriteSerializer,
    RatingSerializer,
    WatchHistorySerializer,
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.select_related("category", "uploaded_by")
    serializer_class = VideoSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = VideoFilter
    search_fields = ("title", "description")
    ordering_fields = ("created_at", "views_count")

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=(IsAuthenticated, CanWatchVideo),
    )
    def watch(self, request, pk=None):
        video = self.get_object()
        Video.objects.filter(pk=video.pk).update(views_count=F("views_count") + 1)
        return Response(
            {"id": video.id, "title": video.title, "video_url": video.video_url}
        )

    @action(detail=True, methods=["post"], permission_classes=(IsAuthenticated, CanWatchVideo))
    def progress(self, request, pk=None):
        video = self.get_object()
        seconds = request.data.get("progress_seconds", 0)
        history, _ = WatchHistory.objects.update_or_create(
            user=request.user, video=video, defaults={"progress_seconds": seconds}
        )
        return Response(WatchHistorySerializer(history).data)

    @action(detail=True, methods=["post"], permission_classes=(IsAuthenticated, CanWatchVideo))
    def rate(self, request, pk=None):
        video = self.get_object()
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating, _ = Rating.objects.update_or_create(
            user=request.user,
            video=video,
            defaults={"score": serializer.validated_data["score"]},
        )
        return Response(RatingSerializer(rating).data)

    @action(detail=True, methods=["get"], permission_classes=())
    def stats(self, request, pk=None):
        video = self.get_object()
        agg = video.ratings.aggregate(average=Avg("score"), count=Count("id"))
        return Response(
            {
                "views_count": video.views_count,
                "average_rating": round(agg["average"], 2) if agg["average"] else None,
                "ratings_count": agg["count"],
                "comments_count": video.comments.count(),
            }
        )

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return (
            Comment.objects.filter(
                video_id=self.kwargs["video_pk"], parent__isnull=True
            )
            .select_related("user")
            .prefetch_related("replies__user")
        )

    def perform_create(self, serializer):
        video = get_object_or_404(Video, pk=self.kwargs["video_pk"])
        serializer.save(user=self.request.user, video=video)

    def get_object(self):
        obj = get_object_or_404(
            Comment, pk=self.kwargs["pk"], video_id=self.kwargs["video_pk"]
        )
        self.check_object_permissions(self.request, obj)
        return obj


class FavoriteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.favorites.select_related("video")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WatchHistoryViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = WatchHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.watch_history.select_related("video")