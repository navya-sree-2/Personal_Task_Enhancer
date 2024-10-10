from django.contrib import admin
from .models import Profile, Category, Notification
# Register your models here.

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Notification)
