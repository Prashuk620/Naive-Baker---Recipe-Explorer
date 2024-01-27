from django.contrib import admin
from django.urls import path,include
from naivebaker_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name = 'index'),
    path('login',views.viewlogin,name = 'login'),
    path('signup',views.signup,name = 'signup'),
    path('home',views.home,name = 'home'),
    path('addRecipe',views.addRecipe,name = 'addRecipe'),
    path('contact',views.contact,name = 'contact'),
    path('dashboard',views.dashboard,name = 'dashboard'),
    path('logout',views.viewlogout,name = 'logout'),
    path('dashboard/saved_recipe',views.saved_recipe,name = 'saved_recipe'),
    path('dashboard/myrecipe',views.myrecipe,name = 'myrecipe'),
    # path('logout',views.view_logout,name = 'logout'),
    # path('user_profile', views.user_profile, name='user_profile')
    path('forget-password/' , views.ForgetPassword , name="forget_password"),
    path('change-password/<token>/' , views.ChangePassword , name="change_password"),
    path('dashboard/myrecipe/myshowrecipe' , views.myshowRecipe , name="myshowRecipe")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
