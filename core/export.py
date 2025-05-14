import pyzed.sl as sl
import pandas as pd
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


def save_sequence(participant_ID, sequence, dataframe):
    # Specify the file path and sheet name
    file_path = OUTPUT_DIR + f"xlsx/{participant_ID}.xlsx"
    sheet_name = f"seq{sequence}"

    # Try to load the existing file and add a new sheet
    try:
        with pd.ExcelFile(file_path) as xls:
            # Check if the sheet already exists
            if sheet_name in xls.sheet_names:
                print(f"Sheet '{sheet_name}' already exists. No new sheet created.")
                return  # Exit if the sheet already exists

        # Write to the Excel file, creating a new sheet
        with pd.ExcelWriter(file_path, engine="openpyxl", mode="a") as writer:
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Data saved to '{sheet_name}' in '{file_path}'.")
