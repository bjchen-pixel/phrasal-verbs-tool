#!/usr/bin/env python3
"""
Add 58 Level 2 Phrasal Verbs to reach 150 total.
Generates cloze sentences, updates JSON & JS data, and synthesizes 116 MP3s using edge-tts.
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

# 58 Curated Level 2 Phrasal Verbs
LEVEL_2_VERBS = [
    {
        "verb": "pick", "phrasal": "pick up", "particle": "up",
        "chineseMeaning": "接電話、接送人、順便買、習得技能",
        "meaning": "Collect someone/something, answer a call, or learn casually",
        "example": "Can you pick up some milk on your way home?",
        "exampleChinese": "你回家的路上能順便買點牛奶嗎？",
        "scenario": "生活採買、接送"
    },
    {
        "verb": "figure", "phrasal": "figure out", "particle": "out",
        "chineseMeaning": "想通、弄明白、解決問題",
        "meaning": "Understand, solve, or find the answer to something",
        "example": "I'm trying to figure out how this machine works.",
        "exampleChinese": "我正在試著弄明白這台機器是怎麼運作的。",
        "scenario": "思考、解決難題"
    },
    {
        "verb": "hang", "phrasal": "hang out", "particle": "out",
        "chineseMeaning": "外出閒晃、聚聚聚會",
        "meaning": "Spend casual time relaxing with friends",
        "example": "We usually hang out at the local cafe on weekends.",
        "exampleChinese": "我們週末通常會在那家當地的咖啡廳聚聚消磨時間。",
        "scenario": "社交、休閒"
    },
    {
        "verb": "hang", "phrasal": "hang on", "particle": "on",
        "chineseMeaning": "稍等一下、堅持住",
        "meaning": "Wait a short time or hold tightly",
        "example": "Hang on a second, I will be right with you.",
        "exampleChinese": "稍等我一下，我馬上就來找你。",
        "scenario": "等待、短暫中斷"
    },
    {
        "verb": "hang", "phrasal": "hang up", "particle": "up",
        "chineseMeaning": "掛斷電話",
        "meaning": "End a telephone call by placing the receiver down",
        "example": "Please do not hang up before I explain everything.",
        "exampleChinese": "在我解釋完一切之前，請先別掛斷電話。",
        "scenario": "通訊聯絡"
    },
    {
        "verb": "hold", "phrasal": "hold on", "particle": "on",
        "chineseMeaning": "稍等片刻、撐住",
        "meaning": "Wait a short moment or endure a difficult situation",
        "example": "Hold on while I grab a pen to write this down.",
        "exampleChinese": "等我一下，我拿支筆把這個記下來。",
        "scenario": "電話、日常等待"
    },
    {
        "verb": "hold", "phrasal": "hold up", "particle": "up",
        "chineseMeaning": "延誤阻礙、支撐住",
        "meaning": "Delay progress or remain strong under pressure",
        "example": "Heavy morning traffic held us up for nearly an hour.",
        "exampleChinese": "早晨繁重的車流讓我們延誤了將近一個小時。",
        "scenario": "交通、進度受阻"
    },
    {
        "verb": "check", "phrasal": "check in", "particle": "in",
        "chineseMeaning": "辦理報到、入住手續",
        "meaning": "Register arrival at an airport, hotel, or clinic",
        "example": "We need to check in at the hotel before dinner.",
        "exampleChinese": "我們需要在吃晚餐前到飯店辦理入住手續。",
        "scenario": "飯店、機場旅行"
    },
    {
        "verb": "check", "phrasal": "check out", "particle": "out",
        "chineseMeaning": "退房結帳、去查看瞧瞧",
        "meaning": "Pay and leave a hotel, or inspect something interesting",
        "example": "You should definitely check out that new bookstore.",
        "exampleChinese": "你一定要抽空去瞧瞧那家新開的書店。",
        "scenario": "旅遊、探索新事物"
    },
    {
        "verb": "call", "phrasal": "call off", "particle": "off",
        "chineseMeaning": "取消活動或會議",
        "meaning": "Cancel an event, arrangement, or scheduled activity",
        "example": "They decided to call off the soccer match due to heavy rain.",
        "exampleChinese": "因為下大雨，他們決定取消這場足球比賽。",
        "scenario": "行程取消、會議"
    },
    {
        "verb": "call", "phrasal": "call back", "particle": "back",
        "chineseMeaning": "回電話",
        "meaning": "Return a phone call to someone later",
        "example": "I am in a meeting right now, so I will call you back later.",
        "exampleChinese": "我現在正在開會，稍後會回電話給你。",
        "scenario": "電話溝通"
    },
    {
        "verb": "show", "phrasal": "show up", "particle": "up",
        "chineseMeaning": "出席、到場現身",
        "meaning": "Arrive or appear at an appointed place",
        "example": "Only ten people showed up for the presentation.",
        "exampleChinese": "只有十個人出席了那場簡報說明會。",
        "scenario": "約會、會議出席"
    },
    {
        "verb": "show", "phrasal": "show off", "particle": "off",
        "chineseMeaning": "炫耀、賣弄顯擺",
        "meaning": "Display abilities or possessions to impress others",
        "example": "He likes to show off his expensive designer watch.",
        "exampleChinese": "他很喜歡炫耀他那支昂貴的名牌手錶。",
        "scenario": "社交行為"
    },
    {
        "verb": "drop", "phrasal": "drop by", "particle": "by",
        "chineseMeaning": "順道拜訪、順路來訪",
        "meaning": "Visit someone informally without making an appointment",
        "example": "Feel free to drop by my office whenever you have questions.",
        "exampleChinese": "你如果有任何問題，隨時歡迎順道來我的辦公室。",
        "scenario": "拜訪、人際往來"
    },
    {
        "verb": "drop", "phrasal": "drop off", "particle": "off",
        "chineseMeaning": "順路送達、把...放下",
        "meaning": "Deliver something or leave someone at a destination",
        "example": "I will drop you off at the MRT station.",
        "exampleChinese": "我順路送你到捷運站下車。",
        "scenario": "交通接送、送貨"
    },
    {
        "verb": "point", "phrasal": "point out", "particle": "out",
        "chineseMeaning": "指出錯誤、點出重點",
        "meaning": "Direct attention toward an important fact or mistake",
        "example": "The editor pointed out several minor typos in the article.",
        "exampleChinese": "編輯指出了文章中的幾處小拼字錯誤。",
        "scenario": "工作審查、討論"
    },
    {
        "verb": "pass", "phrasal": "pass out", "particle": "out",
        "chineseMeaning": "昏倒、失去知覺",
        "meaning": "Become unconscious suddenly, usually from heat or exhaustion",
        "example": "The room was so stuffy that she nearly passed out.",
        "exampleChinese": "房間裡太悶熱了，她差點暈倒過去。",
        "scenario": "健康急救"
    },
    {
        "verb": "pass", "phrasal": "pass away", "particle": "away",
        "chineseMeaning": "過世、逝世（委婉說法）",
        "meaning": "Polite euphemism meaning to die",
        "example": "His grandmother passed away peacefully in her sleep.",
        "exampleChinese": "他的祖母在睡夢中安詳離世。",
        "scenario": "悼念、生老病死"
    },
    {
        "verb": "watch", "phrasal": "watch out", "particle": "out",
        "chineseMeaning": "當心、小心注意",
        "meaning": "Be alert and cautious of potential danger",
        "example": "Watch out for fast-moving bicycles on the sidewalk.",
        "exampleChinese": "在人行道上要當心快速騎行的自行車。",
        "scenario": "安全警示"
    },
    {
        "verb": "follow", "phrasal": "follow up", "particle": "up",
        "chineseMeaning": "後續跟進、進一步追蹤",
        "meaning": "Take further action on something already started",
        "example": "I will follow up with the client early next week.",
        "exampleChinese": "我下週初會再向客戶做進一步的追蹤跟進。",
        "scenario": "職場工作、客戶服務"
    },
    {
        "verb": "reach", "phrasal": "reach out", "particle": "out",
        "chineseMeaning": "主動聯絡、接洽尋求合作",
        "meaning": "Contact someone to offer help, collaborate, or communicate",
        "example": "Please reach out to our support team if you encounter any bugs.",
        "exampleChinese": "如果您遇到任何問題，請隨時主動聯繫我們的支援團隊。",
        "scenario": "職場溝通、商務書信"
    },
    {
        "verb": "wrap", "phrasal": "wrap up", "particle": "up",
        "chineseMeaning": "圓滿結束、收尾工作",
        "meaning": "Conclude a meeting, project, or task successfully",
        "example": "Let us wrap up today's discussion and summarize action items.",
        "exampleChinese": "讓我們結束今天的討論，並總結後續執行項目。",
        "scenario": "會議主持、工作結案"
    },
    {
        "verb": "fill", "phrasal": "fill out", "particle": "out",
        "chineseMeaning": "填寫整份表格",
        "meaning": "Complete an application form by providing all required info",
        "example": "Every applicant must fill out this health questionnaire.",
        "exampleChinese": "每位申請人都必須完整填寫這份健康問卷。",
        "scenario": "行政手續、辦公"
    },
    {
        "verb": "fill", "phrasal": "fill in", "particle": "in",
        "chineseMeaning": "填補空格、臨時代班",
        "meaning": "Fill specific fields or temporarily replace an absent colleague",
        "example": "Can you fill in for Sarah while she is away on vacation?",
        "exampleChinese": "莎拉休假期間，你能替她代班一下嗎？",
        "scenario": "職場代班、填表"
    },
    {
        "verb": "sign", "phrasal": "sign up", "particle": "up",
        "chineseMeaning": "報名參加、註冊帳號",
        "meaning": "Enroll in an event, class, or register for a service",
        "example": "Hundreds of learners signed up for the free online workshop.",
        "exampleChinese": "數百名學員報名參加了這場免費的線上工作坊。",
        "scenario": "報名、帳號註冊"
    },
    {
        "verb": "sign", "phrasal": "sign off", "particle": "off",
        "chineseMeaning": "簽署批准、審核通過",
        "meaning": "Give official formal approval to conclude or release something",
        "example": "The executive director finally signed off on the new budget proposal.",
        "exampleChinese": "執行董事終於簽署核准了這項新預算提案。",
        "scenario": "主管核可、公文簽核"
    },
    {
        "verb": "roll", "phrasal": "roll out", "particle": "out",
        "chineseMeaning": "正式發布推行（新功能/產品）",
        "meaning": "Officially introduce a new system, product, or policy to users",
        "example": "The tech firm plans to roll out the updated mobile feature next month.",
        "exampleChinese": "這家科技公司計劃於下個月正式推出升級的手機新功能。",
        "scenario": "產品發布、政策推行"
    },
    {
        "verb": "work", "phrasal": "work on", "particle": "on",
        "chineseMeaning": "致力於、著手處理",
        "meaning": "Spend time and effort improving or developing something",
        "example": "Our engineering squad is working on a high-speed database engine.",
        "exampleChinese": "我們的工程團隊目前正致力於開發一款高速資料庫引擎。",
        "scenario": "專案開發、工作日常"
    },
    {
        "verb": "carry", "phrasal": "carry out", "particle": "out",
        "chineseMeaning": "落實執行、付諸實施",
        "meaning": "Perform, complete, or execute a planned task or experiment",
        "example": "Scientists carried out multiple tests to confirm the hypothesis.",
        "exampleChinese": "科學家們執行了多次測試以驗證該項假設。",
        "scenario": "研究試驗、專案執行"
    },
    {
        "verb": "carry", "phrasal": "carry on", "particle": "on",
        "chineseMeaning": "繼續進行、堅持下去",
        "meaning": "Continue doing something without pausing",
        "example": "Despite the noisy distractions, they carried on studying.",
        "exampleChinese": "儘管周遭噪音干擾，他們依然繼續堅持讀書。",
        "scenario": "學習日常、專注堅持"
    },
    {
        "verb": "stand", "phrasal": "stand out", "particle": "out",
        "chineseMeaning": "脫穎而出、格外引人注目",
        "meaning": "Be very noticeable, distinctive, or clearly superior",
        "example": "Her impressive public speaking skills made her stand out among candidates.",
        "exampleChinese": "她出色的公開演講能力讓她在眾多候選人中脫穎而出。",
        "scenario": "面試求職、才華展現"
    },
    {
        "verb": "stand", "phrasal": "stand by", "particle": "by",
        "chineseMeaning": "力挺支持、隨時待命",
        "meaning": "Support someone in difficult times, or remain ready for action",
        "example": "I will always stand by my teammates when challenges arise.",
        "exampleChinese": "每當挑戰來臨時，我總是會堅定地力挺我的隊友。",
        "scenario": "團隊支持、待命狀態"
    },
    {
        "verb": "calm", "phrasal": "calm down", "particle": "down",
        "chineseMeaning": "平靜下來、放鬆情緒",
        "meaning": "Become peaceful, quiet, or less agitated",
        "example": "Please take a deep slow breath and calm down.",
        "exampleChinese": "請緩緩深吸一口氣，讓自己平靜下來。",
        "scenario": "情緒調節"
    },
    {
        "verb": "settle", "phrasal": "settle down", "particle": "down",
        "chineseMeaning": "安定下來、定居生活",
        "meaning": "Begin living a stable, peaceful, and permanent routine",
        "example": "After wandering for years, he finally settled down in Canada.",
        "exampleChinese": "漂泊多年之後，他終於在加拿大安頓定居下來。",
        "scenario": "生活規劃、成家立業"
    },
    {
        "verb": "grow", "phrasal": "grow up", "particle": "up",
        "chineseMeaning": "長大成人、成熟成長",
        "meaning": "Develop from childhood into adulthood",
        "example": "I grew up in a quiet farming village surrounded by mountains.",
        "exampleChinese": "我在一個群山環繞的寧靜農村長大成人。",
        "scenario": "童年回憶、成長歷程"
    },
    {
        "verb": "fall", "phrasal": "fall apart", "particle": "apart",
        "chineseMeaning": "散架毀壞、心態崩潰",
        "meaning": "Break into pieces physically or fail completely emotionally",
        "example": "That worn-out leather wallet is beginning to fall apart.",
        "exampleChinese": "那個用得老舊的皮夾已經開始快散架了。",
        "scenario": "物品老化、心理壓力"
    },
    {
        "verb": "fall", "phrasal": "fall behind", "particle": "behind",
        "chineseMeaning": "落後進度、脫節",
        "meaning": "Fail to maintain the necessary pace or schedule",
        "example": "If you procrastinate on homework, you will fall behind quickly.",
        "exampleChinese": "如果你老是拖延功課，很快就會落後進度。",
        "scenario": "課業學習、工作效率"
    },
    {
        "verb": "pay", "phrasal": "pay off", "particle": "off",
        "chineseMeaning": "得到豐厚回報、清償債務",
        "meaning": "Yield good results after effort, or settle debt entirely",
        "example": "Your rigorous consistency will surely pay off in future examinations.",
        "exampleChinese": "你嚴謹持之以恆的努力，在未來的考試中必將得到回報。",
        "scenario": "努力成果、投資"
    },
    {
        "verb": "pay", "phrasal": "pay back", "particle": "back",
        "chineseMeaning": "還錢、償還人情",
        "meaning": "Return borrowed money or repay a kind favor",
        "example": "I promise to pay you back as soon as my wage arrives.",
        "exampleChinese": "我保證薪水一入帳就立刻把錢還你。",
        "scenario": "金錢借貸、人情往來"
    },
    {
        "verb": "cut", "phrasal": "cut down", "particle": "down",
        "chineseMeaning": "縮減用量、減少花費",
        "meaning": "Reduce the quantity or frequency of something consumed",
        "example": "The physician recommended that he cut down on sugary drinks.",
        "exampleChinese": "醫生建議他必須減少含糖飲料的攝取量。",
        "scenario": "健康生活、預算控管"
    },
    {
        "verb": "cut", "phrasal": "cut off", "particle": "off",
        "chineseMeaning": "切斷電源、阻絕通訊",
        "meaning": "Interrupt or disconnect a supply of electricity, water, or phone",
        "example": "The sudden earthquake cut off electrical supply to the entire district.",
        "exampleChinese": "突如其來的地震切斷了整個區域的電力供應。",
        "scenario": "意外災害、水電通訊"
    },
    {
        "verb": "end", "phrasal": "end up", "particle": "up",
        "chineseMeaning": "最終成為、落得...下場",
        "meaning": "Finally reach a specific place or state after a journey or process",
        "example": "We took a wrong highway exit and ended up in a strange town.",
        "exampleChinese": "我們下錯了公路交流道，結果最終來到了一座陌生小鎮。",
        "scenario": "意外走向、命運結果"
    },
    {
        "verb": "sort", "phrasal": "sort out", "particle": "out",
        "chineseMeaning": "梳理整理、妥善解決問題",
        "meaning": "Organize neatly or resolve a complicated difficulty",
        "example": "Give me ten minutes to sort out these messy sales receipts.",
        "exampleChinese": "給我十分鐘，讓我把這些凌亂的銷售發票整理好。",
        "scenario": "資料整理、排解紛爭"
    },
    {
        "verb": "blow", "phrasal": "blow up", "particle": "up",
        "chineseMeaning": "爆炸發作、大發雷霆",
        "meaning": "Explode violently or suddenly become furious with anger",
        "example": "He blew up when he discovered his computer files were deleted.",
        "exampleChinese": "當他發現自己的電腦檔案被刪除時，頓時大發雷霆。",
        "scenario": "脾氣爆發、物理爆炸"
    },
    {
        "verb": "burn", "phrasal": "burn out", "particle": "out",
        "chineseMeaning": "精疲力竭、身心俱疲燃盡",
        "meaning": "Become completely exhausted through chronic overwork and stress",
        "example": "Working excessive overtime without rest will make you burn out rapidly.",
        "exampleChinese": "過度加班而不休息，會讓你很快陷入身心俱疲的倦怠期。",
        "scenario": "職場過勞、心理健康"
    },
    {
        "verb": "cheer", "phrasal": "cheer up", "particle": "up",
        "chineseMeaning": "振作精神、開心起來",
        "meaning": "Become happier or cause someone to feel encouraged",
        "example": "We brought some warm chicken soup to cheer up our sick neighbor.",
        "exampleChinese": "我們帶了點熱雞湯去探望生病的鄰居，希望能讓他打起精神來。",
        "scenario": "安慰打氣、人情關懷"
    },
    {
        "verb": "count", "phrasal": "count on", "particle": "on",
        "chineseMeaning": "信賴仰賴、指望某人",
        "meaning": "Rely with certainty on someone for trustworthy support",
        "example": "You can always count on us whenever you face trouble.",
        "exampleChinese": "每當你遇到困難時，隨時都可以信賴依靠我們。",
        "scenario": "信任承諾、朋友相挺"
    },
    {
        "verb": "run", "phrasal": "run out of", "particle": "out of",
        "chineseMeaning": "用光耗盡（物資/時間）",
        "meaning": "Use up all of something so none remains available",
        "example": "The emergency clinic ran out of oxygen tanks during the blizzard.",
        "exampleChinese": "暴風雪期間，該急診診所的氧氣瓶全部消耗殆盡了。",
        "scenario": "資源告急、庫存短缺"
    },
    {
        "verb": "look", "phrasal": "look out for", "particle": "out for",
        "chineseMeaning": "留意警惕、照顧保護",
        "meaning": "Keep watch carefully for danger or look after someone's welfare",
        "example": "Older siblings should look out for younger ones at crowded amusement parks.",
        "exampleChinese": "在擁擠的遊樂園裡，哥哥姐姐應該要多加照顧年幼的弟妹。",
        "scenario": "照顧保護、小心周遭"
    },
    {
        "verb": "keep", "phrasal": "keep away from", "particle": "away from",
        "chineseMeaning": "遠離危險、避開接觸",
        "meaning": "Maintain a safe physical distance from hazards",
        "example": "Hikers are advised to keep away from unstable cliffs during rains.",
        "exampleChinese": "雨天時強烈建議登山客遠離鬆動不穩定的懸崖邊緣。",
        "scenario": "戶外安全、警告指示"
    },
    {
        "verb": "back", "phrasal": "back up", "particle": "up",
        "chineseMeaning": "資料備份、背後力挺支持",
        "meaning": "Make a safety copy of data or provide confirming support",
        "example": "Always remember to back up your project code before system upgrades.",
        "exampleChinese": "在系統升級之前，切記務必備份您的專案原始碼。",
        "scenario": "資料安全、同事力挺"
    },
    {
        "verb": "back", "phrasal": "back down", "particle": "down",
        "chineseMeaning": "妥協讓步、放棄立場",
        "meaning": "Yield in a dispute or withdraw a strong demand",
        "example": "Neither side in the debate was willing to back down from its stance.",
        "exampleChinese": "辯論中的雙方都沒有任何一方願意從自己的立場妥協讓步。",
        "scenario": "談判博弈、爭端討論"
    },
    {
        "verb": "wind", "phrasal": "wind up", "particle": "up",
        "chineseMeaning": "最終落得...下場、收尾結束",
        "meaning": "Arrive at an unexpected final state, or conclude business",
        "example": "If you drive recklessly, you could wind up in hospital.",
        "exampleChinese": "如果你開車橫衝直撞，最終很可能會進醫院。",
        "scenario": "後果警告、終局收尾"
    },
    {
        "verb": "take", "phrasal": "take apart", "particle": "apart",
        "chineseMeaning": "拆解零件、分拆機器",
        "meaning": "Dismantle something into its individual separate components",
        "example": "The apprentice took the carburetor apart to clean every valve.",
        "exampleChinese": "學徒把化油器全部拆解開來，以便徹底清洗每個閥門。",
        "scenario": "機械修繕、硬體拆裝"
    },
    {
        "verb": "fall", "phrasal": "fall through", "particle": "through",
        "chineseMeaning": "計畫泡湯、協議破局",
        "meaning": "Fail to occur or collapse before final execution",
        "example": "The real estate deal fell through because financing was denied.",
        "exampleChinese": "這筆房地產交易因銀行貸款未獲核准而最終告吹泡湯。",
        "scenario": "合約破局、商務挫折"
    },
    {
        "verb": "catch", "phrasal": "catch up", "particle": "up",
        "chineseMeaning": "趕上進度、敘舊聊近況",
        "meaning": "Reach the same level as others or exchange recent news",
        "example": "Let us have coffee tomorrow afternoon and catch up on our lives.",
        "exampleChinese": "我們明天下午喝杯咖啡，好好聊聊近況敘敘舊吧。",
        "scenario": "朋友敘舊、學業趕超"
    },
    {
        "verb": "give", "phrasal": "give in", "particle": "in",
        "chineseMeaning": "屈服讓步、投降認輸",
        "meaning": "Cease fighting or resisting; agree under relentless persuasion",
        "example": "After lengthy crying, parents gave in and bought the toy.",
        "exampleChinese": "在孩子漫長的哭鬧後，父母最終還是妥協讓步買下了那個玩具。",
        "scenario": "堅持或退讓"
    },
    {
        "verb": "stick", "phrasal": "stick to", "particle": "to",
        "chineseMeaning": "堅持到底、恪守承諾",
        "meaning": "Adhere firmly to a plan, routine, diet, or promise",
        "example": "If you truly want noticeable fitness gains, stick to your training schedule.",
        "exampleChinese": "如果你真心渴望顯著的健身成效，請務必恪守你的訓練日程。",
        "scenario": "自律堅持、承諾履行"
    }
]

# Verb Conjugations for cloze sentences
VERB_FORMS = {
    'pick': ['pick', 'picks', 'picked', 'picking'],
    'figure': ['figure', 'figures', 'figured', 'figuring'],
    'hang': ['hang', 'hangs', 'hung', 'hanged', 'hanging'],
    'hold': ['hold', 'holds', 'held', 'holding'],
    'check': ['check', 'checks', 'checked', 'checking'],
    'call': ['call', 'calls', 'called', 'calling'],
    'show': ['show', 'shows', 'showed', 'shown', 'showing'],
    'drop': ['drop', 'drops', 'dropped', 'dropping'],
    'point': ['point', 'points', 'pointed', 'pointing'],
    'pass': ['pass', 'passes', 'passed', 'passing'],
    'watch': ['watch', 'watches', 'watched', 'watching'],
    'follow': ['follow', 'follows', 'followed', 'following'],
    'reach': ['reach', 'reaches', 'reached', 'reaching'],
    'wrap': ['wrap', 'wraps', 'wrapped', 'wrapping'],
    'fill': ['fill', 'fills', 'filled', 'filling'],
    'sign': ['sign', 'signs', 'signed', 'signing'],
    'roll': ['roll', 'rolls', 'rolled', 'rolling'],
    'work': ['work', 'works', 'worked', 'working'],
    'carry': ['carry', 'carries', 'carried', 'carrying'],
    'stand': ['stand', 'stands', 'stood', 'standing'],
    'calm': ['calm', 'calms', 'calmed', 'calming'],
    'settle': ['settle', 'settles', 'settled', 'settling'],
    'grow': ['grow', 'grows', 'grew', 'grown', 'growing'],
    'fall': ['fall', 'falls', 'fell', 'fallen', 'falling'],
    'pay': ['pay', 'pays', 'paid', 'paying'],
    'cut': ['cut', 'cuts', 'cutting'],
    'end': ['end', 'ends', 'ended', 'ending'],
    'sort': ['sort', 'sorts', 'sorted', 'sorting'],
    'blow': ['blow', 'blows', 'blew', 'blown', 'blowing'],
    'burn': ['burn', 'burns', 'burned', 'burnt', 'burning'],
    'cheer': ['cheer', 'cheers', 'cheered', 'cheering'],
    'count': ['count', 'counts', 'counted', 'counting'],
    'run': ['run', 'runs', 'ran', 'running'],
    'look': ['look', 'looks', 'looked', 'looking'],
    'keep': ['keep', 'keeps', 'kept', 'keeping'],
    'back': ['back', 'backs', 'backed', 'backing'],
    'wind': ['wind', 'winds', 'wound', 'winding'],
    'take': ['take', 'takes', 'took', 'taken', 'taking'],
    'catch': ['catch', 'catches', 'caught', 'catching'],
    'give': ['give', 'gives', 'gave', 'given', 'giving'],
    'stick': ['stick', 'sticks', 'stuck', 'sticking']
}

def make_cloze(verb, phrasal, particle, example):
    forms = VERB_FORMS.get(verb, [verb])
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
    print(f"Loading existing dataset from {DATA_JSON_PATH}...")
    with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
        existing_data = json.load(f)

    existing_verbs = existing_data["verbs"]
    # Mark existing as Level 1
    for v in existing_verbs:
        v["level"] = 1

    existing_ids = {v["id"] for v in existing_verbs}

    # Format new Level 2 verbs
    new_items = []
    for item in LEVEL_2_VERBS:
        slug = item["phrasal"].replace(" ", "_")
        # Handle duplicates like 'give in' which already exists in level 1
        if slug in existing_ids:
            print(f"Skipping already existing {slug}")
            continue

        parts = item["phrasal"].split()
        primary_particle = parts[1] if len(parts) > 1 else item["particle"]
        cloze = make_cloze(item["verb"], item["phrasal"], item["particle"], item["example"])

        entry = {
            "id": slug,
            "level": 2,
            "verb": item["verb"],
            "phrasal": item["phrasal"],
            "particle": item["particle"],
            "primaryParticle": primary_particle,
            "chineseMeaning": item["chineseMeaning"],
            "meaning": item["meaning"],
            "example": item["example"],
            "exampleChinese": item["exampleChinese"],
            "clozeSentence": cloze,
            "scenario": item["scenario"],
            "audio": f"audio/{slug}.mp3",
            "exampleAudio": f"audio/{slug}_example.mp3"
        }
        new_items.append(entry)

    all_verbs = existing_verbs + new_items
    print(f"Existing Level 1 count: {len(existing_verbs)}")
    print(f"Added Level 2 count: {len(new_items)}")
    print(f"Total Combined Phrasal Verbs: {len(all_verbs)}")

    # Update particle metaphors for new particles like 'apart', 'behind'
    particles_meta = existing_data["meta"].get("particles", {})
    if "apart" not in particles_meta:
        particles_meta["apart"] = {"core": "分開散裂、獨立存在", "desc": "表示物理上的分開、破碎散架（fall apart）或將機器零件逐一拆解（take apart）。"}
    if "behind" not in particles_meta:
        particles_meta["behind"] = {"core": "落於後方、遺留積欠", "desc": "表示位置在後、進度落後於他人（fall behind）或把事情拋在腦後。"}
    if "to" not in particles_meta:
        particles_meta["to"] = {"core": "朝向附著、堅持恪守", "desc": "表示目標指向、或是堅守原則原則不放（stick to）。"}

    final_payload = {
        "meta": {
            "total": len(all_verbs),
            "level1Count": len(existing_verbs),
            "level2Count": len(new_items),
            "particles": particles_meta
        },
        "verbs": all_verbs
    }

    # Save JSON & JS
    with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(final_payload, f, ensure_ascii=False, indent=2)

    with open(DATA_JS_PATH, "w", encoding="utf-8") as f:
        f.write("window.PHRASAL_DATA = " + json.dumps(final_payload, ensure_ascii=False, indent=2) + ";\n")

    print("Saved enriched JSON and JS data!")

    # Update phrasal_verbs_audio.csv
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

    print(f"Synthesizing {len(missing_tasks)} new audio files using edge-tts ({VOICE})...")
    for idx, (text, fpath) in enumerate(missing_tasks, 1):
        try:
            comm = edge_tts.Communicate(text, VOICE)
            await comm.save(fpath)
            print(f"[{idx}/{len(missing_tasks)}] Generated: {os.path.basename(fpath)}")
        except Exception as e:
            print(f"[{idx}/{len(missing_tasks)}] Error on {os.path.basename(fpath)}: {e}")

    print("\nAll Level 2 audio files synthesized successfully!")

if __name__ == "__main__":
    asyncio.run(main())
