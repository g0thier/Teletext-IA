from io import BytesIO
import zipfile
from time import sleep

options=[
    "🎸 sous-titre 🎬",
    "🎸 transcription ✏️",
    "👀 caption 🎬",
    "👀 description ✏️",
    "🎸👀 multimodal accessibility 🎬",
    "🎸👀 script ✏️",
]

formats = ["mp3", "mp4", "mpeg", "mpg", "mpga", "m4a", "wav", "webm", "ogg"]

def pipeline(uploaded_file, selection) -> BytesIO | None:
    """
    Prend un fichier (ex: st.file_uploader) et renvoie un ZIP en mémoire
    (BytesIO) compatible avec st.download_button.
    """
    # Verifie et lit le fichier
    if uploaded_file is None:
        return None

    b = uploaded_file.read()
    uploaded_file.seek(0)

    name = getattr(uploaded_file, "name", "file")

    # Action sur la selection
    print(" + ".join(selection))

    # Mouline pour le test
    sleep(len(selection) * 3)

    # Enregistre le fichier
    out = BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(name, b)

    out.seek(0)
    return out