# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q
from frontsite.models import UserProfile, Category, Avatar, Rhyme, Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}), label=u'Komentarz',
        error_messages={'invalid': u'Komentarz ma zły format.'}
    )
    class Meta:
        model = Comment
        fields = ('content', )

class RhymeForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    class Meta:
        model = Rhyme
        fields = ('title', 'content', 'category')
    def save(self, commit=True):
        rhyme = super(RhymeForm, self).save(commit=False)
        if commit is True:
            rhyme.save()
        return rhyme

class AvatarForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput())
    class Meta:
        model = Avatar
        exclude = ('name', 'path', 'profile')

class CategoryForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': u'Tytuł'}), label=u'Tytuł', error_messages={'required': 'Pole wymagane',})
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), label=u'Opis')
    class Meta:
        model = Category
        fields = ('title', 'description')

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': u'Nazwa użytkownika'}), label=u'Nazwa użytkownika', error_messages={'required': 'Pole wymagane',})
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': u'E-mail'}), label=u'E-mail', error_messages={'required': 'Pole wymagane',})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': u'Hasło'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': u'Powtórz'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            raise forms.ValidationError(u'Password must match')
        return self.cleaned_data

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(u'Email "%s" already in use' % email)
        return email

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(user.password)
        if commit is True:
            user.save()
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.save()
        return user

class LoginForm(forms.ModelForm):
    user = None
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label=u'Hasło')
    login = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label=u'Login')
    class Meta:
        model = User
        fields = ('login', 'password')
    def is_valid(self):
        if not super(LoginForm, self).is_valid():
            return False
        try:
            user = User.objects.get(
                Q(username=self.cleaned_data.get('login')) | Q(email=self.cleaned_data.get('login'))
            )
        except User.DoesNotExist:
            self._errors['no_user'] = 'User does not exists'
            return False
        if not check_password(self.cleaned_data.get('password'), user.password):
            self._errors['invalid_password'] = 'Password is invalid'
            return False
        if not user.is_active:
            self._errors['not_active'] = 'User is not active'
            return False
        self.user = auth.authenticate(username=user.username, password=self.cleaned_data.get('password'))
        return True