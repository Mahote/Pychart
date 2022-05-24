# Pychart - Thomas Brunet - Interactive Visualization For Statechart

## How to use the tool

**First you need to have a yaml file that past true the validation**

here is an example of a valide statechart : 
```yaml
statechart:
  description: "description"
  name: Stopwatch
  root state:
    name: active
    parallel states:
    - initial: actual time
      name: display
      position: 333.0,189.0
      states:
      - name: lap time
        position: 137.0,222.0
        transitions:
        - action: stopwatch.unsplit()
          event: split
          target: actual time
      - name: actual time
        position: 353.0,222.0
        transitions:
        - action: stopwatch.split()
          event: split
          target: lap time
    - initial: stopped
      name: timer
      position: 169.0,189.0
      states:
      - name: stopped
        position: 135.0,158.0
        transitions:
        - action: stopwatch.start()
          event: start
          target: running
      - name: running
        position: 342.0,157.0
        transitions:
        - action: stopwatch.stop()
          event: stop
          target: stopped
      transitions:
      - action: stopwatch.reset()
        event: reset
    position: None
```
for more information on the statechart validation you can check the sismic documentation here : https://sismic.readthedocs.io/en/latest/format.html.  
The only thing that changes are the position in the yaml but there are optional.

When you have a correct yaml file you can now use pychart using the following commands :  
you need to be in the git repo of course  
* python3 pychart.py [path to the yaml file]

if you did all the thing above correctly you will have a window like this : 
![example img](doc/img/exampleREADME.png)

to navigate through you statechart you need to select the state on which you want to see the child or the parent (if nothing happen then there is no child or you are already at the root state)

selection example :   
![example selection](doc/img/selectionexample.png)

now you can click on the go to child or go to parent button  
![example button](doc/img/examplebutton.png)

by holding the left mouse click when you select a box you can drag it and position it where you want, same behaviors for the arrows.  
After the position is to your taste you can press the save positions button it will save the boxes positions into the yaml

when you click on an arrow informations are displayed in the bottom of the window like this :  
![arrow informations example](doc/img/arrowinfo.png)

## Tools used for the development
* gaphas : https://gaphas.readthedocs.io/en/stable/
* Gtk (version 3.0): https://python-gtk-3-tutorial.readthedocs.io/en/latest/

* sismic : https://sismic.readthedocs.io/en/latest/

## Credits

* Giussepe Lipari researcher in the Cristal team in the University of Lille, who trust me for this project and helped me in various thing through the adventure.