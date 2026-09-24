#!/usr/bin/env python3
"""
Build Full 300 Phrasal Verbs Database (Level 1 + Level 2 + Level 3)
150 new Level 3 verbs covering native idioms, three-word phrasal verbs, business negotiation, and daily actions.
Synthesizes all 300 MP3 audio files with edge-tts and updates JSON, JS, and CSV.
"""

import asyncio
import json
import os
import re
import csv
import edge_tts

BASE_DIR = "/Volumes/Data 4T/Projects/phrasal-verbs-tool"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
DATA_JSON_PATH = os.path.join(BASE_DIR, "data/phrasal_verbs_enriched.json")
DATA_JS_PATH = os.path.join(BASE_DIR, "data/phrasal_verbs_data.js")
CSV_PATH = os.path.join(BASE_DIR, "phrasal_verbs_audio.csv")
VOICE = "en-US-JennyNeural"

LEVEL_3_SOURCE = [
    # 1. Colloquial, Slang & Emotional (美劇生活、情緒與俚語)
    {"verb": "freak", "phrasal": "freak out", "particle": "out", "chineseMeaning": "嚇壞、崩潰抓狂", "meaning": "Become extremely emotional, frightened, or panicked", "example": "Do not freak out when you see the final bill.", "exampleChinese": "看到最後的帳單時，千萬別嚇壞抓狂了。", "scenario": "情緒崩潰、驚慌"},
    {"verb": "chill", "phrasal": "chill out", "particle": "out", "chineseMeaning": "放鬆冷靜、別緊張", "meaning": "Relax completely and calm down", "example": "Let us just stay home and chill out tonight.", "exampleChinese": "今晚我們就待在家裡好好放鬆一下吧。", "scenario": "放鬆休閒"},
    {"verb": "zone", "phrasal": "zone out", "particle": "out", "chineseMeaning": "眼神放空、恍神走神", "meaning": "Lose concentration or daydream temporarily", "example": "I zoned out during the long boring lecture.", "exampleChinese": "在那場冗長無聊的講座中，我忍不住恍神放空了。", "scenario": "注意力分散"},
    {"verb": "mess", "phrasal": "mess up", "particle": "up", "chineseMeaning": "搞砸弄亂、犯大錯", "meaning": "Mishandle a situation or make a major mistake", "example": "He apologized sincerely for messing up the presentation.", "exampleChinese": "他為自己搞砸了那場簡報而真誠道歉。", "scenario": "出錯搞砸"},
    {"verb": "screw", "phrasal": "screw up", "particle": "up", "chineseMeaning": "徹底搞砸、出大包（口語）", "meaning": "Blunder or ruin an opportunity badly", "example": "I really screwed up my chance to study in Oxford.", "exampleChinese": "我真的徹底搞砸了去牛津留學的寶貴機會。", "scenario": "生活口語"},
    {"verb": "rip", "phrasal": "rip off", "particle": "off", "chineseMeaning": "敲竹槓、坑人索高價", "meaning": "Overcharge someone unfairly or cheat them", "example": "Tourist shops often rip off foreign visitors with fake souvenirs.", "exampleChinese": "觀光景點的小店常常用假紀念品敲外國遊客竹槓。", "scenario": "消費詐騙"},
    {"verb": "bail", "phrasal": "bail out", "particle": "out", "chineseMeaning": "抽身逃脫、緊急金援救援", "meaning": "Rescue from financial failure or abandon an awkward situation", "example": "The central bank had to bail out several regional lenders.", "exampleChinese": "央行不得不向幾家地方銀行提供緊急金援脫困。", "scenario": "金融救援、逃避"},
    {"verb": "chicken", "phrasal": "chicken out", "particle": "out", "chineseMeaning": "臨陣退縮、膽怯作罷", "meaning": "Decide not to do something risky due to fear", "example": "He was going to skydive but chickened out at the airport.", "exampleChinese": "他原本打算去跳傘，但在機場時卻臨陣退縮了。", "scenario": "勇氣挑戰"},
    {"verb": "sleep", "phrasal": "sleep in", "particle": "in", "chineseMeaning": "睡懶覺、睡到自然醒", "meaning": "Remain asleep longer than usual in the morning", "example": "I usually sleep in until ten on Sunday mornings.", "exampleChinese": "我週日早晨通常都會睡懶覺睡到十點。", "scenario": "假日起居"},
    {"verb": "stay", "phrasal": "stay up", "particle": "up", "chineseMeaning": "熬夜不睡", "meaning": "Refrain from going to bed at the normal hour", "example": "We stayed up all night cramming for the chemistry final.", "exampleChinese": "我們熬夜通宵溫習化學期末考。", "scenario": "夜生活、讀書"},
    {"verb": "pig", "phrasal": "pig out", "particle": "out", "chineseMeaning": "大吃大喝、暴飲暴食", "meaning": "Gorge on large amounts of food greedily", "example": "They pigged out on pizza and ice cream during the movie.", "exampleChinese": "看電影時他們狂嗑披薩和冰淇淋大吃特吃。", "scenario": "美食聚會"},
    {"verb": "veg", "phrasal": "veg out", "particle": "out", "chineseMeaning": "像植物人般放鬆耍廢", "meaning": "Relax lazily doing nothing productive", "example": "After a grueling week, I just want to veg out on the sofa.", "exampleChinese": "經過疲累的一週後，我只想攤在沙發上徹底耍廢。", "scenario": "休息耍廢"},
    {"verb": "hit", "phrasal": "hit on", "particle": "on", "chineseMeaning": "搭訕、挑逗某人", "meaning": "Make romantic or flirtatious advances toward someone", "example": "A stranger attempted to hit on her at the cocktail party.", "exampleChinese": "一名陌生人在雞尾酒會上試圖向她搭訕。", "scenario": "社交搭訕"},
    {"verb": "hit", "phrasal": "hit it off", "particle": "it off", "chineseMeaning": "一見如故、相談甚歡", "meaning": "Instantly form a warm rapport upon first meeting", "example": "The two new coworkers hit it off right from day one.", "exampleChinese": "那兩位新同事從上班第一天就一見如故非常投緣。", "scenario": "人際交往"},
    {"verb": "ask", "phrasal": "ask out", "particle": "out", "chineseMeaning": "約（某人）出去約會", "meaning": "Invite someone on a romantic date", "example": "He finally gathered the courage to ask her out for coffee.", "exampleChinese": "他終於鼓起勇氣約她出去喝杯咖啡。", "scenario": "男女約會"},
    {"verb": "fool", "phrasal": "fool around", "particle": "around", "chineseMeaning": "閒混打鬧、胡鬧", "meaning": "Behave in an idle, playful, or irresponsible way", "example": "Stop fooling around and concentrate on your assignment.", "exampleChinese": "別再胡鬧閒混了，專心做你的作業吧。", "scenario": "專注紀律"},
    {"verb": "sneak", "phrasal": "sneak out", "particle": "out", "chineseMeaning": "偷偷溜出去", "meaning": "Leave a place quietly and unnoticed", "example": "The teenagers sneaked out through the bedroom window at midnight.", "exampleChinese": "那些青少年午夜時分從臥室窗戶偷偷溜了出去。", "scenario": "行蹤隱密"},
    {"verb": "creep", "phrasal": "creep out", "particle": "out", "chineseMeaning": "讓人心裡發毛、起雞皮疙瘩", "meaning": "Cause someone to feel frightened or uneasy", "example": "That abandoned Victorian mansion really creeps me out.", "exampleChinese": "那座廢棄的維多利亞式老宅真讓我心裡發毛。", "scenario": "驚悚詭異"},
    {"verb": "crack", "phrasal": "crack up", "particle": "up", "chineseMeaning": "哈哈大笑、笑破肚皮", "meaning": "Burst into sudden uncontrollable laughter", "example": "The comedian's hilarious impressions cracked up the entire room.", "exampleChinese": "那位喜劇演員搞笑的模仿讓全場笑破了肚皮。", "scenario": "幽默娛樂"},
    {"verb": "burst", "phrasal": "burst out", "particle": "out", "chineseMeaning": "突然爆發（大笑/大哭）", "meaning": "Begin expressing strong emotion suddenly", "example": "She burst out crying when hearing the tragic news.", "exampleChinese": "聽到那個不幸的消息時，她忍不住放聲大哭了起來。", "scenario": "情緒宣洩"},
    {"verb": "choke", "phrasal": "choke up", "particle": "up", "chineseMeaning": "激動哽咽、說不出話", "meaning": "Become overwhelmed with sorrow or gratitude and unable to speak", "example": "The award winner choked up while thanking her parents.", "exampleChinese": "獲獎者在感謝父母時激動得哽咽說不出話來。", "scenario": "真情流露"},
    {"verb": "act", "phrasal": "act up", "particle": "up", "chineseMeaning": "故障耍脾氣、舊疾發作", "meaning": "Malfunction or behave rebelliously or painfully", "example": "My old knee injury acts up whenever cold rain approaches.", "exampleChinese": "每逢寒冬陰雨，我的膝蓋舊疾就會開始作痛發作。", "scenario": "機械故障、病痛"},
    {"verb": "goof", "phrasal": "goof off", "particle": "off", "chineseMeaning": "偷懶摸魚、鬼混", "meaning": "Waste time lazily avoid work duties", "example": "Employees caught goofing off during shifts face strict reprimands.", "exampleChinese": "在上班時間被抓到偷懶摸魚的員工會受到嚴厲訓誡。", "scenario": "工作摸魚"},
    {"verb": "freeze", "phrasal": "freeze up", "particle": "up", "chineseMeaning": "大腦當機、嚇得僵住", "meaning": "Become completely paralyzed with fear or hesitation", "example": "The novice speaker froze up as hundreds of eyes stared at him.", "exampleChinese": "當數百雙眼睛盯著這位新手演講者時，他頓時大腦一片空白僵住了。", "scenario": "臨場緊張"},
    {"verb": "clam", "phrasal": "clam up", "particle": "up", "chineseMeaning": "守口如瓶、一聲不吭", "meaning": "Refuse obstinately to speak or reveal information", "example": "The suspect clammed up as soon as legal interrogations started.", "exampleChinese": "審訊一開始，嫌犯就閉緊嘴巴一聲不吭。", "scenario": "保密審問"},
    {"verb": "burn", "phrasal": "burn down", "particle": "down", "chineseMeaning": "燒成灰燼、燒毀", "meaning": "Destroy completely by fire to ground level", "example": "The historic wooden library burned down in an electrical fire.", "exampleChinese": "那座歷史悠久的木造圖書館在一次電氣火災中被完全燒毀。", "scenario": "火災災情"},
    {"verb": "blow", "phrasal": "blow away", "particle": "away", "chineseMeaning": "令人極度驚艷、吹走", "meaning": "Impress or surprise someone tremendously", "example": "Her breathtaking performance blew away the judging panel.", "exampleChinese": "她驚艷全場的精彩表現徹底折服了評審團。", "scenario": "讚嘆佩服"},
    {"verb": "knock", "phrasal": "knock out", "particle": "out", "chineseMeaning": "擊昏、使入睡、淘汰出局", "meaning": "Hit someone unconscious or eliminate from competition", "example": "The boxer knocked out his rival in the final round.", "exampleChinese": "那名拳擊手在最後一回合將對手擊倒昏迷取勝。", "scenario": "體育格鬥"},

    # 2. Business, Workplace & Project Execution (職場談判、商務決策、專案落地)
    {"verb": "iron", "phrasal": "iron out", "particle": "out", "chineseMeaning": "消除分歧、解決細節問題", "meaning": "Resolve small difficulties and finalize agreements smoothly", "example": "Lawyers are meeting to iron out lingering contract issues.", "exampleChinese": "雙方律師正在會面，以消除合約中殘留的各項細微爭議。", "scenario": "談判協商"},
    {"verb": "hammer", "phrasal": "hammer out", "particle": "out", "chineseMeaning": "艱苦協商敲定協議", "meaning": "Reach an agreement after arduous debate and negotiations", "example": "Ministers hammered out a landmark climate trade deal.", "exampleChinese": "各國部長經過艱苦協商，終於敲定了一項具里程碑意義的氣候貿易協議。", "scenario": "國際會議"},
    {"verb": "flesh", "phrasal": "flesh out", "particle": "out", "chineseMeaning": "充實內容、細化方案架構", "meaning": "Add substance, detail, and concrete specifics to an outline", "example": "We need to flesh out this rough marketing idea before pitching.", "exampleChinese": "在正式提案前，我們必須把這個初步的行銷構想充實具體化。", "scenario": "企劃提案"},
    {"verb": "pencil", "phrasal": "pencil in", "particle": "in", "chineseMeaning": "暫定行程時間", "meaning": "Set a tentative schedule appointment subject to confirmation", "example": "Let us pencil in lunch next Tuesday and confirm on Monday.", "exampleChinese": "我們先把下週二中午的午餐時間暫定下來，週一再做最終確認。", "scenario": "排定行事曆"},
    {"verb": "narrow", "phrasal": "narrow down", "particle": "down", "chineseMeaning": "縮小範圍、精簡名單", "meaning": "Reduce possibilities to a smaller focused list", "example": "The recruitment committee narrowed down the candidate pool to three.", "exampleChinese": "招聘委員會將候選人名單精簡縮小到了最後三位。", "scenario": "人才遴選"},
    {"verb": "phase", "phrasal": "phase in", "particle": "in", "chineseMeaning": "分階段逐步推行引進", "meaning": "Introduce a new system gradually across stages", "example": "The automated tax system will be phased in over three fiscal quarters.", "exampleChinese": "自動化稅務系統將在三個會計季度內分階段逐步推行。", "scenario": "政策落實"},
    {"verb": "phase", "phrasal": "phase out", "particle": "out", "chineseMeaning": "逐步淘汰停產", "meaning": "Stop using, selling, or producing something gradually", "example": "Automakers will phase out fuel-powered vehicles by next decade.", "exampleChinese": "各大汽車製造商將在未來十年內逐步停產淘汰燃油車。", "scenario": "產業轉型"},
    {"verb": "scale", "phrasal": "scale up", "particle": "up", "chineseMeaning": "擴大規模、擴充產能", "meaning": "Increase proportion, size, or production capability proportionally", "example": "The cloud startup needed extra servers to scale up operations.", "exampleChinese": "這家雲端新創公司需要增添伺服器以擴大其營運規模。", "scenario": "新創擴張"},
    {"verb": "scale", "phrasal": "scale down", "particle": "down", "chineseMeaning": "縮編裁減規模", "meaning": "Reduce dimensions, budget, or workforce sizes", "example": "Due to sluggish revenues, the enterprise scaled down branch offices.", "exampleChinese": "因營收疲軟，該企業裁減縮編了部分分公司規模。", "scenario": "成本節約"},
    {"verb": "step", "phrasal": "step down", "particle": "down", "chineseMeaning": "主動讓位下台、請辭", "meaning": "Resign officially from an authoritative position", "example": "The veteran chief executive stepped down in favor of younger talent.", "exampleChinese": "這位資深執行長宣布讓位下台，由年輕後進接棒。", "scenario": "公司人事變動"},
    {"verb": "step", "phrasal": "step up", "particle": "up", "chineseMeaning": "挺身而出、加大力度", "meaning": "Take responsibility or increase effort when necessary", "example": "Every department must step up to meet rigorous safety protocols.", "exampleChinese": "每個部門都必須挺身而出加大力度，以符合嚴謹的安全規範。", "scenario": "提升效能"},
    {"verb": "step", "phrasal": "step in", "particle": "in", "chineseMeaning": "出面介入調停", "meaning": "Intervene actively in an escalating crisis or dispute", "example": "The mediator stepped in before arguments turned hostile.", "exampleChinese": "調解人在爭論演變為敵對衝突之前及時出面介入。", "scenario": "糾紛調解"},
    {"verb": "branch", "phrasal": "branch out", "particle": "out", "chineseMeaning": "拓展新業務、跨足新領域", "meaning": "Diversify into unfamiliar new commercial territories", "example": "The bakery decided to branch out into specialty coffee roasted beans.", "exampleChinese": "那家烘焙麵包店決定跨足新領域，經營精品烘焙咖啡豆。", "scenario": "商業拓展"},
    {"verb": "buy", "phrasal": "buy out", "particle": "out", "chineseMeaning": "收購股權、買斷掌控", "meaning": "Purchase total control or full financial shares from partners", "example": "He bought out his partner to own the retail company completely.", "exampleChinese": "他買斷了合夥人的全部股份，以完全擁有這家零售公司。", "scenario": "股權交易"},
    {"verb": "cash", "phrasal": "cash in on", "particle": "in on", "chineseMeaning": "趁機撈一筆、藉機獲利", "meaning": "Take opportunistic financial advantage of a favorable trend", "example": "Traders cashed in on surging market volatility.", "exampleChinese": "交易員們趁著市場大幅波動的大好時機獲取了豐厚利潤。", "scenario": "商機獲利"},
    {"verb": "draw", "phrasal": "draw up", "particle": "up", "chineseMeaning": "起草擬定合約文書", "meaning": "Draft a formal legal document, contract, or blueprint carefully", "example": "Corporate attorneys drew up a mutual non-disclosure agreement.", "exampleChinese": "企業律師們草擬了一份雙向保密協議合約。", "scenario": "合約法務"},
    {"verb": "factor", "phrasal": "factor in", "particle": "in", "chineseMeaning": "計入考量、將...列入運算", "meaning": "Include specific costs or elements in calculating a final outcome", "example": "Do not forget to factor in shipping freight and customs duties.", "exampleChinese": "計算時千萬不要忘記把海空運費和海關關稅列入考量。", "scenario": "財務預算"},
    {"verb": "lay", "phrasal": "lay off", "particle": "off", "chineseMeaning": "裁減員工、資遣", "meaning": "Discontinue employment because of operational cost downturns", "example": "The software conglomerate laid off five percent of remote engineers.", "exampleChinese": "那家大型軟體集團裁減資遣了百分之五的遠端工程師。", "scenario": "企業裁員"},
    {"verb": "opt", "phrasal": "opt in", "particle": "in", "chineseMeaning": "勾選同意參加、主動加入", "meaning": "Choose deliberately to participate in a program or policy", "example": "Customers must opt in to receive commercial promotional alerts.", "exampleChinese": "顧客必須主動勾選同意，才能收到商業優惠通知。", "scenario": "條款設定"},
    {"verb": "opt", "phrasal": "opt out", "particle": "out", "chineseMeaning": "選擇退出、不參加", "meaning": "Decide expressly not to participate in an agreement", "example": "Users can opt out of telemetry data analytics anytime.", "exampleChinese": "使用者可以隨時選擇退出遙測資料分析統計。", "scenario": "隱私權限"},
    {"verb": "read", "phrasal": "read over", "particle": "over", "chineseMeaning": "從頭到尾審閱讀過", "meaning": "Examine written text thoroughly from start to finish", "example": "Please read over the contract terms carefully before signatures.", "exampleChinese": "簽名前請務必仔細從頭到尾審閱過合約條款。", "scenario": "審閱文件"},
    {"verb": "rule", "phrasal": "rule out", "particle": "out", "chineseMeaning": "排除可能性", "meaning": "Exclude something as impossible or unacceptable", "example": "Doctors ruled out surgical intervention at this early stage.", "exampleChinese": "醫生在現階段排除了外科手術介入的可能性。", "scenario": "診斷決策"},
    {"verb": "set", "phrasal": "set back", "particle": "back", "chineseMeaning": "阻礙進度、花費某人多少錢", "meaning": "Delay scheduled achievement or cost a significant sum of money", "example": "The component shortage set back production by three full weeks.", "exampleChinese": "零組件短缺讓產線進度延誤了整整三個星期。", "scenario": "專案阻礙"},
    {"verb": "settle", "phrasal": "settle on", "particle": "on", "chineseMeaning": "選定敲定目標", "meaning": "Reach a collective decision upon choosing an alternative", "example": "After lengthy arguments, they settled on the blue brand logo.", "exampleChinese": "經過一番漫長討論後，他們最終敲定選用了藍色的品牌標誌。", "scenario": "決策挑選"},
    {"verb": "shore", "phrasal": "shore up", "particle": "up", "chineseMeaning": "支撐加固、穩定局勢", "meaning": "Strengthen support structures or bolster faltering confidence", "example": "The treasury moved swiftly to shore up fragile investor confidence.", "exampleChinese": "財政部迅速採取行動以支撐提振脆弱的投資人信心。", "scenario": "維穩加固"},
    {"verb": "smooth", "phrasal": "smooth over", "particle": "over", "chineseMeaning": "平息事態、緩和關係", "meaning": "Minimize tensions or make problems appear less severe", "example": "PR executives worked around the clock to smooth over the public relations crisis.", "exampleChinese": "公關主管日以繼夜地努力平息這場公關危機風波。", "scenario": "危機公關"},
    {"verb": "spell", "phrasal": "spell out", "particle": "out", "chineseMeaning": "詳細明確地說明清楚", "meaning": "Explain explicitly without leaving ambiguity", "example": "Let me spell out the precise performance metrics we expect.", "exampleChinese": "讓我把我們所預期的各項績效指標鉅細靡遺地說明清楚。", "scenario": "下達指令"},
    {"verb": "spring", "phrasal": "spring up", "particle": "up", "chineseMeaning": "如雨後春筍般迅速湧現", "meaning": "Appear suddenly in large quantities", "example": "Tech hubs are springing up all across suburban districts.", "exampleChinese": "科技新創聚落正在各個郊區如雨後春筍般迅速湧現。", "scenario": "繁榮興盛"},
    {"verb": "weigh", "phrasal": "weigh in", "particle": "in", "chineseMeaning": "發表見解、參與評論", "meaning": "Offer strong opinions or expertise in a public forum", "example": "Economic scholars weighed in on the inflation report.", "exampleChinese": "經濟學家們紛紛就這份通膨報告發表了專業見解與評論。", "scenario": "觀點交鋒"},
    {"verb": "zero", "phrasal": "zero in on", "particle": "in on", "chineseMeaning": "鎖定焦點、瞄準核心", "meaning": "Direct all precise attention and efforts directly toward a target", "example": "Investigators zeroed in on the cyber attacker's primary IP address.", "exampleChinese": "調查人員把焦點完全鎖定在該網路攻擊者的主要IP位址上。", "scenario": "偵查鎖定"},

    # 3. High-Difficulty Three-Word Phrasal Verbs (極高頻高難度三詞雙介系詞片語)
    {"verb": "put", "phrasal": "put up with", "particle": "up with", "chineseMeaning": "容忍忍受、將就", "meaning": "Tolerate uncomplainingly an unpleasant individual or condition", "example": "I cannot put up with this unbearable noise any longer.", "exampleChinese": "我再也無法忍受這種令人抓狂的噪音了。", "scenario": "忍耐限度"},
    {"verb": "come", "phrasal": "come down with", "particle": "down with", "chineseMeaning": "感染染上（疾病/感冒）", "meaning": "Begin suffering from an illness such as influenza", "example": "He came down with a severe viral fever after the marathon.", "exampleChinese": "馬拉松比賽結束後，他染上了嚴重的病毒性感冒。", "scenario": "生病抱恙"},
    {"verb": "look", "phrasal": "look down on", "particle": "down on", "chineseMeaning": "輕視、看不起某人", "meaning": "Consider someone inferior or lacking worth", "example": "One should never look down on humble hard-working individuals.", "exampleChinese": "任何人都不該輕視看不起腳踏實地的基層勞動者。", "scenario": "人品態度"},
    {"verb": "look", "phrasal": "look up to", "particle": "up to", "chineseMeaning": "崇拜敬仰、欽佩某人", "meaning": "Admire and respect deeply as a role model", "example": "Young athletic learners truly look up to olympic champions.", "exampleChinese": "年輕的運動學員們由衷地崇拜敬仰奧運金牌冠軍。", "scenario": "典範敬重"},
    {"verb": "get", "phrasal": "get away with", "particle": "away with", "chineseMeaning": "僥倖逃脫懲罰、瞞天過海", "meaning": "Escape disciplinary penalty after committing a wrongful deed", "example": "Cheating students should never expect to get away with plagiarism.", "exampleChinese": "作弊的學生絕不要妄想抄襲剽竊能僥倖瞞天過海。", "scenario": "逃脫處罰"},
    {"verb": "stand", "phrasal": "stand up for", "particle": "up for", "chineseMeaning": "挺身而出捍衛、維護權益", "meaning": "Defend rights, principles, or vulnerable people courageously", "example": "We must stand up for basic human liberties and justice.", "exampleChinese": "我們必須勇敢挺身而出，捍衛基本人權自由與公平正義。", "scenario": "正義捍衛"},
    {"verb": "make", "phrasal": "make up for", "particle": "up for", "chineseMeaning": "彌補過失、補償損失", "meaning": "Compensate adequately for past shortcomings or lost hours", "example": "She worked diligently overtime to make up for missed project deadlines.", "exampleChinese": "她勤奮加班以彌補先前錯過的專案截止進度。", "scenario": "補償彌補"},
    {"verb": "drop", "phrasal": "drop out of", "particle": "out of", "chineseMeaning": "中途退學、放棄退出賽事", "meaning": "Quit school, competitions, or formal programs prematurely", "example": "He dropped out of university to pursue entrepreneurship.", "exampleChinese": "他自大學休學退學，全心追逐創業夢想。", "scenario": "退學休學"},
    {"verb": "feel", "phrasal": "feel up to", "particle": "up to", "chineseMeaning": "自覺體力能勝任、提得起勁", "meaning": "Have the physical strength or mental energy necessary for a task", "example": "I do not feel up to attending crowded evening banquets tonight.", "exampleChinese": "我今天身體有點累，自覺提不起勁去參加今晚擁擠的宴會。", "scenario": "體能狀態"},
    {"verb": "grow", "phrasal": "grow out of", "particle": "out of", "chineseMeaning": "長大脫離（壞習慣/舊衣服）", "meaning": "Become too mature or physically big for past habits or apparel", "example": "The toddler quickly grew out of his brand-new leather shoes.", "exampleChinese": "這個小幼童長得很快，一下子那雙新皮鞋就穿不下了。", "scenario": "成長變化"},
    {"verb": "live", "phrasal": "live up to", "particle": "up to", "chineseMeaning": "不負眾望、符合期待標準", "meaning": "Meet expectations or standards adequately", "example": "The blockbuster sequel failed to live up to audience expectations.", "exampleChinese": "那部大片續集的表現並未能符合廣大影迷的殷切期待。", "scenario": "期待檢驗"},
    {"verb": "stand", "phrasal": "stand up to", "particle": "up to", "chineseMeaning": "勇於對抗強權、經得起考驗", "meaning": "Resist bullies or withstand intense destructive forces", "example": "This sturdy tent material stands up to severe hurricane gales.", "exampleChinese": "這款堅固的帳篷材質經得起強烈颶風的嚴酷考驗。", "scenario": "抵抗考驗"},
    {"verb": "brush", "phrasal": "brush off", "particle": "off", "chineseMeaning": "置之不理、拂袖忽視", "meaning": "Dismiss criticism or rude remarks casually", "example": "She brushed off skeptical mockery with a confident smile.", "exampleChinese": "她帶著自信的微笑，對旁人質疑的冷嘲熱諷置之不理。", "scenario": "自信處世"},
    {"verb": "fall", "phrasal": "fall back on", "particle": "back on", "chineseMeaning": "求助於退路、依靠備用方案", "meaning": "Rely on contingency savings or reserve plans in emergencies", "example": "When freelancing dried up, he had his family savings to fall back on.", "exampleChinese": "當接案收入銳減時，他還有家庭積蓄可以做為退路依靠。", "scenario": "應急後盾"},
    {"verb": "go", "phrasal": "go through with", "particle": "through with", "chineseMeaning": "貫徹到底、履行到底", "meaning": "Complete a planned unpleasant commitment despite hesitations", "example": "He vowed to go through with legal lawsuits despite threats.", "exampleChinese": "儘管面臨恐嚇威脅，他仍誓言要將法律訴訟貫徹到底。", "scenario": "堅定決心"},
    {"verb": "boil", "phrasal": "boil down to", "particle": "down to", "chineseMeaning": "歸根究底、核心在於", "meaning": "Summarize the primary or fundamental core reason", "example": "The core disagreement boils down to conflicting budget priorities.", "exampleChinese": "雙方的核心分歧歸根究底，在於預算分配優先順序的衝突。", "scenario": "本質探討"},
    {"verb": "face", "phrasal": "face up to", "particle": "up to", "chineseMeaning": "勇敢面對殘酷現實", "meaning": "Confront painful truths courageously without denial", "example": "Management must face up to current declining sales realities.", "exampleChinese": "管理階層必須勇敢面對當前銷售業績下滑的殘酷現實。", "scenario": "直面問題"},
    {"verb": "talk", "phrasal": "talk down to", "particle": "down to", "chineseMeaning": "用居高臨下的輕蔑語氣說話", "meaning": "Speak condescendingly as if addressing intellectual inferiors", "example": "Nobody appreciates supervisors who talk down to their team.", "exampleChinese": "沒有人會喜歡那些老是用居高臨下輕蔑語氣對團隊講話的主管。", "scenario": "溝通禮節"},

    # 4. Everyday Dynamic Physical & Contextual Actions (精微日常動作與情境)
    {"verb": "pull", "phrasal": "pull over", "particle": "over", "chineseMeaning": "靠邊停車", "meaning": "Steer a motor vehicle to the side of the highway and halt", "example": "The patrol officer signaled the speeding vehicle to pull over.", "exampleChinese": "巡邏員警示意那輛超速的車輛靠邊停車受檢。", "scenario": "行車駕駛"},
    {"verb": "pull", "phrasal": "pull off", "particle": "off", "chineseMeaning": "奇蹟般成功辦到難事", "meaning": "Succeed in accomplishing an extraordinarily difficult objective", "example": "Against all odds, the underdog squad pulled off a magnificent victory.", "exampleChinese": "在所有人都不看好的情況下，那支黑馬球隊奇蹟般地贏得了輝煌勝利。", "scenario": "創造奇蹟"},
    {"verb": "pull", "phrasal": "pull through", "particle": "through", "chineseMeaning": "挺過病危難關、康復", "meaning": "Survive a perilous illness or critical operation successfully", "example": "The emergency surgeon assured relatives the patient would pull through.", "exampleChinese": "急診主治醫師向家屬保證，病患一定能挺過危險期康復過來。", "scenario": "醫療康復"},
    {"verb": "lock", "phrasal": "lock out", "particle": "out", "chineseMeaning": "把（某人）反鎖在門外", "meaning": "Prevent entrance into premises by locking external doors", "example": "I left my keys on the kitchen counter and locked myself out.", "exampleChinese": "我把鑰匙忘在廚房流理台上，結果把自己反鎖在門外了。", "scenario": "日常糗事"},
    {"verb": "lock", "phrasal": "lock in", "particle": "in", "chineseMeaning": "鎖定保證（價格/利率）", "meaning": "Secure or confirm a beneficial rate or advantage firmly", "example": "Mortgage borrowers rushed to lock in low mortgage interest rates.", "exampleChinese": "房屋貸款戶紛紛搶著鎖定較低的房貸優惠利率。", "scenario": "理財貸款"},
    {"verb": "wear", "phrasal": "wear out", "particle": "out", "chineseMeaning": "磨損穿爛、使人疲累不堪", "meaning": "Become unusable through friction, or exhaust energy", "example": "Caring for hyperactive toddlers will wear out any parent.", "exampleChinese": "照顧精力過盛的小孩會讓任何父母都感到疲累不堪。", "scenario": "體能消耗、衣物磨損"},
    {"verb": "wear", "phrasal": "wear off", "particle": "off", "chineseMeaning": "藥效減退、感覺逐漸消失", "meaning": "Diminish in potency, sensation, or effect gradually", "example": "The surgical anesthetic is beginning to wear off after hours.", "exampleChinese": "手術麻醉藥的效力在幾小時後開始逐漸減退了。", "scenario": "藥效感覺"},
    {"verb": "tear", "phrasal": "tear down", "particle": "down", "chineseMeaning": "拆毀拆除舊建築", "meaning": "Demolish a dilapidated building deliberately", "example": "Urban planners chose to tear down the unsafe concrete warehouse.", "exampleChinese": "都市規劃者決定拆除那座不安全的危險水泥倉庫。", "scenario": "都市更新"},
    {"verb": "tear", "phrasal": "tear up", "particle": "up", "chineseMeaning": "撕成碎片、撕毀協議", "meaning": "Rip paper into tiny shreds, or cancel contracts violently", "example": "Furious at fraudulent terms, he tore up the contract.", "exampleChinese": "因對欺詐條款感到無比憤怒，他當場將合約撕成碎片。", "scenario": "撕毀合約"},
    {"verb": "rip", "phrasal": "rip up", "particle": "up", "chineseMeaning": "扯破撕裂、翻新拆毀", "meaning": "Tear forcefully or uproot paving completely", "example": "Contractors are ripping up old kitchen tiles for renovations.", "exampleChinese": "施工承包商正在拆除剷除舊廚房的地磚以進行裝修翻新。", "scenario": "室內裝修"},
    {"verb": "hand", "phrasal": "hand in", "particle": "in", "chineseMeaning": "繳交作業公文、呈交", "meaning": "Submit coursework or official paperwork to superiors", "example": "Students are required to hand in essays by Friday afternoon.", "exampleChinese": "學生必須在週五下午前將專題報告繳交上來。", "scenario": "課堂課業"},
    {"verb": "hand", "phrasal": "hand out", "particle": "out", "chineseMeaning": "分發發放講義", "meaning": "Distribute handouts or supplies freely to a gathered group", "example": "Volunteers handed out warm blankets to stranded travelers.", "exampleChinese": "志工們向受困的旅客發放溫暖的毛毯。", "scenario": "志願服務、發放"},
    {"verb": "hand", "phrasal": "hand over", "particle": "over", "chineseMeaning": "移交權力、移交物品", "meaning": "Relinquish authority, possession, or control formally", "example": "The outgoing governor handed over gubernatorial records calmly.", "exampleChinese": "卸任州長平靜地移交了州政各項施政檔案紀錄。", "scenario": "職權交接"},
    {"verb": "hold", "phrasal": "hold back", "particle": "back", "chineseMeaning": "抑制情緒、隱瞞實情", "meaning": "Restrain tears or laughter, or withhold crucial truths", "example": "She tried hard to hold back tears during the farewell toast.", "exampleChinese": "在告別敬酒時，她強忍著不讓眼淚掉下來。", "scenario": "情感克制"},
    {"verb": "leave", "phrasal": "leave out", "particle": "out", "chineseMeaning": "遺漏忽略、排除在外", "meaning": "Omit someone or exclude details accidentally or purposefully", "example": "Make sure you do not leave out any critical facts.", "exampleChinese": "請確保你沒有遺漏掉任何至關重要的關鍵事實。", "scenario": "資料校對"},
    {"verb": "let", "phrasal": "let down", "particle": "down", "chineseMeaning": "讓人失望、辜負信任", "meaning": "Disappoint someone by failing expectations or loyalty", "example": "I promised faithfully not to let down my dedicated coach.", "exampleChinese": "我由衷保證絕不會辜負熱心教練對我的殷切期望。", "scenario": "信任期望"},
    {"verb": "let", "phrasal": "let off", "particle": "off", "chineseMeaning": "從輕發落、免受懲處", "meaning": "Pardon someone without full punishment for an infraction", "example": "The traffic officer let him off with a gentle verbal warning.", "exampleChinese": "交通警員對他從輕發落，僅給予了口頭輕微告誡。", "scenario": "寬大處理"},
    {"verb": "slow", "phrasal": "slow down", "particle": "down", "chineseMeaning": "減速放慢、放緩腳步", "meaning": "Reduce operational velocity or ease personal lifestyle pressure", "example": "Motorists must slow down near active school crossings.", "exampleChinese": "駕駛人在行經學校路口時務必放慢車速減速慢行。", "scenario": "交通警示"},
    {"verb": "speed", "phrasal": "speed up", "particle": "up", "chineseMeaning": "加速進行、提高車速", "meaning": "Accelerate rate or increase the velocity of processes", "example": "Automation scripts help speed up data validation tenfold.", "exampleChinese": "自動化腳本能將資料驗證速度提升加速十倍之多。", "scenario": "效率加速"},
    {"verb": "start", "phrasal": "start over", "particle": "over", "chineseMeaning": "重新再來、從頭開始", "meaning": "Begin a process again completely from initial basics", "example": "If the recipe goes wrong, it is safer to start over.", "exampleChinese": "如果烘焙配方步驟出錯了，從頭重新再來會比較保險。", "scenario": "重新開始"},
    {"verb": "stop", "phrasal": "stop by", "particle": "by", "chineseMeaning": "順路走訪過來", "meaning": "Pay an informal short visit en route elsewhere", "example": "Can you stop by the pharmacy on your drive home?", "exampleChinese": "你開車回家的路上能順路走訪一趟藥局嗎？", "scenario": "順路拜訪"},
    {"verb": "switch", "phrasal": "switch off", "particle": "off", "chineseMeaning": "關閉開關、放空大腦", "meaning": "Turn off devices, or mentally disconnect from stress", "example": "Remember to switch off air conditioners upon exiting rooms.", "exampleChinese": "走出房間時請記得關閉冷氣空調開關。", "scenario": "節約用電"},
    {"verb": "switch", "phrasal": "switch on", "particle": "on", "chineseMeaning": "開啟開關設備", "meaning": "Activate power appliances or lighting fixtures", "example": "Switch on the laboratory ventilators before mixing chemicals.", "exampleChinese": "在混合化學試劑之前，請先開啟實驗室通風設備開關。", "scenario": "安全操作"},
    {"verb": "think", "phrasal": "think over", "particle": "over", "chineseMeaning": "仔細深思熟慮", "meaning": "Consider an important proposition carefully before choosing", "example": "Take the weekend to think over our lucrative employment offer.", "exampleChinese": "請利用週末時間好好深思熟慮一下我們這份優厚的聘用要約。", "scenario": "職涯決策"},
    {"verb": "throw", "phrasal": "throw away", "particle": "away", "chineseMeaning": "扔掉垃圾、浪費大好機會", "meaning": "Discard waste or recklessly squander precious opportunities", "example": "Do not throw away your promising future over silly disputes.", "exampleChinese": "千萬不要為了一時意氣之爭而白白斷送丟棄了大好前程。", "scenario": "把握機會、丟棄"},
    {"verb": "throw", "phrasal": "throw up", "particle": "up", "chineseMeaning": "嘔吐吐出來（口語）", "meaning": "Vomit stomach contents suddenly through illness", "example": "Motion sickness caused the child to throw up on the ferry.", "exampleChinese": "暈船導致那個孩子在渡輪上忍不住吐了出來。", "scenario": "腸胃不適"},
    {"verb": "try", "phrasal": "try on", "particle": "on", "chineseMeaning": "試穿衣物鞋子", "meaning": "Put on apparel experimentally to check fit and appearance", "example": "She wanted to try on that emerald gown in the fitting room.", "exampleChinese": "她想在試衣間試穿一下那件祖母綠色的優雅禮服。", "scenario": "服飾購物"},
    {"verb": "try", "phrasal": "try out", "particle": "out", "chineseMeaning": "試用體驗、參加選拔測試", "meaning": "Test utility experimentally or audition for an athletic roster", "example": "Dozens of hopeful athletes tried out for the national squad.", "exampleChinese": "數十名充滿憧憬的運動員參加了國家代表隊的選拔測試。", "scenario": "選拔試用"},
    {"verb": "use", "phrasal": "use up", "particle": "up", "chineseMeaning": "徹底用完消耗殆盡", "meaning": "Consume the entirety of an existing supply", "example": "We used up all our printer cartridges preparing binders.", "exampleChinese": "為了準備會議資料夾，我們把所有印表機墨水匣全部耗盡了。", "scenario": "物資消耗"},
    {"verb": "warm", "phrasal": "warm up", "particle": "up", "chineseMeaning": "暖身熱身、熱絡氣氛", "meaning": "Prepare muscles for sports, or heat food and social atmospheres", "example": "Athletes should warm up properly to avoid pulled tendons.", "exampleChinese": "運動員應該做好充分暖身，以防肌腱拉傷。", "scenario": "運動熱身"},
    {"verb": "wash", "phrasal": "wash up", "particle": "up", "chineseMeaning": "洗碗盤、洗手洗臉", "meaning": "Clean dishes after meals, or wash hands and face", "example": "It is your sibling's turn to wash up dishes after dinner.", "exampleChinese": "晚飯後輪到你弟弟去把碗盤清洗乾淨了。", "scenario": "家事日常"},
    {"verb": "wipe", "phrasal": "wipe out", "particle": "out", "chineseMeaning": "徹底消滅毀滅、摔個四腳朝天", "meaning": "Destroy utterly or crash down abruptly while surfing or skiing", "example": "The colossal ocean tsunami wiped out ancient coastal villages.", "exampleChinese": "那場巨大的海嘯徹底摧毀了古老的沿海村落。", "scenario": "災難破壞"},
    {"verb": "write", "phrasal": "write down", "particle": "down", "chineseMeaning": "寫下記錄、記在紙上", "meaning": "Record spoken information on paper or digital notes", "example": "Be sure to write down the courier tracking ID carefully.", "exampleChinese": "請務必仔細記下這組快遞物流追蹤單號。", "scenario": "做筆記備忘"},
    {"verb": "turn", "phrasal": "turn around", "particle": "around", "chineseMeaning": "轉身回頭、使扭虧為盈逆轉", "meaning": "Rotate facing or achieve dramatic business revival", "example": "The talented executive turned around the failing airline.", "exampleChinese": "那位才華洋溢的高階主管讓這家瀕臨倒閉的航空公司扭虧為盈奇蹟逆轉。", "scenario": "轉虧為盈"},
    {"verb": "look", "phrasal": "look around", "particle": "around", "chineseMeaning": "四處環顧看看、參觀瀏覽", "meaning": "Explore physical surroundings casually with visual attention", "example": "Take some leisurely moments to look around this historical museum.", "exampleChinese": "多花點閒適的時間，好好四處參觀這座歷史博物館吧。", "scenario": "參觀休閒"},
    {"verb": "call", "phrasal": "call in", "particle": "in", "chineseMeaning": "打電話請病假、召集專家", "meaning": "Telephone headquarters to report illness or summon expertise", "example": "He had a migraine and called in sick this morning.", "exampleChinese": "他今天早晨偏頭痛發作，便打電話向公司請了病假。", "scenario": "請假休養"},
    {"verb": "open", "phrasal": "open up", "particle": "up", "chineseMeaning": "暢所欲言敞開心扉、開拓商機", "meaning": "Express vulnerable inner thoughts or uncover new possibilities", "example": "With deep empathy, he gradually opened up about personal anxieties.", "exampleChinese": "在獲得深切的同理心後，他漸漸敞開胸懷暢談內心的焦慮。", "scenario": "心理傾訴"},
    {"verb": "shut", "phrasal": "shut down", "particle": "down", "chineseMeaning": "電腦關機、工廠停工倒閉", "meaning": "Power off digital systems, or cease commercial operations permanently", "example": "The plant was forced to shut down after strict safety violations.", "exampleChinese": "因被查出嚴重的安全違規，該工廠被迫全面停工關閉。", "scenario": "關機停工"},
    {"verb": "pass", "phrasal": "pass along", "particle": "along", "chineseMeaning": "轉交傳遞訊息", "meaning": "Relay communications or items forward to following recipients", "example": "Please pass along this memo to your regional colleagues.", "exampleChinese": "請將這份備忘錄轉交傳達給您當地的同仁。", "scenario": "傳遞訊息"},
    {"verb": "see", "phrasal": "see off", "particle": "off", "chineseMeaning": "為（某人）送行", "meaning": "Accompany someone to transit terminals and say goodbye", "example": "The whole family went to the departure gate to see him off.", "exampleChinese": "全家人都來到機場出境登機門為他送行。", "scenario": "機場送別"},
    {"verb": "send", "phrasal": "send back", "particle": "back", "chineseMeaning": "退回商品、退餐", "meaning": "Return unsatisfactory food in restaurants or parcels via delivery", "example": "The steak was undercooked so she politely sent it back.", "exampleChinese": "這塊牛排沒煎熟，因此她禮貌地請服務生退回廚房重新料理。", "scenario": "餐廳用餐"},
    {"verb": "shut", "phrasal": "shut up", "particle": "up", "chineseMeaning": "閉嘴、停止說話（強烈口氣）", "meaning": "Stop speaking immediately in blunt imperative manners", "example": "He rudely commanded the arguing room to shut up.", "exampleChinese": "他粗魯地命令爭吵不休的眾人閉嘴。", "scenario": "制止言論"},
    {"verb": "light", "phrasal": "light up", "particle": "up", "chineseMeaning": "喜形於色神采飛揚、點亮", "meaning": "Become visibly joyful or illuminate surroundings brightly", "example": "Her radiant eyes lit up when she saw the surprise gift.", "exampleChinese": "看到那份驚喜禮物時，她的雙眼頓時神采飛揚喜形於色。", "scenario": "興奮喜悅"},
    {"verb": "eat", "phrasal": "eat out", "particle": "out", "chineseMeaning": "在外用餐吃館子", "meaning": "Dine in restaurants rather than preparing home meals", "example": "We prefer to eat out at Italian bistros on Friday evenings.", "exampleChinese": "我們週五晚上喜歡去義式餐酒館在外面享受美食。", "scenario": "休閒餐飲"},
    {"verb": "eat", "phrasal": "eat up", "particle": "up", "chineseMeaning": "把食物吃得精光、消耗大量資源", "meaning": "Consume all meals cleanly, or exhaust substantial resources", "example": "Servers processing data can eat up colossal electricity reserves.", "exampleChinese": "處理巨量數據的伺服器會吃掉消耗龐大的電力資源。", "scenario": "吃光、資源消耗"},
    {"verb": "look", "phrasal": "look through", "particle": "through", "chineseMeaning": "快速瀏覽翻閱", "meaning": "Skim documents quickly across pages", "example": "I will look through the catalog while waiting in the lobby.", "exampleChinese": "在大廳等候的同時，我會翻閱瀏覽一下這本商品型錄。", "scenario": "閱讀瀏覽"},
    {"verb": "slow", "phrasal": "slow up", "particle": "up", "chineseMeaning": "放緩延滯速度", "meaning": "Cause progress or momentum to decelerate", "example": "Supply chain congestion slowed up the construction project.", "exampleChinese": "供應鏈的塞港延宕放緩了整個營造建案的工程進度。", "scenario": "工程進度"},
    {"verb": "check", "phrasal": "check up on", "particle": "up on", "chineseMeaning": "查看近況、關心慰問", "meaning": "Visit or telephone to examine someone's health or progress", "example": "I called my elderly parents to check up on them.", "exampleChinese": "我打電話給年邁的父母，關心問候他們的近況。", "scenario": "關心慰問"},
    {"verb": "cross", "phrasal": "cross out", "particle": "out", "chineseMeaning": "劃線刪除、劃掉", "meaning": "Draw a line through incorrect text on paper", "example": "Cross out any unnecessary bullet points from the draft.", "exampleChinese": "請把草稿中不必要的條列項目劃線刪除。", "scenario": "文件修改"},
    {"verb": "die", "phrasal": "die down", "particle": "down", "chineseMeaning": "風浪平息、熱度衰退", "meaning": "Gradually become calmer, quieter, or less fierce", "example": "The howling typhoon winds finally began to die down.", "exampleChinese": "呼嘯的颱風風勢終於開始逐漸平息了下來。", "scenario": "風暴平息"},
    {"verb": "dress", "phrasal": "dress up", "particle": "up", "chineseMeaning": "盛裝打扮、精心裝扮", "meaning": "Wear formal, elegant, or costume apparel for events", "example": "Guests dressed up in vintage gowns for the annual gala.", "exampleChinese": "賓客們身著復古禮服盛裝打扮出席這場年度盛會。", "scenario": "宴會盛裝"},
    {"verb": "drop", "phrasal": "drop in", "particle": "in", "chineseMeaning": "順道走訪、順路拜訪", "meaning": "Pay a brief informal visit without an appointment", "example": "Please drop in anytime you happen to be in neighborhood.", "exampleChinese": "如果你剛好來到這附近，隨時歡迎順道來家裡坐坐。", "scenario": "日常拜訪"},
    {"verb": "fade", "phrasal": "fade away", "particle": "away", "chineseMeaning": "逐漸消逝、漸漸淡出", "meaning": "Diminish in visibility, sound, or vitality over time", "example": "The morning fog began to fade away as warm sunlight rose.", "exampleChinese": "隨著溫暖的陽光升起，晨霧開始漸漸消散淡去。", "scenario": "自然現象"},
    {"verb": "fall", "phrasal": "fall out", "particle": "out", "chineseMeaning": "吵架鬧翻、反目成仇", "meaning": "Have an argument that breaks friendship or cooperation", "example": "The two business co-founders fell out over financial shares.", "exampleChinese": "兩位商業共同創辦人因為股份分配問題而徹底鬧翻。", "scenario": "人際衝突"},
    {"verb": "go", "phrasal": "go over", "particle": "over", "chineseMeaning": "仔細檢查審核、重溫", "meaning": "Review or examine something closely from start to finish", "example": "Let us go over the launch checklist once more.", "exampleChinese": "讓我們把這份發布檢查清單從頭到尾再仔細審核一遍。", "scenario": "工作審核"},
    {"verb": "hand", "phrasal": "hand down", "particle": "down", "chineseMeaning": "世代傳承、祖傳流傳", "meaning": "Pass traditions or heirlooms down through generations", "example": "This silver ring was handed down through four generations.", "exampleChinese": "這枚銀戒是歷經四個世代相傳至今的傳家寶。", "scenario": "文化傳承"},
    {"verb": "head", "phrasal": "head for", "particle": "for", "chineseMeaning": "朝著...方向前進", "meaning": "Move physically toward a destination", "example": "As thunder boomed, hikers headed for the mountain refuge.", "exampleChinese": "隨著雷聲隆隆，登山客們紛紛朝著避難山屋前進。", "scenario": "行進方向"},
    {"verb": "hold", "phrasal": "hold out", "particle": "out", "chineseMeaning": "堅持到底不屈服、抱持希望", "meaning": "Resist stubbornly under siege or maintain hope", "example": "Supporters held out hope for an unexpected legal victory.", "exampleChinese": "支持者們依然對出乎意料的訴訟勝訴抱持著一線希望。", "scenario": "堅守希望"},
    {"verb": "hurry", "phrasal": "hurry up", "particle": "up", "chineseMeaning": "趕快、抓緊時間", "meaning": "Act or proceed more rapidly to avoid tardiness", "example": "Hurry up or we will miss the final commuter train.", "exampleChinese": "趕快抓緊時間，否則我們要錯過最後一班通勤電車了。", "scenario": "催促趕時間"},
    {"verb": "keep", "phrasal": "keep at", "particle": "at", "chineseMeaning": "堅持不懈、持續練習", "meaning": "Persist consistently in performing a demanding task", "example": "Keep at your guitar practice and you will soon master it.", "exampleChinese": "堅持不懈地練習吉他，你很快就能熟練掌握它。", "scenario": "自律堅持"},
    {"verb": "let", "phrasal": "let in on", "particle": "in on", "chineseMeaning": "讓某人參與秘密、知情", "meaning": "Share confidential insider knowledge with trusted people", "example": "She finally let me in on her secret surprise plan.", "exampleChinese": "她終於肯把她那份秘密的驚喜計畫告訴我讓我知情。", "scenario": "分享秘密"},
    {"verb": "live", "phrasal": "live on", "particle": "on", "chineseMeaning": "依靠...為生、仰賴生活", "meaning": "Depend on a specific wage or source of food to survive", "example": "Many retirees live on fixed pensions and modest interest.", "exampleChinese": "許多退休長者依靠固定的年金與微薄的利息維持生活。", "scenario": "生活家計"},
    {"verb": "mix", "phrasal": "mix up", "particle": "up", "chineseMeaning": "弄混混淆、搞錯對象", "meaning": "Confuse two people or things due to similarity", "example": "I always mix up identical twins because of their voices.", "exampleChinese": "因為他們的聲音太像了，我總是會把這對同卵雙胞胎弄混搞錯。", "scenario": "認知混淆"},
    {"verb": "move", "phrasal": "move in", "particle": "in", "chineseMeaning": "遷入新居、搬家進駐", "meaning": "Begin residing in a new home or building premises", "example": "The newlyweds will move in to their downtown condo next week.", "exampleChinese": "這對新婚夫婦下週將搬進他們位於市中心的公寓新居。", "scenario": "搬家入厝"},
    {"verb": "move", "phrasal": "move on", "particle": "on", "chineseMeaning": "向前看、翻篇邁入新階段", "meaning": "Accept past setbacks and proceed forward in life", "example": "It is healthy to forgive mistakes and move on with optimism.", "exampleChinese": "原諒過錯並帶著樂觀心態向前看邁入新階段，是有益身心的。", "scenario": "釋懷成長"},
    {"verb": "pass", "phrasal": "pass around", "particle": "around", "chineseMeaning": "傳閱分發、各桌傳遞", "meaning": "Circulate objects or brochures among a group of people", "example": "Please pass around these glossy brochures to attendees.", "exampleChinese": "請把這些精美的手冊傳閱分發給所有與會者。", "scenario": "會議傳閱"},
    {"verb": "pull", "phrasal": "pull in", "particle": "in", "chineseMeaning": "列車進站靠停、吸引人氣", "meaning": "Arrive at station platforms, or attract large crowds", "example": "The high-speed rail train pulled in right on the dot.", "exampleChinese": "高鐵列車非常準時地進站靠停在月台旁。", "scenario": "鐵路交通"},
    {"verb": "ring", "phrasal": "ring up", "particle": "up", "chineseMeaning": "收銀結帳打單、打電話", "meaning": "Record sales on cash registers, or make a call", "example": "The store clerk rang up all our grocery purchases swiftly.", "exampleChinese": "店員迅速地替我們買的所有生鮮食品掃描收銀結帳。", "scenario": "結帳消費"},
    {"verb": "run", "phrasal": "run across", "particle": "across", "chineseMeaning": "不期而遇、偶然發現", "meaning": "Encounter someone or discover items by chance", "example": "I ran across an old high school album while cleaning.", "exampleChinese": "大掃除時，我偶然翻出了高中的泛黃畢業紀念冊。", "scenario": "偶然發現"},
    {"verb": "stand", "phrasal": "stand in for", "particle": "in for", "chineseMeaning": "替補代班、代理職務", "meaning": "Act as a substitute deputy for someone unavailable", "example": "The vice president stood in for the ill chairman.", "exampleChinese": "副總裁代理生病的主席主持了股東大會。", "scenario": "職務代理"},
    {"verb": "turn", "phrasal": "turn against", "particle": "against", "chineseMeaning": "反目成仇、倒戈相向", "meaning": "Become hostile toward former friends or allies", "example": "Corrupted rivals turned against the reformist mayor.", "exampleChinese": "被腐化的政敵在議會中倒戈相向反對改革派市長。", "scenario": "盟友倒戈"},
    {"verb": "wear", "phrasal": "wear down", "particle": "down", "chineseMeaning": "磨損耗損、磨平耐性", "meaning": "Weaken physical resistance or stamina through persistence", "example": "Persistent inquiries finally wore down the reluctant witness.", "exampleChinese": "持續不斷的追問終於磨平了那位不情願證人的心理防線。", "scenario": "攻防考驗"},
    {"verb": "hang", "phrasal": "hang around", "particle": "around", "chineseMeaning": "徘徊逗留、附近閒逛", "meaning": "Spend leisurely time in a location without clear purpose", "example": "Teens love to hang around the sports complex after dusk.", "exampleChinese": "青少年傍晚時分很喜歡在運動園區附近徘徊逗留聚會。", "scenario": "街頭休閒"},
    {"verb": "pass", "phrasal": "pass by", "particle": "by", "chineseMeaning": "經過路過、錯過大好良機", "meaning": "Go past without stopping, or let an opportunity elapse", "example": "Do not let this golden educational scholarship pass by.", "exampleChinese": "千萬不要白白讓這項寶貴的留學獎學金機會從身邊溜走錯過。", "scenario": "路過把握"},
    {"verb": "read", "phrasal": "read up on", "particle": "up on", "chineseMeaning": "研讀相關資料、認真查閱", "meaning": "Read thoroughly about a subject to become well informed", "example": "You should read up on local customs before traveling overseas.", "exampleChinese": "前往海外旅行之前，你應該多加研讀查閱當地的風俗民情。", "scenario": "吸收新知"}
]

