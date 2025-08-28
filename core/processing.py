import cv2
import pyzed.sl as sl

# import numpy as np
from datetime import datetime

from core import zed_parameters
# from viewers import tracking_viewer


def body_tracking(zed, lsl_outlet):
    display_resolution, image_scale = zed_parameters.display_utilities(zed)

    # Create objects filled in the main loop
    image = sl.Mat()
    key = ""

    # Start body tracking
    print("Press 'q' to QUIT.")

    while True:  # Infinite loop
        key = cv2.waitKey(1) & 0xFF  # Non-blocking key press check

        if key == ord("q"):
            print("You pressed 'q', quitting...")
            key_press = datetime.now()
            lsl_outlet.push_sample([
                f"quit_key_press: {key_press.strftime('%Y-%m-%d %H:%M:%S.%f')}"
            ])
            break

        # Grab a frame
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            # Display frame
            zed.retrieve_image(image, sl.VIEW.LEFT, sl.MEM.CPU, display_resolution)
            image_left_ocv = image.get_data()
            # tracking_viewer.render_2D(
            #     image_left_ocv,
            #     image_scale,
            #     bodies.body_list,
            #     body_param.enable_tracking,
            #     body_param.body_format,
            # )
            cv2.imshow("ZED | 2D View", image_left_ocv)
            cv2.moveWindow("ZED | 2D View", 100, 100)

        # Zed connection failed
        elif zed.grab() != sl.ERROR_CODE.SUCCESS:
            zed_err = datetime.now()
            lsl_outlet.push_sample([
                f"failed_zed_connection: {zed_err.strftime('%Y-%m-%d %H:%M:%S.%f')}"
            ])
            print("Failed ZED connection")
            break

    # Close the viewer
    zed.disable_body_tracking()
    zed.disable_positional_tracking()
    zed.close()

    end_time = datetime.now()
    lsl_outlet.push_sample([
        f"camera_close: {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    ])

    cv2.destroyAllWindows()
