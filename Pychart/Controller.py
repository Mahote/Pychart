import gi
import random
from sismic.model.elements import *
from state_drawer import StateDrawer
from sismic.io import import_from_yaml
from View import View
from Elements.Items import Box_State
gi.require_version('Gtk', '3.0')
from sismic.model import Statechart
from gi.repository import Gtk
from gaphas import Canvas
from gaphas.tool import hover_tool,item_tool,scroll_tool,zoom_tool,view_focus_tool
class Controller():
    def __init__(self, view: View, statechart: Statechart):
        self.view = view
        self.canvasview= self.view._canvasview
        self.statechart = statechart
        self.canvas = self.view._canvas
        self.canvasIntialisation()
        self.apply_default_tool_set(self.view._canvasview)
        self.view.connect('destroy', Gtk.main_quit)
        self.view._toParentButton.connect('clicked', self.parentButton_Clicked)
        self.view._toChildButton.connect('clicked', self.childButton_Clicked)
        self.view.show_all()
    def canvasIntialisation(self):
        childrens = self.statechart.children_for(self.statechart.root)
        for childName in childrens:
            state = self.statechart.state_for(childName)
            state_drawer = StateDrawer(state, self.canvas)
            #if isinstance(state, CompoundState):
                #state_drawer.CallDrawer()
            b = Box_State(self.canvas.connections,70,70,state.name,self.statechart.root)
            x = random.randint(0, 200)
            y = random.randint(0,200)
            b.matrix.translate(x,y)
            self.canvas.add(b)

    def childButton_Clicked(self, _button):
        selection = self.canvasview.selection
        Box = selection.focused_item
        state = self.statechart.state_for(Box.name)
        print(state)
        if(isinstance(Box, Box_State)):
            items = self.canvas.get_all_items()
            childrens = self.statechart.children_for(Box.name)
            print(childrens)
            if(childrens != []):
                for item in items:
                    self.canvas.remove(item)
                for child in childrens:
                    b = Box_State(self.canvas.connections,70,70,child, Box.name)
                    x = random.randint(0, 100)
                    y = random.randint(0,100)
                    b.matrix.translate(x,y)
                    self.canvas.add(b)
    def parentButton_Clicked(self, _button):
        selection = self.canvasview.selection
        items = self.canvas.get_all_items()
        Box = selection.focused_item
        state_parent = self.statechart.parent_for(Box.parent_name)
        if Box.parent_name != self.statechart.root:
            for item in items:
                    self.canvas.remove(item)
            for state in self.statechart.children_for(state_parent):
                b = Box_State(self.canvas.connections,70,70,state, state_parent)
                print('state in canvas :',state)
                print('parent state', state_parent)
                x = random.randint(0, 100)
                y = random.randint(0,100)
                b.matrix.translate(x,y)
                self.canvas.add(b)
        


    def apply_default_tool_set(self,view):
        view.remove_all_controllers()
        view.add_controller(item_tool(view))
        view.add_controller(scroll_tool(view))
        view.add_controller(zoom_tool(view))
        view.add_controller(view_focus_tool(view))
        view.add_controller(hover_tool(view))

with open("../test.yaml") as f:
    statechart = import_from_yaml(f)
name = statechart.root
c = Canvas()
Controller(View(c,name),statechart)
Gtk.main()