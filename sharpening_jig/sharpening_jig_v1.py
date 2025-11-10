# %%
from build123d import *
from ocp_vscode import *
import copy

# %%
axle_r, axle_l = 5/2, 100
gap = 0.5
wheel_r, wheel_l, wheel_t = 10/2, 20, 1
thickness = 5

# %%
with BuildPart(Plane.YZ) as axle:
    Cylinder(axle_r, axle_l)
    RigidJoint("axle", joint_location=Location(Plane.YZ))

show(axle, reset_camera=Camera.KEEP, render_joints=True)

# %%
with BuildPart() as wheel:
    with BuildSketch(Plane.YZ) as wheel_profile:
        Circle(wheel_r - wheel_t)
        with PolarLocations(wheel_r - wheel_t, 8):
            Rectangle(2 * wheel_t, 2 * wheel_t)
        Circle(wheel_r, mode=Mode.INTERSECT)
        Circle(axle_r + gap, mode=Mode.SUBTRACT)
    sweep(wheel_profile.sketch.face(), Line((0, 0, 0), (wheel_l/2, 0, 0)), binormal=Helix(wheel_l, wheel_l/2, wheel_r, direction=(1, 0, 0)))
    mirror(wheel.part, about=Plane.YZ)
    RigidJoint("wheel", joint_location=Location(Plane.YZ))

show(wheel, reset_camera=Camera.KEEP, render_joints=True)

# %%
with BuildPart() as body:
    with BuildSketch(Plane.YZ) as body_profile:
        with BuildLine() as body_outline:
            l0 = JernArc((0, -(wheel_r-wheel_t)), (1, 0), (wheel_r-wheel_t), 60)
            l1 = PolarLine(l0@1, 1.5 * wheel_r + thickness + gap, direction=l0%1, length_mode=LengthMode.VERTICAL)
            l2 = Line(l1@1, (0, (l1@1).Y))
            l3 = Line(l2@1, l0@0)
        make_face()
        mirror(about=Plane.YZ)
        Circle(axle_r+gap, mode=Mode.SUBTRACT)
    extrude(amount=axle_l/2, both=True)
    with Locations((wheel_l, 0, 0), (-wheel_l, 0, 0)) as wheel_locs:
        Box(wheel_l+2*gap, 4*(wheel_r+gap), 2*(wheel_r+2*gap), mode=Mode.SUBTRACT)
        # add(wheel.part)
    RigidJoint("axle", joint_location=Location(Plane.YZ))
    RigidJoint("wheel_1", joint_location=Location(wheel_locs.locations[0].position, (0,90,0)))
    RigidJoint("wheel_2", joint_location=Location(wheel_locs.locations[1].position, (0,90,0)))
    LinearJoint("grips", axis=Axis(body.faces().sort_by(Axis.Z)[-1].center(), (1, 0, 0)), linear_range=(-axle_l/2, axle_l/2))

show(body, reset_camera=Camera.KEEP, render_joints=True)

# %%
with BuildPart() as grips:
    with BuildSketch(Plane.YZ) as grips_profile:
        Rectangle(body.part.bounding_box().size.Y/2 + (gap + thickness), 30, align=(Align.MIN, Align.MIN))
        chamfer(grips_profile.vertices().group_by(Axis.Y)[0], thickness, angle=60)
        mirror(about=Plane.YZ)
        with BuildLine() as grips_outline:
            l0 = Line((0,0), (0, thickness+gap), mode=Mode.PRIVATE)
            l1 = PolarLine(l0@1, body.part.bounding_box().size.Y/2 + gap/2, direction=(1, 0, 0))
            l2 = PolarLine(l1@1, -(thickness+gap), 60, length_mode=LengthMode.VERTICAL)
            l3 = Line(l2@1, l0@0)
            mirror(grips_outline.edges(), about=Plane.YZ)
        make_face(mode=Mode.SUBTRACT)
    extrude(amount=2 * thickness, both=True)
    with BuildSketch(Plane.XZ) as cut_profile:
        with BuildLine() as cut_outline:
            l0 = Line((0,0), (0,thickness+gap))
            l1 = PolarLine(l0@1, 2 * thickness, -60, length_mode=LengthMode.VERTICAL)
            l2 = Line(l1@1, ((l1@1).X, 30))
            l3 = Line(l2@1, (-2*thickness, (l2@1).Y))
            l4 = Line(l3@1, (-2*thickness, 0))
            l5 = Line(l4@1, l0@0)
        make_face()
    extrude(amount=body.part.bounding_box().size.Y, both=True, mode=Mode.SUBTRACT)
    # with Locations(-grips.faces().sort_by(Axis.X)[0].offset(-grips.part.bounding_box().size.X)):
    #     CounterBoreHole(.19*IN/2 + gap/2, 10/2, 2*thickness)
    RigidJoint("grip", joint_location=Location((0, 0, thickness + gap*.75)))

show(grips, reset_camera=Camera.KEEP, render_joints=True)

# %%
wheel_1 = wheel.part
wheel_2 = copy.copy(wheel_1)
grip_1 = grips.part

body.joints["axle"].connect_to(axle.part.joints["axle"])
body.joints["wheel_1"].connect_to(wheel_1.joints["wheel"])
body.joints["wheel_2"].connect_to(wheel_2.joints["wheel"])
body.joints["grips"].connect_to(grip_1.joints["grip"], position=40)
grip_2 = mirror(grip_1, about=Plane.YZ)

show(axle, wheel_1, wheel_2, body, grip_1, grip_2, reset_camera=Camera.KEEP, render_joints=True)

# %%
