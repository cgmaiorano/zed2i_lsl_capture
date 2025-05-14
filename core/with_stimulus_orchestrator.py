import threading

from datetime import datetime
from pylsl import StreamInfo, StreamOutlet

from core import zed_parameters
from core import export

from with_stimulus import processing
from with_stimulus import play_stimulus

from with_stimulus.sharedstate import SharedState

from settings import VLC_EXE, ZED_DEVICE


def run(participant_ID, sequence, video):
    print(f"Beginning Sequence {sequence}")

    sharedstate = SharedState()

    # Create new stream info for lsl, stream camera_open, change source_id from "zed2i-harlem" to appropriate device, ex: "zed2i-midtown"
    info = StreamInfo("MotionTracking", "Markers", 1, 0, "string", ZED_DEVICE)
    outlet = StreamOutlet(info)

    while True:
        key = input(
            "Press 'c' to continue after starting lsl stream in LabRecorder: "
        ).strip()
        if key == "c":
            break

    # Create camera object, initialize camera parameters
    zed_parameters.initialize_zed_parameters(sharedstate.zed)

    start_time = datetime.now()
    outlet.push_sample([f"camera_open: {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"])

    # start recording svo file
    export.record_svo(participant_ID, sequence, sharedstate.zed)

    # Path to the VLC player executable
    vlc_path = VLC_EXE

    # Threads
    body_tracking_thread = threading.Thread(
        target=processing.body_tracking, args=(sharedstate, outlet)
    )
    video_thread = threading.Thread(
        target=play_stimulus.play_video,
        args=(vlc_path, str(video), sharedstate, outlet),
    )

    body_tracking_thread.start()
    video_thread.start()

    # Wait for the threads to finish
    video_thread.join()
    body_tracking_thread.join()

    if sharedstate.quit:
        print(
            f"Manual Quit... ZED Body tracking for Participant: {participant_ID} Sequence: {sequence} INCOMPLETED."
        )
        return

    # save data
    export.save_sequence(participant_ID, sequence, sharedstate.ordered_df)

    print(
        f"ZED Body tracking for Participant: {participant_ID} Sequence: {sequence} is complete"
    )
