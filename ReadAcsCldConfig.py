'''
__author__ = "Simon Geigenberger"
__copyright__ = "Copyright 2017, Esri Deutschland GmbH"
__license__ = "Apache-2.0"
__version__ = "1.0"
__email__ = "s.geigenberger@esri.de"

Adapted for accessibility cloud by Ehtesham Hasnain
'''

import sys
import json

def readAcsCldConfig():
    url = "https://www.accessibility.cloud/place-infos"
    accept = "application/json"
    headers = {}
    params = {}
    filters = ["at-least-partially-accessible-by-wheelchair", "fully-accessible-by-wheelchair", "not-accessible-by-wheelchair", "unknown-wheelchair-accessibility"]

    dictAcsCldConfig = {}

    # Try to open the config file
    try:
        json_data = open("acscldconfig.json").read()
    except:
        print("JSON file does not exist.")
        sys.exit()

    # Try to load the config file as JSON, validate the JSON syntax
    try:
        data = json.loads(json_data)
    except:
        print("JSON file cannot be read.")
        sys.exit()

    #Validates if App-Token is provided
    try:
        AppToken = data["X-App-Token"]
        headers["X-App-Token"] = AppToken
        headers["Accept"] = accept
    except:
        print("Accessibility cloud app-token not provided")
        sys.exit()

    # Validates if parameters (latitude, longitude, radius, limit, filters) are provided
    try:
        parameters = data["requestparameters"]

        try:
            latitude = parameters["latitude"]
            latitude = float(latitude)
            params["latitude"] = latitude
        except:
            print("No latitude provided")
            sys.exit()

        try:
            longitude = parameters["longitude"]
            longitude = float(longitude)
            params["longitude"] = longitude
        except:
            print("No longitude provided")
            sys.exit()

        try:
            accuracy = parameters["radius"]
            accuracy = float(accuracy)
            params["accuracy"] = accuracy
        except:
            print("search radius not provided")

        try:
            limit = parameters["limit"]
            limit = float(limit)
            params["limit"] = limit
        except:
            print("Search limit not provided")

        try:
            searchfilter = parameters["filter"]
            for items in filters:
                filterExists = False
                if items == searchfilter:
                    filterExists = True
                    break
            if not filterExists:
                print("Invalid accessibility search filter")
                sys.exit()
            params["filter"] = searchfilter
        except SystemExit:
            sys.exit()
        except:
            print("No accessibility filters chosen")

        #Validation of the coordinates
        if latitude < 90 and latitude > -90:
            if longitude < 180 and longitude > -180:
                print("Coordinates ok")
            else:
                print("Longitude is out of range.")
                sys.exit()
        else:
            print("Latitude is out of range.")
            sys.exit()

        #Validation of the search radius
        if accuracy < 10001 and accuracy > 0:
            print("Search radius ok")
        else:
            print("Invalid search radius (valid 0 to 10000)")
            sys.exit()

    except SystemExit:
        sys.exit()
    except:
        print("Location parameters not provided")
        sys.exit()

    dictAcsCldConfig["url"] = url
    dictAcsCldConfig["headers"] = headers
    dictAcsCldConfig["params"] = params

    return(dictAcsCldConfig)

#test = readAcsCldConfig()
#print(test)