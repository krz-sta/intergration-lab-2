from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post

# Create your tests here.

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_post_str(self):
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
        )
        self.assertEqual(str(post), 'Test Post')

    def test_post_creation(self):
        post = Post.objects.create(
            title='Another Post',
            content='Some content',
            author=self.user,
        )
        self.assertEqual(Post.objects.count(), 1)


class PostListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_post_list_status_code(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_empty(self):
        response = self.client.get(reverse('post-list'))
        self.assertContains(response, 'Brak postów')