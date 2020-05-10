import time
from subprocess import Popen

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from applications import Applications
from treeview import Treeview
from util import Util

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

        display = self.builder.get_object('Display')
        display.set_vexpand(True)
        self.treeview = Treeview(display, self.open)

        self.window.show_all()

        self.on_search(self.builder.get_object('Search'))
    
    def on_search(self, element):
        self.window.set_size_request(400, 400)
        self.result = self.applications.filter_apps(element.get_text())
        self.display_search()

    def display_search(self):
        self.treeview.clear()
        self.treeview.add_new(self.result)

    def open(self, app_name):
        app = self.result[app_name]

        exec_list = app['exec'].split(' ')
        exec_list = [item for item in exec_list if item.find('%') == -1]

        args = ['nohup']
        args = args + exec_list

        Popen(args, shell=False)
        self.window.hide()
        time.sleep(1)
        Gtk.Window.close(self.window)

if __name__ == '__main__':
    main = Main()
    Gtk.main()