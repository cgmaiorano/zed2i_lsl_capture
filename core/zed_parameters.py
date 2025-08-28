import pyzed.sl as sl

from settings import DEPTH_MODE


def initialize_zed_parameters(zed):
    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
    init_params.camera_fps = 30
    init_params.coordinate_units = sl.UNIT.METER  # Set coordinate units
    init_params.depth_mode = getattr(sl.DEPTH_MODE, DEPTH_MODE)
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open", err, "Exit program.")
        exit(1)

