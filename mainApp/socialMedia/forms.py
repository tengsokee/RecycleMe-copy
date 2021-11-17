"""socialMedia forms.py

This script defines the forms for retrieving user inputs for socialMedia functionalities

Author: Akshita and Sok Ee

This file can also be imported as a module and contains the following
classes or functions:
    * PostForm - form for handling post uploads
    * CommentForm - form for handling comment uploads
    * UserRegisterForm - form for handling registration
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post,Comment,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

'''Sample form
class postForm(forms.ModelForm):
    class Meta:
        model = Contact_form
        fields = ['name','company','phone_num','email','message_type','message']
        widgets = {
            'phone_num': forms.TextInput(attrs={'placeholder': '97123452'})
        }
        labels = {
            'name': _('Name'),
            'company': _('Company'),
            'phone_num': _('Phone number'),
            'email': _('Email'),
            'message_type': _('Type of message'),
            'message': _('Message'),
'''


class PostForm(forms.ModelForm):
    """form for handling post uploads.
    """
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Enter your Post...'
            }))

    class Meta:
        model = Post
        fields = ['content']



class CommentForm(forms.ModelForm):
    """form for handling comment uploads.
    """
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Write your comment...'}
        ))

    class Meta:
        model = Comment
        fields = ['content']

class UserRegisterForm(UserCreationForm):
    """form for handling registration
    """
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

