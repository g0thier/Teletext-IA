import math
import textwrap
import io

def _format_ts_srt(t: float) -> str:
    """Formate un timestamp en HH:MM:SS,mmm (SRT)."""
    ms = int(round((t % 1) * 1000))
    secs = int(math.floor(t))
    if ms == 1000:  # évite 99,1000 -> 100,000
        secs += 1
        ms = 0
    h = secs // 3600
    m = (secs % 3600) // 60
    s = secs % 60
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def _to_srt(segments, max_line_length: int | None = None) -> str:
    """Convertit une liste de segments Whisper en sous-titres SRT."""
    out, idx = [], 1
    for seg in segments:
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        if max_line_length:
            text = "\n".join(textwrap.wrap(text, width=max_line_length))
        out.append(str(idx))
        out.append(f"{_format_ts_srt(seg['start'])} --> {_format_ts_srt(seg['end'])}")
        out.append(text)
        out.append("")  # ligne vide entre blocs
        idx += 1
    return "\n".join(out)

def sous_titre(audio_converted, filename):
    texte = _to_srt(audio_converted)

    srt_filename = f"{filename}.srt"

    # Création du fichier en mémoire
    srt_bytes = io.BytesIO()
    srt_bytes.write(texte.encode("utf-8"))
    srt_bytes.seek(0)

    return srt_filename, srt_bytes

def caption(video_converted, filename):
    return video_converted + filename

def multimodal_accessibility(video_converted, audio_converted, filename):
    return video_converted + audio_converted + filename