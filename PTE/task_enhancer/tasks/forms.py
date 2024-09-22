from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
from .models import Profile

class SignupForm(UserCreationForm): 
    email = forms.EmailField(required=True) 

    class Meta: 
        model = User 
        fields = ['username', 'email', 'password1', 'password2'] 

    def save(self, commit=True): 
        user = super().save(commit=False) 
        user.email = self.cleaned_data['email'] 
        if commit: 
            user.save() 
        return user 


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'gender', 'mobile_number', 'img']


class LoginForm(forms.Form): 
    username = forms.CharField(max_length=150) 
    password = forms.CharField(widget=forms.PasswordInput) 
    captcha = forms.CharField(max_length=6)

# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ['title', 'description', 'due_date', 'priority', 'category']