from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Category, Video


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "required_level", "views_count", "created_at")
    list_filter = ("category", "required_level")
    search_fields = ("title", "description")