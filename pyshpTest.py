import shapefile
from zipcode import ZipCode

def getShapes(shFile):
    shfile = shapefile.Reader(shFile)
    shapes = shfile.shapes()
    return shapes

def getRecords(shFile):
    shfile = shapefile.Reader(shFile)
    records = shfile.records()
    return records

def sortCentroid(e):
    return str(e.centroid[0])

def getTotalPopulation(zipcodeList):
    total = 0
    for zipcode in zipcodeList:
        total = total + zipcode.population
    return total

def createZipObjects(shapes, records):
    zipcodeList = []
    
    # convert shapes to a list(list(list(coordinates)))
    # zipcodes(shapes(coordinates))
    coordShapes = []

    # split the points into parts
    for shape in shapes:
        parts = []

        if len(shape.parts) > 1:
            # multiple parts, split and add each
            start = shape.parts[0]
            
            for partIndex in shape.parts[1:]:
                part = shape.points[start:partIndex]
                parts.append(part)
                start = partIndex      
        else:
            # Only one part, add entire list
            parts.append(shape.points)
        
        coordShapes.append(parts)

    # build ZipCode objects from the geomerty and records
    for shape, record in zip(coordShapes, records):
        zcta = record["ZCTA5CE10"]
        pop = record["POP100"]
        zipObj = ZipCode(zcta, pop, shape)
        zipcodeList.append(zipObj)

    zipcodeList.sort(key=sortCentroid, reverse=True)
    return zipcodeList


def startSplit(totalPopulation, zipcodeList):
    print("Entered startSplit()")
    targetPopulation = int(totalPopulation/8)
    currentSum=0
    currentDistrict = 1
    listIndex = 0
    while currentDistrict <= 8:
        while currentSum <= targetPopulation-1500:
            if zipcodeList[listIndex].added == False or zipcodeList[listIndex].checked == False:
                if zipcodeList[listIndex].added == False and zipcodeList[listIndex].district == 0:
                    currentSum = currentSum + zipcodeList[listIndex].population
                    zipcodeList[listIndex].district = currentDistrict
                    print("Current sum of District " + str(currentDistrict) + " now is " + str(currentSum) + " out of a target " + str(targetPopulation))
                    zipcodeList[listIndex].added = True


                if zipcodeList[listIndex].checked == False:
                    zipcodeList[listIndex].checkNeighbors(zipcodeList, listIndex)
                for neighbor in zipcodeList[listIndex].neighbors:
                    if currentSum + neighbor.population <= targetPopulation and neighbor.added == False and neighbor.district == 0:
                        currentSum = currentSum + neighbor.population
                        neighbor.district = currentDistrict
                        print("Current sum of District " + str(currentDistrict) + " now is " + str(currentSum) + " out of a target " + str(targetPopulation))
                        neighbor.added = True
                for neighbor in zipcodeList[listIndex].neighbors:
                    if neighbor.checked == False:
                        neighbor.checkNeighbors(zipcodeList, neighbor.listIndex)
            listIndex = listIndex + 1
            if listIndex >= len(zipcodeList):
                return
        currentDistrict = currentDistrict + 1
        currentSum = 0
        

def printDistrictDetails(zipcodeList):
    countOne = 0
    popOne =0
    countTwo = 0
    popTwo =0
    countThree = 0 
    popThree = 0
    countFour = 0 
    popFour = 0
    countFive = 0 
    popFive = 0
    countSix = 0 
    popSix = 0
    countSeven = 0 
    popSeven = 0
    countEight = 0
    popEight = 0
    otherCount = 0
    for zip in zipcodeList:
        if zip.district == 1:
            countOne = countOne+1
            popOne = popOne + zip.population
        elif zip.district == 2:
            countTwo = countTwo + 1
            popTwo = popTwo + zip.population
        elif zip.district == 3:
            countThree = countThree + 1
            popThree = popThree + zip.population
        elif zip.district == 4:
            countFour = countFour + 1
            popFour = popFour + zip.population
        elif zip.district == 5:
            countFive = countFive + 1
            popFive = popFive + zip.population
        elif zip.district == 6:
            countSix = countSix + 1
            popSix = popSix + zip.population
        elif zip.district == 7:
            countSeven = countSeven + 1    
            popSeven = popSeven + zip.population  
        elif zip.district == 8:
            countEight = countEight + 1
            popEight = popEight + zip.population
        else:
            otherCount = otherCount +1
            zip.printInformation()
    print("District 1: " + str(countOne) +" zip codes, population: " + str(popOne))
    print("District 2: " + str(countTwo) +" zip codes, population: " + str(popTwo))
    print("District 3: " + str(countThree) +" zip codes, population: " + str(popThree))
    print("District 4: " + str(countFour) +" zip codes, population: " + str(popFour))
    print("District 5: " + str(countFive) +" zip codes, population: " + str(popFive))
    print("District 6: " + str(countSix) +" zip codes, population: " + str(popSix))
    print("District 7: " + str(countSeven) +" zip codes, population: " + str(popSeven))
    print("District 8: " + str(countEight) +" zip codes, population: " + str(popEight))
    print("Other: " + str(otherCount))
    

def main():
    shFile = "./MDdata/Maryland_Census_Data__ZIP_Code_Tabulation_Areas_ZCTAs.shp"
    shapes = getShapes(shFile)
    records = getRecords(shFile)
    zipcodeList = createZipObjects(shapes, records)
    totalPopulation = getTotalPopulation(zipcodeList)
    startSplit(totalPopulation, zipcodeList)
    printDistrictDetails(zipcodeList)
    print(totalPopulation/8)

if __name__ == "__main__": 
    # calling main function 
    main()
