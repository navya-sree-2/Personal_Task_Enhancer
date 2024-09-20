from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm
from django.contrib import messages
from .utils import generate_random_string 
from django.http import JsonResponse 
# Create your views here.
def home(request):  
    return render(request, 'registration/home.html')  

def login_view(request):
    if request.method == 'POST': 
        form = LoginForm(request.POST) 
        if form.is_valid(): 
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password'] 
            captcha = form.cleaned_data['captcha'] 

            # Validate CAPTCHA 
            if captcha == request.session.get('captcha'): 
                user = authenticate(request, username=username, password=password) 
                if user is not None: 
                    login(request, user) 
                    # Clear CAPTCHA from session after successful login 
                    del request.session['captcha'] 
                    return redirect('dashboard')  # Redirect to dashboard or any desired page 
                else: 
                    messages.error(request, 'Invalid username or password.') 
            else: 
                messages.error(request, 'Invalid CAPTCHA. Please try again.') 
    else: 
        form = LoginForm() 
        # Generate CAPTCHA 
        captcha = generate_random_string(length=6) 
        request.session['captcha'] = captcha  # Store CAPTCHA in session 

    context = { 
        'form': form, 
        'captcha': request.session.get('captcha', ''),  # Pass CAPTCHA to the template 
    } 
    return render(request, 'registration/login.html', context) 

def refresh_captcha(request): 
    new_captcha = generate_random_string(length=6) 
    request.session['captcha'] = new_captcha 
    return JsonResponse(new_captcha, safe=False) 

def signup_view(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  # Use the custom SignupForm  
        if form.is_valid():  
            form.save()  
            username = form.cleaned_data.get('username')  
            messages.success(request, f'Account created for {username}!')  
            return redirect('login')  # Redirect to login page after successful signup  
    else:  
        form = SignupForm()  # Use the custom SignupForm  
    return render(request, 'registration/signup.html', {'form': form})  

def logout_view(request):  
    logout(request)  
    messages.success(request, 'You have successfully logged out.')  
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html')
