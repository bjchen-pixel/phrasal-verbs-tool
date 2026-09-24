#!/usr/bin/env python3
"""
Generate Audio using edge-tts (High Fidelity Azure Neural Voice)
No API key required, runs fast and produces crystal clear MP3s.
"""

import asyncio
import os
import csv
import edge_tts

VOICE = "en-US-JennyNeural"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
CSV_FILE = os.path.join(BASE_DIR, "phrasal_verbs_audio.csv")

async def generate_all():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found")
        return

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Checking {len(rows)} audio entries...")
    missing = [r for r in rows if not os.path.exists(os.path.join(BASE_DIR, r["filename"]))]
    print(f"Need to generate: {len(missing)} files")

    for idx, r in enumerate(missing, 1):
        target = os.path.join(BASE_DIR, r["filename"])
        text = r["text"]
        try:
            comm = edge_tts.Communicate(text, VOICE)
            await comm.save(target)
            print(f"[{idx}/{len(missing)}] Generated: {r['filename']} -> '{text}'")
        except Exception as e:
            print(f"[{idx}/{len(missing)}] Failed: {r['filename']} ({e})")

    print("\nAudio generation check complete!")

if __name__ == "__main__":
    asyncio.run(generate_all())