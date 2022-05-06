
from select import select
from gaphas.item import NE,SE,SW,NW, Element, Line
from gaphas.util import text_align
from gaphas.selection import Selection
from gaphas.tool import hover_tool, item_tool, scroll_tool, view_focus_tool, zoom_tool

class Box_State(Element):
    def __init__(self, connections, width: float = 70, height: float = 70, name = '', parent_name = ''):
        self.name = name
        self.parent_name = parent_name
        self.connections = connections
        super().__init__(connections, width, height)
    def draw(self, context):
        global r
        r = True
        cr = context.cairo
        nw = self._handles[NW].pos
        cr.rectangle(nw.x,nw.y, self.width, self.height)
        txt = text_align(cr, self.width/2, 10, self.name)
        if context.hovered:
            cr.set_source_rgba(0.8, 0.8, 1, 0.8)
        else:
            cr.set_source_rgba(1, 1, 1, 0.8)
        cr.set_source_rgb(0, 0, 0.8)
        cr.stroke()
    def connection(self, Box_to_connect):
        arrow = Arrow(self.connections)
        x = self.matrix.tuple()[4]
        y = self.matrix.tuple()[5]
        to_x = Box_to_connect.matrix.tuple()[4]
        to_y = Box_to_connect.matrix.tuple()[5]
        arrow.head._set_pos((x+self.width,y))
        arrow.tail._set_pos((to_x,to_y))
        #self.connections.connect_item(arrow, arrow.head,self, self.ports()[1],)
        #self.connections.connect_item(arrow, arrow.tail,Box_to_connect, Box_to_connect.ports()[0])
        return arrow
class Arrow(Line):
    def __init__(self, connections):
        self._line_width = 5
        self.fuzziness = 2
        super().__init__(connections)
    def draw(self, context):
        cr = context.cairo
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

