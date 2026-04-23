import streamlit as st
import numpy as np
import wave

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Noise Monitor", page_icon="🔊", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* SKY BLUE BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #87CEEB !important;
}

/* REMOVE DARK HEADER */
[data-testid="stHeader"], [data-testid="stToolbar"] {
    background: transparent !important;
}

/* NAVY TEXT */
html, body, p, h1, h2, h3, h4, h5, h6, label, div {
    color: #001f3f !important;
}

/* TITLE */
.title {
    font-size: 60px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

/* CARDS */
.card {
    padding: 25px;
    border-radius: 15px;
    background-color: #ffffff;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

/* BUTTON */
.stButton>button {
    background-color: #001f3f;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background-color: white;
    padding: 10px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">🔊 Urban Noise Monitoring System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ensuring safe & smart noise monitoring using AI</div>', unsafe_allow_html=True)

# ---------------- FILE UPLOAD ----------------
st.markdown("### 📁 Upload Audio File")
uploaded_file = st.file_uploader("Upload WAV file", type=["wav"])

# ---------------- SAFE AUDIO FUNCTION ----------------
def analyze_audio(file):
    try:
        with wave.open(file, 'rb') as wav_file:
            frames = wav_file.readframes(-1)

            if len(frames) == 0:
                return 0

            signal = np.frombuffer(frames, dtype=np.int16)

            if len(signal) == 0:
                return 0

            signal = signal.astype(np.float32)

            rms = np.sqrt(np.mean(signal**2))

            if np.isnan(rms):
                return 0

            return rms

    except:
        return 0

# ---------------- MAIN ----------------
if uploaded_file is not None:

    col1, col2, col3 = st.columns(3)

    rms_value = analyze_audio(uploaded_file)

    # Convert to dB safely
    db = 20 * np.log10(rms_value + 1)

    # Classification
    if db > 85:
        label = "Traffic / Industrial Noise"
        alert = "⚠ HIGH NOISE ALERT"
        level = 95
    elif db > 60:
        label = "Human Activity"
        alert = "Moderate Noise"
        level = 65
    else:
        label = "Quiet Environment"
        alert = "Safe"
        level = 30

    # -------- CARD 1 --------
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Analysis")
        st.write(f"Environment: {label}")
        st.write(f"RMS: {int(rms_value) if rms_value > 0 else 0}")
        st.write(f"dB: {int(db)}")
        st.progress(level)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------- CARD 2 --------
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🚨 Alert")

        if level > 85:
            st.error(alert)
        elif level > 60:
            st.warning(alert)
        else:
            st.success(alert)

        st.markdown('</div>', unsafe_allow_html=True)

    # -------- CARD 3 --------
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📌 Interpretation")

        if level > 85:
            st.write("Very loud environment. Avoid long exposure.")
        elif level > 60:
            st.write("Moderate noise present.")
        else:
            st.write("Quiet and safe environment.")

        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 Upload a WAV file to start analysis")