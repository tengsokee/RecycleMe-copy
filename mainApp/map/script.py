"""Map script.py

This script reads KML files from data.gov.sg website and 
extracts relevant data on the recycling point to store in the app's database

Author: Hing Yee

This file can also be imported as a module and contains the following
classes or functions:
    * read_kml - function for reading KML files from data.gov.sg website to generate recycling points
"""

# Script to insert recycling points in database
import mysql.connector as mysql
import xml.etree.ElementTree as et

db = mysql.connect(
    host = "localhost",
    user = "recycleme",
    passwd = "Recycleme@123",
    database = "recycleme"
)

## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = db.cursor()

## defining the Query
query = "INSERT INTO map_recyclingpoint (name, categories, address, postalCode, description, hyperlink, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

values = [] # use this list to insert recycling points into database

# Import recycling points and save to a list
def read_kml(fname, categories):
    """function for reading KML files from data.gov.sg website to generate recycling points
    Parameters
    ----------
    fname : str
        The file name containing the recycling point
    categories : string
        category name for recycling point
    """
    doc = et.parse(fname)
    nmsp = "{http://www.opengis.net/kml/2.2}"

    if (fname == './recyclingpoints/cash-for-trash-kml.kml' or fname == './recyclingpoints/2nd-hand-goods-collection-points-kml.kml'):
        for pm in doc.iterfind('.//{0}Placemark'.format(nmsp)):

            # save list of longitude and latitude coordinates for displaying of recycling points on map
            for ls in pm.iterfind('{0}Point/{0}coordinates'.format(nmsp)):
                point_string = ls.text.strip().replace('\n','')[:-2]
                coord = []
                for i in point_string.split(","):
                    coord.insert(0, float(i))
                del coord[0]

            name = ""
            address = ""
            postalCode = ""
            description = ""
            hyperlink = ""
            categories = categories
            latitude = coord[0]
            longitude = coord[1]

            # save variables of recycling points
            for ls in pm.iterfind('{0}ExtendedData/{0}SchemaData/{0}SimpleData'.format(nmsp)):
                if ls.get('name') == "HYPERLINK":
                    hyperlink = ls.text
                if ls.get('name') == "DESCRIPTION":
                    description = ls.text
                if ls.get('name') == "ADDRESSUNITNUMBER":
                    address += ls.text
                if ls.get('name') == "ADDRESSSTREETNAME":
                    address = ls.text + ", " + address
                if ls.get('name') == "ADDRESSBLOCKHOUSENUMBER" or ls.get('name') == "ADDRESSBLOCKNUMBER":
                    address = "Blk " + ls.text + ", " + address
                if ls.get('name') == "ADDRESSBUILDINGNAME":
                    if address != "":
                        if address[-1] == " ":
                            address += ls.text
                    else:
                        address += ", " + ls.text
                if ls.get('name') == "ADDRESSPOSTALCODE":
                    postalCode = ls.text
                if ls.get('name') == "NAME":
                    name = ls.text

            if address[-2:] == ", ":
                address = address[0:-2]

            # insert recycling point tuple into list
            rp = (name, categories, address, postalCode, description, hyperlink, latitude, longitude)
            values.append(rp)

    elif (fname == './recyclingpoints/lighting-waste-collection-points-kml.kml'):
        for pm in doc.iterfind('.//{0}Placemark'.format(nmsp)):

            # save list of longitude and latitude coordinates for displaying of recycling points on map
            for ls in pm.iterfind('{0}Point/{0}coordinates'.format(nmsp)):
                point_string = ls.text.strip().replace('\n','')[:-2]
                coord = []
                for i in point_string.split(","):
                    coord.insert(0, float(i))
                del coord[0]

            name = ""
            address = ""
            postalCode = ""
            description = ""
            hyperlink = ""
            categories = categories
            latitude = coord[0]
            longitude = coord[1]

            # save name of recycling points
            for ls in pm.iterfind('{0}ExtendedData/{0}SchemaData/{0}SimpleData'.format(nmsp)):
                if ls.get('name') == "HYPERLINK":
                    hyperlink = ls.text
                if ls.get('name') == "DESCRIPTION":
                    description = ls.text
                if ls.get('name') == "ADDRESSUNITNUMBER":
                    address = ls.text + ", " + address
                if ls.get('name') == "ADDRESSSTREETNAME":
                    position = address.find("#")
                    if position == -1:
                        position = address.find("I") # for recycling point at IKEA
                        address = address[0:position] + ls.text + ", " + address[position:] 
                    else:
                        address = address[0:position] + ls.text + ", " + address[position:]
                if ls.get('name') == "ADDRESSBLOCKHOUSENUMBER":
                    address = "Blk " + ls.text + ", " + address
                if ls.get('name') == "ADDRESSBUILDINGNAME":
                    address += ls.text
                if ls.get('name') == "ADDRESSPOSTALCODE":
                    postalCode = ls.text
                if ls.get('name') == "NAME":
                    name = ls.text

            if address[-2:] == ", ":
                address = address[0:-2]

            # insert recycling point tuple into list
            rp = (name, categories, address, postalCode, description, hyperlink, latitude, longitude)
            values.append(rp)
            
    else:
        for pm in doc.iterfind('.//{0}Placemark'.format(nmsp)):

            # save list of longitude and latitude coordinates for displaying of recycling points on map
            for ls in pm.iterfind('{0}Point/{0}coordinates'.format(nmsp)):
                point_string = ls.text.strip().replace('\n','')[:-2]
                coord = []
                for i in point_string.split(","):
                    coord.insert(0, float(i))
                del coord[0]

            name = ""
            address = ""
            postalCode = ""
            description = ""
            hyperlink = ""
            categories = categories
            latitude = coord[0]
            longitude = coord[1]

            # save name of recycling points
            for ls in pm.iterfind('{0}ExtendedData/{0}SchemaData/{0}SimpleData'.format(nmsp)):
                if ls.get('name') == "HYPERLINK":
                    hyperlink = ls.text
                if ls.get('name') == "DESCRIPTION":
                    description = ls.text
                if ls.get('name') == "ADDRESSBLOCKHOUSENUMBER" or ls.get('name') == "ADDRESSBLOCKNUMBER":
                    address = "Blk " + ls.text + ", " + address
                if ls.get('name') == "ADDRESSUNITNUMBER":
                    address += ls.text
                if ls.get('name') == "ADDRESSSTREETNAME":
                    position = address.find("#")
                    if position == -1:
                        position = address.find(",")
                        position = address.find(",") # second occurence of ","
                        address = address[0:position] + ", " + ls.text + address[position+2:]
                    else:
                        address = address[0:position] + ls.text + ", " + address[position:]
                if ls.get('name') == "ADDRESSBUILDINGNAME":
                    address += ", " + ls.text
                if ls.get('name') == "ADDRESSPOSTALCODE":
                    postalCode = ls.text
                if ls.get('name') == "NAME":
                    name = ls.text

            if address[-2:] == ", ":
                address = address[0:-2]

            # insert recycling point tuple into list
            rp = (name, categories, address, postalCode, description, hyperlink, latitude, longitude)
            values.append(rp)
            
    #print(values)

# Add recycling points for cash for trash
fname = './recyclingpoints/cash-for-trash-kml.kml'
read_kml(fname, "Cash For Trash")

# Add recycling points for 2nd hand goods
fname = './recyclingpoints/2nd-hand-goods-collection-points-kml.kml'
read_kml(fname, "2nd Hand Goods")

# Add recycling points for e-waste
fname = './recyclingpoints/e-waste-recycling-kml.kml'
read_kml(fname, "E-Waste")

# Add recycling points for lighting waste
fname = './recyclingpoints/lighting-waste-collection-points-kml.kml'
read_kml(fname, "Lighting Waste")

## executing the query with values
cursor.executemany(query, values)

## to make final output we have to run the 'commit()' method of the database object
db.commit()

print(cursor.rowcount, "records inserted")