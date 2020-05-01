# Filename: zipcode.py
# Overview: class code for a 'Zipcode'
# Written by: Todd Austin
# Date: 3/26/2020
# 
# Purpose: Used for objects of class Zipcode, includes class functions to print information and check
# for zipcode neighbors.

from shapely.geometry import Polygon, MultiPolygon
import numpy as np

class Zipcode():
    def __init__(self, zip, population, centroid, polyGeo):
        self.zip = zip
        self.population = population
        self.centroid = centroid
        self.polyGeo = polyGeo
        self.geolist = np.array(self.polyGeo)
        self.geometry = []
        if self.geolist.size <= 1:
            chunk = []
            for coord in list(self.polyGeo.exterior.coords):
                chunk.append(coord)
            self.geometry.append(chunk)
        elif self.geolist.size <= 64:
            for geo in self.geolist:
                chunk = []
                for coord in list(geo.exterior.coords):
                    chunk.append(coord)
                self.geometry.append(chunk)
        else:
            chunk = []
            for coord in list(self.polyGeo.exterior.coords):
                chunk.append(coord)
                self.geometry.append(chunk)
        bbox = self.polyGeo.bounds
        self.bounds = bbox
        self.neighbors = []
        self.added = False
        self.checked = False
        self.district = 0 #this will get set when dividing starts

    #uses shapely's 'intersects' function to add neighbors to the objects list of neighbors
    #the intersects function takes two geometries (aka 2 zipcodes outline coordinates) and 
    #returns true or false if they touch
    def checkNeighbors(self, zipcode):
        
        
        if self.polyGeo.intersects(zipcode.polyGeo):
            self.neighbors.append(zipcode)
            zipcode.neighbors.append(self)
         #print("Neighbor Found")

    #Print information on a zipcode
    def printInformation(self):
        print("Zipcode = " + self.zip)
        print("Population = " + str(self.population))
        print("Centroid = " + str(self.centroid))
        print("District = " + str(self.district))
        print("Neighbors: ")
        for neighbor in self.neighbors:
            print(neighbor.zip)
        