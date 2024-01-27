from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Recipe

class RecipeUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Recipe
        feilds = ('user','name','ingredients','instructions','recipe_time','types','mealtypes','mealtimes')

class RecipeUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = Recipe
        feilds = ('user','name','ingredients','instructions','recipe_time','types','mealtypes','mealtimes')

