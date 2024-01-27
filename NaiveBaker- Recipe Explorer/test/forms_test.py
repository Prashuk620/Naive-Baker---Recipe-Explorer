from django.test import TestCase
from django.contrib.auth.models import User
from naivebaker_app.forms import RecipeUserCreationForm 

class RecipeFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_recipe_user_creation_form_valid(self):
        form_data = {
            'user': self.user,
            'name': 'Test Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'instructions': 'Step 1, Step 2',
            'recipe_time': '30 mins',
            'types': 'veg',
            'mealtypes': 'indian',
            'mealtimes': 'breakfast',
        }
        form = RecipeUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_user_creation_form_missing_name(self):
        form_data = {
            'user': self.user,
            'ingredients': 'Ingredient 1, Ingredient 2',
            'instructions': 'Step 1, Step 2',
            'recipe_time': '30 mins',
            'types': 'veg',
            'mealtypes': 'indian',
            'mealtimes': 'breakfast',
        }
        form = RecipeUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_recipe_user_creation_form_blank_instructions(self):
        form_data = {
            'user': self.user,
            'name': 'Test Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'instructions': '',
            'recipe_time': '30 mins',
            'types': 'veg',
            'mealtypes': 'indian',
            'mealtimes': 'breakfast',
        }
        form = RecipeUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('instructions', form.errors)

    def test_recipe_user_creation_form_invalid_recipe_time(self):
        form_data = {
            'user': self.user,
            'name': 'Test Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'instructions': 'Step 1, Step 2',
            'recipe_time': 'invalid_time',
            'types': 'veg',
            'mealtypes': 'indian',
            'mealtimes': 'breakfast',
        }
        form = RecipeUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('recipe_time', form.errors)

    def test_recipe_user_creation_form_empty_mealtypes(self):
        form_data = {
            'user': self.user,
            'name': 'Test Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'instructions': 'Step 1, Step 2',
            'recipe_time': '30 mins',
            'types': 'veg',
            'mealtypes': '',
            'mealtimes': 'breakfast',
        }
        form = RecipeUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mealtypes', form.errors)

    def test_recipe_user_creation_form_invalid_mealtimes(self):
        form_data = {
            'user': self.user,
            'name': 'Test Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'instructions': 'Step 1, Step 2',
            'recipe_time': '30 mins',
            'types': 'veg',
            'mealtypes': 'indian',
            'mealtimes': 'invalid_time',
        }
        form = RecipeUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mealtimes', form.errors)

    def test_recipe_user_creation_form_missing_user(self):
        form_data = {
            'name': 'Test Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'instructions': 'Step 1, Step 2',
            'recipe_time': '30 mins',
            'types': 'veg',
            'mealtypes': 'indian',
            'mealtimes': 'breakfast',
        }
        form = RecipeUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('user', form.errors)
