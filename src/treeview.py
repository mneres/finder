import os
from gi.repository import Gtk, GdkPixbuf

from util import Util

class Treeview():
    def __init__(self, parent, callback_open):

        self.callback_open = callback_open

        # Column Types
        self.TEXT_COLUMN = 'text'
        self.ICON_COLUMN = 'pixbuf'

        # Icons
        self.ICON_THEME = Gtk.IconTheme.get_default()
        self.DEFAULT_ICON = Util.get_path(self, 'assets/system-search-symbolic.svg')
        self.ICON_SIZE_WIDTH = 40
        self.ICON_SIZE_HEIGHT = 40
        
        self.liststore = Gtk.ListStore(str, str)
        # self.liststore = Gtk.ListStore(str)
        self.treeview = Gtk.TreeView(model=self.liststore)

        self.treeview.set_headers_visible(False)

        px_renderer = Gtk.CellRendererPixbuf()
        px_column_icon = Gtk.TreeViewColumn('')
        px_column_icon.pack_start(px_renderer, False)
        px_column_icon.set_cell_data_func(px_renderer, self.get_tree_cell_pixbuf)
        self.treeview.append_column(px_column_icon)

        str_renderer = Gtk.CellRendererText()
        px_column_name = Gtk.TreeViewColumn('')
        px_column_name.pack_start(str_renderer, False)
        # set data connector function/method
        px_column_name.set_cell_data_func(str_renderer, self.get_tree_cell_text)
        self.treeview.append_column(px_column_name)

        self.treeview.connect('row-activated', self.open)

        parent.add(self.treeview)

    def get_tree_cell_text(self, col, cell, model, iter, user_data):
        cell.set_property(self.TEXT_COLUMN, model.get_value(iter, 1))

    def use_default_icon(self, cell):
        cell.set_property(self.ICON_COLUMN, GdkPixbuf.Pixbuf.new_from_file_at_scale(self.DEFAULT_ICON,
            width=self.ICON_SIZE_WIDTH, height=self.ICON_SIZE_HEIGHT, preserve_aspect_ratio=False))

    def get_tree_cell_pixbuf(self, col, cell, model, iter, user_data):
        icon = str(model.get_value(iter, 0))
        if icon == '':
            return

        if icon.__contains__('/'):
            if not os.path.isfile(icon):
                # Use default
                self.use_default_icon(cell)
                return

            # If icon is a path open it from file
            cell.set_property(self.ICON_COLUMN, GdkPixbuf.Pixbuf.new_from_file_at_scale(icon,
                width=self.ICON_SIZE_WIDTH, height=self.ICON_SIZE_HEIGHT, preserve_aspect_ratio=False))
            return
        else:
            # Look for icon by name
            lookup = self.ICON_THEME.lookup_icon(icon, 0, 0)
            if lookup == None:
                # Use default
                self.use_default_icon(cell)
                return
            
            icon_path = lookup.get_filename()
            if not os.path.isfile(icon_path):
                # Use default
                self.use_default_icon(cell)
                return

            cell.set_property(self.ICON_COLUMN, GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_path,
                width=self.ICON_SIZE_WIDTH, height=self.ICON_SIZE_HEIGHT, preserve_aspect_ratio=False))

    def add_new(self, items):
        for item in items:
            self.liststore.append([items[item]['icon'], items[item]['name']])
            # self.liststore.append([items[item]['name']])
    
    def clear(self):
        self.liststore.clear()

    def open(self, widget, row, col):
        model = widget.get_model()
        app = model[row][1]
        # app = model[row][0]
        self.callback_open(app)
