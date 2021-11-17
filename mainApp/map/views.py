"""Map views.py

This script defines the views for Map functionalities. 

Author: Hing Yee, Daniel, Desmond

This file can also be imported as a module and contains the following
classes or functions:
    * map - function for visualising the recycling points on a map, displaying details on recycling points, and adding photos to recycling points
    * validateInputPostalCode - function that checks a postal code is valid and returns a string message on the outcome
    * get_lat_long - returns a dictionary with an array key containing custom error code as the first element and error message or latitude,longitude array, if the postal code is valid and a place with that code exists
    * showNearestPoints - function for visualing the nearest recycling points to a postal code.
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
import requests
from django.urls import reverse
from django.core import serializers
import json
from .forms import RecyclingPointPhotoForm

from .models import RecyclingPoint, RecyclingPointsManager, RecyclingPointPhoto
# Create your views here.

def map(request):
    """function for visualising the recycling points on a map, displaying details on recycling points, and adding photos to recycling points
    """
    #get recycling points and pass into context
    recyclingpoints = RecyclingPoint.objects.all()
    
    tmp_json = serializers.serialize("json",recyclingpoints)
    tmp_Obj = json.loads(tmp_json)

    recyclingpoints_json = json.dumps(tmp_Obj)

    error_message1= ""
    #get image from form on recycling point
    if request.method == 'POST':
        form = RecyclingPointPhotoForm(request.POST, request.FILES)
        print('hello')
  
        if form.is_valid():
                error_message1= ""

    else:
        form = RecyclingPointPhotoForm()

    recyclingpointphotos = RecyclingPointPhoto.objects.all()
    tmp_json2 = serializers.serialize("json",recyclingpointphotos)
    tmp_Obj2 = json.loads(tmp_json2)

    recyclingpointphotos_json = json.dumps(tmp_Obj2)

    error_message1= ""
    #get image from form on recycling point
    if request.method == 'POST':
        form = RecyclingPointPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            if(request.user.is_authenticated):
                form.save()
                return redirect('map:map')
            else:
                error_message1 = "Unable to add photo. You're not logged in"
                
    query = request.GET.get('search')
    if query:
        error_message = validateInputPostalCode(query)
    else:
        error_message = ""
    if(error_message == "valid"):
        results = get_lat_long(query)
        #if code is 4, then the searched location is a valid place in singapore
        if results["response"][0]==4:
            return HttpResponseRedirect(reverse('map:nearestLocations',kwargs={'postalcode':query}))
        else:
            error_message = "no places found"
    context = {
        'recyclingpoints_json': recyclingpoints_json,
        'form': form,
        'recyclingpointphotos_json': recyclingpointphotos_json,
        'search_bar_message':error_message,
        'error_message':error_message1
    }

    return render(request, 'map/map.html', context)

def validateInputPostalCode(query):
    """Validates that an input is a valid postal code

    Parameters
    ----------
    query : str
        The user input entered through a search bar

    Returns
    -------
    string
        a message detailing the outcome of the check
    """
    if query:
        if(len(query)!=6):
            return "Postal codes should have 6 digits"
        else:
            try:
                postalcode = int(query)
                if(10000<=int(query)<=830000):
                    return "valid"
                else:
                    return "invalid postal code"
            except:
                return "Postal codes shouldn't have letters"


def get_lat_long(postalcode):
    """Get the latitude and longitude of a postal code

    Parameters
    ----------
    postalcode : str
        The postal code

    Returns
    -------
    dictionary
        a standard key with an array as value. The first element of the array contains a custom error code and the subsequent elements contain an error message if a place with the postal code is not found. Otherwise, the second and third elements are the latitude and longitude respectively
    """
    url = "https://developers.onemap.sg/commonapi/search?searchVal="+str(postalcode)+"&returnGeom=Y&getAddrDetails=Y&pageNum=1"
    try:
        response = requests.get(url)
        
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        return {"response":[1,"server error. please try again later"]}
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        return {"response":[2,"Unidentified error. Please try again later"]}
    else:
        results = json.loads(response.text)
        if(len(results["results"])>0):
            latitude = float(results["results"][0]["LATITUDE"])
            longitude = float(results["results"][0]["LONGITUDE"])
            return {"response":[4,latitude,longitude]}
        else:
            return {"response":[0,"no results found"]}

def showNearestPoints(request,postalcode):
    """View for visualisation of the nearest recycling points to a postalcode. 

    Parameters
    ----------
    postalcode : str
        The user input postal code from which to find nearest recycling points
    """
    lat_long = (get_lat_long(postalcode))["response"]
    recyclingpoints = serializers.serialize("json",RecyclingPoint.objects.all())
    tmp_Obj = json.loads(recyclingpoints)
    recyclingpoints_json = json.dumps(tmp_Obj)
    recyclingpointsphotos = serializers.serialize("json",RecyclingPointPhoto.objects.all())
    tmp_Obj = json.loads(recyclingpointsphotos)
    recyclingpointsphotos_json = json.dumps(tmp_Obj)

    error_message1= ""
    #get image from form on recycling point
    if request.method == 'POST':
        form = RecyclingPointPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            if(request.user.is_authenticated):
                form.save()
                return redirect('map:map')
            else:
                error_message1 = "Unable to add photo. You're not logged in"
                

    else:
        form = RecyclingPointPhotoForm()
    #finds and extract input in search bar when search is clicked
    query = request.GET.get('search')
    if query:
        error_message = validateInputPostalCode(query)
        print(error_message)
    else:
        error_message = ""
    if(error_message == "valid"):
        results = get_lat_long(query)
        #if code is 4, then the searched location is a valid place in singapore
        if results["response"][0]==4:
            return HttpResponseRedirect(reverse('map:nearestLocations',kwargs={'postalcode':query}))
        else:
            error_message = "no places found"
    context = {
        'recyclingpoints_json':recyclingpoints_json,
        'postalcode':postalcode,
        'lat':lat_long[1],
        'long':lat_long[2],
        'recyclingpointsphotos':recyclingpointsphotos_json,
        'search_bar_message':error_message,
        'error_message':error_message1
    }
    return render(request, 'map/nearest_locations.html', context)