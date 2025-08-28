import pyzed.sl as sl
from datetime import datetime

from settings import OUTPUT_DIR


def record_svo(participant_ID, sequence, zed, lsl_outlet):
    output_svo_file = OUTPUT_DIR + f"svo/{participant_ID}_seq{sequence}.svo2"
    recording_param = sl.RecordingParameters(
        output_svo_file, sl.SVO_COMPRESSION_MODE.H265
    )  # Enable recording with the filename specified in argument

    err = zed.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Recording ZED : ", err)
        exit(1)

    # Start Recording
    svo_start_time = datetime.now()
    lsl_outlet.push_sample([
        f"SVO_recording_start: {svo_start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    ])

    sl.RuntimeParameters()
