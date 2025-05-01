from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegisterForm
from django import forms
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView



# Aplica LoginRequiredMixin y never_cache a BlogListView
@method_decorator(never_cache, name='dispatch')
class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'
    login_url = 'login'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})


class ReviewCreateView(CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})


def bienvenida(request):
    return render(request, 'blogapp/Bienvenida.html')


# Login

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!') # El mensaje de éxito
            return redirect('blogapp:blog_list')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.') # El mensaje de error
            return render(request, 'blogapp/Login.html', {'error': 'Credenciales inválidas'})
    else:
        return render(request, 'blogapp/Login.html')
    

# Registrar

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error.as_text())
            return render(request, 'blogapp/Login.html', {'register_form': form, 'active_form': 'register'})
    else:
        form = RegisterForm()
        return render(request, 'blogapp/Login.html', {'register_form': form, 'active_form': 'register'})


def password_reset_done_redirect(request):
    messages.success(request, "Correo de recuperación enviado. Revisa tu bandeja de entrada.")
    return redirect('login')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

def add_comment(request, blog_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.reviewer = review
            comment.blog_id = blog_pk
            comment.review_id = review_pk
            comment.commenter = request.user
            comment.save()
            return redirect('blogapp:blog_detail', pk=blog_pk)
    else:
        form = CommentForm()
    return render(request, 'blogapp/add_comment.html', {'form': form, 'review': review})

    

