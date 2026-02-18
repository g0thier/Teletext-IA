import tempfile
import whisper
import os

model = whisper.load_model("turbo")

def audio_pipeline(uploaded_file):
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