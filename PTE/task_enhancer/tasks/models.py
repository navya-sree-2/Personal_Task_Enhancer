from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    fullname = models.CharField(max_length=100, blank=True)  # Fullname field
    gender = models.CharField(max_length=10, blank=True)
    mobile_number = models.CharField(max_length=10, blank=True)
    img = models.ImageField(default='default.jpeg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  # This will return the name of the category


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]

    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('IP', 'In Progress'),
        ('C', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title