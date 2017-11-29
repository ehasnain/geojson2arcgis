'''
__author__ = "Ehtesham Hasnain"
__email__ = "e.hasnain@esri.de"
'''

import sys
import requests
import json

def run(AcsCldConfig):

    #load AcsCldConfig initial data
    url = AcsCldConfig["url"]

    headers = AcsCldConfig["headers"]

    params = AcsCldConfig["params"]

    #send request over HTTP
    r = requests.get(url, params=params, headers=headers, stream=True)

    #Exception handling of server error if any
    text = r.text
    text_json = json.loads(text)

    try:
        error = text_json["error"]
        print("X-app-token error:", error["reason"], "\nDetails: ", error["details"])
        sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print("X-App-Token valid")

    #load data in json format
    try:
        data = r.json()
    except:
        print(r.text)
        sys.exit()

    #extract features from the json data
    try:
        feature_data = data["features"]
    except:
        print("No feature data available")
        sys.exit()

    #Exception of no point feature data
    if feature_data == []:
        print("No accessibility data found at this location with the given search parameters")
        sys.exit()

    #format data in DataToAGO.py acceptable format for upload/update of point feature layer
    dictData = []

    for d in feature_data:
        geometry = d["geometry"]
        coordinate = geometry["coordinates"]
        properties = d["properties"]
        name = properties["name"]
        accessibility = properties["accessibility"]
        accessible = {}
        for item in accessibility:
            accessible[list(accessibility)[0]] = accessibility[list(accessibility)[0]]
        wheelchair = accessible[list(accessible)[0]]
        id = (properties["originalId"])
        category = properties["category"]
        sourceId = properties["sourceId"]

        dictElement = {}

        dictElement["Name"] = name
        if wheelchair[list(wheelchair)[0]]:
            if list(accessibility)[0] == "partiallyAccessibleWith":
                dictElement[list(wheelchair)[0] + "Accessible"] = "partially"
            else:
                dictElement[list(wheelchair)[0] + "Accessible"] = "Yes"
        else:
            dictElement[list(wheelchair)[0] + "Accessible"] = "No"
        dictElement["id"] = float(id)
        dictElement["lon"] = coordinate[0]
        dictElement["lat"] = coordinate[1]
        dictElement["sourceId"] = sourceId
        dictElement["attribute"] = category

        dictData.append(dictElement)

    return dictData

