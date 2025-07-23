# %%
from build123d import *
from ocp_vscode import *

# %%
door_w, padding, thickness = 30, 20, 20

with BuildPart() as guard:
    Box(2*door_w+padding, 2*padding+door_w, thickness)
    with BuildSketch(guard.faces().sort_by(Axis.X)[0]):
        Rectangle(thickness, door_w)
    extrude(amount=-2*door_w, mode=Mode.SUBTRACT, taper=-2)
    fillet(guard.edges().filter_by(Axis.Z), padding/4)

show(guard)