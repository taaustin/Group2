import sys
import subprocess

print("Verifying Python Version...")
try:
    version = subprocess.check_output(["python3", "--version"])    
except:
    print("Python3 not installed")
    sys.exit(0)

version = version.decode("UTF-8").strip()
version_num = version.split(' ')
version_num = version_num[1].split('.')
if (int(version_num[1]) < 5):
    print("Please update to Python 3.5 or greater")
    sys.exit(0)
else:
    print(version)

print("Verifying pip3 install")
try:
    subprocess.call(["pip3", "--version"])
except:
    print("Installing pip3...")
    subprocess.call(["sudo", "apt-get", "install", "python3-pip"])

print("Verifying gi module install")
try:
    import gi
    gi.require_version("Gtk", "3.0")
except:
    print("Intalling gi python module")
    subprocess.call(["pip3", "install", "PyGOject"])

print("Verifying shapely python module install")
try:
    import shapely
except:
    print("Installing shapely python module")
    subprocess.call(["pip3", "install", "shapely"])
    
print("Verifying geopandas python module")
try:
    import geopandas
except:
    print("Installing geopandas python module")
    subprocess.call(["pip3", "install", "geopandas"])

print("Set up complete")
