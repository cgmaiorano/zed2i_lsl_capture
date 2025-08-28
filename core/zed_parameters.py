import pyzed.sl as sl

def initialize_zed_parameters(zed):
    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720
    init_params.depth_mode = sl.DEPTH_MODE.NONE

    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print("Camera open failed:", status)
        exit()


