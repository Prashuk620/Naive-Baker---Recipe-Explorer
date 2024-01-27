from django.contrib import admin

# Register your models here.
# from django.contrib import admin
from naivebaker_app.models import Contact,Recipe,Profile

# Register your models here.
admin.site.register(Contact)
admin.site.register(Recipe)
admin.site.register(Profile)
