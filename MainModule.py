'''
__author__ = "Simon Geigenberger"
__copyright__ = "Copyright 2017, Esri Deutschland GmbH"
__license__ = "Apache-2.0"
__version__ = "1.0"
__email__ = "s.geigenberger@esri.de"

Improvised for accessibility cloud by Ehtesham Hasnain

This module is used to set up the configuration data and call the functions in the GetAcsCldData and DataToAGO modules.
'''

import ReadAGOLConfig
import GetAcsCldData
import ReadAcsCldConfig
import DataToAGO

dictAGOLConfig = ReadAGOLConfig.readAGOLConfig()
print("ArcGIS Online / Portal configuration read in.")

dictAcsCldConfig = ReadAcsCldConfig.readAcsCldConfig()
print("Accessibility cloud configuration read in")

#The accessibility cloud data is loaded
gacd = GetAcsCldData.run(dictAcsCldConfig)
print("Accessibility cloud data loaded")

#The data of the data frame with the OSM data is loaded as a Feature Collection to the ArcGIS Online or Portal account.
dta = DataToAGO.run(dictAGOLConfig, gacd)
print("Upload to ArcGIS Online / Portal finished.")
