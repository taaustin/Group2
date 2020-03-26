# Filname: zipcode.py
# Overiview: class code for a 'Zipcode'
# Written by: Todd Austin
# Date: 3/26/2020
# 
# Purpose: Used for objects of class Zipcode, includes class functions to print information and check
# for zipcode neighbors.

from shapely.geometry import Polygon
class Zipcode():
    def __init__(self, zip, population, centroid, geometry):
        self.zip = zip
        self.population = population
        self.centroid = centroid
        self.geometry = geometry
        self.neighbors = []
        self.district = 0 #this will get set when dividing starts

    #uses shapely's 'intersects' function to add neighbors to the objects list of neighbors
    #the intersects function takes two geometries (aka 2 zipcodes outline coordinates) and 
    #returns true or false if they touch
    def checkNeighbors(self, zipcode):
        if self.geometry.intersects(zipcode.geometry):
            self.neighbors.append(zipcode)
            zipcode.neighbors.append(self)
            print("Neighbor Found")

    #Print information on a zipcode
    def printInformation(self):
        print("Zipcode = " + self.zip)
        print("Population = " + str(self.population))
        print("Centroid = " + str(self.centroid))
        print("District = " + str(self.district))
        print("Neighbors: ")
        for neighbor in self.neighbors:
            print(neighbor.zip)