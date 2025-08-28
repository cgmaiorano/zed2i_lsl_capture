# `zed2i_lsl_capture`

A repository containing the necessary code to record an svo file from the ZED 2i for post processing and stream live markers to Lab Streaming Layer.

![stability-experimental](https://img.shields.io/badge/stability-experimental-orange.svg)
[![LGPL--2.1 License](https://img.shields.io/badge/license-LGPL--2.1-blue.svg)](https://github.com/childmindresearch/mobi-motion-tracking/blob/main/LICENSE)
[![pages](https://img.shields.io/badge/api-docs-blue)](https://github.com/childmindresearch/zed2i_3d_lsl_capture)

Welcome to `zed2i_lsl_capture`, a Python Repository designed for recording data from the ZED 2i stereo camera developed by StereoLabs (https://github.com/stereolabs/) and stream live marker events via LSL (https://labstreaminglayer.readthedocs.io/info/intro.html). This repository records data, compresses it to an svo file, and streams the start and stop event triggers to LSL. The markers streamed to LSL include the camera open, SVO recording start, SVPO recording end, and camera close events.

## Supported software & devices

The package currently supports the ZED 2i and is reliant on proper installation of the `zed-sdk` (https://github.com/stereolabs/zed-sdk) and the `zed-python-api` (https://github.com/stereolabs/zed-python-api). It is also reliant on pylsl (https://labstreaminglayer.readthedocs.io/info/getting_started.html). If you want to run this data collection pipeline without LSL integration see (https://github.com/childmindresearch/zed2i_3d_capture). This package also requires VLC Media Player to be installed.

**Special Note**
    The ZED SDK is only supported on Windows devices. Please see https://www.stereolabs.com/docs#supported-platforms for full details on ZED supported platforms.
    

## Processing pipeline implementation

The main processing pipeline of the `zed2i_lsl_capture` module can be described as follows:

- **Provide participant specific arguments**: The user provides the participant ID and sequence number in the command line.
- **Initiate the camera**: The zed camera will be triggerred to open. If the camera cannot be accessed, an error will be thrown. 
- **Wait for LSL stream**: The program will wait for the user to enter "c" for continue in the terminal after the user has initiated the Motion Tracking stream in LabRecorder.
- **Recording begins**: Data collection then begins. The program will continuously collect data until the "q" key is pressed by the user when data collection is complete.
- **Export data**: The recording of the participant will be saved as a .svo2 file located in output_svo/.

## LSL Event Markers

Below is a complete list of all possible LSL event markers to be streamed dependent on various events that may occur during data collection:

- camera_open
- SVO_recording_start
- SVO_recording_end
- camera_close


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
zed2i_lsl_venv\Scripts\activate
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
uv pip install keyboard pylsl
```


## Quick start

1. Navigate to the ZED SDK directory:

```sh
cd "C:\Program Files (x86)\ZED SDK"
```

2. Clone this repository inside ZED SDK:

```sh
git clone https://github.com/childmindresearch/zed2i_lsl_capture.git
```

3. Navigate to root:

```sh
cd zed2i_lsl_capture
```


## Run participant 100 for sequence 1:

```sh
uv run main.py -p "100" -s "1"
```