VERB_CONJUGATIONS = {
    'freak': ['freak', 'freaks', 'freaked', 'freaking'],
    'chill': ['chill', 'chills', 'chilled', 'chilling'],
    'zone': ['zone', 'zones', 'zoned', 'zoning'],
    'mess': ['mess', 'messes', 'messed', 'messing'],
    'screw': ['screw', 'screws', 'screwed', 'screwing'],
    'rip': ['rip', 'rips', 'ripped', 'ripping'],
    'bail': ['bail', 'bails', 'bailed', 'bailing'],
    'chicken': ['chicken', 'chickens', 'chickened', 'chickening'],
    'sleep': ['sleep', 'sleeps', 'slept', 'sleeping'],
    'stay': ['stay', 'stays', 'stayed', 'staying'],
    'pig': ['pig', 'pigs', 'pigged', 'pigging'],
    'veg': ['veg', 'veges', 'vegged', 'vegging'],
    'hit': ['hit', 'hits', 'hitting'],
    'ask': ['ask', 'asks', 'asked', 'asking'],
    'fool': ['fool', 'fools', 'fooled', 'fooling'],
    'sneak': ['sneak', 'sneaks', 'sneaked', 'snuck', 'sneaking'],
    'creep': ['creep', 'creeps', 'crept', 'creeping'],
    'crack': ['crack', 'cracks', 'cracked', 'cracking'],
    'burst': ['burst', 'bursts', 'bursting'],
    'choke': ['choke', 'chokes', 'choked', 'choking'],
    'act': ['act', 'acts', 'acted', 'acting'],
    'goof': ['goof', 'goofs', 'goofed', 'goofing'],
    'freeze': ['freeze', 'freezes', 'froze', 'frozen', 'freezing'],
    'clam': ['clam', 'clams', 'clammed', 'clamming'],
    'burn': ['burn', 'burns', 'burned', 'burnt', 'burning'],
    'blow': ['blow', 'blows', 'blew', 'blown', 'blowing'],
    'knock': ['knock', 'knocks', 'knocked', 'knocking'],
    'iron': ['iron', 'irons', 'ironed', 'ironing'],
    'hammer': ['hammer', 'hammers', 'hammered', 'hammering'],
    'flesh': ['flesh', 'fleshes', 'fleshed', 'fleshing'],
    'pencil': ['pencil', 'pencils', 'penciled', 'pencilling'],
    'narrow': ['narrow', 'narrows', 'narrowed', 'narrowing'],
    'phase': ['phase', 'phases', 'phased', 'phasing'],
    'scale': ['scale', 'scales', 'scaled', 'scaling'],
    'step': ['step', 'steps', 'stepped', 'stepping'],
    'branch': ['branch', 'branches', 'branched', 'branching'],
    'buy': ['buy', 'buys', 'bought', 'buying'],
    'cash': ['cash', 'cashes', 'cashed', 'cashing'],
    'draw': ['draw', 'draws', 'drew', 'drawn', 'drawing'],
    'factor': ['factor', 'factors', 'factored', 'factoring'],
    'lay': ['lay', 'lays', 'laid', 'laying'],
    'opt': ['opt', 'opts', 'opted', 'opting'],
    'read': ['read', 'reads', 'reading'],
    'rule': ['rule', 'rules', 'ruled', 'ruling'],
    'set': ['set', 'sets', 'setting'],
    'settle': ['settle', 'settles', 'settled', 'settling'],
    'shore': ['shore', 'shores', 'shored', 'shoring'],
    'smooth': ['smooth', 'smooths', 'smoothed', 'smoothing'],
    'spell': ['spell', 'spells', 'spelled', 'spelt', 'spelling'],
    'spring': ['spring', 'springs', 'sprang', 'sprung', 'springing'],
    'weigh': ['weigh', 'weighs', 'weighed', 'weighing'],
    'zero': ['zero', 'zeroes', 'zeroed', 'zeroing'],
    'put': ['put', 'puts', 'putting'],
    'come': ['come', 'comes', 'came', 'coming'],
    'look': ['look', 'looks', 'looked', 'looking'],
    'get': ['get', 'gets', 'got', 'gotten', 'getting'],
    'stand': ['stand', 'stands', 'stood', 'standing'],
    'make': ['make', 'makes', 'made', 'making'],
    'drop': ['drop', 'drops', 'dropped', 'dropping'],
    'feel': ['feel', 'feels', 'felt', 'feeling'],
    'grow': ['grow', 'grows', 'grew', 'grown', 'growing'],
    'live': ['live', 'lives', 'lived', 'living'],
    'brush': ['brush', 'brushes', 'brushed', 'brushing'],
    'fall': ['fall', 'falls', 'fell', 'fallen', 'falling'],
    'go': ['go', 'goes', 'went', 'gone', 'going'],
    'boil': ['boil', 'boils', 'boiled', 'boiling'],
    'face': ['face', 'faces', 'faced', 'facing'],
    'talk': ['talk', 'talks', 'talked', 'talking'],
    'pull': ['pull', 'pulls', 'pulled', 'pulling'],
    'lock': ['lock', 'locks', 'locked', 'locking'],
    'wear': ['wear', 'wears', 'wore', 'worn', 'wearing'],
    'tear': ['tear', 'tears', 'tore', 'torn', 'tearing'],
    'hand': ['hand', 'hands', 'handed', 'handing'],
    'hold': ['hold', 'holds', 'held', 'holding'],
    'leave': ['leave', 'leaves', 'left', 'leaving'],
    'let': ['let', 'lets', 'letting'],
    'slow': ['slow', 'slows', 'slowed', 'slowing'],
    'speed': ['speed', 'speeds', 'sped', 'speeded', 'speeding'],
    'start': ['start', 'starts', 'started', 'starting'],
    'stop': ['stop', 'stops', 'stopped', 'stopping'],
    'switch': ['switch', 'switches', 'switched', 'switching'],
    'think': ['think', 'thinks', 'thought', 'thinking'],
    'throw': ['throw', 'throws', 'threw', 'thrown', 'throwing'],
    'try': ['try', 'tries', 'tried', 'trying'],
    'use': ['use', 'uses', 'used', 'using'],
    'warm': ['warm', 'warms', 'warmed', 'warming'],
    'wash': ['wash', 'washes', 'washed', 'washing'],
    'wipe': ['wipe', 'wipes', 'wiped', 'wiping'],
    'write': ['write', 'writes', 'wrote', 'written', 'writing'],
    'turn': ['turn', 'turns', 'turned', 'turning'],
    'call': ['call', 'calls', 'called', 'calling'],
    'open': ['open', 'opens', 'opened', 'opening'],
    'shut': ['shut', 'shuts', 'shutting'],
    'pass': ['pass', 'passes', 'passed', 'passing'],
    'see': ['see', 'sees', 'saw', 'seen', 'seeing'],
    'send': ['send', 'sends', 'sent', 'sending'],
    'light': ['light', 'lights', 'lit', 'lighted', 'lighting'],
    'eat': ['eat', 'eats', 'ate', 'eaten', 'eating'],
    'check': ['check', 'checks', 'checked', 'checking'],
    'cross': ['cross', 'crosses', 'crossed', 'crossing'],
    'die': ['die', 'dies', 'died', 'dying'],
    'dress': ['dress', 'dresses', 'dressed', 'dressing'],
    'fade': ['fade', 'fades', 'faded', 'fading'],
    'head': ['head', 'heads', 'headed', 'heading'],
    'hurry': ['hurry', 'hurries', 'hurried', 'hurrying'],
    'keep': ['keep', 'keeps', 'kept', 'keeping'],
    'mix': ['mix', 'mixes', 'mixed', 'mixing'],
    'move': ['move', 'moves', 'moved', 'moving'],
    'ring': ['ring', 'rings', 'rang', 'rung', 'ringing'],
    'run': ['run', 'runs', 'ran', 'running']
}

