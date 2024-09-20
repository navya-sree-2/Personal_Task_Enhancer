# urls.py 
from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views 
 
urlpatterns = [ 
    path('', views.home, name='home'), 
    path('login/', views.login_view, name='login'), 
    path('signup/', views.signup_view, name='signup'), 
    path('logout/', views.logout_view, name='logout'), 
    path('refresh-captcha/', views.refresh_captcha, name='refresh_captcha'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/pass_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/pass_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/pass_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/pass_reset_complete.html'), name='password_reset_complete'),
    # path('profile/<username>', views.profile, name='profile'),
]