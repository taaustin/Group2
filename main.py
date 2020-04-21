import os
import math
from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
import random
import pyshpTest
import shapely.geometry

def makeTranslator(offsetX, offsetY, scale):
    def translate(x, y):
        return [(x + offsetX) * scale, (y + offsetY) * scale]
    return translate


def fatoia(floats):
    for i in range(len(floats)):
        floats[i] = int(math.ceil(floats[i]))
    return floats


shpPath = os.path.join('MDdata',
                       'Maryland_Census_Data__ZIP_Code_Tabulation_Areas_ZCTAs.shp')

print("Reading shapefile...")
shapes = pyshpTest.getShapes(shpPath)
records = pyshpTest.getRecords(shpPath)
zipcodeList = pyshpTest.createZipObjects(shapes,records)
totalPopulation = pyshpTest.getTotalPopulation(zipcodeList)
pyshpTest.startSplit(totalPopulation, zipcodeList)
#data = shapefileWork.readShapefile(shpPath)
#zips = shapefileWork.createZipObjects(data)

print("Processing...")

t = zipcodeList[0].centroid.y
b = zipcodeList[0].centroid.y
l = zipcodeList[0].centroid.x
r = zipcodeList[0].centroid.x

print("Calculating bounding box...")

# build a bounding box
for z in zipcodeList:
    if z.centroid.x < l:
        l = z.centroid.x
    if z.centroid.x > r:
        r = z.centroid.x
    if z.centroid.y < t:
        t = z.centroid.y
    if z.centroid.y > b:
        b = z.centroid.y

print(l,t,r,b)

# construct a translation function
scale = 2000
tf = makeTranslator(-l, -t, scale)
size = fatoia(tf(r, b))
print("Bouding box:", size)

img = Image.new('RGB', (size[0] + 100, size[1] + 100), 'black')
pixels = img.load()
mdColors = [(224, 58, 62), (255, 213, 32)]
colors = ['#4287f5', '#4287f5', '#dea350', '#c7d437', '#27de16', '#a0ebe7', '#9d25a1', '#918e90']

#for i in range(1330):
#    randColors.append((
#        random.randint(10, 250),
#        random.randint(10, 250),
#        random.randint(10, 250)
#    ))

for z in zipcodeList:
    # calculate middle point
    # center = fatoia(tf(z.centroid.x, z.centroid.y))

    # invert Y axis
    #center[1] = img.size[1] - center[1]

    # print each record
    # print('ZCTA={0:5} POP={1:5} CENTER={2}'.format(
    #     z.zip,
    #     z.population,
    #     center
    # ))

    # color = mdColors[random.randint(0, 1)]
    #color = randColors[int(z.zip) - 20601]  # [0-1329]
    if z.district == 1:
        color = colors[0]
    elif z.district == 2:
        color = colors[1]
    elif z.district == 3:
        color = colors[2]
    elif z.district == 4:
        color = colors[3]
    elif z.district == 5:
        color = colors[4]
    elif z.district == 6:
        color = colors[5]
    elif z.district == 7:
        color = colors[6]
    elif z.district == 8:
        color = colors[7]
    rad = scale // 150
    # for x in range(center[0] - rad, center[0] + rad):
    #     for y in range(center[1] - rad, center[1] + rad):
    #         if x > 0 and y > 0 and x < img.size[0] and y < img.size[1]:
    #             pixels[x, y] = color

    draw = ImageDraw.Draw(img)
    #sq = [center[0] - rad, center[1] - rad, center[0] + rad, center[1] + rad]
    #draw.rectangle(sq, color, color)
    # draw.text(
    #     (center[0] + rad, center[1] + rad),  z.zip + ' ' + str(z.population))
    # draw.polygon(z.geometry, color, color)
    
    if type(z.polyGeo) == shapely.geometry.MultiPolygon:
        for poly in z.polyGeo:
            points = list(poly.exterior.coords)
            points = [tuple(tf(p[0], p[1])) for p in points]
            #print(points)
            draw.polygon(points, color, color)
    elif type(z.polyGeo) == shapely.geometry.Polygon:
            points = list(z.polyGeo.exterior.coords)
            points = [tuple(tf(p[0], p[1])) for p in points]
            #print(points)
            draw.polygon(points, color, color)
    else:
        print("Unknown geometry type:", type(z.polyGeo))

    # exit()

# flip image vertically

a = 1
b = 0
c = -l #left/right (i.e. 5/-5)
d = 0
e = 1
f = -t #up/down (i.e. 5/-5)
# img = img.transform(img.size, Image.AFFINE, (a, b, c, d, e, f))
img = ImageOps.flip(img)
img.show()
# img.save('test.gif')