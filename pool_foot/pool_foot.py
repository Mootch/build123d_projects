# %%
from build123d import *
from ocp_vscode import *

# %%
with BuildPart() as foot:
    Cylinder(64/2, 4.5, align=(Align.CENTER, Align.CENTER, Align.MAX))
    Cylinder(30/2, 15, align=(Align.CENTER, Align.CENTER, Align.MIN))
    Cylinder(26/2, 15, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
    with PolarLocations(26/2, 8):
        Box(1, 2, 12, align=(Align.CENTER, Align.CENTER, Align.MIN))
    chamfer(foot.edges(Select.LAST).group_by(Axis.Z)[-2].filter_by(lambda x: x.distance_to((0,0,12))<12.51), 11, 0.45)
    with PolarLocations(30/2-.5, 4):
        Wedge(13, 13, 2, 0, 0, 0, 2, rotation=(90,0,0), align=(Align.MIN, Align.MIN, Align.CENTER))
    Cylinder(5/2, 5, mode=Mode.SUBTRACT, align=(Align.CENTER, Align.CENTER, Align.MAX))

show(foot, reset_camera=Camera.KEEP)

# %%
with BuildSketch() as drawing:
    border = TechnicalDrawing(designed_by="Andy",
                              title="POOL FOOT",
                              sub_title="")
    page_size = border.bounding_box().size

    vis, hid = foot.part.project_to_viewport((10, -10, 10))
    with BuildLine() as part_view:
        with Locations(0.25*page_size):
            add(vis)
    
    vis, hid = foot.part.project_to_viewport((0,0,1000), (0,1,0))
    with BuildLine() as top_view:
        with Locations((-0.2*page_size.X, 0.25*page_size.Y)):
            add(vis)

    vis, hid = foot.part.project_to_viewport((0,-1000,0), (0,0,1))
    with BuildLine() as front_view:
        with Locations((-0.2*page_size.X, -0.1*page_size.Y)):
            add(vis)
          
    vis, hid = foot.part.split(Plane.XZ, Keep.BOTTOM).project_to_viewport((0,-1000,0), (0,0,1))
    with BuildLine() as section_view:
        with Locations((0.2*page_size.X, -0.1*page_size.Y)):
            add(vis)

show(drawing, part_view, top_view, front_view, section_view)