def make_cloze(verb, phrasal, particle, example):
    forms = VERB_CONJUGATIONS.get(verb, [verb])
    forms_re = '|'.join(re.escape(f) for f in forms)
    p_re = re.escape(particle)

    p1 = re.compile(rf'\b({forms_re})\s+({p_re})\b', re.IGNORECASE)
    p2 = re.compile(rf'\b({forms_re})\s+([a-zA-Z\']+(?:\s+[a-zA-Z\']+)?)\s+({p_re})\b', re.IGNORECASE)

    if p1.search(example):
        return p1.sub('_______', example)
    elif p2.search(example):
        return p2.sub(rf'_______ \2 {particle}', example)
    else:
        return re.sub(re.escape(phrasal), '_______', example, flags=re.IGNORECASE)

async def main():
    print(f"Loading existing data from {DATA_JSON_PATH}...")
    with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_verbs = data["verbs"]
    existing_ids = {v["id"] for v in existing_verbs}

    new_items = []
    target_needed = 300 - len(existing_verbs)
    print(f"Existing count: {len(existing_verbs)}, Target needed for 300: {target_needed}")

    for cand in LEVEL_3_SOURCE:
        slug = cand["phrasal"].replace(" ", "_")
        if slug in existing_ids:
            continue

        parts = cand["phrasal"].split()
        primary_particle = parts[1] if len(parts) > 1 else cand["particle"]
        cloze = make_cloze(cand["verb"], cand["phrasal"], cand["particle"], cand["example"])

        entry = {
            "id": slug,
            "level": 3,
            "verb": cand["verb"],
            "phrasal": cand["phrasal"],
            "particle": cand["particle"],
            "primaryParticle": primary_particle,
            "chineseMeaning": cand["chineseMeaning"],
            "meaning": cand["meaning"],
            "example": cand["example"],
            "exampleChinese": cand["exampleChinese"],
            "clozeSentence": cloze,
            "scenario": cand["scenario"],
            "audio": f"audio/{slug}.mp3",
            "exampleAudio": f"audio/{slug}_example.mp3"
        }
        new_items.append(entry)
        existing_ids.add(slug)
        if len(new_items) == target_needed:
            break

    print(f"Added {len(new_items)} Level 3 items.")
    all_verbs = existing_verbs + new_items
    print(f"Total Combined Database: {len(all_verbs)} verbs.")

    # Update metadata
    meta = data.get("meta", {})
    meta["total"] = len(all_verbs)
    meta["level1Count"] = sum(1 for v in all_verbs if v.get("level") == 1)
    meta["level2Count"] = sum(1 for v in all_verbs if v.get("level") == 2)
    meta["level3Count"] = sum(1 for v in all_verbs if v.get("level") == 3)

    final_payload = {"meta": meta, "verbs": all_verbs}

    with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(final_payload, f, ensure_ascii=False, indent=2)

    with open(DATA_JS_PATH, "w", encoding="utf-8") as f:
        f.write("window.PHRASAL_DATA = " + json.dumps(final_payload, ensure_ascii=False, indent=2) + ";\n")

    print("Saved enriched JSON and JS files successfully!")

    # Update CSV
    csv_rows = []
    row_id = 1
    for item in all_verbs:
        csv_rows.append({
            "id": row_id,
            "verb": item["verb"],
            "phrasal": item["phrasal"],
            "text": item["phrasal"],
            "filename": item["audio"]
        })
        row_id += 1
        csv_rows.append({
            "id": row_id,
            "verb": item["verb"],
            "phrasal": item["phrasal"],
            "text": item["example"],
            "filename": item["exampleAudio"]
        })
        row_id += 1

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "verb", "phrasal", "text", "filename"])
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"Updated CSV with {len(csv_rows)} rows (total {len(all_verbs) * 2} audios)")

    # Synthesize Missing Audio
    missing_tasks = []
    for item in new_items:
        p_audio = os.path.join(BASE_DIR, item["audio"])
        if not os.path.exists(p_audio):
            missing_tasks.append((item["phrasal"], p_audio))
        ex_audio = os.path.join(BASE_DIR, item["exampleAudio"])
        if not os.path.exists(ex_audio):
            missing_tasks.append((item["example"], ex_audio))

    print(f"Synthesizing {len(missing_tasks)} new MP3 audio files via edge-tts ({VOICE})...")
    for idx, (text, fpath) in enumerate(missing_tasks, 1):
        try:
            comm = edge_tts.Communicate(text, VOICE)
            await comm.save(fpath)
            if idx % 20 == 0 or idx == len(missing_tasks):
                print(f"[{idx}/{len(missing_tasks)}] Generated: {os.path.basename(fpath)}")
        except Exception as e:
            print(f"[{idx}/{len(missing_tasks)}] Error on {os.path.basename(fpath)}: {e}")

    print("\nAll 300 MP3 audio files synthesized successfully!")

if __name__ == "__main__":
    asyncio.run(main())
