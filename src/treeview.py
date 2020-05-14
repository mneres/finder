from gi.repository import Gtk, GdkPixbuf

class Treeview():
    def __init__(self, parent, callback_open):

        self.callback_open = callback_open

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
        cell.set_property('text', model.get_value(iter, 1))
        # cell.set_property('text', model.get_value(iter, 0))

    def get_tree_cell_pixbuf(self, col, cell, model, iter, user_data):
        icon = str(model.get_value(iter, 0))
        if icon == '':
            return

        if icon.__contains__('/'):
            cell.set_property('pixbuf', GdkPixbuf.Pixbuf.new_from_file_at_scale(model.get_value(iter, 0),
                width=40, height=40, preserve_aspect_ratio=False))
        else:    
            cell.set_property('pixbuf', Gtk.IconTheme.get_default().load_icon(icon, 40, 0))

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
