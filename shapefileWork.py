# Filname: shapefileWork.py
# Overiview: Main file for working with a shapefile
# Written by: Todd Austin
# Date: 3/26/2020
# 
# Purpose: Used to read shapefile, and create objects of class Zipcode
# then generates a list of these zipcode objects sorted from East to West. 

import geopandas as gpd
from shapely.geometry import Polygon
from zipcode import Zipcode

#read the shapefile found in the directory provided
def readShapefile(filepath):
    #read file
    data = gpd.read_file(filepath)
    return data

#used to sort the list of zipcodes from east to west
def sortCentroid(e):
    return str(e.centroid)

#Creates objects, see zipcode.py for class details, uses class function to check for neighbors
def createZipObjects(data):
    zipcodeList = []
    for index,row in data.iterrows():
        zipObj = Zipcode(row["ZCTA5CE10"], row["POP100"], row["geometry"].centroid, row["geometry"])
        zipcodeList.append(zipObj)
    for zipcode in zipcodeList:   
        for zipcode2 in zipcodeList:
            if zipcode != zipcode2:
                if zipcode2 in zipcode.neighbors or zipcode in zipcode2.neighbors:
                    break
                else:
                    zipcode.checkNeighbors(zipcode2)
                    
    zipcodeList.sort(key=sortCentroid)
    return zipcodeList

def searchForZip(zipcodeToSearchFor, zipcodes):
    for zipcode in zipcodes:
        if zipcode.zip == zipcodeToSearchFor:
            return zipcode
    print("Zip not found")
    return

#Main function
def main():
    print("Please wait, loading shapefile data...")
    data = readShapefile()
    zipcodes = createZipObjects(data)
    #zipcodes[0].printInformation() #first in list, furthest east, Ocean City
    #zipcodes[len(zipcodes)-1].printInformation() # last in list, furthest west, Western MD
    zipcodeToSearchFor = input("Search for a zipcode, enter it here: ")
    searchResults = searchForZip(zipcodeToSearchFor, zipcodes)
    print("\nYou're searched returned:\n")
    searchResults.printInformation()
    

if __name__ == "__main__": 
    # calling main function 
    main()