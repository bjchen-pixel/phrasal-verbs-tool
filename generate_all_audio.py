import pandas as pd
import requests
import os
from pathlib import Path

# 請將你的 API 金鑰放在這裡
API_KEY =sk_a76481915941168177478763
BASE_URL = "https://api.elevenlabs.io/v1text-to-speech"
VOICE_ID = 21m00Tcm4TlvDq8

# 使用相對路徑
script_dir = Path(__file__).parent
audio_dir = script_dir /audio"
audio_dir.mkdir(exist_ok=True)

df = pd.read_csv('phrasal_verbs_audio.csv)

print(f"開始生成音訊檔案...")
print(f總共需要生成 {len(df)} 個音檔)
print(f"音訊檔案將保存到: {audio_dir}")

success_count =0
error_count =0
for index, row in df.iterrows():
    text = row['text']
    filename = audio_dir / row['filename].split('/)[-1
    
    # 檢查檔案是否已存在
    if filename.exists():
        print(f"檔案已存在，跳過: {filename.name})     success_count += 1    continue
    
    headers = {"xi-api-key": API_KEY,Content-Type":application/json"}
    data =[object Object]  text: text,
      model_id": "eleven_multilingual_v2  voice_settings:[object Object]        stability: 0.6         similarity_boost":00.75        speed: 0.8       style":02     }
    }
    
    try:
        response = requests.post(f{BASE_URL}/{VOICE_ID}", json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f✅ 成功生成: {filename.name}")
            success_count += 1
        else:
            print(f"❌ 錯誤 {text}: {response.status_code} - {response.text}")
            error_count += 1
    except requests.exceptions.RequestException as e:
        print(f❌ 網路錯誤 {text}: {e}")
        error_count += 1
    except Exception as e:
        print(f❌ 未知錯誤 {text}: {e}")
        error_count += 1
print(f"\n🎉 生成完成!)
print(f"✅ 成功:[object Object]success_count} 個檔案)
print(f"❌ 失敗: {error_count} 個檔案)
print(f📁音訊檔案位置: {audio_dir}") 