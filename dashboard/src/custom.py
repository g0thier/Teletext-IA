from io import BytesIO
import zipfile
from time import sleep
from src.i_audio import audio_pipeline
from src.i_video import video_pipeline
from src.o_subti import sous_titre, caption, audio_video
from src.o_texte import transcription, description, script

options=[
    "🎸 sous-titre 🎬",
    "🎸 transcription ✏️",
    "👀 caption 🎬",
    "👀 description ✏️",
    "🎸👀 audio video 🎬",
    "🎸👀 script ✏️"
]

formats = ["mp3", "mp4", "mpeg", "mpg", "mpga", "m4a", "wav", "webm", "ogg"]

def pipeline(uploaded_file, selection) -> BytesIO | None:
    """
    Prend un fichier (ex: st.file_uploader) et renvoie un ZIP en mémoire
    (BytesIO) compatible avec st.download_button.
    """
    if uploaded_file is None:
        return None

    # Lit le fichier original
    b = uploaded_file.read()
    uploaded_file.seek(0)

    filename = getattr(uploaded_file, "name", "file")

    audio_converted = None
    video_converted = None

    # Conversion IA audio & video
    if "🎸" in "".join(selection):
        audio_converted = audio_pipeline(uploaded_file)

    if "👀" in "".join(selection):
        video_converted = video_pipeline(uploaded_file)


    # Génère les fichiers de sortie (en mémoire)
    files_bytes: list[tuple[str, BytesIO]] = []

    # Conversion format str & txt
    for option in selection:
        name_n_file = None

        if option == "🎸 sous-titre 🎬":
            name_n_file = sous_titre(audio_converted, filename)

        elif option == "🎸 transcription ✏️":
            name_n_file = transcription(audio_converted, filename)

        elif option == "👀 caption 🎬":
            name_n_file = caption(video_converted, filename)

        elif option == "👀 description ✏️":
            name_n_file = description(video_converted, filename)

        elif option == "🎸👀 audio video 🎬":
            name_n_file = audio_video(video_converted, audio_converted, filename)

        elif option == "🎸👀 script ✏️":
            name_n_file = script(video_converted, audio_converted, filename)
    
        if name_n_file is not None:
            files_bytes.append(name_n_file)

    # Crée le ZIP en mémoire
    out = BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        # (Optionnel) inclure l'original
        if 1 == 0 : z.writestr(filename, b)

        # Ajoute tous les outputs
        for out_name, out_bio in files_bytes:
            out_bio.seek(0)
            z.writestr(out_name, out_bio.read())

    out.seek(0)
    return out