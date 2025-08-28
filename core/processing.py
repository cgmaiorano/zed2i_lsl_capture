import cv2
import pyzed.sl as sl
from datetime import datetime


def processing(zed, lsl_outlet):

    image = sl.Mat()
    runtime = sl.RuntimeParameters()

    while True:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.LEFT)
            img_np = image.get_data()
            if img_np is not None and img_np.size > 0:
                cv2.imshow("ZED", img_np)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("Invalid image")
        else:
            print("Grab failed")

    # Stop Recording
    zed.disable_recording()
    end_time = datetime.now()
    lsl_outlet.push_sample([
        f"SVO_recording_stop: {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    ])

    # Close viewer
    zed.close()
    end_time = datetime.now()
    lsl_outlet.push_sample([
        f"camera_close: {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    ])

    cv2.destroyAllWindows()
