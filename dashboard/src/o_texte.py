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
    out = []

    for segment in video_converted:
        out.append(f"Scene {int(segment["id"])} from {segment["start"]} to {segment["end"]}")
        out.append(f"↳ {segment["text"].capitalize()}.")
        out.append("")  # ligne vide entre blocs

    texte = "\n".join(out)

    txt_filename = f"{filename}_description.txt"

    # Création du fichier en mémoire
    txt_bytes = io.BytesIO()
    txt_bytes.write(texte.encode("utf-8"))
    txt_bytes.seek(0)

    return txt_filename, txt_bytes

def script(video_converted, audio_converted, filename):
    return video_converted + audio_converted + filename