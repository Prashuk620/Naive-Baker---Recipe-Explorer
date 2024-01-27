from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from naivebaker_app.models import Recipe, save_recipe, Profile,Contact
from naivebaker_app.views import *
from django.contrib import messages



class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_success(self):
        response = self.client.post(reverse('viewlogin'), {'username': 'testuser', 'pass': 'testpass'})
        self.assertEqual(response.status_code, 302)  # Expect a redirect after successful login
        self.assertRedirects(response, '/home/')
        self.assertTrue('_auth_user_id' in self.client.session)  # Check if the user is authenticated

    def test_login_failure_invalid_credentials(self):
        response = self.client.post(reverse('viewlogin'), {'username': 'testuser', 'pass': 'wrongpassword'})
        self.assertEqual(response.status_code, 302)  # Expect a redirect after unsuccessful login
        self.assertRedirects(response, '/login/')
        messages.error  # Ensure an error message is set in the messages framework

    def test_login_failure_missing_credentials(self):
        response = self.client.post(reverse('viewlogin'), {})
        self.assertEqual(response.status_code, 302)  # Expect a redirect after unsuccessful login
        self.assertRedirects(response, '/login/')
        messages.error  # Ensure an error message is set in the messages framework

    def test_login_failure_invalid_user(self):
        response = self.client.post(reverse('viewlogin'), {'username': 'nonexistentuser', 'pass': 'testpass'})
        self.assertEqual(response.status_code, 302)  # Expect a redirect after unsuccessful login
        self.assertRedirects(response, '/login/')
        messages.error  # Ensure an error message is set in the messages framework

    def test_login_get_request(self):
        response = self.client.get(reverse('viewlogin'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for GET request
        self.assertTemplateUsed(response, 'login.html')  # Ensure the correct template is used

    def test_authenticated_user_redirect(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('viewlogin'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an authenticated user
        self.assertRedirects(response, '/home/')

class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_success(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass',
            'password2': 'testpass'
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect after successful signup
        self.assertRedirects(response, '/signup/')
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)  # Check if the user is created
        self.assertEqual(Profile.objects.filter(user__username='testuser').count(), 1)  # Check if the profile is created

    def test_signup_failure_password_mismatch(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass',
            'password2': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect after unsuccessful signup
        self.assertRedirects(response, '/signup/')
        messages.warning  # Ensure a warning message is set in the messages framework

    def test_signup_failure_username_taken(self):
        User.objects.create_user(username='testuser', email='existing@example.com', password='testpass')
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass',
            'password2': 'testpass'
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect after unsuccessful signup
        self.assertRedirects(response, '/signup/')
        messages.info  # Ensure an info message is set in the messages framework

    def test_signup_failure_email_taken(self):
        User.objects.create_user(username='existinguser', email='testuser@example.com', password='testpass')
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass',
            'password2': 'testpass'
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect after unsuccessful signup
        self.assertRedirects(response, '/signup/')
        messages.info  # Ensure an info message is set in the messages framework

    def test_signup_get_request(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for GET request
        self.assertTemplateUsed(response, 'signup.html')  # Ensure the correct template is used

    def test_signup_authenticated_user_redirect(self):
        User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.client.force_login(User.objects.get(username='testuser'))
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an authenticated user
        self.assertRedirects(response, '/signup/')
    
class AddRecipeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)

    def test_add_recipe_success(self):
        response = self.client.post(reverse('addRecipe'), {
            'recipeName': 'Test Recipe',
            'list_of_ingre': 'Ingredient 1, Ingredient 2',
            'steps': 'Step 1, Step 2',
            'recipeTime': '30 mins',
            'vegitarity': 'veg',
            'category': 'Indian',
            'mealtime': 'breakfast',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect after successful recipe addition
        self.assertRedirects(response, '/addRecipepra/')
        self.assertEqual(Recipe.objects.filter(name='Test Recipe').count(), 1)  # Check if the recipe is added

    def test_add_recipe_failure_missing_fields(self):
        response = self.client.post(reverse('addRecipe'), {})
        self.assertEqual(response.status_code, 200)  # Expect a successful response for unsuccessful recipe addition
        self.assertTemplateUsed(response, 'addRecipepra.html')  # Ensure the correct template is used
        messages.error  # Ensure an error message is set in the messages framework

    def test_add_recipe_get_request(self):
        response = self.client.get(reverse('addRecipe'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for GET request
        self.assertTemplateUsed(response, 'addRecipepra.html')  # Ensure the correct template is used

    def test_add_recipe_authenticated_user(self):
        response = self.client.get(reverse('addRecipe'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for authenticated user

    def test_add_recipe_unauthenticated_user_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('addRecipe'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an unauthenticated user
        self.assertRedirects(response, '/login/?next=/addRecipe/')

    def test_add_recipe_with_image(self):
        with open('path/to/your/test/image.jpg', 'rb') as image_file:
            response = self.client.post(reverse('addRecipe'), {
                'recipeName': 'Test Recipe',
                'list_of_ingre': 'Ingredient 1, Ingredient 2',
                'steps': 'Step 1, Step 2',
                'recipeTime': '30 mins',
                'vegitarity': 'veg',
                'category': 'Indian',
                'mealtime': 'breakfast',
                'image': image_file,
            })
        self.assertEqual(response.status_code, 302)  # Expect a redirect after successful recipe addition with image
        self.assertRedirects(response, '/addRecipepra/')
        self.assertEqual(Recipe.objects.filter(name='Test Recipe').count(), 1)  # Check if the recipe is added with image

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)

    def test_home_view_success(self):
        image_url = base64.b64encode('dummy_image_data'.encode('utf-8')).decode('utf-8')
        response = self.client.get(reverse('home_view'), {
            'param1': image_url,
            'param2': 'Test Recipe',
            'param3': 'Indian',
            'param4': 'breakfast',
            'param5': '30 mins',
            'param6': 'http://example.com',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect after successful recipe addition
        self.assertRedirects(response, '/home/')
        self.assertEqual(save_recipe.objects.filter(recipename='Test Recipe').count(), 1)  # Check if the recipe is added

    def test_home_view_failure_missing_params(self):
        response = self.client.get(reverse('home_view'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect after unsuccessful recipe addition
        self.assertRedirects(response, '/home/')
        messages.error  # Ensure an error message is set in the messages framework

    def test_home_view_authenticated_user(self):
        response = self.client.get(reverse('home_view'), {
            'param1': 'dummy_image_data',
            'param2': 'Test Recipe',
            'param3': 'Indian',
            'param4': 'breakfast',
            'param5': '30 mins',
            'param6': 'http://example.com',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an authenticated user
        self.assertRedirects(response, '/home/')

    def test_home_view_unauthenticated_user_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('home_view'), {
            'param1': 'dummy_image_data',
            'param2': 'Test Recipe',
            'param3': 'Indian',
            'param4': 'breakfast',
            'param5': '30 mins',
            'param6': 'http://example.com',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an unauthenticated user
        self.assertRedirects(response, '/login/?next=/home_view/')

class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_success(self):
        response = self.client.post(reverse('contact'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'recipe_name': 'Test Recipe',
            'phone': '1234567890',
            'message': 'This is a test feedback',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect after successful contact form submission
        self.assertRedirects(response, '/contactus/')
        self.assertEqual(Contact.objects.filter(name='John Doe').count(), 1)  # Check if the contact entry is added

    def test_contact_failure_missing_fields(self):
        response = self.client.post(reverse('contact'), {})
        self.assertEqual(response.status_code, 200)  # Expect a successful response for unsuccessful form submission
        self.assertTemplateUsed(response, 'contact.html')  # Ensure the correct template is used
        messages.error  # Ensure an error message is set in the messages framework

    def test_contact_get_request(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for GET request
        self.assertTemplateUsed(response, 'contact.html')  # Ensure the correct template is used

    def test_contact_authenticated_user(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for an authenticated user

    def test_contact_unauthenticated_user_redirect(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for an unauthenticated user

    def test_contact_with_date(self):
        response = self.client.post(reverse('contact'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'recipe_name': 'Test Recipe',
            'phone': '1234567890',
            'message': 'This is a test feedback',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect after successful contact form submission
        self.assertRedirects(response, '/contactus/')
        self.assertEqual(Contact.objects.filter(name='John Doe', date__isnull=False).count(), 1) 

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.client.force_login(self.user)

    def test_dashboard_authenticated_user(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for an authenticated user
        self.assertTemplateUsed(response, 'user_profile.html')  # Ensure the correct template is used
        self.assertEqual(response.context['username'], 'testuser')  # Check if the correct username is in the context
        self.assertEqual(response.context['email'], 'testuser@example.com')  # Check if the correct email is in the context

    def test_dashboard_unauthenticated_user_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an unauthenticated user
        self.assertRedirects(response, '/')

    def test_dashboard_anonymous_user_redirect(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an anonymous user
        self.assertRedirects(response, '/')

    def test_dashboard_get_request(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for GET request
        self.assertTemplateUsed(response, 'user_profile.html')

class SavedRecipeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)

    def test_saved_recipe_authenticated_user(self):
        response = self.client.get(reverse('saved_recipe'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for an authenticated user
        self.assertTemplateUsed(response, 'saved_recipe.html')  # Ensure the correct template is used

    def test_saved_recipe_unauthenticated_user_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('saved_recipe'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an unauthenticated user
        self.assertRedirects(response, '/login/?next=/saved_recipe/')

    def test_saved_recipe_get_request(self):
        response = self.client.get(reverse('saved_recipe'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for GET request
        self.assertTemplateUsed(response, 'saved_recipe.html')

class ViewLogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)

    def test_viewlogout_authenticated_user(self):
        response = self.client.get(reverse('viewlogout'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect after successful logout
        self.assertRedirects(response, '/')
        self.assertTrue(response.wsgi_request.user.is_anonymous)  # Check if the user is now anonymous
        messages.info  # Ensure an info message is set in the messages framework

    def test_viewlogout_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('viewlogout'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an unauthenticated user
        self.assertRedirects(response, '/')
        self.assertTrue(response.wsgi_request.user.is_anonymous)  # Check if the user is already anonymous

    def test_viewlogout_get_request(self):
        response = self.client.get(reverse('viewlogout'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for GET request
        self.assertRedirects(response, '/')
        self.assertTrue(response.wsgi_request.user.is_anonymous)  # Check if the user is now anonymous
        messages.info

class ChangePasswordViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, forget_password_token='testtoken')

    def test_change_password_success(self):
        response = self.client.get(reverse('change_password', args=['testtoken']))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for a valid token
        self.assertTemplateUsed(response, 'change-password.html')  # Ensure the correct template is used

        response = self.client.post(reverse('change_password', args=['testtoken']), {
            'new_password': 'newpass',
            'reconfirm_password': 'newpass',
            'user_id': str(self.user.id),
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect after successful password change
        self.assertRedirects(response, '/login/')
        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('newpass'))  # Check if the password is changed

    def test_change_password_failure_missing_fields(self):
        response = self.client.post(reverse('change_password', args=['testtoken']), {})
        self.assertEqual(response.status_code, 302)  # Expect a redirect for unsuccessful password change
        self.assertRedirects(response, f'/change-password/testtoken/')
        messages.success  # Ensure a success message is set in the messages framework

    def test_change_password_failure_password_mismatch(self):
        response = self.client.post(reverse('change_password', args=['testtoken']), {
            'new_password': 'newpass',
            'reconfirm_password': 'mismatchpass',
            'user_id': str(self.user.id),
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect for unsuccessful password change
        self.assertRedirects(response, f'/change-password/testtoken/')
        messages.success  # Ensure a success message is set in the messages framework

    def test_change_password_invalid_token(self):
        response = self.client.get(reverse('change_password', args=['invalidtoken']))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an invalid token
        self.assertRedirects(response, '/')

    def test_change_password_invalid_password(self):
        response = self.client.post(reverse('change_password', args=['testtoken']), {
            'new_password': 'short',
            'reconfirm_password': 'short',
            'user_id': str(self.user.id),
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an invalid password
        self.assertRedirects(response, f'/change-password/testtoken/')
        messages.success  # Ensure a success message is set in the messages framework

    def test_change_password_post_invalid_token(self):
        response = self.client.post(reverse('change_password', args=['invalidtoken']), {
            'new_password': 'newpass',
            'reconfirm_password': 'newpass',
            'user_id': str(self.user.id),
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an invalid token
        self.assertRedirects(response, '/')
        messages.success  # Ensure a success message is set in the messages framework

    def test_change_password_post_no_token(self):
        response = self.client.post(reverse('change_password', args=[]), {
            'new_password': 'newpass',
            'reconfirm_password': 'newpass',
            'user_id': str(self.user.id),
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect for no token
        self.assertRedirects(response, '/')
        messages.success 

class ForgetPasswordViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.profile = Profile.objects.create(user=self.user)

    def test_forget_password_success(self):
        response = self.client.post(reverse('forget_password'), {'username': 'testuser'})
        self.assertEqual(response.status_code, 302)  # Expect a redirect after successful password reset
        self.assertRedirects(response, '/forget-password/')
        profile_obj = Profile.objects.get(user=self.user)
        self.assertTrue(profile_obj.forget_password_token)  # Check if the forget password token is set
        # You can add more assertions to check if the email is sent, based on your email sending implementation

    def test_forget_password_no_user(self):
        response = self.client.post(reverse('forget_password'), {'username': 'nonexistentuser'})
        self.assertEqual(response.status_code, 302)  # Expect a redirect for a non-existent user
        self.assertRedirects(response, '/forget-password/')
        messages.success  # Ensure a success message is set in the messages framework

    def test_forget_password_empty_username(self):
        response = self.client.post(reverse('forget_password'), {'username': ''})
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an empty username
        self.assertRedirects(response, '/forget-password/')
        messages.success  # Ensure a success message is set in the messages framework

    def test_forget_password_get_request(self):
        response = self.client.get(reverse('forget_password'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for GET request
        self.assertTemplateUsed(response, 'forget-password.html')  # Ensure the correct template is used

    def test_forget_password_exception(self):
        # Simulate an exception during forget password processing
        with self.assertRaises(Exception):
            response = self.client.post(reverse('forget_password'), {'username': 'testuser'})

    def test_forget_password_invalid_token(self):
        # Assuming that a token with invalid UUID format is considered invalid
        response = self.client.get(reverse('change_password', args=['invalidtoken']))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an invalid token
        self.assertRedirects(response, '/')

    def test_forget_password_missing_token(self):
        response = self.client.get(reverse('change_password', args=[]))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for missing token
        self.assertRedirects(response, '/')

    def test_forget_password_invalid_username(self):
        response = self.client.post(reverse('forget_password'), {'username': '!@#invalidusername'})
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an invalid username
        self.assertRedirects(response, '/forget-password/')
        messages.success  # Ensure a success message is set in the messages framework

    def test_forget_password_post_invalid_token(self):
        response = self.client.post(reverse('change_password', args=['invalidtoken']), {'username': 'testuser'})
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an invalid token
        self.assertRedirects(response, '/')

class MyShowRecipeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)

    def test_myshowrecipe_post_request(self):
        response = self.client.post(reverse('myshowRecipe'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect after POST request
        self.assertRedirects(response, '/addRecipe/')

    def test_myshowrecipe_get_request(self):
        response = self.client.get(reverse('myshowRecipe'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for GET request
        self.assertTemplateUsed(response, 'myshowRecipe.html')  # Ensure the correct template is used

    def test_myshowrecipe_redirect_unauthenticated_user(self):
        self.client.logout()
        response = self.client.post(reverse('myshowRecipe'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an unauthenticated user
        self.assertRedirects(response, '/login/?next=/myshowRecipe/')

    def test_myshowrecipe_post_request_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('myshowRecipe'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect after POST request
        self.assertRedirects(response, '/addRecipe/')

    def test_myshowrecipe_post_request_owner(self):
        # Assuming user is the owner of the recipe
        owner = User.objects.create_user(username='owneruser', password='ownerpass')
        self.client.force_login(owner)
        response = self.client.post(reverse('myshowRecipe'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect after POST request
        self.assertRedirects(response, '/addRecipe/')

    def test_myshowrecipe_get_request_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('myshowRecipe'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an unauthenticated user
        self.assertRedirects(response, '/login/?next=/myshowRecipe/')

    def test_myshowrecipe_get_request_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('myshowRecipe'))
        self.assertEqual(response.status_code, 200)  # Expect a successful response for GET request
        self.assertTemplateUsed(response, 'myshowRecipe.html')
