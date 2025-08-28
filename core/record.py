########################################################################
#
# Copyright (c) 2022, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

import keyboard
import pyzed.sl as sl
from datetime import datetime


def main(zed, outlet, participant_ID, sequence):

    init = sl.InitParameters()
    init.depth_mode = sl.DEPTH_MODE.NONE # Set configuration parameters for the ZED
    init.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode

    status = zed.open(init) 
    if status != sl.ERROR_CODE.SUCCESS: 
        print("Camera Open", status, "Exit program.")
        exit(1)

    start_time = datetime.now()
    outlet.push_sample([f"camera_open: {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"])

    output_svo_file = f"output_svo/{participant_ID}_seq{sequence}.svo2"
    recording_param = sl.RecordingParameters(output_svo_file, sl.SVO_COMPRESSION_MODE.H264) # Enable recording with the filename specified in argument
    err = zed.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Recording ZED : ", err)
        exit(1)

    svo_start_time = datetime.now()
    outlet.push_sample([
        f"SVO_recording_start: {svo_start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    ])

    runtime = sl.RuntimeParameters()
    print("SVO is Recording, use q key to stop.")
    frames_recorded = 0

    while True:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            frames_recorded += 1
            print("Frame count: " + str(frames_recorded), end="\r")
        
        if keyboard.is_pressed('q'):
            print("\n'q' pressed. Stopping recording.")
            break

    # Graceful exit
    zed.disable_recording()
    end_time = datetime.now()
    outlet.push_sample([
        f"SVO_recording_stop: {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    ])

    zed.close()
    outlet.push_sample([
        f"camera_close: {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    ])