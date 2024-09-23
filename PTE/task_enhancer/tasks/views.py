from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, UserUpdateForm, ProfileUpdateForm, TaskForm
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
from .models import Profile, Task, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
    user = request.user
    # Ensure profile exists
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)



@login_required
def task_list(request):
    category_id = request.GET.get('category', None)
    if category_id:
        tasks = Task.objects.filter(user=request.user, category_id=category_id).order_by('due_date')
    else:
        tasks = Task.objects.filter(user=request.user).order_by('due_date')
    paginator = Paginator(tasks, 5)  # Change '5' to the number of tasks you want per page
    page = request.GET.get('page', 1)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    categories = Category.objects.all()
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'categories': categories
    })


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'tasks/delete_task.html', {'task': task})


def dashboard_view(request):
    user = request.user
    total_tasks = Task.objects.filter(user=user).count()
    pending_tasks = Task.objects.filter(user=user, status='P').count()
    in_progress_tasks = Task.objects.filter(user=user, status='IP').count()
    completed_tasks = Task.objects.filter(user=user, status='C').count()

    context = {
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
    }
    
    return render(request, 'dash.html', context)

