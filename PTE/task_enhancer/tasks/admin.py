from django.contrib import admin
from .models import Profile, Task, Category 
# Register your models here.

admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Category)