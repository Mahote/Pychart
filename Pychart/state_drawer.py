from random import random
from Elements.Items import Arrow, Box_State
from gaphas import Canvas
from gaphas.view import GtkView
from sismic.model import Statechart
import random
class StateDrawer:
    def __init__(self, state, canvas: Canvas, canvasView : GtkView):
        """
            Constructor for the StateDrawer
        """
        self.state = state
        self.canvas = canvas
        self.canvasView = canvasView
    def boxDrawer(self, stateList : list):
        """
            Draw boxes in the canvas view from gaphas, if the state as a position in the yaml 
            then the box is draw at this position else the position is choose randomly
        """
        connections = self.canvas.connections
        x = random.randint(0,200)
        y = random.randint(0,200)
        print(len(stateList))
        if len(stateList)>0:
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
        """
            Draw the transition from a state to another state in or outside of the scope
        """
        itemsToConnect = self.canvas.get_all_items()
        boxToConnect = list(itemsToConnect)
        stateNameList = list()
        if len(statelist)>0:
            for item in boxToConnect:
                stateNameList.append(item.state.name)
            for box1 in boxToConnect:
                #transition from the box1
                transitionsOUT= statechart.transitions_from(box1.state.name)
                for transition in transitionsOUT:
                    for box2 in boxToConnect:
                        # We check if the box2 name is equal to the transition target 
                        # then its a transition between two boces in the same scope
                        # draw the arrow between the two boxes
                        if(transition.source == box1.state.name and transition.target == box2.state.name):
                            arrow = box1.transitionB2B(box2,transition,view)
                            self.canvas.add(arrow)
                    if(transition.source == box1.state.name and transition.target not in stateNameList):
                        # if the transition target is not in the scope we draw an arrow that point to nothing
                        if(transition.target != None):
                            arrow = box1.transition(True,transition,view)
                            self.canvas.add(arrow)

                transitionsIN = statechart.transitions_to(box1.state.name)
                # transitions where the transition target is a box in boxToConnect
                for transition in transitionsIN:
                    # Draw the arrow if the transition is a transition from a box outside the scope to 
                    # a box inside the scope
                    if(transition.target == box1.state.name and transition.source not in stateNameList):
                        if(transition.source != None):
                            arrow = box1.transition(False,transition,view)
                            self.canvas.add(arrow)
    def cleanCanvas(self):
        #Clear the canvas view
        items = self.canvas.get_all_items()
        for item in items:
            self.canvas.remove(item)

            