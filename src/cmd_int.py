import sys

def printHelp(pgName):
    print("Usage: python3 " + pgName + ".py [Options]...")
    print("Requirements:")
    print("\t1. Either \'--show\', \'--save\', or both must be specified")
    print("\t2. The center point radius must be less than 1/3 the size of the scale")
    if pgName == "zipdistrict.py":
        print("\t3. Number of districts must be between 1 and 400 inclusive")
    print("Avaible Options:")
    print("\t--show : Display map in default graphics application")
    print("\t--save [Path] : Save map, supported file formats include: jpeg, png, gif")
    print("\t-f [Path] : Specify the input shape file path, must be valid shapefile")
    print("\t-s [Integer] : Set the scale of the generated map; default value is 500")
    print("\t-c [Integer] : Set center point radii; default value is 0 (i.e. None)")
    print("\t-z [ZipColumn] : Specify the zip column to use; default value is \'ZCTA5CE10\'")
    print("\t-p [PopColumn] : Specify the population column to use; default value is \'POP100\'")
    print("\t-g [GeoColumn] : Specify the geometry column to use; default value is \'geometry\'")
    if pgName == "zipdistrict.py":
        print("\t-d [Integer] : Set the number of districs to divide Maryland into; default value is 8")
        

def checkMult(cmd, argv):
    if cmd in argv:
        print("err: Multiple declarations of \'" + cmd + "\'")
        sys.exit()
        
def parseInput(pgName, argv):
    args = {"show": False,
            "save": None,
            "numDis": 8,
            "inFile": "etc/MDdata/Maryland_Census_Data__ZIP_Code_Tabulation_Areas_ZCTAs.shp",
            "scale": 500,
            "centRad": 0,
            "zipCol": "ZCTA5CE10",
            "popCol": "POP100",
            "geoCol": "geometry"
    }
    
    i = 0
    while i in range(len(argv)):
        if "--help" in argv:
            printHelp(pgName)
            sys.exit()
        elif "--show" in argv:
            args["show"] = True
            argv.remove("--show")
            
        elif "--save" in argv:
            index = argv.index("--save")
            try:
                fileName = argv[index+1]
                temp = fileName.split('.')
                fileExt = temp[len(temp)-1]
                if fileExt == "jpeg" or fileExt == "png" or fileExt == "gif":
                    pass
                else:
                    raise Exception()
            except:
                print("err: Invalid file name provided")
                sys.exit()
                
            args["save"] = fileName
            argv.remove("--save")
            checkMult("--save", argv)
            i += 1
            
        elif "-s" in argv:
            index = argv.index("-s")
            try:
                scale = int(argv[index+1])
            except:
                print("err: Invalid scale provided")
                sys.exit()
            args["scale"] = scale
            argv.remove("-s")
            checkMult("-s", argv)
            i += 1

        elif "-c" in argv:
            index = argv.index("-c")
            try:
                centRad = int(argv[index+1])
            except:
                print("err: Invalid centroid radius provided")
                sys.exit()
            args["centRad"] = centRad
            argv.remove("-c")
            checkMult("-c", argv)
            i += 1

        elif pgName == "zipdistricts.py" and "-d" in argv:
            index = argv.index("-d")
            try:
                numDis = int(argv[index+1])
                if numDis < 1 or numDis > 400:
                    raise Exception()
            except:
                print("err: Invalid number of districts provides")
                sys.exit()
            args["numDis"] = numDis;
            argv.remove("-d")
            checkMult("-c", argv)
            i += 1

        elif "-f" in argv:
            index = argv.index("-f")
            try:
                args["inFile"] = argv[index+1]
            except:
                print("err: Invalid Number of parameters")
                sys.exit()
            argv.remove("-f")
            checkMult("-f", argv)
            i += 1

        elif "-z" in argv:
            index = argv.index("-z")
            try:
                args["zipCol"] = argv[index+1]
            except:
                print("err: Invalid Number of parameters")
                sys.exit()
            argv.remove("-z")
            checkMult("-z",argv)
            i += 1
            
        elif  "-p" in argv:
            index = argv.index("-p")
            try:
                args["popCol"] = argv[index+1]
            except:
                print("err: Invalid Number of parameters")
                sys.exit()
            argv.remove("-p")
            checkMult("-p", argv)
            i += 1

        elif "-g" in argv:
            index = argv.index("-g")
            try:
                args["geoCol"] = argv[index+1]
            except:
                print("err: Invalid Number of parameters")
                sys.exit()
            argv.remove("-g")
            checkMult("-g")
            i += 1
            
        else:
            print("err: Invalid user input: \'" + argv[i] + "\' is not a recognized parameter")
            sys.exit()

    if args["show"] == False and args["save"] == None:
        print("err: Either \'--show\', \'--save\', or both must be specified")
        sys.exit()
    elif args["centRad"] > args["scale"]/3:
        print("err: Center point radius is to large")
        sys.exit()
        
    return args
