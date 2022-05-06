from random import random
from sre_parse import State
from tkinter import Canvas
from sismic.model.elements import BasicState,CompoundState, DeepHistoryState, ShallowHistoryState, OrthogonalState

from Elements.Items import Box_State
from gaphas.view import GtkView
import random
class StateDrawer:
    def __init__(self, state, canvasView : GtkView):
        self.state = State
        self.canvasView = canvasView

    def CallDrawer(self, stateList):
        connections = self.canvasView.connections
        x = random.randint(0,200)
        y = random.randint(0,200)
        for state in stateList:
            
            b = Box_State(connections,name=state,)
        