"""
URL configuration for blogproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blogapp.views import login_view, password_reset_done_redirect
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', include('blogapp.urls')),
    path('', include('blogapp.urls')),
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='blogapp/Login.html'), name='login'),
    path('blogs/', include('blogapp.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        email_template_name='registration/password_reset_email.html',
        html_email_template_name='registration/password_reset_email.html'
    ), name='password_reset'),
    path('password_reset/done/', password_reset_done_redirect, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)