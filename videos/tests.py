from django.test import TestCase

# Create your tests here.
from django.db import IntegrityError

from accounts.models import User
from .models import (
    Category,
    Video,
    WatchHistory,
    Rating,
    Comment,
    Favorite,
)


class VideoModelsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123",
        )

        self.category = Category.objects.create(
            name="Fitness",
        )

        self.video = Video.objects.create(
            title="Test Workout",
            description="Test workout video",
            video_url="https://example.com/video.mp4",
            category=self.category,
            uploaded_by=self.user,
            required_level=1,
            duration_seconds=600,
        )

    def test_category_slug_is_created_automatically(self):
        self.assertEqual(self.category.slug, "fitness")

    def test_video_creation(self):
        self.assertEqual(self.video.title, "Test Workout")
        self.assertEqual(self.video.category, self.category)
        self.assertEqual(self.video.uploaded_by, self.user)
        self.assertEqual(self.video.views_count, 0)

    def test_video_str(self):
        self.assertEqual(str(self.video), "Test Workout")

    def test_watch_history(self):
        history = WatchHistory.objects.create(
            user=self.user,
            video=self.video,
            progress_seconds=120,
        )

        self.assertEqual(history.progress_seconds, 120)
        self.assertEqual(history.user, self.user)
        self.assertEqual(history.video, self.video)

    def test_watch_history_is_unique_per_user_and_video(self):
        WatchHistory.objects.create(
            user=self.user,
            video=self.video,
        )

        with self.assertRaises(IntegrityError):
            WatchHistory.objects.create(
                user=self.user,
                video=self.video,
            )

    def test_rating(self):
        rating = Rating.objects.create(
            user=self.user,
            video=self.video,
            score=5,
        )

        self.assertEqual(rating.score, 5)
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.video, self.video)

    def test_rating_is_unique_per_user_and_video(self):
        Rating.objects.create(
            user=self.user,
            video=self.video,
            score=5,
        )

        with self.assertRaises(IntegrityError):
            Rating.objects.create(
                user=self.user,
                video=self.video,
                score=4,
            )

    def test_comment(self):
        comment = Comment.objects.create(
            user=self.user,
            video=self.video,
            text="Great workout!",
        )

        self.assertEqual(comment.text, "Great workout!")
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.video, self.video)

    def test_comment_reply(self):
        parent = Comment.objects.create(
            user=self.user,
            video=self.video,
            text="Main comment",
        )

        reply = Comment.objects.create(
            user=self.user,
            video=self.video,
            parent=parent,
            text="Reply",
        )

        self.assertEqual(reply.parent, parent)
        self.assertIn(reply, parent.replies.all())

    def test_favorite(self):
        favorite = Favorite.objects.create(
            user=self.user,
            video=self.video,
        )

        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.video, self.video)

    def test_favorite_is_unique_per_user_and_video(self):
        Favorite.objects.create(
            user=self.user,
            video=self.video,
        )

        with self.assertRaises(IntegrityError):
            Favorite.objects.create(
                user=self.user,
                video=self.video,
            )