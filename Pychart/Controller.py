import gi
import random
from sismic.model.elements import *
from state_drawer import StateDrawer
from sismic.io import import_from_yaml, export_to_plantuml
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
        self.canvasview = self.view._canvasview
        self.statechart = statechart
        self.rootState = self.statechart.state_for(self.statechart.root)
        self.canvasIntialisation()
        self.apply_default_tool_set(self.view._canvasview)
        self.view.connect('destroy', Gtk.main_quit)
        self.view._toParentButton.connect('clicked', self.parentButton_Clicked)
        self.view._toChildButton.connect('clicked', self.childButton_Clicked)
        self.view.show_all()
    def canvasIntialisation(self):
        childrens = self.statechart.children_for(self.rootState.name)
        states = self.mappingState(childrens)
        stateDrawer = StateDrawer(self.rootState, self.view._canvas)
        stateDrawer.boxDrawer(states)
        stateDrawer.transitionDrawer(states,self.statechart)

    def childButton_Clicked(self, _button):
        selection = self.canvasview.selection
        Box = selection.focused_item
        if(isinstance(Box, Box_State)):
            drawer = StateDrawer(Box.state, self.view._canvas)
            childrens = self.statechart.children_for(Box.state.name)
            states = self.mappingState(childrens)
            drawer.boxDrawer(states)
            drawer.transitionDrawer(states, self.statechart)
    def parentButton_Clicked(self, _button):
        selection = self.canvasview.selection 
        Box = selection.focused_item
        
        if(isinstance(Box, Box_State) and Box.state_parent.name != self.statechart.root):
            stateParentName = self.statechart.parent_for(Box.state_parent.name)
            drawer = StateDrawer(Box.state_parent, self.view._canvas)
            childrens = self.statechart.children_for(stateParentName)
            states = self.mappingState(childrens)
            drawer.boxDrawer(states)
            drawer.transitionDrawer(states,self.statechart)
    def mappingState(self, stateNameList):
        statesList = list()
        for stateName in stateNameList:
            statesList.append(self.statechart.state_for(stateName))
        return statesList

    def apply_default_tool_set(self,view):
        view.remove_all_controllers()
        view.add_controller(item_tool(view))
        view.add_controller(scroll_tool(view))
        view.add_controller(zoom_tool(view))
        view.add_controller(view_focus_tool(view))
        view.add_controller(hover_tool(view))

with open("../test.yaml") as f:
    statechart = import_from_yaml(f)
    export_to_plantuml(statechart,"statechart")
name = statechart.root
c = Canvas()
Controller(View(c,name),statechart)
Gtk.main()