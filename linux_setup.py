''''''''''''''''''''''''''''''
# File : linux_setup.py
# Description : Basic script that attempts to import non-native
#               python libraries that are required for this application
#               to run. If a library is not found then it is installed
#               with 'pip3'
#
# Author : Ryan Jahnige
# Date : 5/4/2020
#
# Usage : python3 linux_setup.py
''''''''''''''''''''''''''''''
import sys
import subprocess

# Check for python version the user is running
print("Verifying Python Version...")
try:
    version = subprocess.check_output(["python3", "--version"])    
except:
    print("Python3 not installed")
    sys.exit(0)

# Versify that the python version is greater than 3.5, otherwise exit
version = version.decode("UTF-8").strip()
version_num = version.split(' ')
version_num = version_num[1].split('.')
if (int(version_num[1]) < 5):
    print("Please update to Python 3.5 or greater")
    sys.exit(0)
else:
    print(version)

# Check for compatible 'pip3' install, version number is no checked
print("Verifying pip3 install")
try:
    version = subprocess.check_output(["pip3", "--version"])
except:
    print("\'pip3\' is not installed, please refer to the README")
    sys.exit(0)

version = version.decode("UTF-8").strip()
print(verison)

# Check for gi python package, this package is used for the GUI
# If the user only plans on using the CLI then this can be comented out
print("Verifying gi package install")
try:
    import gi
    gi.require_version("Gtk", "3.0")
except:
    print("Intalling gi python module")
    subprocess.call(["pip3", "install", "PyGOject"])

# Check for shapely python package, this packed is required by
# the backend
print("Verifying shapely package install")
try:
    import shapely
except:
    print("Installing shapely python module")
    subprocess.call(["pip3", "install", "shapely"])

# Check for geopandas python package, this package is also
# required by the backend
print("Verifying geopandas package install")
try:
    import geopandas
except:
    print("Installing geopandas python module")
    subprocess.call(["pip3", "install", "geopandas"])

# Set-up has completed, this does not necessarily mean that it
# was successful, be sure to check the output of the 'pip3'
# installs to ensure all packages were installed correctly
print("Set up complete")
