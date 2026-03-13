from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

# I also used AI here to help me test my app

class UserAuthTests(TestCase):
    def setUp(self):
        # setUp runs before every test. We use it to create a test client and a mock user.
        self.client = Client()
        self.password = 'strongtestpassword123'
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password=self.password
        )

    # --- LOGIN TESTS ---
    def test_login_page_get(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_page_post_success(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': self.password
        })
        # Should redirect to the blogsite home page upon successful login
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('blogsite:home'))

    def test_login_page_post_failure(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        # Should return to the same page (200 OK) and display an error message
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Username or password is incorrect" in str(m) for m in messages))

    # --- LOGOUT TESTS ---
    def test_logout_page(self):
        # Log the user in first
        self.client.login(username='testuser', password=self.password)
        # Hit the logout route
        response = self.client.get(reverse('users:logout'))
        # Should redirect back to the login page
        self.assertRedirects(response, reverse('users:login'))

    # --- REGISTER TESTS ---
    def test_register_page_get(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    # --- EDIT PROFILE TESTS ---
    def test_edit_profile_unauthenticated_redirects(self):
        # A user who isn't logged in should be redirected to the login page
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('users:login') + '?next=')) # Django's default redirect behavior

    def test_edit_profile_authenticated_success(self):
        # Log the user in
        self.client.login(username='testuser', password=self.password)
        
        # Submit the edit profile form
        response = self.client.post(reverse('users:edit_profile'), {
            'username': 'updated_testuser',
            'email': 'updated@example.com'
        })
        
        # Should redirect to login page (as defined in your views)
        self.assertRedirects(response, reverse('users:login'))
        
        # Refresh the user from the database and check if the details actually changed
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated_testuser')
        self.assertEqual(self.user.email, 'updated@example.com')


