# harmonix_music_player.py
import streamlit as st
import os

# ---------------- SETTINGS ----------------
APP_NAME = "Harmonix — Music Player"
MUSIC_FOLDER = "music_files"
ALBUM_ART = "./assests/album_art.jpg"  # Put your image in same folder
os.makedirs(MUSIC_FOLDER, exist_ok=True)

# --------------- PAGE CONFIG ---------------
st.set_page_config(page_title=APP_NAME, page_icon="🎵", layout="centered")
st.markdown(
    f"<h1 style='text-align: center; color: #ff4b4b;'>{APP_NAME}</h1>",
    unsafe_allow_html=True
)

# Display album art
if os.path.exists(ALBUM_ART):
    st.image(ALBUM_ART, width=700, caption="🎼 Harmonix Player")
else:
    st.image("./assests/logo.png", width=300, caption="🎼 Harmonix Player")

st.write("Upload songs below to get started 🎧")

# --------------- UPLOAD SONGS ---------------
uploaded_files = st.file_uploader(
    "Upload MP3 Songs", type="mp3", accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        with open(os.path.join(MUSIC_FOLDER, file.name), "wb") as f:
            f.write(file.getbuffer())
    st.success(f"✅ Uploaded {len(uploaded_files)} song(s)")

# --------------- PLAYLIST ---------------
playlist = [f for f in os.listdir(MUSIC_FOLDER) if f.lower().endswith(".mp3")]

if playlist:
    selected_song = st.selectbox("🎵 Choose a Song", playlist)

    # Audio controls
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("▶️ Play"):
        st.session_state["current_song"] = selected_song
        st.session_state["is_playing"] = True

    if col2.button("⏸ Pause"):
        st.session_state["is_playing"] = False

    if col3.button("⏯ Resume"):
        st.session_state["is_playing"] = True

    if col4.button("⏹ Stop"):
        st.session_state["is_playing"] = False
        st.session_state["current_song"] = None

    # Volume
    volume = st.slider("🔊 Volume", 0.0, 1.0, 0.5)

    # Now Playing
    if st.session_state.get("is_playing") and st.session_state.get("current_song"):
        song_path = os.path.join(MUSIC_FOLDER, st.session_state["current_song"])
        with open(song_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        st.markdown(f"**Now Playing:** {st.session_state['current_song']} 🎶")
    else:
        st.info("⏸ Music is paused or stopped.")

else:
    st.warning("📂 No songs yet! Upload MP3 files above.")
