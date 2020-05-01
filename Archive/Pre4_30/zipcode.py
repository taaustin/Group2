# Filname: zipcode.py
# Overiview: class code for a 'ZipCode'
# Written by: Todd Austin
# Date: 3/26/2020
# 
# Purpose: Used for objects of class ZipCode, includes class functions to print information and check
# for zipcode neighbors.

from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon

class ZipCode():
    def __init__(self, zip, population, geometry):#, centroid): # have to include centroid again for geopandas
        self.zip = zip
        self.population = population
        self.geometry = geometry

        polygons = [Polygon(p) for p in geometry]

        self.polyGeo = MultiPolygon(polygons)
        self.centroid = [self.polyGeo.centroid.x, self.polyGeo.centroid.y]
        bbox = self.polyGeo.bounds
        
        self.bounds = bbox #(bbox[0], bbox[1], bbox[2], bbox[3])

        #self.centroid = centroid
        self.neighbors = []
        self.checked = False
        self.added = False
        self.listIndex = 0
        self.district = 0 #this will get set when dividing starts
        self.color = (0,0,0)
        #print(type(geometry[0]))
        #print(geometry[0])
        #exit()

    def checkNeighbors(self, zipcodeList, zipcodeIndex):
        i = zipcodeIndex
        loopindex = zipcodeIndex
        print("Entered checkNeighbors() with " + self.zip + " at index " + str(i))
        if self.polyGeo.is_valid == False:
            self.polyGeo = self.polyGeo.buffer(0)
        print("start for loop")
        if loopindex >= len(zipcodeList)-5:
            loopindex = len(zipcodeList) - 5
        for zipcode in zipcodeList[loopindex:loopindex+5]:
            if zipcode.checked == False and zipcode.zip != self.zip:
                print("Sending " + zipcode.zip + " to checkIntersection()")
                self.checkIntersection(zipcode)
                zipcode.listIndex = i
            i = i+1
        self.checked = True
        print("Finished checkNeighbors()")
        return

    #uses shapely's 'intersects' function to add neighbors to the objects list of neighbors
    #the intersects function takes two geometries (aka 2 zipcodes outline coordinates) and 
    #returns true or false if they touch
    def checkIntersection(self, zipcode):
        print("entered checkIntersection(), checking intersection between " + self.zip + " and " + zipcode.zip)
        if zipcode.polyGeo.is_valid == False:
            zipcode.polyGeo = zipcode.polyGeo.buffer(0)
        if self.polyGeo.intersects(zipcode.polyGeo):
            self.neighbors.append(zipcode)
            zipcode.neighbors.append(self)
            print("Neighbor Found")

        #else:
        #    self.polyGeo = self.polyGeo.buffer(0)
        #    zipcode.polyGeo = zipcode.polyGeo.buffer(0)
        #    if self.polyGeo.intersects(zipcode.polyGeo):
        #        self.neighbors.append(zipcode)
        #        zipcode.neighbors.append(self)
        #        print("Neighbor Found")
        #    return

    #Print information on a zipcode
    def printInformation(self):
        print("ZipCode = " + self.zip)
        print("Population = " + str(self.population))
        print("Centroid = " + str(self.centroid))
        print("District = " + str(self.district))
        print("Neighbors: ")
        for neighbor in self.neighbors:
            print(neighbor.zip)

    def printDistrict(self, zipcodeList):
        count =0
        pop = 0
        for zipcode in zipcodeList:
            if self.district == zipcode.district:
                print(zipcode.zip + "    " + str(zipcode.population))
                count = count + 1
                pop = pop + zipcode.population
        print("Total of " + str(count) + " zip codes in District " + str(self.district))
        print("District population = " + str(pop))