from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


#crear modelo de blog
class Blog(models.Model):
    title = models.CharField(max_length=200)

    content = CKEditor5Field('Content', config_name='extends')

    #ENRICH TEXT ADDED
    
    # contenido = RichTextField(blank=True, null=True)
    content = CKEditor5Field('Content', config_name='default') 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    def __str__(self):
        return self.title

#crear modelo de blog
class SportsSubsection(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='sports_subsections')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='subsection_images/', blank=True, null=True)

    def __str__(self):
        return self.name

#Permite dividir el blog en temas o categorías, y gestionar valoraciones.
class Subsection(models.Model):
    blog = models.ForeignKey(Blog, related_name='subsections', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='subsections/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subsections', null=True)  # <--- Añade esta línea
    rating = models.FloatField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    rating_sum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

#Permite comentarios flexibles en diferentes tipos de subsecciones.
class SubsectionComment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    subsection = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.author.username} en {self.subsection.name}"

#Permite a los usuarios valorar y comentar blogs.
class Review(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username} - {self.blog.title}"

#Permite a los usuarios publicar contenido multimedia en subsecciones.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    subsection = GenericForeignKey('content_type', 'object_id')
    text = models.TextField()
    media = models.FileField(upload_to='post_media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    def __str__(self):
        return self.text[:50]


#Permite comentar publicaciones.
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

#Permite valorar subsecciones.
class SubsectionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()  # 1 a 5

    class Meta:
        unique_together = ('user', 'subsection')


#Permite que cada usuario tenga una foto de perfil personalizada.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

#crear perfil de usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


#Cuando se guarda un usuario, también se guarda su perfil si existe
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()