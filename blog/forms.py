from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, TextInput, Textarea


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body"]
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок',
            }),
            "body": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Основной текст',
                "rows": 4,
            }),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Оставьте комментарий',
                "rows": 3,
            }),
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Это поле необходимо заполнить')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['type'] = 'login'
        self.fields['username'].widget.attrs['name'] = 'username'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['type'] = 'password'
        self.fields['password1'].widget.attrs['name'] = 'password1'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['name'] = 'password2'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['type'] = 'email'
        self.fields['email'].widget.attrs['name'] = 'email'
        self.fields['email'].widget.attrs['placeholder'] = "example@site.com"
