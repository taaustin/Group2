# Filname: geoShapework.py
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
    shapefile = filepath#
    #read file
    data = gpd.read_file(shapefile)
    return data

def checkDistrict(zipcodeList, districtNum):
    for zipcode in zipcodeList:
        if zipcode.district == districtNum:
            for zipNeigh in zipcode.neighbors:
                if zipNeigh.added == False:
                    print("*****************************************************************************")
                    print("*****************************************************************************")



#Creates objects, see zipcode.py for class details, uses class function to check for neighbors
def createZipObjects(data, zipColumn="ZCTA5CE10", popColumn="POP100", geoColumn="geometry"):
    zipcodeList = []
    for index,row in data.iterrows():
        zipObj = Zipcode(row[zipColumn], row[popColumn], row[geoColumn].centroid, row[geoColumn])
        zipcodeList.append(zipObj)
    for zipcode in zipcodeList:   
        for zipcode2 in zipcodeList:
            #verify it isnt the same zip in question
            if zipcode.zip != zipcode2.zip:
                #if they aren;t already in eachother's neighors check them.
                if zipcode2 in zipcode.neighbors and zipcode in zipcode2.neighbors:
                    continue
                else:
                    zipcode.checkNeighbors(zipcode2)
    return zipcodeList

#Helper function to search for a zipcode, takes the zipcode to search for and the zipcode list.
def searchForZip(zipcodeToSearchFor, zipcodes):
    for zipcode in zipcodes:
        if zipcode.zip == zipcodeToSearchFor:
            return zipcode
    print("Zip not found")
    return

#Function to get the total population of all zipcodes.
def getTotalPopulation(zipcodeList):
    sum = 0
    for zipcode in zipcodeList:
        sum = sum + zipcode.population
    return sum

#Main function
def main():
    filepath = "./MDdata/Maryland_Census_Data__ZIP_Code_Tabulation_Areas_ZCTAs.shp"
    print("Please wait, loading shapefile data...")
    data = readShapefile(filepath)
    zipcodes = createZipObjects(data)
    zipcodeToSearchFor = input("Search for a zipcode, enter it here: ")
    searchResults = searchForZip(zipcodeToSearchFor, zipcodes)
    print("\nYou're searched returned:\n")
    searchResults.printInformation()


if __name__ == "__main__": 
    # calling main function 
    main()
