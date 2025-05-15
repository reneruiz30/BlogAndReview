from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import SportsSubsection, SubsectionComment, Post, Comment, Subsection, Profile



class RegisterForm(UserCreationForm):
    document = forms.CharField(required=False, label="Número de documento")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class SubsectionCommentForm(forms.ModelForm):
    class Meta:
        model = SubsectionComment
        fields = ['text']

class SubsectionImageForm(forms.ModelForm):
    class Meta:
        model = SportsSubsection
        fields = ['image']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'media']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class SportsSubsectionForm(forms.ModelForm):
    class Meta:
        model = SportsSubsection
        fields = ['name', 'description', 'image']  # Add any other fields you want in the form

class SubsectionForm(forms.ModelForm):
    class Meta:
        model = Subsection
        fields = ['name', 'description', 'image']  # Puedes agregar más campos si lo necesitas

#
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# Si tienes un modelo Profile para la foto de perfil:

class AvatarChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']