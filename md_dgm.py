'''
# Filename : md_dgm.py
# Description : This file uses the Gtk to provide an interactive
#               user interface for our users.  
'''

import sys
import shutil
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib
from PIL import Image

class MD_DGM_APP:
    # Initialize the home window from 'design_format.glade'
    def __init__(self):
        self.confirm_warning = False
        self.builder = Gtk.Builder()
        self.builder.add_from_file("design_format.glade")
        self.builder.connect_signals(self)
        
        window = self.builder.get_object("home_window")
        window.show_all()

    # Returns control to calling program on exit
    def on_home_destroy(self, *args):
        Gtk.main_quit()

    # Retrieve window to display the user choosen map
    def Map_Window(self, *args):
        window = self.builder.get_object("map_window")

        # Unminimize window if it is minimized
        if window.props.visible:
            window.deiconify()

        # Otherwise configure window
        else:
            window.connect('delete-event', lambda w, e: w.hide() or True)
            window.set_title(args[1])
            map_img = self.builder.get_object("map_img")

            # Get image from file, resize and display to screen
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("test.gif")
            pixbuf = pixbuf.scale_simple(1500, 750, GdkPixbuf.InterpType.BILINEAR)
            image = Gtk.Image()
            image.set_from_pixbuf(pixbuf)
            map_img.add(image)
            
            window.show_all()

    # Removes the map image from the window so it can be
    # reconfigured with a new image
    def on_map_delete(self, *args):
        map_img = self.builder.get_object("map_img")
        imgList = map_img.get_children()
        for item in imgList:
            map_img.remove(item)


    def on_close_msg_box(self, *args):
        map_img = self.builder.get_object("map_img")
        imgList = map_img.get_children()
        map_img.remove(imgList[1])
    
    # Creates a dialog that allows a user to specify a folder and filename
    # to which they wish to save the image file
    def on_map_save_clicked(self, *args):
        dialog = Gtk.FileChooserDialog(title="Save file",
                                       parent=self.builder.get_object("map_window"),
                                       action=Gtk.FileChooserAction.SAVE)
        
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        dialog.set_default_size(800, 400)

        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_name("test.gif")
        
        response = dialog.run()
        map_img = self.builder.get_object("map_img")
        if (len(map_img.get_children()) < 2):
            box = Gtk.HBox(spacing=10)
            box.set_halign(Gtk.Align.START)
            box.set_valign(Gtk.Align.END)

            btn = Gtk.Button.new_from_icon_name(icon_name=Gtk.STOCK_CLOSE, size=0)
            btn.connect("clicked", self.on_close_msg_box)
            box.pack_start(child=btn, expand=False, fill=False, padding=0)
            
            msg = Gtk.Label()
            box.pack_end(child=msg, expand=False, fill=False, padding=0)
            
            map_img.add_overlay(box)
        else:
            box = map_img.get_children()[1]
            msg = box.get_children()[1]
            
        if response == Gtk.ResponseType.OK:
            text = "Image saved to " + dialog.get_filename()
            msg.set_label(text)

            try:
                shutil.copyfile("test.gif", dialog.get_filename())
            except:
                text = "Error: " + str(sys.exc_info()[0])
                msg.set_label(text)
                
        else:
            msg.set_label("Canceled: Image not saved")

        box.show_all()
        dialog.destroy()

    # Not yet implemented
    def on_map_zoomIn_clicked(self, *args):
        map_img = self.builder.get_object("map_img")
        img = map_img.get_children()[0]
        width = img.get_pixbuf().get_width()
        height = img.get_pixbuf().get_height()
        
        if width < 4500:
            width += 1000
            height += 350
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("test.gif")
            pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
            image = Gtk.Image()
            image.set_from_pixbuf(pixbuf)
            for item in map_img.get_children():
                map_img.remove(item)
            map_img.add(image)
            map_img.show_all()
        
    def on_map_zoomOut_clicked(self, *args):
        map_img = self.builder.get_object("map_img")
        img = map_img.get_children()[0]
        width = img.get_pixbuf().get_width()
        height = img.get_pixbuf().get_height()
        
        if width > 1500:
            width -= 1000
            height -= 350
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("test.gif")
            pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
            image = Gtk.Image()
            image.set_from_pixbuf(pixbuf)
            for item in map_img.get_children():
                map_img.remove(item)
            map_img.add(image)
            map_img.show_all()

    # Display a warning when the user wishes to generate a map that
    # that has already been generated this session. 
    def Warning_Window(self, *args):
        window = self.builder.get_object("warning_window")
        label = self.builder.get_object("event_content")
        self.fileName = args[0]
        
        text_str = "Data has already been generated and is unsaved, this\nwill overwrite the data in \"" + args[0] + "\"\n\nDo you want to continue?"
        
        label.set_label(text_str)
        window.show_all()

    # Exit warning window and signify to not overwrite
    def on_warning_quit_clicked(self, *args):
        window = self.builder.get_object("warning_window")
        window.hide()

    # Exit warning window and signify overwrite
    def on_warning_continue_clicked(self, *args):
        window = self.builder.get_object("warning_window")
        files = self.builder.get_object("files")
        
        for file in files:
            if file.get_label() == self.fileName:
                files.remove(file)

        link = Gtk.LinkButton(label=self.fileName, uri=self.fileName)
        link.connect("clicked", self.Map_Window, self.fileName)
        link.show()
        files.add(link)
        
        window.hide()

    # Generate map of ZCTA's, will eventually call main.py as opposed to
    # just using the file it generated
    def on_zcta_map_button_clicked(self, *args):
        files = self.builder.get_object("files")
        overwrite_warning = False
        fileName = ""
        
        # Determine whether to overwrite the file
        fileList = files.get_children()
        for file in fileList:
            if file.get_label() == "test.gif":
                overwrite_warning = True
                fileName = file.get_label()

        # Display link to map window or display waring window
        if overwrite_warning:
            self.Warning_Window(fileName)
        else:
            link = Gtk.LinkButton(label="test.gif", uri="test.gif")
            link.connect("clicked", self.Map_Window, "test.gif")
            link.show()
            files.add(link)

def main():
    app = MD_DGM_APP()
    Gtk.main()

if __name__ == "__main__":
    main()
