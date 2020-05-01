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
                    print("FUCKIN RUGHT this shit wasnt added  " + zipNeigh.zip)
                    print("*****************************************************************************")


def getStartPop(zipcodeList):
    zip1 = searchForZip('21010',zipcodeList)
    zip1.added = True
    zip1.checked = True
    zip1.district = 1
    pop = zip1.population
    zip2 = searchForZip('21824', zipcodeList)
    zip2.added = True
    zip2.checked = True
    zip2.district = 1
    pop = pop + zip2.population
    zip2 = searchForZip('21866', zipcodeList)
    zip2.added = True
    zip2.checked = True
    zip2.district = 1
    pop = pop + zip2.population
    return pop

def createDistricts(zipcodeList, totalPopulation):
    targetPopulation = totalPopulation/8
    currentPopulation = getStartPop(zipcodeList)
    currentDistrict = 1
    workerZip = zipcodeList[0]
    while currentDistrict < 4:
        while currentPopulation < targetPopulation:
            if workerZip.added == False:
                currentPopulation = currentPopulation + workerZip.population
                workerZip.district = currentDistrict
                workerZip.added = True
            
            #check my neighbors
            for neighbor in workerZip.neighbors:
                if currentPopulation + neighbor.population <= targetPopulation and neighbor.added == False: #if the neighbors population wont put us over threshold and it hasnt already been added, add it
                    currentPopulation = currentPopulation + neighbor.population
                    neighbor.district = currentDistrict
                    neighbor.added = True
            
            #I've been checked
            workerZip.checked = True
            check = False
            for neighbor in workerZip.neighbors:
                #print("CHECKING " + workerZip.zip + " VS " +neighbor.zip)
                if neighbor.checked == False:
                    #print("FOUND ONE NOT CHECKED, CHANGING WORKIERZIP TO " +neighbor.zip)
                    workerZip = neighbor
                    check = True
                    break
                else:
                    continue
            if check == False:
                #print("DROPPED DOWN TO NEXT LEVEL CHECK")
                for neighbor in workerZip.neighbors:
                    for neigh in neighbor.neighbors:
                        #print("CHECKING " + neighbor.zip + " VS " +neigh.zip)
                        if neighbor.zip == "21804" and neigh.zip == "21802":
                            workerZip = searchForZip('21659',zipcodeList)
                            #return
                        if neighbor.zip == "21651" and neigh.zip == "21650":
                            return
                        if neigh.checked == False:
                            #print("FOUND ONE NOT CHECKED, CHANGING WORKIERZIP TO " +neigh.zip)
                            workerZip = neigh
                            check = True
                            break
                    if check == True:
                        break
            if check == False:
                for zipcode in zipcodeList:
                    if zipcode.added == True and zipcode.checked == False:
                        workerZip = zipcode
                        
                #print("BREAKING WITH " + workerZip.zip)
                #return
        #checkDistrict(zipcodeList, currentDistrict)
        currentDistrict = currentDistrict + 1
        currentPopulation = 0

#Creates objects, see zipcode.py for class details, uses class function to check for neighbors
def createZipObjects(data):
    zipcodeList = []
    for index,row in data.iterrows():
        zipObj = Zipcode(row["ZCTA5CE10"], row["POP100"], row["geometry"].centroid, row["geometry"])
        zipcodeList.append(zipObj)
    for zipcode in zipcodeList:   
        for zipcode2 in zipcodeList:
            if zipcode.zip != zipcode2.zip:
                if zipcode2 in zipcode.neighbors and zipcode in zipcode2.neighbors:
                    continue
                else:
                    zipcode.checkNeighbors(zipcode2)
    totalPopulation = getTotalPopulation(zipcodeList)                
    zipcodeList.sort(reverse=True, key=lambda z: z.centroid.x) #sorted east to west
    #createDistricts(zipcodeList, totalPopulation) #<<<<<---------------------------------------------
    return zipcodeList

def searchForZip(zipcodeToSearchFor, zipcodes):
    for zipcode in zipcodes:
        if zipcode.zip == zipcodeToSearchFor:
            return zipcode
    print("Zip not found")
    return

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
    #zipcodes[0].printInformation() #first in list, furthest east, Ocean City
    #zipcodes[len(zipcodes)-1].printInformation() # last in list, furthest west, Western MD
    zipcodeToSearchFor = input("Search for a zipcode, enter it here: ")
    searchResults = searchForZip(zipcodeToSearchFor, zipcodes)
    print("\nYou're searched returned:\n")
    searchResults.printInformation()
    #print("-------------------------------------------")
    #for zipcode in zipcodes:
    #    if zipcode.district == 1:
    #        print(zipcode.zip)
    #print("-------------------------------------------")
    #for zipcode in zipcodes:
    #    if zipcode.added and zipcode.checked:
    #        print(zipcode.zip)
    

if __name__ == "__main__": 
    # calling main function 
    main()