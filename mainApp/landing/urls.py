"""landing urls.py

This script defines the mapping of urls to views for landing page

"""
from django.urls import path
from landing.views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
]
