"""landing views.py

This script defines the views for landing page

This file can also be imported as a module and contains the following
classes or functions:
    * Index - view for visualing the landing page
"""

from django.shortcuts import render
from django.views import View

class Index(View):
    """ view for visualing the landing page
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'landing/index.html')