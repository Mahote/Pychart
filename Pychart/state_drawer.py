from random import random
from sismic.model.elements import BasicState,CompoundState, DeepHistoryState, ShallowHistoryState, OrthogonalState

from Elements.Items import Arrow, Box_State
from gaphas import Canvas
from gaphas.view import GtkView
from gaphas.segment import LineSegment
from sismic.model import Statechart
import random
class StateDrawer:
    def __init__(self, state, canvas: Canvas, canvasView : GtkView):
        self.state = state
        self.canvas = canvas
        self.canvasView = canvasView
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
        liste = list(itemsToConnect)
        strlist = list()
        for item in liste:
            strlist.append(item.state.name)
        for item1 in liste:
            transitionsOUT= statechart.transitions_from(item1.state.name)
            for transition in transitionsOUT:
                for item2 in liste:  
                    if(transition.source == item1.state.name and transition.target == item2.state.name):
                        arrow = item1.transitionB2B(item2)
                        self.canvas.add(arrow)
                if(transition.source == item1.state.name and transition.target not in strlist):
                    if(transition.target != None):
                        print("transitionOUT : " , transition)
                        arrow = Arrow(self.canvas.connections)
                        arrow = item1.transition(False)
                        self.canvas.add(arrow)
            transitionsIN = statechart.transitions_to(item1.state.name)
            for transition in transitionsIN:
                if(transition.target == item1.state.name and transition.source not in strlist):
                    if(transition.source != None):
                        arrow = Arrow(self.canvas.connections)
                        arrow = item1.transition(True)
                        self.canvas.add(arrow)
                        print("transitionIN : " , transition)
                        
    def transitionExtern(self,listOfItems,statechart):
        res = list()
        for item1 in listOfItems:
            transitions = statechart.transitions_from(item1.state.name)
            for item2 in listOfItems:
                for transition in transitions:  
                    if(transition.source == item1.state.name and transition.target != item2.state.name):
                        res.append(transition)
    def cleanCanvas(self):
        items = self.canvas.get_all_items()
        for item in items:
            self.canvas.remove(item)

            