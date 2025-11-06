from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://the-internet.herokuapp.com/")
BROWSER = os.getenv("BROWSER", "chrome")
SHORT_TIMEOUT = int(os.getenv("SHORT_TIMEOUT", 3))
LONG_TIMEOUT = int(os.getenv("LONG_TIMEOUT", 10))
VIDEO_RECORDING = os.getenv("VIDEO_RECORDING", "False").lower() == "true"
HEADLESS = os.getenv("HEADLESS", "True").lower() == "true"
MAXIMIZED = os.getenv("MAXIMIZED", "False").lower() == "true"
USERNAME = os.getenv("USERNAME", "tomsmith")
PASSWORD = os.getenv("PASSWORD", "SuperSecretPassword!")
