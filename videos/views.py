from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import VideoFilter
from .models import Category, Video
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, VideoSerializer


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