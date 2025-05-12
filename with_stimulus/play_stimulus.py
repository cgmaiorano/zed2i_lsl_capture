import time
import subprocess
from datetime import datetime


def play_video(vlc_path, video_path, sharedstate, lsl_outlet):
    sharedstate.wait_for_thread.wait()

    DETACHED_PROCESS = 0x00000008
    process = subprocess.Popen(
        [
            vlc_path,
            video_path,
            "--play-and-exit",
            "--no-video-title-show",
            "--no-video-deco",
            "--fullscreen",
            "--quiet",
            "--directx-device=\\.\DISPLAY2",  # Windows-specific
        ],
        creationflags=DETACHED_PROCESS,
    )

    # Optionally: Wait until process starts running a bit
    time.sleep(2)

    start_time = datetime.now()
    lsl_outlet.push_sample([
        f"stimulus_start: {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    ])

    # Monitor process and shared stop_event
    try:
        while process.poll() is None:  # While VLC is still running
            if sharedstate.stop_event.is_set():
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
                break
            time.sleep(0.1)  # avoid tight loop
    except Exception as e:
        vlc_err = datetime.now()
        lsl_outlet.push_sample([
            f"VLC_window_failure: {vlc_err.strftime('%Y-%m-%d %H:%M:%S.%f')}"
        ])
        print(f"Error monitoring VLC process: {e}")

    end_time = datetime.now()
    lsl_outlet.push_sample([
        f"stimulus_end: {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    ])

    sharedstate.stop_event.set()
