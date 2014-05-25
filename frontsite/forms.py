# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
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
        return user

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    login = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = User
        fields = ('login', 'password')
    def is_valid(self):
        if not super(LoginForm, self).is_valid():
            return False
        return True