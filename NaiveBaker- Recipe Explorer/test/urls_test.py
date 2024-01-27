from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from naivebaker_app.views import index, login, signup, home, addRecipe, contact, dashboard, saved_recipe, myrecipe, myshowRecipe

class UrlsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_authenticated(self):
        # home view requires authentication
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_unauthenticated(self):
        # the home view requires authentication
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redirects to index for unauthenticated users

    def test_addRecipe_view_authenticated(self):
        # the addRecipe view requires authentication
        self.client.force_login(self.user)
        response = self.client.get(reverse('addRecipe'))
        self.assertEqual(response.status_code, 200)

    def test_addRecipe_view_unauthenticated(self):
        # the addRecipe view requires authentication
        response = self.client.get(reverse('addRecipe'))
        self.assertEqual(response.status_code, 302)  # Redirects to index for unauthenticated users

    def test_contact_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_authenticated(self):
        #the dashboard view requires authentication
        self.client.force_login(self.user)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_unauthenticated(self):
        # the dashboard view requires authentication
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirects to index for unauthenticated users

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects to index after logout

    def test_saved_recipe_view_authenticated(self):
        # saved_recipe view requires authentication
        self.client.force_login(self.user)
        response = self.client.get(reverse('saved_recipe'))
        self.assertEqual(response.status_code, 200)

    def test_saved_recipe_view_unauthenticated(self):
        #saved_recipe view requires authentication
        response = self.client.get(reverse('saved_recipe'))
        self.assertEqual(response.status_code, 302)  # Redirects to index for unauthenticated users

    def test_myrecipe_view_authenticated(self):
        # the myrecipe view requires authentication
        self.client.force_login(self.user)
        response = self.client.get(reverse('myrecipe'))
        self.assertEqual(response.status_code, 200)

    def test_myrecipe_view_unauthenticated(self):
        # the myrecipe view requires authentication
        response = self.client.get(reverse('myrecipe'))
        self.assertEqual(response.status_code, 302)  # Redirects to index for unauthenticated users

    def test_forget_password_view(self):
        response = self.client.get(reverse('forget_password'))
        self.assertEqual(response.status_code, 200)

    def test_change_password_view(self):
        response = self.client.get(reverse('change_password', args=['token']))
        self.assertEqual(response.status_code, 200)

    def test_home_view_save_view(self):
        response = self.client.get(reverse('save-view'))
        self.assertEqual(response.status_code, 200)

    def test_addedrecipe_view_authenticated(self):
        # the addedrecipe view requires authentication
        self.client.force_login(self.user)
        response = self.client.get(reverse('addedrecipe-view'))
        self.assertEqual(response.status_code, 200)

    def test_addedrecipe_view_unauthenticated(self):
        # the addedrecipe view requires authentication
        response = self.client.get(reverse('addedrecipe-view'))
        self.assertEqual(response.status_code, 302)  # Redirects to index for unauthenticated users

    def test_invalid_url(self):
        response = self.client.get('/invalid-url/')
        self.assertEqual(response.status_code, 404)
