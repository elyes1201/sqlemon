# -*- coding: utf-8 -*-
"""Télécharge les BGM Pokémon Rouge/Bleu pour SQLemon dans static/music/."""

import subprocess, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

MUSIC_DIR = os.path.join(os.path.dirname(__file__), "static", "music")
os.makedirs(MUSIC_DIR, exist_ok=True)

# Chemin ffmpeg (winget installe là)
FFMPEG_DIR = os.path.expanduser(
    r"~\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1-full_build\bin"
)

TRACKS = [
    ("pallet.mp3",       "ytsearch1:Pokemon Red Blue Pallet Town theme music original"),
    ("viridianforest.mp3","ytsearch1:Pokemon Red Blue Viridian Forest music original"),
    ("mtmoon.mp3",        "ytsearch1:Pokemon Red Blue Mt Moon music original"),
    ("cerulean.mp3",      "ytsearch1:Pokemon Red Blue Cerulean City music original"),
    ("lavender.mp3",      "ytsearch1:Pokemon Red Blue Lavender Town music original"),
    ("vermilion.mp3",     "ytsearch1:Pokemon Red Blue Vermilion City music original"),
    ("cinnabar.mp3",      "ytsearch1:Pokemon Red Blue Cinnabar Island music original"),
    ("indigo.mp3",        "ytsearch1:Pokemon Red Blue Pokemon League Indigo Plateau music original"),
]

for filename, query in TRACKS:
    out_path = os.path.join(MUSIC_DIR, filename)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10_000:
        print(f"[OK] {filename} déjà présent")
        continue
    print(f"[DL] {filename} …")
    result = subprocess.run([
        sys.executable, "-m", "yt_dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "5",
        "--no-playlist",
        "--ffmpeg-location", FFMPEG_DIR,
        "--js-runtimes", r"nodejs:C:\Program Files\nodejs\node.exe",
        "--output", out_path.replace(".mp3", ".%(ext)s"),
        "--quiet",
        query,
    ])
    if result.returncode == 0 and os.path.exists(out_path):
        size = os.path.getsize(out_path)
        print(f"  OK {filename} ({size//1024} Ko)")
    else:
        print(f"  ECHEC {filename}")

print("\nTerminé. Fichiers dans static/music/:")
for f in os.listdir(MUSIC_DIR):
    path = os.path.join(MUSIC_DIR, f)
    print(f"  {f}  {os.path.getsize(path)//1024} Ko")
