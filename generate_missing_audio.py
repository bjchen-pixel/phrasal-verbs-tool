import pandas as pd
from pathlib import Path

# 讀取原始CSV
df = pd.read_csv('phrasal_verbs_audio.csv')

# 取得audio資料夾內實際存在的檔案
audio_dir = Path('audio')
existing_files = {f.name for f in audio_dir.iterdir() if f.is_file()}

# 找出缺失的檔案
missing = df[~df['filename'].apply(lambda x: Path(x).name in existing_files)]

# 重新編號
missing['id'] = range(1, len(missing) + 1)

# 儲存缺失檔案清單
missing.to_csv('missing_audio.csv', index=False)

print(f"總共需要 {len(df)} 個音訊檔案")
print(f"實際存在 {len(existing_files)} 個檔案")
print(f"缺失 {len(missing)} 個檔案")
print(f"缺失檔案已儲存到 missing_audio.csv")

# 顯示缺失檔案清單
print("缺失的檔案：")
for _, row in missing.iterrows():
    print(f"{row['id']}. {row['filename']} - {row['text']}") 