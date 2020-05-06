'''''''''''''''''''''''''''
# File : md_dgm.py
# Description : This file loads the graphical user interface from 
#               "design_format.glade" and handles all events that
#               the home window offers.
#
# Author : Ryan Jahnige
'''''''''''''''''''''''''''

import os
import sys
import threading

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw

sys.path.insert(1, "src")
sys.path.insert(1, "etc")
import geoShapeWork
import ziprender
import zipdistrict
import md_map 

class MD_DGM_APP:
    # Initialize the home window from 'design_format.glade'
    def __init__(self):
        if (not os.path.exists("etc/.tmp")):
            os.mkdir("etc/.tmp")
        self.builder = Gtk.Builder()
        self.builder.add_from_file("etc/design_format.glade")
        self.builder.connect_signals(self)

        self.builder.get_object("home_window").show_all()
        self.builder.get_object("spinner").hide()

    # Destroy home window on exit
    def on_home_destroy(self, *args):
        for fileName in os.listdir("etc/.tmp/"):
            os.remove("etc/.tmp/" + fileName)
        Gtk.main_quit()
        
    # Display a warning when the user wishes to generate a map that
    # that has already been generated this session. 
    def Warning_Window(self, *args):
        home = self.builder.get_object("home_window").set_sensitive(False)
        window = self.builder.get_object("warning_window")
        
        label = self.builder.get_object("event_content")
        self.fileName = args[0]
        self.build_districts = args[1]
        
        text_str = "Map has already been generated, this\nwill overwrite the contents of \"" + args[0] + "\"\n\nDo you want to continue?"
        
        label.set_label(text_str)
        window.show_all()

    # Exit warning window and signify to not overwrite
    def on_warning_quit_clicked(self, *args):
        self.builder.get_object("home_window").set_sensitive(True)
        window = self.builder.get_object("warning_window")
        window.hide()

    # Exit warning window and signify overwrite
    def on_warning_continue_clicked(self, *args):
        self.builder.get_object("home_window").set_sensitive(True)
        window = self.builder.get_object("warning_window")
        files = self.builder.get_object("files")
        
        for fileID in files:
            if fileID.get_label() == self.fileName:
                files.remove(fileID)

        # Generate requested data
        self.fileName = "etc/.tmp/" + self.fileName + ".jpeg"
        shapefile = threading.Thread(target=self.shapefile_thread, args=(self.fileName, self.build_districts))
        shapefile.daemon = True
        shapefile.start()
        self.builder.get_object("zcta_map_button").set_sensitive(False)
        self.builder.get_object("districts_map_button").set_sensitive(False)
                
        window.hide()
        
    # Generate map of districts based on ZCTA populations
    def on_districts_map_button_clicked(self, *args):
        files = self.builder.get_object("files")
        overwrite_warning = False
        fileName = ""
        
        # Determine whether to overwrite the file
        fileList = files.get_children()
        for fileID in fileList:
            if fileID.get_label() == "districts_map":
                overwrite_warning = True
                fileName = fileID.get_label()
                
        # Display link to map window or display waring window
        if overwrite_warning:
            self.Warning_Window(fileName, True)
        else:
            shapefile = threading.Thread(target=self.shapefile_thread, args=("etc/.tmp/districts_map.jpeg", True))
            shapefile.daemon = True
            shapefile.start()
            
            self.builder.get_object("zcta_map_button").set_sensitive(False)
            self.builder.get_object("districts_map_button").set_sensitive(False)

    # Generate map of ZCTA's
    def on_zcta_map_button_clicked(self, *args):
        files = self.builder.get_object("files")
        overwrite_warning = False
        fileName = ""
        
        # Determine whether to overwrite the file
        fileList = files.get_children()
        for fileID in fileList:
            if fileID.get_label() == "zcta_map":
                overwrite_warning = True
                fileName = fileID.get_label()
                
        # Display link to map window or display waring window
        if overwrite_warning:
            self.Warning_Window(fileName, False)
        else:
            shapefile = threading.Thread(target=self.shapefile_thread, args=("etc/.tmp/zcta_map.jpeg", False))
            shapefile.daemon = True
            shapefile.start()
            
            self.builder.get_object("zcta_map_button").set_sensitive(False)
            self.builder.get_object("districts_map_button").set_sensitive(False)

    # Create map window or open existing, note that all open windows are stored
    # the global array map_windows defined in md_map
    def open_map_window(self, *args):
        if args[1] in md_map.map_windows:
            md_map.map_windows[args[1]].bring_front()
        else:
            md_map.map_windows[args[1]] = md_map.Map_Window(args[1])

    # Update GUI to inform user of gereration process
    def update_log(self, txt_str):
        status_log = self.builder.get_object("status_log")
        status_log.set_text(txt_str)
        return False

    # Add a link to the GUI for the user to open the generated map
    def add_link(self, fileName):
        fileName = fileName.split("/")
        fileName = fileName[2].split(".")
        fileName = fileName[0]
        
        files = self.builder.get_object("files")
        link = Gtk.LinkButton(label=fileName, uri=fileName)
        link.connect("clicked", self.open_map_window, fileName)
        link.show()
        files.add(link)

        self.builder.get_object("spinner").hide()
        self.builder.get_object("status_log").hide()
        self.builder.get_object("zcta_map_button").set_sensitive(True)
        self.builder.get_object("districts_map_button").set_sensitive(True)
        return False

    # Make log visible to the user
    def show_log(self, *args):
        self.builder.get_object("spinner").show()
        status_log = self.builder.get_object("status_log")
        status_log.show()

    # Generate map based on arguments passed in
    # @args[0] : String that contains file name to save generated data in
    # @args[1] : Boolean - False colors by ZCTA, True generates and colors by distric
    def shapefile_thread(self, *args):
        GLib.idle_add(self.show_log)
        
        GLib.idle_add(self.update_log, "Gathering Data...")
        shpPath = "./etc/MDdata/Maryland_Census_Data__ZIP_Code_Tabulation_Areas_ZCTAs.shp"

        GLib.idle_add(self.update_log, "Reading Shapefile...")
        data = geoShapeWork.readShapefile(shpPath)
        
        GLib.idle_add(self.update_log, "Building ZCTAs...")
        zipcodes = geoShapeWork.createZipObjects(data)

        if (args[1]):
            GLib.idle_add(self.update_log, "Creating connnected graph...")
            zipcodes = zipdistrict.createConnectedGraph(zipcodes)

            GLib.idle_add(self.update_log, "Splitting by population...")
            output = zipdistrict.cluster(zipcodes, 8)

            GLib.idle_add(self.update_log, "Coloring districts...")
            ziprender.colorByDistrict(output, ziprender.randomColors(8), 15)

            GLib.idle_add(self.update_log, "Rendering districts...")
            img = ziprender.renderZipCodes(output, scale=2000, centroidRadius=15)
        else:
            GLib.idle_add(self.update_log, "Coloring ZCTAs...")
            ziprender.colorByZip(zipcodes, ziprender.randomColors(len(zipcodes)))
            
            GLib.idle_add(self.update_log, "Rendering ZCTAs...")
            img = ziprender.renderZipCodes(zipcodes, scale=2000, centroidRadius=15)
            
        img.save(args[0])
        GLib.idle_add(self.add_link, args[0])

def main():
    app = MD_DGM_APP()
    Gtk.main()

if __name__ == "__main__":
    main()

