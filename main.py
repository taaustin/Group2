import shapefile
import os
import math
from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
import random


def makeTranslator(offsetX, offsetY, scale):
    def translate(x, y):
        return [(x + offsetX) * scale, (y + offsetY) * scale]
    return translate


def fatoia(floats):
    for i in range(len(floats)):
        floats[i] = int(math.ceil(floats[i]))
    return floats


shpPath = os.path.join('data',
                       'Maryland_Census_Data__ZIP_Code_Tabulation_Areas_ZCTAs')

with shapefile.Reader(shpPath) as s:
    # construct a translation function
    scale = 1000
    tf = makeTranslator(-s.bbox[0], -s.bbox[1], scale)
    size = fatoia(tf(s.bbox[2], s.bbox[3]))
    print(size)

    img = Image.new('RGB', (size[0] + 100, size[1] + 100), 'black')
    pixels = img.load()
    mdColors = [(224, 58, 62), (255, 213, 32)]
    randColors = []

    for i in range(1330):
        randColors.append((
            random.randint(10, 250),
            random.randint(10, 250),
            random.randint(10, 250)
        ))

    for sr in s.iterShapeRecords():
        # calculate middle point
        bounds = sr.shape.bbox
        xMid = (bounds[0] + bounds[2]) / 2
        yMid = (bounds[1] + bounds[3]) / 2
        center = fatoia(tf(xMid, yMid))

        # invert Y axis
        center[1] = img.size[1] - center[1]

        # print each record
        print('ZCTA={0:5} POP={1:5} CENTER={2}'.format(
            sr.record[1],
            sr.record[11],
            center
        ))

        # color = mdColors[random.randint(0, 1)]
        color = randColors[int(sr.record[1]) - 20601]  # [0-1329]
        rad = scale // 150
        for x in range(center[0] - rad, center[0] + rad):
            for y in range(center[1] - rad, center[1] + rad):
                if x > 0 and y > 0 and x < img.size[0] and y < img.size[1]:
                    pixels[x, y] = color

        ImageDraw.Draw(img).text(
            (center[0] + rad, center[1] + rad),  sr.record[1] + ' ' + str(sr.record[11]))

    # flip image vertically
    #img = ImageOps.flip(img)
    # img.show()
    img.save('test.gif')
