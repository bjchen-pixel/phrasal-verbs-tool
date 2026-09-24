#!/usr/bin/env python3
"""
Audio Generator using edge-tts (Microsoft Azure Neural TTS)
Generates crystal clear pronunciation for any missing phrasal verbs or example sentences.
"""

import asyncio
import json
import os
import edge_tts

VOICE = "en-US-JennyNeural"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data.json")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

async def generate():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(AUDIO_DIR, exist_ok=True)

    tasks = []
    for verb, phrasals in data.items():
        for p_name, p_info in phrasals.items():
            # Phrase audio
            audio_path = os.path.join(BASE_DIR, p_info["audio"])
            if not os.path.exists(audio_path):
                tasks.append((p_name, audio_path))
            
            # Example audio
            ex_audio_path = os.path.join(BASE_DIR, p_info["exampleAudio"])
            if not os.path.exists(ex_audio_path):
                tasks.append((p_info["example"], ex_audio_path))

    total = len(tasks)
    print(f"Found {total} missing audio files to generate...")

    success = 0
    for idx, (text, filepath) in enumerate(tasks, 1):
        try:
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(filepath)
            print(f"[{idx}/{total}] Generated: {os.path.basename(filepath)} -> '{text}'")
            success += 1
        except Exception as e:
            print(f"[{idx}/{total}] Failed: {os.path.basename(filepath)} ({e})")

    print(f"\nCompleted! Generated {success}/{total} files successfully.")

if __name__ == "__main__":
    asyncio.run(generate())
