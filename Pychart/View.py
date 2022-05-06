from tokenize import String
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gaphas import Canvas
from gaphas.view import GtkView
class View(Gtk.Window):
    def __init__(self, canvas : Canvas, title : str):
        super(View,self).__init__(default_width=600, default_height=600)
        self.title = title
        self._canvasview = GtkView()
        self._canvas = canvas
        self.set_title(self.title)

        self._box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL,6)
        self.add(self._box)
        
        self._buttonBox = Gtk.Box.new(Gtk.Orientation.VERTICAL,6)
        self._frame = Gtk.Frame()
        self._frame.add(self._buttonBox)

        self._box.add(self._frame)
        
        self._stateInteraction = Gtk.Label.new("State Interaction")
        self._buttonBox.add(self._stateInteraction)

        self._toChildButton = Gtk.Button.new_with_label("go to child")
        self._toParentButton = Gtk.Button.new_with_label("go to parent")
        
        self._buttonBox.add(self._toChildButton)
        self._buttonBox.add(self._toParentButton)
        
        self._canvasview.model = self._canvas

        scrolledWindow = Gtk.ScrolledWindow.new()
        scrolledWindow
        scrolledWindow.set_hexpand(True)
        scrolledWindow.add(self._canvasview)
        self._box.add(scrolledWindow)
        self.connect("destroy", Gtk.main_quit)

        self.show_all()