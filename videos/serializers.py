from xml.etree.ElementTree import Comment

from rest_framework import serializers

from .models import Category, Comment, Favorite, Rating, Video, WatchHistory

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

class WatchHistorySerializer(serializers.ModelSerializer):
    video_title = serializers.CharField(source="video.title", read_only=True)

    class Meta:
        model = WatchHistory
        fields = ("id", "video", "video_title", "progress_seconds", "watched_at")
        read_only_fields = ("video", "watched_at")


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "score", "created_at")


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "user", "text", "parent", "created_at", "replies")
        read_only_fields = ("created_at",)

    def get_replies(self, obj):
        if obj.parent_id is not None:
            return []
        return CommentSerializer(obj.replies.all(), many=True).data

    def validate_parent(self, value):
        if value is None:
            return value
        if value.parent_id is not None:
            raise serializers.ValidationError("Only one level of replies is allowed.")
        if value.video_id != int(self.context["view"].kwargs["video_pk"]):
            raise serializers.ValidationError(
                "Parent comment belongs to another video."
            )
        return value


class FavoriteSerializer(serializers.ModelSerializer):
    video_title = serializers.CharField(source="video.title", read_only=True)

    class Meta:
        model = Favorite
        fields = ("id", "video", "video_title", "created_at")