# Filname: zipcode.py
# Overiview: class code for a 'Zipcode'
# Written by: Todd Austin
# Date: 3/26/2020
# 
# Purpose: Used for objects of class Zipcode, includes class functions to print information and check
# for zipcode neighbors.

from shapely.geometry import Polygon
class Zipcode():
    def __init__(self, zip, population, geometry):#, centroid): # have to include centroid again for geopandas
        self.zip = zip
        self.population = population
        
        self.geometry = geometry
        self.polyGeo = Polygon(geometry)
        self.centroid = Polygon(geometry).centroid
        #self.centroid = centroid
        self.neighbors = []
        self.district = 0 #this will get set when dividing starts

    #uses shapely's 'intersects' function to add neighbors to the objects list of neighbors
    #the intersects function takes two geometries (aka 2 zipcodes outline coordinates) and 
    #returns true or false if they touch
    def checkNeighbors(self, zipcode):
        #self.polyGeo = self.polyGeo.buffer(0)
        #zipcode.polyGeo = zipcode.polyGeo.buffer(0)
        #if zipcode.polyGeo.is_valid and self.polyGeo.is_valid:
        if self.polyGeo.intersects(zipcode.polyGeo):
            self.neighbors.append(zipcode)
            zipcode.neighbors.append(self)
            print("Neighbor Found")
        else:
            self.polyGeo = self.polyGeo.buffer(0)
            zipcode.polyGeo = zipcode.polyGeo.buffer(0)
            if self.polyGeo.intersects(zipcode.polyGeo):
                self.neighbors.append(zipcode)
                zipcode.neighbors.append(self)
                print("Neighbor Found")
        #    return

    #Print information on a zipcode
    def printInformation(self):
        print("Zipcode = " + self.zip)
        print("Population = " + str(self.population))
        print("Centroid = " + str(self.centroid))
        print("District = " + str(self.district))
        print("Neighbors: ")
        for neighbor in self.neighbors:
            print(neighbor.zip)