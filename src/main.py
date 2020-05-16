import time
import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango

from applications import Applications
from treeview import Treeview

from util import Util

sys.path.append('/usr/lib/python3.8/site-packages')

class Main():
    def __init__(self):
        self.applications = Applications()
        self.applications.generate_apps_file() 

        gladeFile = Util.get_path(self, 'assets/main.glade')
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gladeFile)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object('Main')
        self.window.connect('delete-event', Gtk.main_quit)
        # self.window.set_skip_taskbar_hint(True)

        display = self.builder.get_object('Display')
        display.set_vexpand(True)
        self.treeview = Treeview(display, self.open)

        self.search_entry = self.builder.get_object('Search')
        self.search_entry.modify_font(Pango.FontDescription('Tahoma 25'))

        # Populate apps
        self.result = self.applications.filter_apps('')
        self.treeview.add_new(self.result)

        self.window.show_all()

    def on_key_press(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == 'Escape':
            Gtk.Window.close(self.window)
            return False
        
        if keyname == 'Up' \
            or keyname == 'Down' \
            or keyname == 'Return' :
            return False
        else:
            if not self.search_entry.is_focus():
                self.search_entry.grab_focus()
        return False        

    
    def on_search(self, element):
        search_text = element.get_text()

        self.result = self.applications.filter_apps(search_text)
        self.display_app_search()

    def display_app_search(self):
        self.treeview.clear()
        self.treeview.add_new(self.result)

    def open(self, app_name):
        self.applications.launch_app(app_name)
        time.sleep(1)
        Gtk.Window.close(self.window)

if __name__ == '__main__':
    main = Main()
    Gtk.main()
