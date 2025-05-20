from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import SportsSubsection, SubsectionComment, Post, Comment, Subsection, Profile


#Clase de registro de usuarios
class RegisterForm(UserCreationForm):
    document = forms.CharField(required=False, label="Número de documento")

#Modelo de registro de usuarios
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


#Permite agregar comentarios a las secciones 
class SubsectionCommentForm(forms.ModelForm):
    class Meta:
        model = SubsectionComment
        fields = ['text']

#Permite subir o modificar la imagen de una subsección
class SubsectionImageForm(forms.ModelForm):
    class Meta:
        model = SportsSubsection
        fields = ['image']
        
#Permite crear publicaciones con texto y archivos multimedia (imagen o video).
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'media']


#Permite agregar comentarios a las publicaciones
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

#Permite agregar una subsección a un deporte
class SportsSubsectionForm(forms.ModelForm):
    class Meta:
        model = SportsSubsection
        fields = ['name', 'description', 'image']  # Add any other fields you want in the form

#Permite crear o editar subsecciones generales, incluyendo nombre, descripción e imagen.
class SubsectionForm(forms.ModelForm):
    class Meta:
        model = Subsection
        fields = ['name', 'description', 'image']  # Puedes agregar más campos si lo necesitas

#Permite a los usuarios editar su información básica de perfil.
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']



# Permite a los usuarios cambiar su foto de perfil
class AvatarChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']