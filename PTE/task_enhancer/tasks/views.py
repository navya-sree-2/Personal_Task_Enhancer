from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from django.http import HttpResponse
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

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!') 
def signup_view(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send activation email
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            # Print the message to check email content
            print(message)

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            try:
                email.send()  # Attempt to send the email
                print("Email sent successfully")
            except Exception as e:
                print(f"Error sending email: {e}")

            messages.success(request, "Please confirm your email address to complete the registration")
            return redirect('login')

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
