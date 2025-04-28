import time
import pyzed.sl as sl

from datetime import datetime
from pylsl import StreamInfo, StreamOutlet

from core import zed_parameters
from core import export

from without_stimulus import processing


def run(participant_ID, sequence):
    print(f"Beginning CAMI Protocol Sequence {sequence}")

    zed = sl.Camera()

    # Create camera object, initialize camera parameters
    zed_parameters.initialize_zed_parameters(zed)
    start_time = datetime.now()

    # Create new stream info for lsl, stream camera_open, change source_id from "zed2i-harlem" to appropriate device, ex: "zed2i-midtown"
    info = StreamInfo("MotionTracking", "Markers", 1, 0, "string", "zed2i-harlem")
    outlet = StreamOutlet(info)
    outlet.push_sample([f"camera_open: {start_time}"])

    # start recording svo file
    export.record_svo(participant_ID, sequence, zed)

    # main processing
    ordered_df = processing.body_tracking(zed, outlet)

    if ordered_df is None:
        print(
            f"Manual Quit... ZED Body tracking for Participant: {participant_ID} Sequence: {sequence} INCOMPLETED."
        )
        return

    # save data
    export.save_sequence(participant_ID, sequence, ordered_df)
