from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.db import models

from .models import Blog, Review, Comment, SportsSubsection, SubsectionComment, Post
from .forms import RegisterForm, SubsectionCommentForm, SubsectionImageForm, PostForm, CommentForm, SportsSubsectionForm, SubsectionForm

from django.views.generic import DetailView
from .models import Post, Comment
from .models import Subsection
from django.contrib.contenttypes.models import ContentType
from .models import Subsection, SportsSubsection, Post
from .forms import PostForm

from django.contrib.auth.forms import UserChangeForm
from .forms import EditProfileForm, AvatarChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Remove this line:
# from .forms import ProfileForm, AvatarForm


# Muestra una lista de todos los blogs.
@method_decorator(never_cache, name='dispatch')
class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'
    login_url = 'login'


#Vista de BlogDetail
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subsections = self.object.subsections.all()
        paginator = Paginator(subsections, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

#Permite a un usuario autenticado crear un nuevo blog.
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blogapp/blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})

#Permite crear una reseña para un blog.
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


# Gestiona el inicio de sesión de usuarios.
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
    

# Permite registrar un nuevo usuario.
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


#Redirige tras solicitar recuperación de contraseña, mostrando un mensaje de éxito.
def password_reset_done_redirect(request):
    messages.success(request, "Correo de recuperación enviado. Revisa tu bandeja de entrada.")
    return redirect('login')

#Permite añadir un comentario a una reseña de blog.
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



from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect


#
@method_decorator(csrf_protect, name='dispatch')
class SportsSubsectionDetailView(DetailView):
    model = SportsSubsection
    template_name = 'blogapp/subsection_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SubsectionCommentForm()
        context['image_form'] = SubsectionImageForm(instance=self.object)
        return context

    # Permite a los usuarios editar su perfil
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = SubsectionCommentForm(request.POST)
        image_form = SubsectionImageForm(request.POST, request.FILES, instance=self.object)
        if 'image' in request.FILES and image_form.is_valid():
            image_form.save()
            return redirect('blogapp:subsection_detail', pk=self.object.pk)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.subsection = self.object
            comment.author = request.user
            comment.save()
            return redirect('blogapp:subsection_detail', pk=self.object.pk)
        context = self.get_context_data(object=self.object)
        context['form'] = comment_form
        context['image_form'] = image_form
        return self.render_to_response(context)

# Muestra el detalle de una subsección general y permite añadir posts.
@login_required
def subsection_detail(request, pk):
    subsection = get_object_or_404(Subsection, pk=pk)
    content_type = ContentType.objects.get_for_model(subsection)
    posts = Post.objects.filter(content_type=content_type, object_id=subsection.id)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.content_type = content_type
            post.object_id = subsection.id
            post.save()
            return redirect('blogapp:subsection_detail', pk=pk)
    else:
        post_form = PostForm()
    return render(request, 'blogapp/subsection_detail.html', {
        'subsection': subsection,
        'post_form': post_form,
        'posts': posts,
    })

# Permiten dar "me gusta" a un post.
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes += 1
    post.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# Permiten dar "No me gusta" a un post.
@login_required
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.dislikes += 1
    post.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# Permiten comentar a un post.
