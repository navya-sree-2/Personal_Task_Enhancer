from django.contrib import admin
from .models import Profile, Task, Category, Notification
# Register your models here.

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Notification)

from django.contrib import admin
from django.utils import timezone
from .models import Task
from notifications.signals import notify

@admin.action(description='Check for overdue tasks and notify users')
def check_overdue_tasks(modeladmin, request, queryset):
    overdue_tasks = Task.objects.filter(is_completed=False, due_date__lt=timezone.now())
    for task in overdue_tasks:
        notify.send(
            task.user,
            recipient=task.user,
            verb=f'Task "{task.title}" is overdue!'
        )
    modeladmin.message_user(request, 'Overdue task notifications sent.')

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'is_completed']
    actions = [check_overdue_tasks]

admin.site.register(Task, TaskAdmin)
