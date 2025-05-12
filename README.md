# `zed2i_3d_lsl_capture`

A repository containing the necessary code to record motion tracking data from the ZED 2i with or without a sitmulus and stream live markers to Lab Streaming Layer.

![stability-experimental](https://img.shields.io/badge/stability-experimental-orange.svg)
[![LGPL--2.1 License](https://img.shields.io/badge/license-LGPL--2.1-blue.svg)](https://github.com/childmindresearch/mobi-motion-tracking/blob/main/LICENSE)
[![pages](https://img.shields.io/badge/api-docs-blue)](https://github.com/childmindresearch/zed2i_3d_lsl_capture)

Welcome to `zed2i_3d_lsl_capture`, a Python Repository designed for recording 3D motion tracking data from the ZED 2i stereo camera developed by StereoLabs (https://github.com/stereolabs/) and stream live marker events via LSL (https://labstreaminglayer.readthedocs.io/info/intro.html). This repository performs real time body tracking on a single person, collects the data, and saves it to an .xlsx file in the acceptable format for `mobi_motion_tracking`. The markers streamed to LSL include the camera open, stimulus start, stimulus end, and camera close events. This repository can be run with or without a live stimulus. 

## Supported software & devices

The package currently supports the ZED 2i and is reliant on proper installation of the `zed-sdk` (https://github.com/stereolabs/zed-sdk) and the `zed-python-api` (https://github.com/stereolabs/zed-python-api). It is also reliant on pylsl (https://labstreaminglayer.readthedocs.io/info/getting_started.html). If you want to run this data collection pipeline without LSL integration see (https://github.com/childmindresearch/zed2i_3d_capture).

**Special Note**
    The ZED SDK is only supported on Windows devices. Please see https://www.stereolabs.com/docs#supported-platforms for full details on ZED supported platforms.
    

## Processing pipeline implementation

The main processing pipeline of the `zed2i_3d_lsl_capture` module can be described as follows:

- **Determine sitmulus presence**: The user provides the participant ID and sequence number in the command line. A path to a stimulus video may also be provided. If a video path is provided the cli will call with_stimulus_orchestrator.py, otherwise without_stimulus_orchestrator.py will be called.
- **Initiate the camera**: The zed camera will be triggerred to open first in both orchestrators. If the camera cannot be accessed, an error will be thrown. 
- **Begin body tracking**: Skeletal joints will begin being captured at 30 fps. Both pathways can be manually interrupted by pressing the 'q' key.
    - **Present stimulus**: If a video path is provided, the stimulus will be displayed.
- **Body tracking ends**: If a stimulus is being displayed, body tracking will automatically complete at the end of the stimulus video. If there is no stimulus, body tracking can be concluded by pressing the 'd' key.
    - **Trim data**: If a stimulus was played, the body tracking data will automatically by trimmed from both the start and end to be time-synced with the stimulus. If there was no sitmulus, the full data collection session will be returned.
- **Export data**: The live recording of the participant will be saved as a .svo2 file located in collected_data/svo. Joint data will be saved in an .xlsx file located in collected_data/xlsx.

## LSL Event Markers

Below is a complete list of all possible LSL event markers to be streamed dependent on various events that may occur during data collection:

- camera_open
- SVO_recording_start
- thread_stop_event
- quit_key_press
- body_tracking_frame_number
- failed_zed_connection
- camera_close
- VLC_window_failure
- stimulus_start
- stimulus_end


## Installation

1. Install the ZED SDK from StereoLabs. Installation documentation can be found here: https://www.stereolabs.com/docs/installation/windows 
    - *** When prompted to select the folder location for the ZED SDK, you can use the default path ("C:\Program Files (x86)\ZED SDK") or change it based on your preference. However, this readme is based on the default path.

2. Grant administrative permissions to the ZED SDK. 
    - Navigate to the ZED SDK folder in "C:\Program Files (x86)" in file explorer
    - Right click on the folder -> select properties -> go to security tab -> click edit
    - Select the correct user to grant access to and tick the box next to full control under "Allow" 
    - Click apply and Ok
    - Restart your terminal

3. Create a virtual environment. Any environment management tool can be used, but the following steps describe setting up a uv venv:

create a virtual environment named zed2i_lsl_venv
```sh
uv venv zed2i_lsl_venv
```
 activate the environment
```sh
zed2i_lsl_venv\Source\activate
```

4. Install the ZED Python API. Installation support documentation can be found here on the Stereolabs website (https://www.stereolabs.com/docs/app-development/python/install). However, follow our steps below for proper CMI/MoBI-specific API installation:

ensure pip is installed 
```sh
python -m ensurepip
```
install API dependencies
```sh
uv pip install cython numpy opencv-python requests
```
run get_python_api.py
```sh
cd "C:\Program Files (x86)\ZED SDK"
```
```sh
uv run get_python_api.py
```


5. Install repository-dependent packages

```sh
uv pip install pandas pygetwindow pylsl screeninfo
```


## Quick start

Navigate to the ZED SDK directory:

```sh
cd "C:\Program Files (x86)\ZED SDK"
```

Clone this repository inside ZED SDK:

```sh
git clone https://github.com/childmindresearch/zed2i_3d_lsl_capture.git
```

Navigate to root:

```sh
cd zed2i_3d_lsl_capture
```

**Special Note**
    
    Prior to running the commands below: 
        - create directories to store collected data: `collected_data\xlsx` and `collected_data\svo`
        - rename your source_id with the name of your zed device in `core\with_stimulus_orchestrator.py` line 21 and in `core\without_stimulus_orchestrator.py` line 18.
        - navigate to `core\with_stimulus_orchestrator.py` and replace `vlc_path` with the correct path to your vlc player executable.


#### Run participant 100 for sequence 1 WITHOUT STIMULUS:

```sh
python -m main -p "100" -s "1"
```

#### Run participant 100 for sequence 1 WITH STIMULUS:

```sh
python -m main -p "100" -s "1" --video "C:\path\to\stimulus\video.avi"
```

## Post-Processing

If there was a stimulus presented, the raw xlsx files can be trimmed by the stimulus_start and stimulus_end times saved in your xdf file from LSL. The trimmed xlsx files are then prepared to be compared to a "gold standard" through `mobi_motion_tracking` https://github.com/childmindresearch/mobi-motion-tracking. 
