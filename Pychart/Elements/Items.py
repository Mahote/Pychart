
from re import A
from select import select
from gaphas.item import NE,SE,SW,NW, Element, Line
from gaphas.util import text_align
import random
from gaphas.port import LinePort,Port
from gaphas.constraint import constraint
from gaphas.tool import hover_tool, item_tool, scroll_tool, view_focus_tool, zoom_tool


class Box_State(Element):
    def __init__(self, connections, width: float = 70, height: float = 70, state = None, state_parent = None):
        self.state = state
        self.state_parent = state_parent
        self.connections = connections
        super().__init__(connections, width, height)
    def draw(self, context):
        cr = context.cairo
        nw = self._handles[NW].pos
        cr.rectangle(nw.x,nw.y, self.width, self.height)
        txt = text_align(cr, self.width/2, 10, self.state.name)
        if context.hovered:
            cr.set_source_rgba(0.8, 0.8, 1, 0.8)
        else:
            cr.set_source_rgba(1, 1, 1, 0.8)
        cr.set_source_rgb(0, 0, 0.8)
        cr.stroke()
    def transitionB2B(self, Box_to_connect,transition,view):
        arrow = Arrow(self.connections,transition,view)
        constraint_head = self.ports()[1].constraint(arrow,arrow.head,self)
        constraint_tail = Box_to_connect.ports()[1].constraint(arrow,arrow.tail,Box_to_connect)
        self.connections.connect_item(arrow, arrow.head,self, self.ports()[1], constraint=constraint_head)
        self.connections.connect_item(arrow, arrow.tail,Box_to_connect, Box_to_connect.ports()[1], constraint=constraint_tail)
        
        y1 = self.matrix.tuple()[5]
        pos_y1 = random.randint(y1,y1+self.height)
        arrow.head.pos.y = pos_y1
        
        y2 = Box_to_connect.matrix.tuple()[5]
        pos_y2 = random.randint(y2,y2+Box_to_connect.height)
        arrow.tail.pos.y = pos_y2
        return arrow

    def transition(self, in_or_out : bool,transition,view):
        #out = True | in = False
        arrow = Arrow(self.connections,transition,view)
        x = self.matrix.tuple()[4]
        y = self.matrix.tuple()[5]
        pos_x = random.randint(x,x+self.width)
        lineport = LinePort(self.handles()[2].pos, self.handles()[3].pos)
        if(in_or_out):
            constraint_head = lineport.constraint(arrow,arrow.head,self)
            self.connections.connect_item(arrow,arrow.head,self,lineport,constraint_head)
            arrow.head._set_pos((pos_x,y+self.height))
            arrow.tail._set_pos((pos_x,y+(self.height*2)))
            arrow.connections.add_constraint(arrow,constraint(vertical=(arrow.tail.pos,arrow.head.pos)))
            
        else:
            constraint_tail = lineport.constraint(arrow,arrow.tail,self)
            self.connections.connect_item(arrow,arrow.tail,self,lineport,constraint_tail)
            
            arrow.tail._set_pos((pos_x,y+self.height))
            arrow.head._set_pos((pos_x,y+(self.height*2)))
            
            arrow.connections.add_constraint(arrow,constraint(vertical=(arrow.tail.pos,arrow.head.pos)))
        return arrow
class Arrow(Line):
    def __init__(self, connections,transition,view):
        self.view = view
        self.transition = transition
        self.connections = connections
        self._line_width = 5
        self.fuzziness = 2
        super().__init__(connections)
    def draw(self, context):
        cr = context.cairo
        x = (self.head.pos.x + self.tail.pos.x)/2
        y = (self.head.pos.y + self.tail.pos.y)/2
        text = text_align(cr,x,y+10,self.transition.event,)
        if(context.selected):
            arrow_informations = self.view.arrow_informations
            arrow_informations[0][1] = self.transition.event
            arrow_informations[1][1] = self.transition.guard
            arrow_informations[2][1] = self.transition.action

        return super().draw(context)
    def draw_tail(self, context):
        cr = context.cairo
        cr.line_to(0,0)
        cr.line_to(10,10)
        cr.move_to(0,0)
        cr.line_to(10,-10)
        cr.stroke()
    def draw_head(self, context):
        return super().draw_head(context)

