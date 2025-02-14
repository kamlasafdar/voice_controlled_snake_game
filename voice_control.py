import sounddevice as sd
import numpy as np
import queue
import tempfile
import wave
import os
import time
import string
from faster_whisper import WhisperModel

# Audio Settings
SAMPLE_RATE = 16000  # Required for Whisper
DURATION = 3  # Record for 3 seconds
CHANNELS = 1  # Mono
BLOCKSIZE = 1024
audio_queue = queue.Queue()

# Load Whisper Model (English Only)
model = WhisperModel("base", device="cpu", compute_type="int8")  # Use "cuda" if available

# Global variable for the last valid command
last_valid_command = "right"

def audio_callback(indata, frames, time, status):
    """Collects audio data in real-time."""
    if status:
        print(f"⚠️ Warning: {status}")
    audio_queue.put(indata.copy())

def start_listening(callback, game):
    print("✅ Microphone is listening... (English mode)")

    try:
        while game.running:
            command = listen_for_command()
            if command:
                print(f"🎙️ Command received: {command}")
                callback(command)
            time.sleep(0.1)
    except Exception as e:
        print(f"❌ Voice recognition error: {e}")

def listen_for_command():
    global last_valid_command
    print("🎤 Speak now (English)...")

    audio_buffer = []
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback, blocksize=BLOCKSIZE):
        for _ in range(int(SAMPLE_RATE * DURATION / BLOCKSIZE)):
            try:
                data = audio_queue.get(timeout=DURATION)
                audio_buffer.append(data)
            except queue.Empty:
                print("⚠️ No audio detected!")
                return last_valid_command

    print("🎙️ Processing audio with Whisper...")

    # Convert to numpy array and save as WAV
    audio_data = np.concatenate(audio_buffer, axis=0)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        with wave.open(tmpfile.name, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
        temp_audio_path = tmpfile.name

    # Transcribe using Whisper (English only)
    segments, _ = model.transcribe(temp_audio_path, language="en")
    os.remove(temp_audio_path)

    # Extract and clean the transcribed text
    command = " ".join(segment.text.strip().lower() for segment in segments)
    command = command.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation

    print(f"🔍 Whisper Output (Cleaned): {command}")

    # Check if the command is valid
    valid_commands = ["up", "down", "left", "right"]
    if command in valid_commands:
        print(f"✅ Recognized Command: {command}")
        last_valid_command = command
        return command
    else:
        print(f"❌ Unrecognized Command: {command}")
        return last_valid_command
