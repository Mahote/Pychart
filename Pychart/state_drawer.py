from ctypes import sizeof
from random import random
from sre_parse import State
from tkinter import Canvas
from typing import List
from sismic.model.elements import BasicState,CompoundState, DeepHistoryState, ShallowHistoryState, OrthogonalState

from Elements.Items import Box_State
from gaphas import Canvas
from gaphas.view import GtkView
from sismic.model import Statechart
import random
class StateDrawer:
    def __init__(self, state, canvas: Canvas):
        self.state = state
        self.canvas = canvas

    def boxDrawer(self, stateList : list):
        connections = self.canvas.connections
        x = random.randint(0,200)
        y = random.randint(0,200)
        print(len(stateList))
        if len(stateList)>=1:
            self.cleanCanvas()
            for state in stateList:
                x = random.randint(0,300)
                y = random.randint(0,300)
                b = Box_State(connections,70,70,state, self.state)
                b.matrix.translate(x,y)
                self.canvas.add(b)
    def transitionDrawer(self, statelist : list, statechart : Statechart):
        itemsToConnect = self.canvas.get_all_items()
        for item1 in itemsToConnect:
            transitions = statechart.transitions_from(item1.state.name)
            for item2 in itemsToConnect:
                for transition in transitions:
                    if(transition.source == item1.state.name and transition.target == item2.state.name):
                        print("do arrow from ", item1.state.name, "to ", item2.state.name)
                        print("transition : " , transition)
                    
        
    def cleanCanvas(self):
        items = self.canvas.get_all_items()
        for item in items:
            self.canvas.remove(item)

            