import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 你好嗎？", 
    page_icon="🌟", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 (繽紛圖卡風格 🎨) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&family=Fredoka:wght@600&display=swap');

    /* 全局背景：活潑的圓點背景 */
    .stApp { 
        background-color: #FFF9C4;
        background-image: radial-gradient(#FFD54F 2px, transparent 2px);
        background-size: 30px 30px;
        font-family: 'Noto Sans TC', sans-serif;
    }
    
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }

    /* --- 1. 頂部 Hero 區塊 --- */
    .header-container {
        background: white;
        border-radius: 30px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 8px 0px #FFB300; /* 立體陰影 */
        border: 4px solid #FF6F00;
        margin-bottom: 30px;
        position: relative;
    }
    
    .main-title {
        font-family: 'Fredoka', sans-serif;
        color: #FF6F00;
        font-size: 40px;
        margin: 0;
        line-height: 1.2;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .sub-title {
        color: #5D4037;
        font-size: 20px;
        font-weight: 700;
        margin-top: 5px;
    }
    
    .teacher-tag {
        display: inline-block;
        background: #4DB6AC;
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: bold;
        margin-top: 15px;
        box-shadow: 0 4px 0 #00897B;
        font-size: 14px;
    }

    /* --- 2. 單字卡片 (重點設計) --- */
    .word-card {
        background: white;
        border-radius: 25px;
        padding: 15px 10px;
        text-align: center;
        border: 3px solid #FFF;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        height: 100%;
        margin-bottom: 15px;
        position: relative;
        overflow: hidden;
    }
    
    .word-card:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: #FFCA28;
    }
    
    /* 卡片頂部顏色條 */
    .card-top {
        height: 8px;
        width: 100%;
        background: #FFCA28;
        position: absolute;
        top: 0; left: 0;
    }

    .icon-box {
        font-size: 45px;
        margin-bottom: 5px;
        filter: drop-shadow(0 4px 4px rgba(0,0,0,0.1));
    }
    
    .amis-word {
        font-size: 18px;
        font-weight: 900;
        color: #3E2723;
        margin-bottom: 2px;
    }
    
    .zh-word {
        font-size: 14px;
        color: #8D6E63;
        font-weight: 500;
    }

    /* --- 3. 對話框設計 --- */
    .chat-box {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 8px solid #29B6F6;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
    }
    
    .chat-icon {
        font-size: 30px;
        margin-right: 15px;
        min-width: 40px;
        text-align: center;
    }
    
    .chat-content { flex-grow: 1; }
    
    .chat-amis {
        font-size: 18px;
        font-weight: 700;
        color: #0277BD;
    }
    
    .chat-zh {
        font-size: 15px;
        color: #78909C;
    }

    /* --- 4. 按鈕與 Tab --- */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(to bottom, #FFCA28 0%, #FFB300 100%);
        color: #5D4037 !important;
        font-weight: 900;
        border: none;
        box-shadow: 0 5px 0 #F57F17;
        padding: 10px 0;
        margin-top: 5px;
    }
    .stButton>button:active {
        box-shadow: none;
        transform: translateY(5px);
    }

    /* Tab 樣式 */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.8);
        border-radius: 50px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 40px;
        font-weight: bold;
        color: #8D6E63 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF6F00 !important;
        color: white !important;
    }
    
    /* 測驗區 */
    .quiz-card {
        background: white;
        padding: 30px;
        border-radius: 30px;
        text-align: center;
        border: 4px dashed #FFB74D;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 資料與圖示設定 (重點：加上 Emoji) ---

VOCABULARY = [
    {"amis": "kapah",       "zh": "好",           "emoji": "👍", "file": "v_kapah"},
    {"amis": "haw",         "zh": "嗎 (疑問)",     "emoji": "❓", "file": "v_haw"},
    {"amis": "kisu",        "zh": "你",           "emoji": "🫵", "file": "v_kisu"},
    {"amis": "maan",        "zh": "什麼",         "emoji": "🤔", "file": "v_maan"},
    {"amis": "dademakan",   "zh": "辦事情",       "emoji": "💼", "file": "v_dademakan"},
    {"amis": "misu",        "zh": "你(的)",       "emoji": "🎒", "file": "v_misu"},
    {"amis": "cima",        "zh": "誰",           "emoji": "👤", "file": "v_cima"},
    {"amis": "ngangan",     "zh": "名字",         "emoji": "📛", "file": "v_ngangan"},
    {"amis": "pina",        "zh": "多少",         "emoji": "🔢", "file": "v_pina"},
    {"amis": "pina tu",     "zh": "多少了",       "emoji": "📊", "file": "v_pinatu"},
    {"amis": "mihecaan",    "zh": "歲/年",        "emoji": "🎂", "file": "v_mihecaan"},
    {"amis": "hacuwa",      "zh": "何時",         "emoji": "📅", "file": "v_hacuwa"},
    {"amis": "remiad",      "zh": "天/日子",      "emoji": "☀️", "file": "v_remiad"},
    {"amis": "kasuvucan",   "zh": "生日",         "emoji": "🎁", "file": "v_kasuvucan"}, 
]

SENTENCES = [
    {"amis": "Kapah haw kisu?", "zh": "你好嗎？", "emoji": "👋", "file": "s_kapah_haw"},
    {"amis": "A u maan ku dademakan nu misu?", "zh": "你要辦什麼事？", "emoji": "📝", "file": "s_maan_dademakan"},
    {"amis": "Cima ku ngangan nu misu?", "zh": "你叫什麼名字？", "emoji": "🤝", "file": "s_cima_ngangan"},
    {"amis": "Pina tu ku mihecaan nu misu?", "zh": "你幾歲了?", "emoji": "🎂", "file": "s_pina_mihecaan"},
    {"amis": "Hacuwa a remiad ku kasuvucan nu misu?", "zh": "你的生日是何時？", "emoji": "🗓️", "file": "s_hacuwa_kasuvucan"},
]

QUIZ_DATA = [
    {"q": "Kapah ______ kisu?", "zh": "你好嗎？", "ans": "haw", "opts": ["haw", "maan", "cima"]},
    {"q": "A u ______ ku dademakan nu misu?", "zh": "你要辦什麼事？", "ans": "maan", "opts": ["maan", "hacuwa", "pina"]},
    {"q": "______ ku ngangan nu misu?", "zh": "你叫什麼名字？", "ans": "Cima", "opts": ["Cima", "Pina", "Hacuwa"]},
    {"q": "______ tu ku mihecaan nu misu?", "zh": "你幾歲了?", "ans": "Pina", "opts": ["Pina", "Cima", "Maan"]},
    {"q": "______ a remiad ku kasuvucan nu misu?", "zh": "你的生日是何時？", "ans": "Hacuwa", "opts": ["Hacuwa", "Pina", "Cima"]},
]

# --- 1.5 語音核心 ---
def play_audio(text, filename_base=None):
    if filename_base:
        for ext in ['mp3', 'm4a']:
            path = f"audio/{filename_base}.{ext}"
            if os.path.exists(path):
                st.audio(path, format=f'audio/{ext}')
                return
    try:
        tts = gTTS(text=text, lang='id') 
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇")

# --- 2. 隨機出題邏輯 ---
def init_quiz():
    st.session_state.score = 0
    st.session_state.current_q = 0
    
    # Q1
    q1_target = random.choice(VOCABULARY)
    others = [v for v in VOCABULARY if v['amis'] != q1_target['amis']]
    q1_options = random.sample(others, 2) + [q1_target]
    random.shuffle(q1_options)
    st.session_state.q1_data = {"target": q1_target, "options": q1_options}

    # Q2
    q2_data = random.choice(QUIZ_DATA)
    random.shuffle(q2_data['opts'])
    st.session_state.q2_data = q2_data

    # Q3
    q3_target = random.choice(SENTENCES)
    other_sentences = [s['zh'] for s in SENTENCES if s['zh'] != q3_target['zh']]
    q3_options = random.sample(other_sentences, 2) + [q3_target['zh']]
    random.shuffle(q3_options)
    st.session_state.q3_data = {"target": q3_target, "options": q3_options}

if 'q1_data' not in st.session_state:
    init_quiz()

# --- 3. 介面呈現 ---

def show_learning_mode():
    st.markdown("<h3 style='color:#5D4037; text-align:center; margin-bottom:20px;'>🌈 圖解單字卡</h3>", unsafe_allow_html=True)
    
    # 單字區：使用 3 欄位排版，讓卡片更緊湊可愛
    cols = st.columns(3)
    for idx, item in enumerate(VOCABULARY):
        with cols[idx % 3]:
            display_text = item['amis']
            if item['amis'] == "kasuvucan":
                display_text += "<br><span style='font-size:10px'>(kasubucan)</span>"
                
            st.markdown(f"""
            <div class="word-card">
                <div class="card-top"></div>
                <div class="icon-box">{item['emoji']}</div>
                <div class="amis-word">{display_text}</div>
                <div class="zh-word">{item['zh']}</div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(item['amis'], filename_base=item['file'])
            st.write("") # 間距
    
    st.markdown("---")
    st.markdown("<h3 style='color:#5D4037; text-align:center; margin-bottom:20px;'>💬 聊天練習</h3>", unsafe_allow_html=True)
    
    # 句子區
    for s in SENTENCES:
        st.markdown(f"""
        <div class="chat-box">
            <div class="chat-icon">{s['emoji']}</div>
            <div class="chat-content">
                <div class="chat-amis">{s['amis']}</div>
                <div class="chat-zh">{s['zh']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        play_audio(s['amis'], filename_base=s['file'])

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; color: #FF6F00;'>🏆 闖關挑戰</h3>", unsafe_allow_html=True)
    st.progress(st.session_state.current_q / 3)
    st.write("")

    # Q1
    if st.session_state.current_q == 0:
        data = st.session_state.q1_data
        target = data['target']
        
        st.markdown(f"""
        <div class="quiz-card">
            <div style="font-size:60px;">🔊</div>
            <h3>請聽語音，選出正確圖案</h3>
        </div>
        """, unsafe_allow_html=True)
        play_audio(target['amis'], filename_base=target['file'])
        
        st.write("")
        cols = st.columns(3)
        for idx, opt in enumerate(data['options']):
            with cols[idx]:
                if st.button(f"{opt['emoji']} {opt['zh']}", key=f"q1_{idx}"):
                    if opt['amis'] == target['amis']:
                        st.balloons()
                        st.success("Bingo! 答對了！")
                        time.sleep(1)
                        st.session_state.score += 1
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.error("再試一次！")

    # Q2
    elif st.session_state.current_q == 1:
        data = st.session_state.q2_data
        st.markdown(f"""
        <div class="quiz-card">
            <div style="font-size:60px;">🧩</div>
            <h3>句子填空</h3>
            <h2 style="color:#0277BD; background:#E1F5FE; padding:10px; border-radius:10px;">
                {data['q'].replace('______', '❓')}
            </h2>
            <p>{data['zh']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        ans = st.radio("請選擇缺少的字：", data['opts'])
        if st.button("送出答案"):
            if ans == data['ans']:
                st.balloons()
                st.success("太厲害了！")
                time.sleep(1)
                st.session_state.score += 1
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("加油！再想一下！")

    # Q3
    elif st.session_state.current_q == 2:
        data = st.session_state.q3_data
        target = data['target']
        st.markdown(f"""
        <div class="quiz-card">
            <div style="font-size:60px;">🎧</div>
            <h3>這句話是什麼意思？</h3>
        </div>
        """, unsafe_allow_html=True)
        play_audio(target['amis'], filename_base=target['file'])
        
        for opt in data['options']:
            if st.button(opt):
                if opt == target['zh']:
                    st.balloons()
                    st.success("恭喜通關！你是阿美語小天才！🎉")
                    time.sleep(1)
                    st.session_state.score += 1
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.error("再聽一次看看！")

    # 結算
    else:
        st.markdown(f"""
        <div class="quiz-card" style="border-color:#4DB6AC;">
            <h1 style='color: #FF6F00;'>🎉 挑戰成功！</h1>
            <p>你已經學會如何自我介紹了！</p>
            <div style='font-size: 80px; margin: 20px 0;'>🌟</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 再玩一次"):
            init_quiz()
            st.rerun()

# --- 4. 主程式 ---
def main():
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">Kapah haw kisu?</h1>
        <div class="sub-title">你好嗎？</div>
        <div class="teacher-tag">
            講師：胡美芳 &nbsp;|&nbsp; 教材提供者：胡美芳
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📖 學習模式", "🎮 測驗挑戰"])
    
    with tab1:
        show_learning_mode()
    
    with tab2:
        show_quiz_mode()

if __name__ == "__main__":
    main()
