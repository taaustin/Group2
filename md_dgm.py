'''''''''''''''''''''''''''
# File : md_dgm.py
# Description : This file loads the graphical user interface from 
#               "design_format.glade" and handles all events that
#               the home window offers.
#
# Author : Ryan Jahnige
# Date : 5/14/2020
#
# Usage : python3 md_dgm.py
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

''''''''''''''''''''''''''''''''''''''
# Warning : Displays a warning when the user wishes to generate a map that
#             that has already been generated this session
# Return : Either Gtk.ResponseType.OK or Gtk.ResponseType.CANCEL
''''''''''''''''''''''''''''''''''''''
class Warning(Gtk.Dialog):

    ''''''''''''''''''''''''''''''''
    # __init__() : Default constructor
    # @fileName : The name of the link in the home window that is being
    #             overwritten
    # Return : Display warning window
    ''''''''''''''''''''''''''''''''
    def __init__(self, fileName):
        Gtk.Dialog.__init__(self, title="Warning")
        
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(250, 150)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.MOUSE)
        self.set_border_width(6)

        # Set warning window content and format
        label = Gtk.Label()
        header = "<span font-size='large'> WARNING</span>"
        body = "\n\nMap has already been generated, this\nwill overwrite the contents of\n" + fileName + "\n\nDo you want to continue?\n\n"
        label.set_markup(header + body)

        box = self.get_content_area()
        box.add(label)
        self.show_all()

''''''''''''''''''''''''''''''''''''''
# MD_DGM_APP : Loads the content of 'display_format.glade' fo initialization
#              of the home window and handles all user events
''''''''''''''''''''''''''''''''''''''
class MD_DGM_APP(Gtk.Window):
    
    '''''''''''''''''''''
    # __init__() : Default constructor
    # Return : Display home window
    '''''''''''''''''''''
    def __init__(self):
        if (not os.path.exists("etc/.tmp")):
            os.mkdir("etc/.tmp")
        self.builder = Gtk.Builder()
        self.builder.add_from_file("etc/design_format.glade")
        self.builder.connect_signals(self)

        self.builder.get_object("home_window").show_all()
        self.builder.get_object("spinner").hide()

    ''''''''''''''''''''''''''''''''''''
    # on_home_destroy() : Destroy home window on exit
    # @args : None
    # Return : Exit Application
    ''''''''''''''''''''''''''''''''''''
    def on_home_destroy(self, *args):
        for fileName in os.listdir("etc/.tmp/"):
            os.remove("etc/.tmp/" + fileName)
        Gtk.main_quit()
        

    '''''''''''''''''''''''''''''''''''''''''
    # on_districts_map_button_clickked() : Generate map of districts
    #                                      based on ZCTA populations
    # @args : None
    # Return : Begin districts map generation or display Waring()
    '''''''''''''''''''''''''''''''''''''''''
    def on_districts_map_button_clicked(self, *args):
        files = self.builder.get_object("files")
        overwrite_warning = False
        fileName = ""
        
        # Determine whether the data has already be generated this session
        for fileID in files:
            if fileID.get_label() == "districts_map":
                overwrite_warning = True
                fileName = fileID.get_label()
                
        # Begin distric map generation or display waring window
        if overwrite_warning:
            dialog = Warning(fileName)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                dialog.destroy()
                # Remove previously generated data from home window
                for fileID in files:
                    if fileID.get_label() == "districts_map":
                        files.remove(fileID)
            else:    
                dialog.destroy()
                return

        # Begin map generation if no overwrite warning or user chose to continue
        shapefile = threading.Thread(target=self.shapefile_thread, args=("etc/.tmp/districts_map.jpeg", True))
        shapefile.daemon = True
        shapefile.start()
        
        self.builder.get_object("zcta_map_button").set_sensitive(False)
        self.builder.get_object("districts_map_button").set_sensitive(False)

    '''''''''''''''''''''''''''''''''''''''
    # on_zcta_map_button_clicked() : Generate map of ZCTA's
    # @args : None
    # Return : Begin ZCTA map generation or display Warning()
    '''''''''''''''''''''''''''''''''''''''
    def on_zcta_map_button_clicked(self, *args):
        files = self.builder.get_object("files")
        overwrite_warning = False
        fileName = ""
        
        # Determine whether to overwrite the file
        for fileID in files:
            if fileID.get_label() == "zcta_map":
                overwrite_warning = True
                fileName = fileID.get_label()
                
        # Call shapefile_thread() to generate map or display waring window
        if overwrite_warning:
            dialog = Warning(fileName)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                dialog.destroy()
                # Remove previously generated data from home window
                for fileID in files:
                    if fileID.get_label() == "zcta_map":
                        files.remove(fileID)
            else:    
                dialog.destroy()
                return

        # Begin map generation if no overwrite warning or user chose to continue
        shapefile = threading.Thread(target=self.shapefile_thread, args=("etc/.tmp/zcta_map.jpeg", False))
        shapefile.daemon = True
        shapefile.start()
            
        self.builder.get_object("zcta_map_button").set_sensitive(False)
        self.builder.get_object("districts_map_button").set_sensitive(False)

    ''''''''''''''''''''''''''''''''''''''''''''
    # open_map_window() : Create map window or open existing, note that all open windows are stored
    #                     in the global array map_windows defined in md_map
    # @args[1] : Name of the link that is being opened
    # Return : Construct map window and display to user
    ''''''''''''''''''''''''''''''''''''''''''''
    def open_map_window(self, *args):
        if args[1] in md_map.map_windows:
            md_map.map_windows[args[1]].bring_front()
        else:
            md_map.map_windows[args[1]] = md_map.Map_Window(args[1])

    ''''''''''''''''''''''''''''''''''''''''''''
    # update_log() : Update GUI to inform user of gereration process
    # @txt_str : String that indicates the current state of the generation process
    # Return : False - 'status_log' is updated in the home window
    ''''''''''''''''''''''''''''''''''''''''''''
    def update_log(self, txt_str):
        status_log = self.builder.get_object("status_log")
        status_log.set_text(txt_str)
        return False

    '''''''''''''''''''''''''''''''''''''''''''''
    # Add a link to the GUI for the user to open the generated map
    '''''''''''''''''''''''''''''''''''''''''''''
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

    '''''''''''''''''''''''''''''''''''''''''''''''
    # show_log() : Make log visible to the user
    # Return : Log is visible on home window
    '''''''''''''''''''''''''''''''''''''''''''''''
    def show_log(self, *args):
        self.builder.get_object("spinner").show()
        status_log = self.builder.get_object("status_log")
        status_log.show()

    '''''''''''''''''''''''''''''''''''''''''''''''
    # shapefile_thread() : Generate map based on arguments passed in
    # @args[0] : String that contains file name to save generated data in
    # @args[1] : Boolean - False colors by ZCTA, True colors by distric
    # Return : Map has been generated
    '''''''''''''''''''''''''''''''''''''''''''''''
    def shapefile_thread(self, *args):
        GLib.idle_add(self.show_log)
        
        GLib.idle_add(self.update_log, "Gathering Data...")
        shpPath = "./etc/MDdata/Maryland_Census_Data__ZIP_Code_Tabulation_Areas_ZCTAs.shp"

        GLib.idle_add(self.update_log, "Reading Shapefile...")
        data = geoShapeWork.readShapefile(shpPath)
        
        GLib.idle_add(self.update_log, "Building ZCTAs...")
        zipcodes = geoShapeWork.createZipObjects(data)

        # Generate map divided into districts
        if (args[1]):
            GLib.idle_add(self.update_log, "Creating connnected graph...")
            zipcodes = zipdistrict.createConnectedGraph(zipcodes)

            GLib.idle_add(self.update_log, "Splitting by population...")
            output = zipdistrict.cluster(zipcodes, 8)

            GLib.idle_add(self.update_log, "Coloring districts...")
            ziprender.colorByDistrict(output, ziprender.randomColors(8), 15)

            GLib.idle_add(self.update_log, "Rendering districts...")
            img = ziprender.renderZipCodes(output, scale=2000, centroidRadius=15)

        # Generate map divided into ZCTAs
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

