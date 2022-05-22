from random import random
from Elements.Items import Arrow, Box_State
from gaphas import Canvas
from gaphas.view import GtkView
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
                if(b.state.position != None):
                    position = (b.state.position).split(",")
                    b.matrix.translate(float(position[0]),float(position[1]))
                else:
                    b.matrix.translate(x,y)
                self.canvas.add(b)
    def transitionDrawer(self, statelist : list, statechart : Statechart, view):
        itemsToConnect = self.canvas.get_all_items()
        liste = list(itemsToConnect)
        strlist = list()
        if len(statelist)>=1:
            for item in liste:
                strlist.append(item.state.name)
            for item1 in liste:
                transitionsOUT= statechart.transitions_from(item1.state.name)
                for transition in transitionsOUT:
                    
                    for item2 in liste:  
                        if(transition.source == item1.state.name and transition.target == item2.state.name):
                            arrow = item1.transitionB2B(item2,transition,view)
                            self.canvas.add(arrow)
                    
                    if(transition.source == item1.state.name and transition.target not in strlist):
                        if(transition.target != None):
                            arrow = item1.transition(True,transition,view)
                            self.canvas.add(arrow)

                transitionsIN = statechart.transitions_to(item1.state.name)
                for transition in transitionsIN:
                    if(transition.target == item1.state.name and transition.source not in strlist):
                        if(transition.source != None):
                            arrow = item1.transition(False,transition,view)
                            self.canvas.add(arrow)
    def cleanCanvas(self):
        items = self.canvas.get_all_items()
        for item in items:
            self.canvas.remove(item)

            