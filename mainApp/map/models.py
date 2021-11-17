"""Map models.py

This script defines the entities and managers for Map functionalities. 

Author: Hing Yee

This file can also be imported as a module and contains the following
classes or functions:
    * RecyclingPointsManager - contains control functions that manages the recycling point entity
    * RecyclingPoint - model for a recycling point. Contains the fields of a recycling point
    * RecyclingPointPhoto - model for a recycling point photo. Contains the fields for a photo
"""
from django.db import models

# Create your models here.

class RecyclingPointsManager(models.Manager):
    """Manages recycling points created
    """
    def createRecyclingPoint(self, name, categories, address, postalCode, description, hyperlink, latitude, longitude):
        """Creates a recycling point

        Parameters
        ----------
        name : str
            Name of recycling point
        categories : str
            Category of recycling point
        address : str
            Address of recycling point
        postalCode : str
            Postal code of recycling point
        description : str
            Description of recycling point
        hyperlink : str
            Hyperlink of recycling point
        latitude: float
            Latitude of recycling point
        longitude: float
            Longitude of recycling point

        Returns
        -------
        Recycling point
            A recycling point object
        """
        recyclingPoint = self.create(name=name,categories=categories,address=address,postalCode=postalCode,description=description,hyperlink=hyperlink, latitude=latitude, longitude=longitude)
        recyclingPoint.save()
        return recyclingPoint

    def getRecyclingPoint(self, RecyclingPt_id):
        """Finds a specific recycling point based on recycling point id
        Parameters
        ----------
        RecyclingPt_id : int
            Unique id of recycling point

        Returns
        -------
        Queryset
            All stored information on the recycling point.
        """
        recyclingPoint = self.filter(id=RecyclingPt_id)
        return recyclingPoint

class RecyclingPoint(models.Model):
    """Details of a recycling point
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    categories = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    postalCode = models.CharField(max_length=6)
    description = models.TextField(max_length=500)
    hyperlink = models.URLField(max_length=300)
    latitude = models.CharField(max_length=50, default="")
    longitude = models.CharField(max_length=50, default="")
    objects = RecyclingPointsManager()
    def __str__(self):
        return str(self.id)
    
# photos many to one relationship with recyclingpoint
class RecyclingPointPhoto(models.Model):
    """Photos of a recycling point
    """
    photo_id = models.ForeignKey(RecyclingPoint, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)
    photo_url = models.ImageField(upload_to='recyclingpoint_pics/')

