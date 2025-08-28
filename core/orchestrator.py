import pyzed.sl as sl
from pylsl import StreamInfo, StreamOutlet
from core import record

def run(participant_ID, sequence):
    print(f"Beginning Sequence {sequence}")

    zed = sl.Camera()

    # Create new stream info for lsl, stream camera_open
    info = StreamInfo("MotionTracking", "Markers", 1, 0, "string", "zed_camera")
    outlet = StreamOutlet(info)

    while True:
        key = input(
            "Press 'c' to continue after starting lsl stream in LabRecorder: "
        ).strip()
        if key == "c":
            break

    # start recording
    record.main(zed, outlet, participant_ID, sequence)

    print(
        f"ZED Data Collection for Participant: {participant_ID} Sequence: {sequence} is complete"
    )
