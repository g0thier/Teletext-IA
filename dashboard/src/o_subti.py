import math
import textwrap
import io
import srt
from datetime import timedelta


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

## 
## Fonctions pour full_accessibility()
##

SOURCE_ORDER = {"image": 0, "son": 1} # Ordre de priorité

def _parse_srt_text(text: str, source: str):
    """Parse un SRT depuis une chaîne et marque la provenance."""
    items = list(srt.parse(text or ""))
    for it in items:
        it._source = source
    return items

def _active_on_segment(sub, seg_start, seg_end):
    # recouvrement strict, pas de tolérance
    return (sub.start < seg_end) and (sub.end > seg_start)

def _fuse_srt_strings(video_str: str, audio_str: str) -> str:
    subs_img = _parse_srt_text(video_str, "image")
    subs_son = _parse_srt_text(audio_str, "son")
    all_subs = subs_img + subs_son

    if not all_subs:
        return ""

    # 1) Points de rupture = tous les starts et ends
    cuts = set()
    for it in all_subs:
        cuts.add(it.start)
        cuts.add(it.end)
    # trier et retirer les segments nuls
    cuts = sorted(cuts)

    # 2) Segments consécutifs [t_i, t_{i+1})
    segments = []
    for i in range(len(cuts) - 1):
        a, b = cuts[i], cuts[i+1]
        if a < b:
            segments.append((a, b))

    # 3) Pour chaque segment, concaténer les textes actifs
    fused = []
    idx = 1
    for seg_start, seg_end in segments:
        actives = [it for it in all_subs if _active_on_segment(it, seg_start, seg_end)]

        if not actives:
            continue  # pas de texte actif sur ce segment

        # Ordre de concaténation :
        #   - d'abord l'ordre chronologique (start)
        #   - en cas d'égalité, tri par source pour stabilité
        actives.sort(key=lambda it: (it.start, getattr(it, "_source", "")))

        # >>> tri par source d'abord, puis par start
        actives.sort(key=lambda it: (SOURCE_ORDER.get(getattr(it, "_source", ""), 99), it.start))

        texts = [it.content.strip() for it in actives if it.content and it.content.strip()]
        if not texts:
            continue  # rien à écrire

        content = "\n".join(texts)

        fused.append(
            srt.Subtitle(
                index=idx,
                start=seg_start,
                end=seg_end,
                content=content
            )
        )
        idx += 1

    return srt.compose(fused)


## 
## Fonctions Accessible 
##

def sous_titre(audio_converted, filename):
    texte = _to_srt(audio_converted)

    srt_filename = f"{filename}.srt"

    # Création du fichier en mémoire
    srt_bytes = io.BytesIO()
    srt_bytes.write(texte.encode("utf-8"))
    srt_bytes.seek(0)

    return srt_filename, srt_bytes

def caption(video_converted, filename):
    out = []

    for segment in video_converted:
        out.append(str(segment["id"]))
        out.append(f"{segment["start"].get_timecode()} --> {segment["end"].get_timecode()}")
        out.append(f"({segment["text"]})")
        out.append("")  # ligne vide entre blocs

    texte = "\n".join(out)

    srt_filename = f"{filename}_caption.srt"

    # Création du fichier en mémoire
    srt_bytes = io.BytesIO()
    srt_bytes.write(texte.encode("utf-8"))
    srt_bytes.seek(0)

    return srt_filename, srt_bytes

def full_accessibility(video_converted, audio_converted, filename):
    _, audio_bytes = sous_titre(audio_converted, filename)
    _, video_bytes = caption(video_converted, filename)

    # Lire et décoder
    audio_str = audio_bytes.read().decode("utf-8")
    video_str = video_bytes.read().decode("utf-8")

    texte = _fuse_srt_strings(video_str, audio_str)

    srt_filename = f"{filename}_AV.srt"

    # Création du fichier en mémoire
    srt_bytes = io.BytesIO()
    srt_bytes.write(texte.encode("utf-8"))
    srt_bytes.seek(0)

    return srt_filename, srt_bytes