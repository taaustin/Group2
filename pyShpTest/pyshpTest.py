import shapefile
from zipcode import Zipcode

#shfile = shapefile.Reader("./MDdata/Maryland_Census_Data__ZIP_Code_Tabulation_Areas_ZCTAs.shp")
#shapes = shfile.shapes()
#records = shfile.records()
#shape = shfile.shape(0)


def getShapes(shFile):
    shfile = shapefile.Reader(shFile)
    shapes = shfile.shapes()
    return shapes

def getRecords(shFile):
    shfile = shapefile.Reader(shFile)
    records = shfile.records()
    return records

def sortCentroid(e):
    return str(e.centroid)


def createZipObjects(shapes, records):
    zipcodeList = []
    i = 0
    for zipcode in shapes:
        zip = records[i]["ZCTA5CE10"]
        population = records[i]["POP100"]
        geometry = zipcode.points       
        zipObj = Zipcode(zip, population, geometry)#, centroid)
        zipcodeList.append(zipObj)
        i = i+1
    zipcodeList.sort(key=sortCentroid)
    zipcodes = createNeighbors(zipcodeList)

def createNeighbors(zipcodeList):
    i = 10
    while i < len(zipcodeList):
        for zipcode in zipcodeList[i-10:i-5]:   
            for zipcode2 in zipcodeList[0:i]:
                if zipcode != zipcode2:
                    if zipcode2 in zipcode.neighbors or zipcode in zipcode2.neighbors:
                        break
                    else:
                        #print(zipcode.zip + "    " + zipcode2.zip)
                        zipcode.checkNeighbors(zipcode2)
        if i+5 < len(zipcodeList):
            i = i+5
            print(i)
        elif i+5 > len(zipcodeList):
            i = len(zipcodeList)
            print(i)
        else:
            return zipcodeList
    return zipcodeList
    #        #else:
    #        #    break
                    
    #zipcodeList.sort(key=sortCentroid)
    return zipcodeList

    

    
    #for index,row in data.iterrows():
    #    zipObj = Zipcode(row["ZCTA5CE10"], row["POP100"], row["geometry"].centroid, row["geometry"])
    #    zipcodeList.append(zipObj)
    #
    #
    #
    #for zipcode in zipcodeList:   
    #    for zipcode2 in zipcodeList:
    #        if zipcode != zipcode2:
    #            if zipcode2 in zipcode.neighbors or zipcode in zipcode2.neighbors:
    #                break
    #            else:
    #                zipcode.checkNeighbors(zipcode2)
    #                
    #zipcodeList.sort(key=sortCentroid)
    #return zipcodeList

        #print(row["ZCTA5CE10"])
#get geometry from first 5 polygons
#selection = data[0]




#for index,row in selection.iterrows():
#    poly_area = row['geometry'].centroid
#    print(poly_area)
    #print("Polygon area at index {0} is: {1:.3f}".format(index,poly_area))


#print(selection['geometry'])

def main():
    shFile = "./MDdata/Maryland_Census_Data__ZIP_Code_Tabulation_Areas_ZCTAs.shp"
    shapes = getShapes(shFile)
    records = getRecords(shFile)

    zipcodes = createZipObjects(shapes, records)
    zipcodes[0].printInformation()
    #for zipcode in zipcodes:
    #    if zipcode.zip == "21012":
    #        zip1 = zipcode
    #    elif zipcode.zip == "21409":
    #        zip2 = zipcode
    ##zip1.checkNeighbors(zip2)
    #zip1.printInformation()
    #zipcodes[1].printInformation()
    #zipcodes[len(zipcodes)-1].printInformation()

if __name__ == "__main__": 
    # calling main function 
    main()