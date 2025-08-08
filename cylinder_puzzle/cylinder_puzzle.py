# %%
from ocp_vscode import *
from build123d import *
from math import sqrt

# %%
wid, tol = 20, 1
len = 2*wid*(sqrt(2)/2+sqrt(2)/6+2/3)

with BuildPart() as puzzle:
    with GridLocations(wid/3, 0, 3, 1):
        Cylinder(wid/6, len, rotation=(90,0,0))
    Box(len,wid/3,wid/3,rotation=(0,0,45), mode=Mode.SUBTRACT)
    short1 = Cylinder(wid/6, len, rotation=(90,-45,0), align=(Align.CENTER, Align.CENTER, Align.CENTER))
    Cylinder(wid/6, 0.1, rotation=(90,-45,0), mode=Mode.SUBTRACT)
    Box(wid, len, wid/3, mode=Mode.INTERSECT)
    outer = Box(wid+tol, len+tol, wid/6, align=(Align.CENTER,Align.CENTER,Align.MAX), mode=Mode.PRIVATE)
    walls = offset(outer, 1.2, openings=(outer.faces().sort_by(Axis.Z)[-1]), kind=Kind.INTERSECTION, mode=Mode.PRIVATE)
    walls.color = Color(0,0,1,.5)

    temp = puzzle.solids().sort_by(Axis.Y)[3].moved(Location((-2/3*wid,-len/2,0)))
    temp.orientation += (0,180,-135)

show(puzzle, walls)

# %%
stack = puzzle.solids().sort_by(Axis.Y)[0:4]
stack.append(temp)
Compound(stack)

# %%
assembly = puzzle.solids()
assembly.append(walls)
Compound(assembly)