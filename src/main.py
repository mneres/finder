import time
from subprocess import Popen

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango

from applications import Applications
from folders import Folders
from treeview import Treeview
from folders_treeview import FoldersTreeview

from util import Util

class Main():
    def __init__(self):
        self.applications = Applications()
        self.folders = Folders()

        self.applications.generate_apps_file() 

        gladeFile = Util.get_path(self, 'assets/main.glade')
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gladeFile)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object('Main')
        self.window.connect('delete-event', Gtk.main_quit)

        display = self.builder.get_object('Display')
        display.set_vexpand(True)
        self.treeview = Treeview(display, self.open)

        folders_display = self.builder.get_object('FoldersDisplay')
        folders_display.set_vexpand(True)
        self.folders_treeview = FoldersTreeview(folders_display, self.open_folder)

        self.search_entry = self.builder.get_object('Search')
        self.search_entry.modify_font(Pango.FontDescription('Tahoma 25'))

        # Populate apps
        self.result = self.applications.filter_apps('')
        self.treeview.add_new(self.result)

        self.window.show_all()

        self.folder_frame = self.builder.get_object('FolderFrame')
        self.folder_frame.hide()

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

        if (search_text == ''):
            self.folders_treeview.clear()
            self.folder_frame.hide()
            return

        self.folders_result = self.folders.filter_folders(search_text)
        self.display_folder_search()

    def display_app_search(self):
        self.treeview.clear()
        self.treeview.add_new(self.result)

    def display_folder_search(self):
        self.folders_treeview.clear()
        self.folders_treeview.add_new(self.folders_result)

        self.window.show_all()

    def open(self, app_name):
        app = self.result[app_name]

        exec_list = app['exec'].split(' ')
        exec_list = [item for item in exec_list if item.find('%') == -1]

        args = ['nohup']
        args = args + exec_list
        print(args)
        Popen(args, shell=False)
        self.window.hide()
        time.sleep(1)
        Gtk.Window.close(self.window)
    
    def open_folder(self, folder_path):
        args = ['nohup', 'caja', '--no-desktop', '--browser', folder_path + '/']

        Popen(args, shell=False)
        self.window.hide()
        time.sleep(1)
        Gtk.Window.close(self.window)

if __name__ == '__main__':
    main = Main()
    Gtk.main()