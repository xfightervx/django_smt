from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post
# Create your tests here.


class BlogTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="a"
        )

        cls.post = Post.objects.create(
            title = "A test Title",
            body = "This is a the test Body",
            author = cls.user
        )
    
    def test_post_model(self):
        self.assertEqual(self.post.title, "A test Title")
        self.assertEqual(self.post.body, "This is a the test Body")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "A test Title")
        self.assertEqual(self.post.get_absolute_url(), "/post/1")

    def test_url_exits_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code , 200)
    
    def test_url_exist_postdetails(self):
        response = self.client.get("/post/1")
        self.assertEqual(response.status_code, 200)
    
    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code , 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "This is a the test Body")

    def test_post_detailview(self):
        response = self.client.get(reverse("post_detail",
                                   kwargs = {"pk":self.post.pk}))
        noresponse = self.client.get("/post/100000")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(noresponse.status_code, 404)
        self.assertContains(response, "A test Title")
        self.assertTemplateUsed(response, "post_detail.html")
        