''''''''''''''''''''''''''''''''''''
# File : md_map.py
# Description: This file manages map windows, the defaul format
#             is loaded from "map_format.glade" and all open
#             map windows are saved in the global variable
#             map_windows.
#
# Author : Ryan Jahnige
''''''''''''''''''''''''''''''''''''

import sys
import shutil
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

# Contains all open map windows
map_windows = {}

class Map_Window:
    # Retrieve window to display the user choosen map
    # @args[0] : String that contains the file file name of the map
    #            to open
    def __init__(self, *args):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("etc/map_format.glade")
        self.builder.connect_signals(self)
        
        window = self.builder.get_object("map_window")
        window.set_title(args[0])
        map_img = self.builder.get_object("map_img")
        
        # Get image from file, resize and display to screen
        fileName = "etc/.tmp/" + args[0] + ".jpeg"
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(fileName)
        pixbuf = pixbuf.scale_simple(1500, 750, GdkPixbuf.InterpType.BILINEAR)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        map_img.add(image)
            
        window.show_all()

    # Unminimize window or bring to the front
    def bring_front(self):
        window = self.builder.get_object("map_window")
        window.deiconify()

    # Removes file name from gloabal array map_windows
    def on_map_delete(self, *args):
        global map_windows
        fileName = self.builder.get_object("map_window").get_title()
        del map_windows[fileName]

    def on_close_msg_box(self, *args):
        map_overlay = self.builder.get_object("map_overlay")
        map_overlay.remove(map_overlay.get_children()[1])
    
    # Creates a dialog that allows a user to specify a folder and filename
    # to which they wish to save the image file
    def on_map_save_clicked(self, *args):
        fileName = self.builder.get_object("map_window").get_title()
        fileName += ".jpeg"
        dialog = Gtk.FileChooserDialog(title="Save file",
                                       parent=self.builder.get_object("map_window"),
                                       action=Gtk.FileChooserAction.SAVE)
        
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        dialog.set_default_size(800, 400)

        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_name(fileName)
        
        response = dialog.run()
        map_overlay = self.builder.get_object("map_overlay")
        if (len(map_overlay.get_children()) < 2):
            box = Gtk.HBox(spacing=10)
            box.set_halign(Gtk.Align.START)
            box.set_valign(Gtk.Align.END)

            btn = Gtk.Button.new_from_icon_name(icon_name=Gtk.STOCK_CLOSE, size=0)
            btn.connect("clicked", self.on_close_msg_box)
            box.pack_start(child=btn, expand=False, fill=False, padding=0)
        
            msg = Gtk.Label()
            box.pack_end(child=msg, expand=False, fill=False, padding=0)
            
            map_overlay.add_overlay(box)
        else:
            box = map_overlay.get_children()[1]
            msg = box.get_children()[1]
            
        if response == Gtk.ResponseType.OK:
            text = "Image saved to " + dialog.get_filename()
            #msg.set_label(text)

            # Try to save file to users file system, cannot save to
            # directories that the user does not have permission for
            try:
                shutil.copyfile("etc/.tmp/" + fileName, dialog.get_filename())
            except:
                text = "Error: " + str(sys.exc_info()[0])
                #msg.set_label(text)
                
        else:
            text = "Canceled: Image not saved"
            #msg.set_label("Canceled: Image not saved")

        msg.set_markup("<span color='white'>" + text + "</span>") 
        box.show_all()
        dialog.destroy()

    # For this function to work properly it requires that the pillow image file
    # saved has a scale of 2000 
    def on_map_zoomIn_clicked(self, *args):
        map_img = self.builder.get_object("map_img")
        img = map_img.get_children()[0]
        width = img.get_pixbuf().get_width()
        height = img.get_pixbuf().get_height()
        title = self.builder.get_object("map_window").get_title()
        fileName = "etc/.tmp/" + title + ".jpeg"
        
        if width < 4500:
            width += 1000
            height += 350
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(fileName)
            pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
            image = Gtk.Image()
            image.set_from_pixbuf(pixbuf)
            for item in map_img.get_children():
                map_img.remove(item)
            map_img.add(image)
            map_img.show_all()

    # For this function to work properly it requires that the pillow image file
    # saved has a scale of 2000 
    def on_map_zoomOut_clicked(self, *args):
        map_img = self.builder.get_object("map_img")
        img = map_img.get_children()[0]
        width = img.get_pixbuf().get_width()
        height = img.get_pixbuf().get_height()
        title = self.builder.get_object("map_window").get_title()
        fileName = "etc/.tmp/" + title + ".jpeg"
        
        if width > 1500:
            width -= 1000
            height -= 350
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(fileName)
            pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
            image = Gtk.Image()
            image.set_from_pixbuf(pixbuf)
            for item in map_img.get_children():
                map_img.remove(item)
            map_img.add(image)
            map_img.show_all()

