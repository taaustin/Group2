# Filename: ziprender.py
# Overview: Renders ZipCode objects
# Written by: Dennis Dove
# Date: 4/22/2020
# 
# Purpose: Provides a set of functions that facilitate rendering of ZipCode objects to Pillow Image objects.

import os
import math
from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from random import randint
import geoShapeWork

def makeTranslator(offsetX, offsetY, scale):
    '''Gets a function that performs a translate and a scale on coordinates.
       :param offsetX: the x-coordinate translation
       :param offsetY: the y-coordinate translation
       :param scale: the scaling factor to apply
       :return: a function(x,y) that will transform the x and y coordinates and return an array [x,y].'''
    def translate(xy):
        return ((xy[0] + offsetX) * scale, (xy[1] + offsetY) * scale)
    return translate


def getBoundingBox(boundingBoxes):
    '''Gets a bounding box that contains all of the given bounding boxes.
       :param boundingBoxes: a List of (minx, miny, maxx, maxy) bounding boxes.
       :return: a (minx, miny, maxx, maxy) bounding box'''
    # start with the first box
    # convert to list so the elements can be changed
    ret = list(boundingBoxes[0])

    # expand the box to fit each subsequent box
    for box in boundingBoxes:
        if box[0] < ret[0]:
            ret[0] = box[0]
        if box[1] < ret[1]:
            ret[1] = box[1]   
        if box[2] > ret[2]:
            ret[2] = box[2]    
        if box[3] > ret[3]:
            ret[3] = box[3]

    return tuple(ret)


def randomColors(count, min=0, max=255):
    '''Builds a list of random RGB tuples.
       :param count: the number of colors to generate.
       :return: a list of RGB tuples.'''
    return [(randint(min, max), randint(min, max), randint(min, max)) for n in range(count)]


def colorByDistrict(zips, colors, radius=0):
    '''Applies a color to each ZCTA based on district number.
       :param zips: a list of ZipCode objects
       :param colors: a list of RGB tuples
       :param radius: an optional amount of maximum shift to apply to each ZCTA'''
    if radius == 0:
        # simple assignment
        for zcta in zips:
            zcta.color = colors[zcta.district-1]
            zcta.centroidColor = tuple(a + 75 for a in zcta.color)
    else:
        # modify RGB by the same random amount per ZCTA
        for zcta in zips:
            # if zcta.district == 0:
            #     zcta.color = '#ff0000'
            # else:
            offset = randint(-radius, radius)
            zcta.color = tuple(a + offset for a in colors[zcta.district-1])
            zcta.centroidColor = tuple(a + 75 for a in zcta.color)


def colorByZip(zips, colors):
    '''Applies a color to each ZCTA based on ZIP code.
       :param zips: a list of ZipCode objects
       :param colors: a list of RGB tuples'''
    for zcta in zips:
        zcta.color = colors[int(zcta.zip) % len(colors)]  # [0-1329]
        zcta.centroidColor = tuple(a + 75 for a in zcta.color)

def colorHtmlToRgb(color):
    '''Converts an hex HTML color code to an RGB tuple.
       :param color: a hexadecimal HTML color code (e.g. #a0ebe7)
       :return: an RGB tuple'''
    # from https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    h = color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def renderZipCodes(zips, scale, background='black'):
    '''Renders a list of ZipCode objects to a new PIL.Image.
       :param zips: a list of ZipCode objects
       :param scale: a scaling factor for the output
       :param background: the background color for the image
       :return: a PIL.Image object with the rendered map.'''
    print("Rendering zip codes...")

    # Get a bounding box for all geometry
    boxList = [z.bounds for z in zips]
    boxAll = getBoundingBox(boxList)

    # construct a translation function
    translate = makeTranslator(-boxAll[0], -boxAll[1], scale)
    imageSize = tuple(math.ceil(t) for t in translate(boxAll[2:]))

    print("Image size:", imageSize)

    img = Image.new('RGB', imageSize, background)
    draw = ImageDraw.Draw(img)

    for z in zips:
        # fill background
        for poly in z.geometry:
            points = [translate(p) for p in poly]
            draw.polygon(points, z.color)

        # dot at center
        r = 2
        center = translate((z.centroid.x, z.centroid.y))
        tlbr = (center[0] - r, center[1] - r, center[0] + r, center[1] + r)        
        draw.ellipse(tlbr, z.centroidColor)
        # draw.text(center, z.zip, z.centroidColor)
        
    
    # flip image vertically
    return ImageOps.flip(img)


# ########################################################################
# # THIS SHOULD BE CALLED ELSEWHERE
# # All of this work should be done by the caller to renderZipCodes
# # 1. Read in shapefile
# # 2. Split by population
# # 3. Apply color
# # 3. Render
# # 4. Show/Save
# ########################################################################
# shpPath = os.path.join('MDdata',
#                        'Maryland_Census_Data__ZIP_Code_Tabulation_Areas_ZCTAs.shp')

# print("Reading shapefile...")
# data = geoShapeWork.readShapefile(shpPath)
# #records = pyshpTest.getRecords(shpPath)
# zipcodeList = geoShapeWork.createZipObjects(data)
# #totalPopulation = pyshpTest.getTotalPopulation(zipcodeList)
# #pyshpTest.startSplit(totalPopulation, zipcodeList)
# #pyshpTest.divideUp(zipcodeList, totalPopulation)

# # customColors = ['#4287f5', '#4287f5', '#dea350', '#c7d437', '#27de16', '#a0ebe7', '#9d25a1', '#918e90']
# # colorByDistrict(zipcodeList, [colorHtmlToRgb(h) for h in customColors], 15)
# colorByDistrict(zipcodeList, randomColors(8), 15)
# # colorByZip(zipcodeList, randomColors(len(zipcodeList)))

# img = renderZipCodes(zipcodeList, scale=2000)
# img.show()
# # img.save('test.gif')