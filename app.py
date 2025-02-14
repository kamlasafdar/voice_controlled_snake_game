import streamlit as st
import subprocess
import sys

# Install pygame during runtime
subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])


st.title("🎮 Voice-Controlled Snake Game 🐍")

if st.button("Start Game 🎮"):
    st.write(f"Launching the game...")
    subprocess.Popen(["python", "game_runner.py"])