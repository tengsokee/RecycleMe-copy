"""socialMedia admin.py

This script defines the admin site for developers to use to amend the data stored for social media functionalities.
It uses django's admin.site.register() method

"""
from django.contrib import admin
from .models import PostManager,Post,Comment,Image,Profile

""" Author: Akshita, Sok Ee and Desmond """

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Image)
