import io
import os

def transcription(audio_converted, filename):
    base_name = os.path.splitext(filename)[0]
    txt_filename = f"{base_name}_transcription.txt"

    # Création du fichier en mémoire
    txt_bytes = io.BytesIO()

    # Écriture "comme dans le fichier txt", mais dans le buffer mémoire
    for segment in audio_converted:
        parole = segment["text"]
        txt_bytes.write((parole + "\n").encode("utf-8"))

    txt_bytes.seek(0)

    return txt_filename, txt_bytes

def description(video_converted, filename):
    return video_converted + filename

def script(video_converted, audio_converted, filename):
    return video_converted + audio_converted + filename