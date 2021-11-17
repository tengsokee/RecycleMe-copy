"""Map urls.py

This script defines the mapping of urls to views for map functionalities

Author: Hing Yee, Daniel, Desmond
"""
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'map'
urlpatterns = [
    path('', views.map, name = 'map'),
    path('<int:postalcode>',views.showNearestPoints,name = 'nearestLocations')
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)