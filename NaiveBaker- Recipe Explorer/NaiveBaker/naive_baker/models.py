from django.db import models
import os,datetime
from django.contrib.auth.models import User


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    recipe_name = models.CharField(max_length=122)
    phone = models.CharField(max_length=122)
    feedback = models.TextField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return self.name
    
# take image at path function

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)


# take recipes 
class Recipe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to = filepath,null=True,blank=True)
    recipe_time = models.CharField(max_length=8,null = True)
    type=(
        ('veg',"VEG"),
        ('nonveg',"NONVEG")
    )
    types = models.CharField(max_length=10,choices=type,default="veg")
    mealtype=(
        ('indian',"INDIAN"),
        ('thai',"THAI"),
        ('mexican',"MEXICAN"),
        ('french',"FRENCH"),
        ('chinese',"CHINESE")
    )
    mealtypes = models.CharField(max_length=20,choices=mealtype,default="indian")
    mealtime=(
        ('breakfast',"BREAKFAST"),
        ('lunch',"LUNCH"),
        ('dinner',"DINNER")
    )
    mealtimes = models.CharField(max_length=40,choices=mealtime,default="breakfast")
    vegitarity = models.CharField(max_length=8,null = True,default="veg")
    category = models.CharField(max_length=10,null = True,default="Indian")
    meal_time = models.CharField(max_length=20,null = True,default="breakfast")
    # def __str__(self):
    #     return self.name



class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
