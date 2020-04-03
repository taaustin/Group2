'''
# Filename : md_dgm.py
# Description : This file uses the Gtk to provide an interactive
#               user interface for our users. 
#
# Important Notes : It must be run with python3. The "Zoom In" and 
#                   "Zoom out" buttons have not yet been implemented.
#                    The save map feature has not be programed to save 
#                    the file yet, although this will be easy to do.
#                    There is also a bug when displaying the "warning
#                    window" that is documented in backlog.  
'''

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

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
        map_img.remove(imgList[0])

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
        log = self.builder.get_object("user_log")
        if response == Gtk.ResponseType.OK:
            text = "File saved to " + dialog.get_filename()
            log.set_label(text)
        elif response == Gtk.ResponseType.CANCEL:
            log.set_label("Canceled: File not saved")

        dialog.destroy()


    # Not yet implemented
    def on_map_zoomIn_clicked(self, *args):
        return
    def on_map_zoomOut_clicked(self, *args):
        return

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
