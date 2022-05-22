import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gaphas import Canvas
from gaphas.view import GtkView
class View(Gtk.Window):
    def __init__(self, canvas : Canvas, title : str):
        super(View,self).__init__(default_width=800, default_height=600)
        self.title = title
        self._canvasview = GtkView()
        self._canvas = canvas
        self.set_title(self.title)


        self._box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL,6)
        self._mainbox = Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        self.add(self._box)
        self._buttonBox = Gtk.Box.new(Gtk.Orientation.VERTICAL,6)
        self._frame = Gtk.Frame()
        self._frame.add(self._buttonBox)
        self._box.add(self._frame)
        self._box.add(self._mainbox)
        
        self._stateInteraction = Gtk.Label.new("State Interaction")
        self._buttonBox.add(self._stateInteraction)

        self._toChildButton = Gtk.Button.new_with_label("go to child")
        self._toParentButton = Gtk.Button.new_with_label("go to parent")
        self._saveBoxesPositions = Gtk.Button.new_with_label("save positions")

        
        self._buttonBox.add(self._toChildButton)
        self._buttonBox.add(self._toParentButton)
        self._buttonBox.add(self._saveBoxesPositions)
        self._canvasview.model = self._canvas

        scrolledWindow = Gtk.ScrolledWindow.new()
        scrolledWindow.add(self._canvasview)
        scrolledWindow.set_size_request(450,450)
        scrolledWindow.set_hexpand(True)

        self.arrow_informations = Gtk.ListStore(str,str)
        self.arrow_informations.append(["Event","None"])
        self.arrow_informations.append(["Guard","None"])
        self.arrow_informations.append(["Action","None"])
    

        treeview = Gtk.TreeView(model=self.arrow_informations)
        renderer_name = Gtk.CellRendererText()  
        renderer_detail = Gtk.CellRendererText()
        transitions_name = Gtk.TreeViewColumn("events",renderer_name, text=0)
        transitions_detail = Gtk.TreeViewColumn("details",renderer_detail, text=1)
        treeview.append_column(transitions_name)
        treeview.append_column(transitions_detail)
        scrolledtreeview = Gtk.ScrolledWindow()
        scrolledtreeview.add(treeview)
        scrolledtreeview.set_size_request(150,150)
        scrolledtreeview.set_hexpand(True)
        self._mainbox.add(scrolledWindow)
        self._mainbox.add(scrolledtreeview)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()