@login_required
def comment_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# Permiten eliminar posts o comentarios (solo si eres el autor).
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        messages.success(request, "La publicación ha sido borrada exitosamente.")
    else:
        messages.error(request, "No tienes permiso para borrar esta publicación.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

# Permite eliminar comentarios (solo si eres el autor).
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user:
        comment.delete()
        messages.success(request, "El comentario ha sido borrado exitosamente.")
    else:
        messages.error(request, "No tienes permiso para borrar este comentario.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

# Permite editar un post (solo si eres el autor).
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('blogapp:subsection_detail', pk=post.subsection.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blogapp/edit_post.html', {'form': form, 'post': post})
    else:
        messages.error(request, "No tienes permiso para editar esta publicación.")
        return redirect('blogapp:subsection_detail', pk=post.subsection.pk)
    
    # Permite crear una subsección dentro de un blog.
@login_required
def create_subsection(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        form = SubsectionForm(request.POST, request.FILES)
        if form.is_valid():
            subsection = form.save(commit=False)
            subsection.blog = blog
            subsection.owner = request.user  
            subsection.save()
            return redirect('blogapp:blog_detail', pk=blog.id)
    else:
        form = SubsectionForm()
    return render(request, 'blogapp/create_subsection.html', {'form': form, 'blog': blog})

# Permite añadir un post a una subsección 
@login_required
def add_post_to_subsection(request, subsection_type, subsection_id):
    if subsection_type == 'sports':
        subsection = get_object_or_404(SportsSubsection, pk=subsection_id)
    else:
        subsection = get_object_or_404(Subsection, pk=subsection_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.content_type = ContentType.objects.get_for_model(subsection)
            post.object_id = subsection.id
            post.save()
            # Redirige al detalle de la subsección correspondiente
            if subsection_type == 'sports':
                return redirect('blogapp:subsection_detail', pk=subsection.id)
            else:
                return redirect('blogapp:subsection_detail', pk=subsection.id)
    else:
        form = PostForm()
    return render(request, 'blogapp/add_post.html', {'form': form, 'subsection': subsection})

from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import Blog


# Alternativa a la vista de detalle de blog, con paginación de subsecciones.
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    subsections = blog.subsections.all()
    paginator = Paginator(subsections, 6)  # 6 subsecciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'object': blog,
        'page_obj': page_obj,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'blogapp/subsections_partial.html', context)
    return render(request, 'blogapp/blog_detail.html', context)

#Permiten editar o eliminar subsecciones (solo si eres el propietario).
class SubsectionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Subsection
    fields = ['name', 'description', 'image']
    template_name = 'blogapp/subsection_form.html'

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.blog.pk})

    def test_func(self):
        return self.request.user == self.get_object().owner

#
class SubsectionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Subsection
    template_name = 'blogapp/subsection_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.blog.pk})

    def test_func(self):
        return self.request.user == self.get_object().owner


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Subsection, SubsectionVote

# Permite a los usuarios valorar una subsección (1 a 5 estrellas), recalcula el promedio.
@csrf_exempt
@login_required
def rate_subsection(request, subsection_id, rating):
    if request.method == 'POST':
        try:
            subsection = Subsection.objects.get(pk=subsection_id)
            rating = int(rating)
            user = request.user

            vote, created = SubsectionVote.objects.get_or_create(
                user=user,
                subsection=subsection,
                defaults={'value': rating}
            )
            if not created and vote.value != rating:
                # Si el voto ya existe y el valor es diferente, actualiza el valor
                vote.value = rating
                vote.save()
            # Si el voto ya existe y el valor es igual, no hace nada

            # Recalcular el promedio
            votes = SubsectionVote.objects.filter(subsection=subsection)
            if votes.exists():
                avg = votes.aggregate(models.Avg('value'))['value__avg']
            else:
                avg = 0
            subsection.rating = avg
            subsection.rating_count = votes.count()
            subsection.rating_sum = votes.aggregate(models.Sum('value'))['value__sum'] or 0
            subsection.save()

            return JsonResponse({'success': True, 'new_rating': round(subsection.rating or 0, 1)})
        except Subsection.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'No existe la subsección'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

# Permite editar el perfil y el avatar del usuario.
@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        # Handle delete image action
        if 'delete_image' in request.POST:
            if profile.avatar:
                profile.avatar.delete(save=True)
                messages.success(request, 'Foto de perfil eliminada exitosamente.')
            return redirect('blogapp:edit_profile')
        form_profile = EditProfileForm(request.POST, instance=user)
        form_avatar = AvatarChangeForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeForm(user, request.POST)
        if form_profile.is_valid() and form_avatar.is_valid():
            form_profile.save()
            form_avatar.save()
            # Procesar cambio de contraseña si los campos están presentes y válidos
            if 'old_password' in request.POST and request.POST.get('old_password'):
                if password_form.is_valid():
                    user = password_form.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, '¡Tu contraseña fue actualizada exitosamente!')
                else:
                    messages.error(request, 'Por favor corrija el error en el cambio de contraseña.')
                    return render(request, 'blogapp/edit_profile.html', {
                        'form_profile': form_profile,
                        'form_avatar': form_avatar,
                        'password_form': password_form,
                        'user': user,
                    })
            return redirect('blogapp:blog_list')
    else:
        form_profile = EditProfileForm(instance=user)
        form_avatar = AvatarChangeForm(instance=profile)
        password_form = PasswordChangeForm(user)
    return render(request, 'blogapp/edit_profile.html', {
        'form_profile': form_profile,
        'form_avatar': form_avatar,
        'password_form': password_form,
        'user': user,
    })

#Permiten cambiar nombre de usuario.
@login_required
def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        if new_username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'El nombre de usuario ya está tomado.')
            else:
                request.user.username = new_username
                request.user.save()
                messages.success(request, 'Username actualizado Correctamente.')
                return redirect('blogapp:edit_profile')
    return render(request, 'blogapp/change_username.html')

#Permiten cambiar eL avatar del usuario.
@login_required
def change_avatar(request):
    if request.method == 'POST':
        form = AvatarChangeForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Avatar actualizado Correctamente.')
            return redirect('blogapp:edit_profile')
    else:
        form = AvatarChangeForm(instance=request.user.profile)
    return render(request, 'blogapp/change_avatar.html', {'form': form})

#Permiten cambiar el email del usuario.
@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if new_email:
            request.user.email = new_email
            request.user.save()
            messages.success(request, 'Email actualizado Correctamente.')
            return redirect('blogapp:edit_profile')
        else:
            messages.error(request, 'Proporcione una dirección de correo electrónico válida.')
    return render(request, 'blogapp/change_email.html')

#Permiten cambiar la contraseña del usuario.
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importantte!
            messages.success(request, '¡Tu contraseña fue actualizada exitosamente!')
            return redirect('blogapp:blog_list')
        else:
            messages.error(request, 'Por favor corrija el error a continuación.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'blogapp/change_password.html', {'form': form})