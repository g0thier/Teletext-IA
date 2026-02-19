import tempfile
import os
import re
import cv2
from PIL import Image
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from transformers import pipeline

# Initialisation modèles 
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

def _get_scenes(path): 
    video = open_video(path)
    manager = SceneManager()
    manager.add_detector(ContentDetector(threshold=30.0))
    manager.detect_scenes(video)

    scenes = manager.get_scene_list()
    return scenes

def _dedupe_tail(text: str) -> str:
    s = re.sub(r'(\b.+?\b)( \1)+$', r'\1', text.strip()) # simple expression 
    return re.sub(r'(\b[\w ]+\b)(\s*-\s*\1)+$', r'\1', s.strip()) # sign intersection 

def _extract_frame(input_path, frame_number):
    cap = cv2.VideoCapture(input_path)

    # aller directement à la frame demandée
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    ok, frame_bgr = cap.read()
    cap.release()
    if not ok:
        raise RuntimeError(f"Impossible de lire la frame {frame_number}.")
    
    # OpenCV lit en BGR → convertir en RGB
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    # Vers PIL (le pipeline accepte PIL / numpy / torch)
    img = Image.fromarray(frame_rgb)

    return img

def _build_segments(scenes, path):
    segments = []

    for i, (start, end) in enumerate(scenes, 1):
        middle = int((end.frame_num + start.frame_num)/2)
        
        f_image = _extract_frame(path, middle)

        text = captioner(f_image)[0]['generated_text']
        text = _dedupe_tail(text)

        segment = {
        "id": i,
        "start": start,
        "end": end,
        "text": text,
        }

        segments.append(segment)

    return segments

def video_pipeline(uploaded_file):
    # Cree un fichier temporaire pour le traitement
    suffix = "." + uploaded_file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    # Converti en segments de texte
    try:
        scenes = _get_scenes(tmp_path)
        segments = _build_segments(scenes, tmp_path)

        return segments
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)