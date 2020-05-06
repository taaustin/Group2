# Filename: zipdistrict.py
# Overview: Groups ZipCode objects into districts
# Written by: Dennis Dove
# Date: 5/1/2020
# 
# Purpose: Provides functions that can manage lists of ZipCode objects and split them into districts.

from random import randint
from sys import float_info

def createConnectedGraph(zipcodes):
    '''Ensures all Zipcodes are connected via the neighbors property. Segments of the
       graph are connected at the nearest pair of Zipcodes with each segment.
       :param zipcodes: a list of Zipcode objects
       :return: a connected list of Zipcode objects'''
    # get all disconnected graphs
    graphs = []

    while len(zipcodes) > 0:
        neighborhood = []
        getNeighborhood(zipcodes[0], neighborhood, zipcodes)
        graphs.append(neighborhood)
    
    print('Neighborhoods:', len(graphs))
    print('Stitching graphs together...')

    # combine neighborhoods into one giant graph
    while len(graphs) > 1:
        minDist = float_info.max
        minOuter = None
        minInner = None
        minGraph = None

        # find closest pair of zips
        for innerZip in graphs[0]:
            for outerGraph in graphs[1:]:
                for outerZip in outerGraph:
                    dist = innerZip.centroid.distance(outerZip.centroid)
                    if  minDist > dist:
                        minDist = dist
                        minInner = innerZip
                        minOuter = outerZip
                        minGraph = outerGraph

        # connect the two graphs via the nearest zips
        minInner.neighbors.append(minOuter)
        minOuter.neighbors.append(minInner)

        print(f'Connecting {minInner.zip} and {minOuter.zip}')

        # marge the neighborhoods
        for z in minGraph:
            graphs[0].append(z)
        
        graphs.remove(minGraph)

    return graphs[0]


def getNeighborhood(zip, neighborhood, allZips):
    '''Gets a list of all Zipcode objects connected to zip via the neighbors property.
       The Zipcodes are removed from the allZips list upon discovery.
       :param zip: the starting Zipcode object
       :param neighborhood: a list of Zipcodes connected to zip
       :param allZips: a list of all known Zipcode objects
       :return: a list of Zipcode objects connected to this Zipcode'''
    neighborhood.append(zip)
    allZips.remove(zip)

    for n in zip.neighbors:
        if n in allZips:
            getNeighborhood(n, neighborhood, allZips)


def cluster(zipcodes, numDistricts):
    '''Splits a list of Zipcode objects into districts with approximately equal population.
       :param zipcodes: a list of Zipcode objects
       :param numDistricts: the number of equal population districts that will be created
       :return: a list of Zipcode objects each with an assigned district property'''
    totalPop = sum([z.population for z in zipcodes])
    targetPop = totalPop / numDistricts
    output = []
    
    print('Target district pop:', targetPop)
    
    zipcodes = createConnectedGraph(zipcodes)
    zipcodes.sort(reverse=True, key=lambda z: z.centroid.x) #sorted east to west

    districts = [[0, []]] # array of [pop, [zips]]
    currDistrict = 0
    queue = []

    queue.append(zipcodes[0])
    print(f'Starting district {currDistrict} from {zipcodes[0].zip} (seed)...')

    while len(queue) > 0 and currDistrict < numDistricts:
        if len(districts[currDistrict][1]) == 0:
            # nothing to compare against
            curr = queue.pop(0)
        else:
            # find best candidate that is in queue
            bestDist = float_info.max
            bestCand = None

            for cand in queue:
                dist = cand.centroid.distance(districts[currDistrict][1][0].centroid)
                if bestDist>dist:
                    bestDist=dist
                    bestCand=cand
            curr = bestCand
            queue.remove(bestCand)

        curr.district = currDistrict
        output.append(curr)                
        zipcodes.remove(curr)

        # queue up this zips neighbors
        for adj in curr.neighbors:
            if adj in zipcodes and not adj in queue:
                queue.append(adj)
        
        # add this zip to the district
        districts[currDistrict][0] += curr.population
        districts[currDistrict][1].append(curr)

        # check population limit
        if districts[currDistrict][0] > targetPop:
            # done with this district
            #print('Target pop reached for district', currDistrict, districts[currDistrict][0])
            currDistrict = currDistrict + 1
            districts.append([0, []])
            queue = []
            queue.append(zipcodes[0])
            print(f'Starting district {currDistrict} from {zipcodes[0].zip} (population)...')
    
        # see if there are no more contig. zips
        if len(queue) == 0 and len(zipcodes) != 0:
            # done with this district
            #print('Zips exhausted for district', currDistrict, districts[currDistrict][0])
            currDistrict = currDistrict + 1
            districts.append([0, []])
            queue = []
            queue.append(zipcodes[0])
            print(f'Starting district {currDistrict} from {zipcodes[0].zip} (continuity)...')
    
    # add any remaining zips to nearest district
    # districtBounds = [[z.bounds for z in d[1]] for d in districts]
    # districtBounds = [ziprender.getBoundingBox(d) for d in districtBounds]
    
    while len(zipcodes) != 0:
        curr = zipcodes.pop()
        curr.district = curr.neighbors[0].district
        output.append(curr)
        print(f'Putting {curr.zip} in district {curr.district} (leftover)...')

    return output

# # color and render
# ziprender.colorByDistrict(output, ziprender.randomColors(numDistricts, max=200), 15)
# #customColors = ['#4287f5', '#4287f5', '#dea350', '#c7d437', '#27de16', '#a0ebe7', '#9d25a1', '#918e90']
# #ziprender.colorByDistrict(output, [ziprender.colorHtmlToRgb(h) for h in customColors], 15)

# print('Rendering...')

# img = ziprender.renderZipCodes(output, 500)
# img.show()