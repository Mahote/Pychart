import gi
gi.require_version('Gtk', '3.0')
from state_drawer import StateDrawer
from sismic.io import import_from_yaml,export_to_yaml
from View import View
from Elements.Items import Box_State
from gi.repository import Gtk
from gaphas import Canvas
from gaphas.tool import hover_tool,item_tool,scroll_tool,zoom_tool,view_focus_tool
class Controller():
    def __init__(self, view: View, statechart, statechartpath : str):
        self.view = view
        self.statechart = statechart
        self.path = statechartpath
        self.canvasview = self.view._canvasview
        self.canvas = self.view._canvas
        
        self.rootState = self.statechart.state_for(self.statechart.root)
        self.canvasIntialisation()
        self.apply_default_tool_set(self.view._canvasview)
        self.view.connect('destroy', Gtk.main_quit)
        self.view._toParentButton.connect('clicked', self.parentButton_Clicked)
        self.view._toChildButton.connect('clicked', self.childButton_Clicked)
        self.view._saveBoxesPositions.connect('clicked', self.saveButton_CLicked)
        self.view.show_all()
    def canvasIntialisation(self):
        childrens = self.statechart.children_for(self.rootState.name)
        states = self.mappingState(childrens)
        stateDrawer = StateDrawer(self.rootState, self.canvas, self.canvasview)
        stateDrawer.boxDrawer(states)
        stateDrawer.transitionDrawer(states,self.statechart,self.view)

    def childButton_Clicked(self, _button):
        selection = self.canvasview.selection
        Box = selection.focused_item
        if(isinstance(Box, Box_State)):
            self.view.set_title(Box.state.name)
            drawer = StateDrawer(Box.state, self.canvas, self.canvasview)
            childrens = self.statechart.children_for(Box.state.name)
            states = self.mappingState(childrens)
            drawer.boxDrawer(states)
            drawer.transitionDrawer(states, self.statechart,self.view)
    
    def parentButton_Clicked(self, _button):
        selection = self.canvasview.selection 
        Box = selection.focused_item
        if(isinstance(Box, Box_State) and Box.state_parent.name != self.statechart.root):
            stateParentName = self.statechart.parent_for(Box.state_parent.name)
            drawer = StateDrawer(Box.state_parent, self.canvas, self.canvasview)
            childrens = self.statechart.children_for(stateParentName)
            states = self.mappingState(childrens)
            drawer.boxDrawer(states)
            drawer.transitionDrawer(states,self.statechart,self.view)
    
    def saveButton_CLicked(self, _button):
        items = self.canvas.get_all_items()
        for item in items:
            if(isinstance(item,Box_State)):
                state = item.state
                x = item.matrix.tuple()[4]
                y = item.matrix.tuple()[5]
                state.set_position(str(x)+","+str(y))
        
        for state in self.statechart.states:
            print(self.statechart.state_for(state).position)
        export_to_yaml(self.statechart, self.path)
    
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
    def start(self):
        Gtk.main()