from gi.repository import Gtk, GdkPixbuf

class FoldersTreeview():
    def __init__(self, parent, callback_open):

        self.callback_open = callback_open

        # self.liststore = Gtk.ListStore(str, str)
        self.liststore = Gtk.ListStore(str)
        self.treeview = Gtk.TreeView(model=self.liststore)

        self.treeview.set_headers_visible(False)

        # px_renderer = Gtk.CellRendererPixbuf()
        px_column = Gtk.TreeViewColumn('')
        # px_column.pack_start(px_renderer, False)
        str_renderer = Gtk.CellRendererText()
        px_column.pack_start(str_renderer, False)
        # set data connector function/method
        # px_column.set_cell_data_func(px_renderer, self.get_tree_cell_pixbuf)
        px_column.set_cell_data_func(str_renderer, self.get_tree_cell_text)
        self.treeview.append_column(px_column)

        self.treeview.connect('row-activated', self.open)

        parent.add(self.treeview)

    def get_tree_cell_text(self, col, cell, model, iter, user_data):
        # cell.set_property('text', model.get_value(iter, 1))
        cell.set_property('text', model.get_value(iter, 0))

    def get_tree_cell_pixbuf(self, col, cell, model, iter, user_data):
        cell.set_property('pixbuf', GdkPixbuf.Pixbuf.new_from_file_at_scale(model.get_value(iter, 0),
                            width=40, height=40, preserve_aspect_ratio=False))

    def add_new(self, items):
        for item in items:
            path = [items[item]['path']]
            self.liststore.append(path)
    
    def clear(self):
        self.liststore.clear()

    def open(self, widget, row, col):
        model = widget.get_model()
        # app = model[row][1]
        app = model[row][0]
        self.callback_open(app)