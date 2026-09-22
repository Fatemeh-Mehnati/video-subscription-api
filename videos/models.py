from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField()
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="videos"
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_videos",
    )
    required_level = models.PositiveSmallIntegerField(default=1)
    duration_seconds = models.PositiveIntegerField()
    views_count = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title