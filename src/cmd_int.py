import sys

def printHelp():
    print("Usage: python3 " + __name__ + ".py [Options]...")
    print("Either \'--show\', \'--save\', or both must be specified")
    print("The center point radius must be less than 1/3 the size of the scale")
    print("Avaible Options:")
    print("\t--show : Display map in default graphics application")
    print("\t--save [fileName] : Save map, supported file formats include: jpeg, png, gif")
    print("\t-s [Integer] : Set the scale of the generated map; default value is 500")
    print("\t-c [Integer] : Set center point radius of ZCTA's; default value is 0 (i.e. None)")

def parseInput(argv):
    args = {"show": False,
            "save": None,
            "scale": 500,
            "centRad": 0}

    i = 0
    while i in range(len(argv)):
        if "--help" in argv:
            printHelp()
            sys.exit()
        elif "--show" in argv:
            args["show"] = True
            argv.remove("--show")
            
        elif "--save" in argv:
            index = argv.index("--save")
            fileName = argv[index+1]
            
            try:
                fileExt = fileName.split('.')[1]
                if fileExt == "jpeg" or fileExt == "png" or fileExt == "gif":
                    pass
                else:
                    raise Exception()
            except:
                print("err: Invalid file name provided")
                sys.exit()
                
            args["save"] = fileName
            argv.remove("--save")
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
            i += 1
        else:
            print("err: Invalid user input: \'" + argv[i] + "\' is not a recognized parameter")
            sys.exit()
            
    if args["centRad"] > args["scale"]/3:
        print("err: Center point radius is to large")
        sys.exit()
        
    return args
