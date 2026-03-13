from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Posts, Tag
from django.core.files.uploadedfile import SimpleUploadedFile

# I used AI here to thoroughly test my app. I'm not familiar enough with Django's testing to write something
# myself, but I didn't want to move forward without ensuring that everything works so far. I did this in addition 
# to manually testing my app myself.

class BlogTests(TestCase):
    def setUp(self):
        """Set up a user, a tag, and a test client for all tests."""
        self.user = User.objects.create_user(username='blogger', password='password123')
        self.tag = Tag.objects.create(name="Python")
        self.client = Client()
        
        # Create a sample image for testing image uploads
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/jpeg'
        )

    # --- MODEL TESTS ---

    def test_post_short_description(self):
        """Tests if the short_description correctly trims long content."""
        long_text = "word " * 60  # Creates a string with 60 words
        post = Posts.objects.create(
            author=self.user,
            title="Long Post",
            content=long_text,
            image=self.test_image
        )
        
        description = post.short_description()
        # Based on your logic: it checks for > 50 words but returns the first 30
        self.assertTrue(description.endswith("..."))
        self.assertEqual(len(description.split()), 30) # 30 words + "..."

    # --- VIEW TESTS ---

    def test_home_page_status_code(self):
        """Verify the home page loads correctly."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_create_post_view(self):
        """Verify that a logged-in user can create a post and the author is set automatically."""
        self.client.login(username='blogger', password='password123')
        
        response = self.client.post(reverse('create'), {
            'title': 'New Test Post',
            'content': 'This is a test content.',
            'image': self.test_image,
            'tags': [self.tag.id]
        })
        
        # Check if redirected to home
        self.assertEqual(response.status_code, 302)
        
        # Check if the post actually exists and the author was set to 'blogger'
        post = Posts.objects.get(title='New Test Post')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.tags.count(), 1)

    def test_delete_post_view(self):
        """Verify that a post can be deleted."""
        post = Posts.objects.create(
            author=self.user, 
            title="Delete Me", 
            content="Bye", 
            image=self.test_image
        )
        
        # Perform the delete (Your view handles POST for deletion)
        response = self.client.post(reverse('delete_posts', args=[post.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Posts.objects.filter(id=post.id).exists())