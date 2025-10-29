"""
Module for recording test videos using Selenium WebDriver and ffmpeg.
Supports parallel execution, headless mode, and CI environments.
Requires: ffmpeg, filelock, selenium, pytest-xdist.
"""

import threading
import time
import base64
import subprocess
from datetime import datetime
from pathlib import Path
from filelock import FileLock
import allure
import logging

logger = logging.getLogger(__name__)

FPS = 15
INTERVAL = 1.0 / FPS
MIN_FRAME_SIZE = 512
MAX_FRAMES = 2000
JPEG_QUALITY = 80


def start_video_recording(driver, test_name, worker_id="local"):
    """
    Starts background video recording for a test.
    Returns: (stop_func, video_path)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = Path("tests_recordings") / worker_id / f"{test_name}_{timestamp}"
    frames_dir = base_dir / "frames"
    video_path = base_dir / f"{test_name}_{timestamp}.mp4"
    lock_file = base_dir / f"{worker_id}.lock"

    frames_dir.mkdir(parents=True, exist_ok=True)

    stop_event = threading.Event()

    def capture_loop():
        idx = 0
        while not stop_event.is_set():
            try:
                if not getattr(driver, "session_id", None):
                    break
                res = driver.execute_cdp_cmd(
                    "Page.captureScreenshot", {"format": "jpeg", "quality": JPEG_QUALITY, "fromSurface": True}
                )
                data = res.get("data")
                if data:
                    raw = base64.b64decode(data)
                    if len(raw) > MIN_FRAME_SIZE and (not MAX_FRAMES or idx < MAX_FRAMES):
                        frame_file = frames_dir / f"frame_{idx:06d}.jpg"
                        frame_file.write_bytes(raw)
                        idx += 1
            except Exception as e:
                if "invalid session id" in str(e).lower():
                    break
                logger.debug("Capture error: %s", e)
            time.sleep(INTERVAL)

    thread = threading.Thread(target=capture_loop, daemon=True)
    thread.start()

    def stop_and_assemble():
        stop_event.set()
        thread.join(timeout=5)

        frame_files = sorted(frames_dir.glob("frame_*.jpg"))
        valid_frames = [f for f in frame_files if f.stat().st_size > MIN_FRAME_SIZE]

        if not valid_frames:
            logger.warning(f"No valid frames for {test_name}")
            return

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(frames_dir / "frame_%06d.jpg"),
            "-vf",
            "scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(video_path),
        ]

        try:
            proc = subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
            logger.info(f"Video created: {video_path}")
            with FileLock(lock_file):
                allure.attach.file(
                    str(video_path), name=f"Recording - {test_name}", attachment_type=allure.attachment_type.MP4
                )
        except Exception as e:
            logger.error(f"ffmpeg failed: {e}")

    return stop_and_assemble, str(video_path)
