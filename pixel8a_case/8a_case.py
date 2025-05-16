# %%
from build123d import *
from ocp_vscode import *

# %%
phone_x, phone_y, phone_z = 73, 153, 9.3
corner_r, edge_r, cut_r = 11, 3, 1
thickness = 2
usb_x, usb_y = 14, 7
speaker_span, speaker_x, speaker_y = 37, 14, 4
camera_x, camera_y, camera_offset = phone_x-edge_r, 18.4, phone_y/2-22.4
buttons_offset, buttons_x, buttons_y = phone_y/2-60, 46, 3
mic_r, mic_offset = 2, 16.5-phone_x/2
notch_x, notch_y = 36, 4
logo_scale = 30
logo = import_svg("Boston_Bruins-svg.svg")
scaled_logo = scale(logo, by=logo_scale/max(Compound(logo).bounding_box().size))

# %%
with BuildPart() as phonecase:
    Box(phone_x, phone_y, phone_z)
    fillet(phonecase.edges().filter_by(Axis.Z), corner_r)
    phonebody = fillet(phonecase.faces().filter_by(Axis.Z).edges(), edge_r)                         # make phone body
    extrude(phonecase.faces().filter_by(Axis.Z)[-1], thickness)                                     # extra extrude to make some thickness on top of shell
    offset(phonecase.part, amount=thickness, openings=phonecase.faces().filter_by(Axis.Z)[0])      # make case shell
    extrude(phonebody.faces().filter_by(Axis.Z)[-1], thickness*2, taper=-60, mode=Mode.SUBTRACT)    # taper cut top opening of case
    fillet(phonecase.edges().sort_by(Axis.Z)[-1], radius=2)
    with Locations((0,phone_y/2-edge_r,phone_z/2)) as speaker_notch:
        Box(notch_x, notch_y, thickness*2, mode=Mode.SUBTRACT)
    
    with BuildSketch(Plane(phonecase.faces().sort_by(Axis.Y)[0], x_dir=(1,0,0))) as bottom:
        RectangleRounded(usb_x, usb_y, cut_r)
        with GridLocations(speaker_span, 0, 2, 1) as speakers:
            RectangleRounded(speaker_x, speaker_y, cut_r)
    extrude(amount=-10, mode=Mode.SUBTRACT)                                                         # cut bottom holes
    temp_edges = phonecase.edges(Select.LAST).filter_by(Axis.X).group_by(Axis.Y)[1:3]
    fillet(temp_edges, radius=.8)
    
    with BuildSketch(Plane(phonecase.faces().sort_by(Axis.Z)[0], x_dir=(-1,0,0))) as back:
        with Locations((0,camera_offset)) as cameracut:
            Rectangle(camera_x, camera_y)
    extrude(amount=-thickness*2, mode=Mode.SUBTRACT)                                                # cut camera window
        
    with BuildSketch(Plane(origin=(phone_x/2-1,buttons_offset,0), x_dir=(0,1,0),z_dir=(1,0,0))) as buttons:
        RectangleRounded(buttons_x, buttons_y, cut_r)
    extrude(amount=10, taper=-60, mode=Mode.SUBTRACT)                                               # cut buttons
    button_round = phonecase.edges(Select.LAST).filter_by(Axis.Y).group_by(Axis.X)[-2]
    fillet(button_round, radius=1.2)
    
    with BuildSketch(phonecase.faces().sort_by(Axis.Y)[-1]) as top:
        with Locations((1,mic_offset)) as mic_loc:
            Circle(mic_r)
    extrude(amount=-10, mode=Mode.SUBTRACT)                                                         # cut mic hole
    
    with BuildSketch(Plane(origin=(0,-phone_y/4,phone_z/2+thickness))) as grip_plane:
        with GridLocations(phone_x+2*thickness, 5, 2, 10) as grips:
            Rectangle(thickness/2, thickness/8)
    extrude(amount=-(phone_z+2*thickness), mode=Mode.SUBTRACT)                                      # cut grips
    fillet([phonecase.edges(Select.LAST).group_by(Axis.X)[i] for i in [0,-1]], thickness/4.01)      # round grips

    with BuildSketch(Plane(origin=(0,-phone_y/4,-phone_z/2), x_dir=(-1,0,0), z_dir=(0,0,-1))) as logo_plane:
        add(scaled_logo.moved(Location(-scaled_logo.center(CenterOf.BOUNDING_BOX))))
    extrude(amount=thickness, mode=Mode.SUBTRACT)                                                   # cut logo

show(phonecase)
# %%
