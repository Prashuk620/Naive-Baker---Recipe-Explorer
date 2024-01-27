from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from naivebaker_app.models import Contact, Recipe, Profile,save_recipe

class ContactModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name='John Doe',
            email='john@example.com',
            recipe_name='Test Recipe',
            phone='1234567890',
            feedback='This is a test feedback',
            date=date.today(),
        )

    def test_contact_str(self):
        self.assertEqual(str(self.contact), 'John Doe')
        self.assertEqual(str(self.contact), 'RohanMistry')
        self.assertEqual(str(self.contact), 'WebDev23')
        self.assertEqual(str(self.contact), ' ')

        self.contact.name = 'Alice'
        self.assertEqual(str(self.contact), 'Alice')

        self.contact.name = 'Bob'
        self.assertEqual(str(self.contact), 'Bob')

        self.contact.name = 'Charlie'
        self.assertEqual(str(self.contact), 'Charlie')

        self.contact.name = ''
        self.assertEqual(str(self.contact), '')

        self.contact.name = 'John Doe'
        self.assertEqual(str(self.contact), 'John Doe')  

        self.contact.email = 'alice@example.com'
        self.assertEqual(str(self.contact), 'John Doe')  

    
        self.contact.feedback = 'New feedback'
        self.assertEqual(str(self.contact), 'John Doe')

        
        self.contact.date = date(2023, 1, 1)
        self.assertEqual(str(self.contact), 'John Doe')


class RecipeModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            owner=user,
            name='Test Recipe',
            ingredients='Ingredient 1, Ingredient 2',
            instructions='Step 1, Step 2',
            recipe_time='30 mins',
            types='veg',
            mealtypes='indian',
            mealtimes='breakfast',
            vegitarity='veg',
            category='Indian',
            meal_time='breakfast',
        )

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), 'Test Recipe')

    def test_recipe_default_values(self):
        self.assertEqual(self.recipe.types, 'veg')
        self.assertEqual(self.recipe.mealtypes, 'indian')
        self.assertEqual(self.recipe.mealtimes, 'breakfast')
        self.assertEqual(self.recipe.vegitarity, 'veg')
        self.assertEqual(self.recipe.category, 'Indian')
        self.assertEqual(self.recipe.meal_time, 'breakfast')

    def test_recipe_name_change(self):
        self.recipe.name = 'New Recipe Name'
        self.assertEqual(self.recipe.name, 'New Recipe Name')

    def test_recipe_instructions_change(self):
        self.recipe.instructions = 'New Instructions'
        self.assertEqual(self.recipe.instructions, 'New Instructions')

    def test_recipe_recipe_time_change(self):
        self.recipe.recipe_time = '45 mins'
        self.assertEqual(self.recipe.recipe_time, '45 mins')

    def test_recipe_types_change(self):
        self.recipe.types = 'non-veg'
        self.assertEqual(self.recipe.types, 'non-veg')

    def test_recipe_vegitarity_change(self):
        self.recipe.vegitarity = 'non-veg'
        self.assertEqual(self.recipe.vegitarity, 'non-veg')

    def test_recipe_image_upload_to(self):
        #we have a method `filepath` in your models.py
        expected_path = 'uploads/'
        self.assertTrue(self.recipe.image.path.startswith(expected_path))

    def test_recipe_image_blank_null(self):
        # Checks that image field is blank and null
        field = Recipe._meta.get_field('image')
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_recipe_invalid_type(self):
        # Checks that an invalid type choice raises a ValueError
        with self.assertRaises(ValueError):
            self.recipe.types = 'invalid_type'
            self.recipe.save()

    def test_recipe_invalid_mealtype(self):
        # Checks that an invalid mealtype choice raises a ValueError
        with self.assertRaises(ValueError):
            self.recipe.mealtypes = 'invalid_mealtype'
            self.recipe.save()

    def test_recipe_invalid_mealtime(self):
        # Checks that an invalid mealtime choice raises a ValueError
        with self.assertRaises(ValueError):
            self.recipe.mealtimes = 'invalid_mealtime'
            self.recipe.save()



class ProfileModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(
            user=user,
            forget_password_token='randomtoken',
        )

    def test_profile_str(self):
        self.assertEqual(str(self.profile), 'testuser')




class SaveRecipeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = save_recipe.objects.create(
            user=self.user,
            recipename='Test Recipe',
            image='dummy_image_data',
            cusinetype='Indian',
            meal_time='breakfast',
            preptime='30 mins',
            cooklink='http://example.com',
        )

    def test_save_recipe_str(self):
        self.assertEqual(str(self.recipe), "testuser's Test Recipe Recipe")

    def test_save_recipe_default_values(self):
        self.assertEqual(self.recipe.cusinetype, 'Indian')
        self.assertEqual(self.recipe.meal_time, 'breakfast')

    def test_save_recipe_blank_null_fields(self):
        self.assertTrue(save_recipe._meta.get_field('image').blank)
        self.assertTrue(save_recipe._meta.get_field('image').null)
        self.assertTrue(save_recipe._meta.get_field('cusinetype').blank)
        self.assertTrue(save_recipe._meta.get_field('cusinetype').null)
        self.assertTrue(save_recipe._meta.get_field('meal_time').blank)
        self.assertTrue(save_recipe._meta.get_field('meal_time').null)
        self.assertTrue(save_recipe._meta.get_field('preptime').blank)
        self.assertTrue(save_recipe._meta.get_field('preptime').null)
        self.assertTrue(save_recipe._meta.get_field('cooklink').blank)
        self.assertTrue(save_recipe._meta.get_field('cooklink').null)

    def test_save_recipe_url(self):
        self.assertEqual(self.recipe.cooklink, 'http://example.com')
    def test_save_recipe_user(self):
        self.assertEqual(self.recipe.user.username, 'testuser')

    def test_save_recipe_recipename(self):
        self.assertEqual(self.recipe.recipename, 'Test Recipe')

    def test_save_recipe_image(self):
        self.assertEqual(self.recipe.image, 'dummy_image_data')

    def test_save_recipe_cusinetype(self):
        self.assertEqual(self.recipe.cusinetype, 'Indian')

    def test_save_recipe_meal_time(self):
        self.assertEqual(self.recipe.meal_time, 'breakfast')

    def test_save_recipe_preptime(self):
        self.assertEqual(self.recipe.preptime, '30 mins')

    def test_save_recipe_cooklink(self):
        self.assertEqual(self.recipe.cooklink, 'http://example.com')

    # Additional test cases
    def test_save_recipe_recipename_change(self):
        self.recipe.recipename = 'New Recipe Name'
        self.assertEqual(self.recipe.recipename, 'New Recipe Name')

    def test_save_recipe_cusinetype_change(self):
        self.recipe.cusinetype = 'Italian'
        self.assertEqual(self.recipe.cusinetype, 'Italian')

    def test_save_recipe_meal_time_change(self):
        self.recipe.meal_time = 'lunch'
        self.assertEqual(self.recipe.meal_time, 'lunch')

    def test_save_recipe_preptime_change(self):
        self.recipe.preptime = '45 mins'
        self.assertEqual(self.recipe.preptime, '45 mins')

    def test_save_recipe_cooklink_change(self):
        self.recipe.cooklink = 'http://newexample.com'
        self.assertEqual(self.recipe.cooklink, 'http://newexample.com')

    def test_save_recipe_user_change(self):
        new_user = User.objects.create_user(username='newuser', password='newpass')
        self.recipe.user = new_user
        self.assertEqual(self.recipe.user.username, 'newuser')