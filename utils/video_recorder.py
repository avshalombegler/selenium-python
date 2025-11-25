"""
Module for recording test videos using Selenium WebDriver and ffmpeg.
Supports parallel execution, headless mode, and CI environments.
Requires: ffmpeg, filelock, selenium, pytest-xdist.
"""

from __future__ import annotations

import base64
import logging
import subprocess
import threading
import time
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from selenium import webdriver

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver

logger = logging.getLogger(__name__)

FPS = 15
INTERVAL = 1.0 / FPS
MIN_FRAME_SIZE = 512
MAX_FRAMES = 2000
JPEG_QUALITY = 80


def start_video_recording(
    driver: WebDriver, test_name: str, worker_id: str = "local"
) -> tuple[Callable[[], None], str]:
    """
    Starts background video recording for a test.
    Returns: (stop_func, video_path)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = Path("tests_recordings") / worker_id / f"{test_name}_{timestamp}"
    frames_dir = base_dir / "frames"
    video_path = base_dir / f"{test_name}_{timestamp}.mp4"

    frames_dir.mkdir(parents=True, exist_ok=True)

    stop_event = threading.Event()

    def capture_loop() -> None:
        logger.info("Capture loop started for Firefox.")
        idx = 0
        while not stop_event.is_set():
            try:
                if not getattr(driver, "session_id", None):
                    break

                if isinstance(driver, webdriver.Chrome):
                    res = driver.execute_cdp_cmd("Page.captureScreenshot", {"format": "png", "fromSurface": True})
                    data = res.get("data")
                    if data:
                        raw = base64.b64decode(data)
                else:
                    logger.info("Using Firefox screenshot method.")
                    raw = driver.get_screenshot_as_png()
                    # logger.info(f"Raw screenshot size: {len(raw)} bytes.")

                if len(raw) > MIN_FRAME_SIZE and (not MAX_FRAMES or idx < MAX_FRAMES):
                    frame_file = frames_dir / f"frame_{idx:06d}.png"
                    frame_file.write_bytes(raw)
                    # logger.info(f"Saved frame {idx}: {frame_file}")
                    idx += 1
                else:
                    logger.debug(f"Frame {idx} skipped (size: {len(raw)})")
            except Exception as e:
                logger.error(f"Capture error: {e}")
                if "invalid session id" in str(e).lower():
                    break
            time.sleep(INTERVAL)

    thread = threading.Thread(target=capture_loop, daemon=True)
    thread.start()

    def stop_and_assemble() -> None:
        logger.info("Stopping video recording and assembling.")
        stop_event.set()
        thread.join(timeout=5)
        logger.info(f"Thread joined. Frames dir: {frames_dir}")

        frame_files = sorted(frames_dir.glob("frame_*.png"))
        valid_frames = [f for f in frame_files if f.stat().st_size > MIN_FRAME_SIZE]
        logger.info(f"Found {len(valid_frames)} valid frames.")

        if not valid_frames:
            logger.warning(f"No valid frames for {test_name}")
            return

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(frames_dir / "frame_%06d.png"),
            "-vf",
            "scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(video_path),
        ]

        try:
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
            logger.info(f"Video created: {video_path}")
        except Exception as e:
            logger.error(f"ffmpeg failed: {e}")

    return stop_and_assemble, str(video_path)
