from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from naivebaker_app.models import Contact,Recipe
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage
from django.contrib.auth.decorators import login_required
from .models import *
from .helpers import send_forget_password_mail
from .views import *

# Create your views here.
def index(request) :
    return render(request,'index.html')

def myshowRecipe(request) :
    if request.method == "POST" :
        owner = request.user
        print(owner)
        return redirect('/addRecipe')

    return render(request,'myshowRecipe.html')

def viewlogin(request) :
    if request.method == "POST" :
        uname = request.POST.get("username")
        pass1 = request.POST.get("pass")
        myuser = authenticate(username = uname,password = pass1)

        if myuser is not None :
            login(request,myuser)
            messages.success(request,"Logged In Successfully")
            return redirect('/home')
        else :
            messages.error(request,"Invalid Credentials")
            return redirect('/login')

    return render(request,'login.html')

def signup(request) :
    
        if request.method == "POST" :
            uname = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password1")
            confirmpassword = request.POST.get("password2")

            if password != confirmpassword :
                messages.warning(request,"Password is Incorrect") 
                return redirect('/signup')
            
            try : 
                 if User.objects.get(username=uname):
                    messages.info(request,'UserName is Taken')
                    return redirect('/signup')
            except :
                 pass
            try : 
                 if User.objects.get(email=email):
                    messages.info(request,'Email is Taken')
                    return redirect('/signup')
            except :
                 pass

            myuser = User.objects.create_user(uname,email,password)
            myuser.save()
            profile_obj = Profile.objects.create(user = myuser )
            profile_obj.save()
            messages.info(request,'Sign Up is Done Successfully,Please Login')
            return redirect('/signup')
        return render(request,'signup.html')
    
def addRecipe(request) :
    # if request.user.is_anonymous:
    #     return redirect("/login")
    if request.method == "POST":

        recipe = Recipe()
        recipe.name = request.POST.get('recipeName')
        recipe.ingredients = request.POST.get('list_of_ingre')
        recipe.instructions = request.POST.get('steps')
        recipe.recipe_time = request.POST.get('recipeTime')
        recipe.vegitarity = request.POST.get('vegitarity')
        recipe.category = request.POST.get('category')
        recipe.meal_time = request.POST.get('mealtime')
        recipe.owner = request.user
        if len(request.FILES) != 0:
            recipe.image = request.FILES['image']
        recipe.save()
        messages.success(request, "Recipe is added successfully!!!")
        redirect('/addRecipe')

    return render(request,'addRecipe.html')

def contact(request) :
        # if request.user.is_anonymous:
        #     return redirect("/login")
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            recipe_name = request.POST.get('recipe_name')
            phone = request.POST.get('phone')
            feedback = request.POST.get('message')
            contact = Contact(name=name,email=email,recipe_name = recipe_name,phone = phone,feedback=feedback,date = datetime.today())
            contact.save()
            messages.success(request, "Thanks for your valuable feedback")
            redirect('/contactus')
        return render(request,'contact.html')

def viewlogout(request) :
    logout(request)
    messages.info(request,"Logged Out Successfully")
    return redirect('/')

@login_required
def dashboard(request):
     if request.user.is_anonymous:
        return redirect("/")
     else :
        current_user = request.user
        username = current_user.username
        email = current_user.email
        context = {'username' : username,
                'email' : email}
        return render(request,'user_profile.html',context)
         
def myrecipe(request) : 
    user_id = request.user
    user_recipes = Recipe.objects.filter(owner_id=user_id)
    return render(request, 'myrecipe.html', {'user_recipes': user_recipes})

def home_view(request):
    imageurl = request.GET.get('param1', '')
    recipename = request.GET.get('param2', '')
    cusinetype = request.GET.get('param3', '')
    meal_time = request.GET.get('param4', '')
    prep_time = request.GET.get('param5', '')
    cooklink = request.GET.get('param6', '')

    imageurl = base64.b64decode(imageurl).decode('utf-8')
    # Your processing logic goes here
    savedone = save_recipe()
    savedone.user =   request.user
    savedone.recipename = recipename
    savedone.image = imageurl
    savedone.cusinetype = cusinetype
    savedone.meal_time = meal_time
    savedone.preptime = prep_time
    savedone.cooklink = cooklink
    savedone.save()
    messages.success(request, "Recipe is added successfully!!")
    return redirect('/home')
def saved_recipe(request):
    user_id = request.user
    user_recipes = save_recipe.objects.filter(user_id=user_id)
    print(user_recipes)
    return render(request, 'saved_recipe.html', {'user_recipes': user_recipes})
