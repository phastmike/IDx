"""
Constants and configuration
"""

# Application

APP_NAME = "Pico IDx"
APP_VERSION = "1.1"
APP_AUTHOR = "CT1ENQ"
APP_YEAR = 2022

# Temperature
# Announces temperature as audio
# when above this threshold

TEMPERATURE_THRESHOLD = 35.0

# Audio

AUDIO_PATH = "audio/"
AUDIO_ID_FILE = "main_id.wav"
AUDIO_ANN_FILE = "main_an.wav"

# Sampling rate

SAMPLING_PERIOD_SEC = 0.05
SAMPLING_PERIOD_MS = int(SAMPLING_PERIOD_SEC * 1000)
SAMPLING_FREQ = 1.0 / (SAMPLING_PERIOD_SEC)
USAGE_CHECK_DURATION = 8

# ID Interval

SLEEP_MIN = 10
