from rest_framework import serializers

from .models import Category, Video


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")
        extra_kwargs = {"slug": {"required": False}}


class VideoSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Video
        fields = (
            "id", "title", "description", "category", "uploaded_by",
            "required_level", "duration_seconds", "views_count", "created_at",
            "video_url",
        )
        read_only_fields = ("views_count", "created_at")
        extra_kwargs = {"video_url": {"write_only": True}}