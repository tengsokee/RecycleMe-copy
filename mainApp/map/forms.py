"""Map forms.py

This script defines the forms for retrieving user inputs for map functionalities

Author: Hing Yee

This file can also be imported as a module and contains the following
classes or functions:
    * RecyclingPointsPhotoForm - form for handling user photo uploads.
"""
from django import forms
from .models import RecyclingPointPhoto


class RecyclingPointPhotoForm(forms.ModelForm):
    """Form for the recycling point photo model"""
    class Meta:
        model = RecyclingPointPhoto
        fields = ('photo_id', 'photo_url',)
