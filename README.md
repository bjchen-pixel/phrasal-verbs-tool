# 🧠 PhrasalFlow - 英語高頻片語動詞互動學習神器

> 融合**雙真人發音**、**三階段階梯學習**、**3D 單字卡記憶**、**認知介系詞思維地圖**與**多模式智慧測驗**的現代化英語片語學習應用。

---

## 🌟 核心特色 (Key Features)

### 1. 🎯 三階段階梯學習地圖（覆蓋率達 90%+ 母語日常、影集與職場）
- **🥇 第一階：黃金核心（92 詞）**：精選 16 大核心動詞（`take`, `get`, `make`, `put`, `turn` 等），打牢最底層高頻骨架。
- **🥈 第二階：流暢實戰（58 詞）**：補齊日常生活與職場極高頻片語（如 `pick up`, `figure out`, `hang out`, `follow up`, `roll out`, `wrap up`, `fill out` 等）。
- **🥉 第三階：母語高階（150 詞）**：涵蓋美劇道地俚語（`freak out`, `chill out`, `zone out`, `mess up`, `rip off` 等）、商務談判（`iron out`, `hammer out`, `flesh out`, `pencil in` 等）、高難度三詞雙介系詞片語（`put up with`, `come down with`, `look down on`, `stand up for` 等）與精微動作（`pull over`, `lock out`, `wear out` 等）。
- **總收錄量達 300 組精選片語**，支援「第一階 / 第二階 / 第三階 / 全階段」自由切換。

### 2. 🎧 100% 完整雙語音發音覆蓋 (Dual Audio Coverage)
- **300 組片語發音** + **300 句情境真實例句發音**，全數 600 個音訊引用 100% 完備。
- **雙引擎發音支援**：
  - 預錄微軟高音質神經網路發音（Microsoft Azure Neural Voice / JennyNeural）。
  - 瀏覽器原生 **Web Speech API** 智慧容錯（即時朗讀、零延遲、無需聯網亦可發音）。
- **可自訂語速**：支援 0.75x、1.0x、1.25x 自由切換。

### 2. 📖 探索與篩選清單 (Explore & Cards)
- **16 大核心動詞分類**：`take`, `get`, `make`, `break`, `run`, `do`, `have`, `put`, `go`, `come`, `set`, `look`, `turn`, `bring`, `give`, `keep`。
- **即時模糊搜尋**：即時支援片語英文、中文釋義、例句與情境標籤檢索。
- **掌握度篩選**：全部、學習中、已精通、星號收藏夾。

### 3. 🎴 沉浸式 3D 單字卡訓練 (3D Flashcard Deck)
- 擬真 3D 翻轉卡片體驗。
- **正面**：片語動詞 + 介系詞徽章 + 適用情境 + 片語發音。
- **背面**：中文釋義 + 英文詳細定義 + 經典例句 + 中文翻譯 + 例句發音。
- **直覺快捷鍵**：
  - `Space`：翻轉卡片
  - `←` / `→`：上/下一張
  - `P`：重播發音
- 支援「已掌握」與「還不熟」標記，並提供隨機洗牌（Shuffle）功能。

### 4. 🎯 智慧測驗中心 (Smart Quiz Hub)
- **三種挑戰模式**：
  1. **釋義配對題**：看片語選中文意思。
  2. **情境克漏字**：閱讀真實句子，選出合適的片語動詞填空。
  3. **聽力聽辨挑戰**：聆聽純英語音，聽辨正確片語。
- **自訂題量**：5 題（快速複習）、10 題（標準挑戰）、20 題（深度衝刺）、全部片語。
- **即時回饋與錯題本**：作答後即時標示正確/錯誤，測驗結束可一鍵「複習錯題」針對弱點強化！

### 5. 🗺️ 介系詞思維地圖 (Particle Mind Map)
- 揭密片語動詞的核心祕密：**搞懂介系詞（Particle），就不用死背！**
- 完整拆解 10 大核心介系詞的空間與認知隱喻：
  - `UP`（向上、徹底完成、浮現提高）
  - `OUT`（向外、徹底耗盡、顯露發掘）
  - `OFF`（分離脫離、中斷停止、啟程出發）
  - `DOWN`（向下、降低抑制、記錄停止）
  - `ON`（接觸附著、持續進行、承擔）
  - `IN / INTO`（進入內部、收納吸收、轉化改變）
  - `AWAY`（遠離散去、消滅擺脫）
  - `BACK`（返回原處、回溯回應）
  - `OVER`（跨越上方、重複翻覆、掌控審視）
  - `THROUGH`（穿透貫穿、經歷完成）
- 點擊任一介系詞，即可一鍵查看所有採用該介系詞的片語動詞！

### 6. 🌙 現代化視覺與本機儲存 (Modern Design & Persistence)
- **精緻設計系統**：深色/淺色主題切換、毛玻璃（Glassmorphism）效果、音波脈動動畫、流暢微動態。
- **本機無痕儲存**：學習進度、星號收藏、已精通狀態、播放速度與深淺主題自動儲存在瀏覽器 `localStorage`。
- **雙模運作**：
  - 直接在檔案總管雙擊 `index.html` 即可免伺服器離線使用！
  - 亦可搭配任何本機 HTTP 伺服器使用。

---

## 📂 專案結構 (Directory Structure)

```text
phrasal-verbs-tool/
├── index.html                 # 現代化主頁面
├── legacy_index_v1.html       # 原版歷史備份存檔
├── css/
│   └── app.css                # 現代化 CSS 設計系統（深淺主題、動畫、毛玻璃）
├── js/
│   └── app.js                 # 應用程式狀態管理、音訊控制與四大互動模組
├── data/
│   ├── phrasal_verbs_data.js  # 離線可用的完整資料結構（支援 file:// 免跨域）
│   └── phrasal_verbs_enriched.json # 結構化 JSON 資料檔（含克漏字與介系詞隱喻）
├── audio/                     # 600 個高品質 MP3 發音檔（300 片語 + 300 例句）
├── phrasal_verbs_audio.csv    # 完整音訊對應表 (600 條記錄)
├── generate_all_audio.py      # 音訊生成腳本（基於 edge-tts 神經網路發音）
└── README.md                  # 專案說明文件
```

---

## 🚀 啟動與使用 (Getting Started)

### 方法一：直接開啟（最簡單）
直接使用任何瀏覽器（Chrome、Edge、Safari）雙擊打開 `index.html` 即可開始學習！

### 方法二：透過本機 HTTP 伺服器
```bash
# 使用 Python 啟動
python3 -m http.server 8095

# 或使用 npx serve
npx serve .
```
接著於瀏覽器造訪 `http://localhost:8095`。

---

## 🛠️ 音訊補全工具 (Audio Generator)

本專案已全面補齊所有 300 組片語動詞與例句音檔（共 600 首 MP3）。若日後有擴充新增片語，可隨時執行：

```bash
python3 generate_all_audio.py
```
該工具會自動掃描缺漏的音訊並透過微軟 Azure 類神經語音引擎（`en-US-JennyNeural`）自動合成高品質 MP3。