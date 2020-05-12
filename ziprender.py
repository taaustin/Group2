# Filename: ziprender.py
# Overview: Renders ZipCode objects
# Written by: Dennis Dove
# Date: 4/22/2020
#
# Purpose: Provides a set of functions that facilitate rendering of ZipCode objects to Pillow Image objects.

import os
import sys
import math
from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont
from random import randint
from collections import defaultdict
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.ops import nearest_points
sys.path.insert(1, "src")
import geoShapeWork
import cmd_int

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
            zcta.centroidColor = tuple(a + 100 for a in zcta.color)
    else:
        # modify RGB by the same random amount per ZCTA
        for zcta in zips:
            # if zcta.district == 0:
            #     zcta.color = '#ff0000'
            # else:
            offset = randint(-radius, radius)
            zcta.color = tuple(a + offset for a in colors[zcta.district-1])
            zcta.centroidColor = tuple(a + 100 for a in zcta.color)


def colorByZip(zips, colors):
    '''Applies a color to each ZCTA based on ZIP code.
       :param zips: a list of ZipCode objects
       :param colors: a list of RGB tuples'''
    for zcta in zips:
        zcta.color = colors[int(zcta.zip) % len(colors)]  # [0-1329]
        zcta.centroidColor = tuple(a + 100 for a in zcta.color)


def colorHtmlToRgb(color):
    '''Converts an hex HTML color code to an RGB tuple.
       :param color: a hexadecimal HTML color code (e.g. #a0ebe7)
       :return: an RGB tuple'''
    # from https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    h = color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def renderZipCodes(zips, scale, centroidRadius, background='black'):
    '''Renders a list of ZipCode objects to a new PIL.Image.
       :param zips: a list of ZipCode objects
       :param scale: a scaling factor for the output
       :param background: the background color for the image
       :return: a PIL.Image object with the rendered map.'''
    print(f"Rendering {len(zips)} zip codes...")

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
        center = translate((z.centroid.x, z.centroid.y))
        tlbr = (center[0] - centroidRadius, center[1] - centroidRadius,
                center[0] + centroidRadius, center[1] + centroidRadius)
        draw.ellipse(tlbr, z.centroidColor)
        #draw.rectangle(tlbr, fill=z.centroidColor)
        # draw.text(center, z.zip, z.centroidColor)

    dists = defaultdict(list)
    colors = dict()

    for z in zips:
        #for poly in z.polyGeo:
        colors[z.district] = z.centroidColor
        if type(z.polyGeo) == Polygon:
            dists[z.district].append(z.polyGeo)
        elif type(z.polyGeo) == MultiPolygon:
            for poly in z.polyGeo:
                dists[z.district].append(poly)
    
    for dist, polys in dists.items():
        print(f'District {dist} with {len(polys)} polygons..')
        m = MultiPolygon(polys)
        r = centroidRadius * 2

        p1, p2 = nearest_points(m, m.centroid)


        center = translate((p1.x, p1.y))
        tlbr = (center[0] - r, center[1] - r,
                center[0] + r, center[1] + r)
        draw.rectangle(tlbr, colors[dist])

    # flip image vertically
    return ImageOps.flip(img)

def printDistrictStats(img, xy, zips):
    '''Prints a list of ZipCode statistics to an existing PIL.Image.
       :param img: a PIL.Image object to print to
       :param xy: a tuple containing x and y coordinates
       :param zips: a list of ZipCode objects'''
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('UbuntuMono-R.ttf', size=100)
    
    pops = dict()
    colors = dict()

    for z in zips:
        oldPop = pops.get(z.district, 0)
        pops[z.district] = oldPop + z.population

        if oldPop == 0:
            colors[z.district] = z.color


    for dist, pop in pops.items():
        line = f"District {dist}: {pop}"

        draw.text(xy, line, fill=colors[dist], font=font)
        xy = (xy[0], xy[1] + font.getsize(line)[1])

    img.show()
    return img

# ########################################################################
# # THIS SHOULD BE CALLED ELSEWHERE
# # All of this work should be done by the caller
# # 1. Read in shapefile
# # 2. Split by population
# # 3. Apply color
# # 3. Render
# # 4. Show/Save
# ########################################################################
def main(argv):
    '''A command line interface for this map rendering module
       :param argv: a list of command line arguments'''
    args = cmd_int.parseInput("ziprender.py", argv)

    print("Reading shapefile...")
    data = geoShapeWork.readShapefile(args["inFile"])

    print("Creating zip objects...")
    zips = geoShapeWork.createZipObjects(data, args["zipCol"], args["popCol"], args["geoCol"])

    print("Rendering map...")
    colors = randomColors(len(zips), 10, 190)
    colorByZip(zips, colors)
    
    img = renderZipCodes(zips, scale=args["scale"], centroidRadius=args["centRad"])

    # either save to a file or show on screen
    if args["show"]:
        img.show()
    if args["save"] != None:
        img.save(args["save"])

if __name__ == "__main__":
    main(sys.argv[1:])

'''''''''''''''''''''''''''''''''''''''
if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 6:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        print(f'Invalid number of arguments: {len(sys.argv)}')
        print(f'Usage: {sys.argv[0]} shapePath imagePath [zipColumn] [popColumn] [geoColumn]')
'''''''''''''''''''''''''''''''''''''''
