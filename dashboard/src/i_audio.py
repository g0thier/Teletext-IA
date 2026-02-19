import tempfile
import whisper
import os
import platform
import streamlit as st

@st.cache_resource(show_spinner=False)
def get_whisper_model():
    model_name = "turbo" if platform.processor() else "base"
    return whisper.load_model(model_name)

def audio_pipeline(uploaded_file):
    model = get_whisper_model()

    # Cree un fichier temporaire pour le traitement
    suffix = "." + uploaded_file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    # Converti en segments de texte
    try:
        result = model.transcribe(tmp_path)
        return result['segments']
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)