import django_filters

from .models import Video


class VideoFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")
    required_level = django_filters.NumberFilter()

    class Meta:
        model = Video
        fields = ("category", "required_level")