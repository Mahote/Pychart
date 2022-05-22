import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Controller import Controller
from View import View
from gaphas import Canvas
from sismic.io import import_from_yaml
if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("Usage : Python3 pychat.py [yaml file]")
    else:
        path = sys.argv[1]
        try:
            with open(path) as f:
                statechart = import_from_yaml(f)
        except ValueError:
            print("Can't open yaml file")
        rootname = statechart.root
        c = Canvas()
        v = View(c,rootname)
        controller = Controller(v,statechart,path)
        controller.start()