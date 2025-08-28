import pyzed.sl as sl
import cv2

zed = sl.Camera()
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD720
init_params.depth_mode = sl.DEPTH_MODE.NONE

status = zed.open(init_params)
if status != sl.ERROR_CODE.SUCCESS:
    print("Camera open failed:", status)
    exit()

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

zed.close()
cv2.destroyAllWindows()
