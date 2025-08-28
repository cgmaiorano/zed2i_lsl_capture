import cv2
import numpy as np
import pyzed.sl as sl
from datetime import datetime



def processing(zed, lsl_outlet):
    
    # Create objects filled in the main loop
    image = sl.Mat()
    key = ""

    # Start 
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
            zed.retrieve_image(image, sl.VIEW.LEFT)
            img_zed = image.get_data().copy()
            img_np = np.array(img_zed, copy=True)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)
            if img_np is not None and img_np.size > 0:
                cv2.imshow("ZED", img_bgr)

        # Zed connection failed
        elif zed.grab() != sl.ERROR_CODE.SUCCESS:
            zed_err = datetime.now()
            lsl_outlet.push_sample([
                f"failed_zed_connection: {zed_err.strftime('%Y-%m-%d %H:%M:%S.%f')}"
            ])
            print("Failed ZED connection")
            break
    
    # Stop Recording
    zed.disable_recording()
    end_time = datetime.now()
    lsl_outlet.push_sample([
        f"recording_stop: {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    ])

    # Close viewer
    zed.close()
    end_time = datetime.now()
    lsl_outlet.push_sample([
        f"camera_close: {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    ])

    cv2.destroyAllWindows()
