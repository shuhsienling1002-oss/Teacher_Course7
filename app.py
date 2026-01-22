import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 你好嗎？", 
    page_icon="👋", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺設計 (清爽薄荷對話風 🌿) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap');

    /* 全局背景：清爽的淡薄荷綠 */
    .stApp { 
        background: linear-gradient(180deg, #E0F2F1 0%, #FFFFFF 100%); 
        font-family: 'Noto Sans TC', sans-serif;
    }
    
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }
    
    /* 標題區域：現代極簡風 */
    .header-box {
        background-color: #00695C;
        color: white;
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 105, 92, 0.2);
    }
    
    h1 {
        color: white !important;
        font-weight: 700 !important;
        margin: 0 !important;
        font-size: 2.2rem !important;
    }
    
    .sub-info {
        background: rgba(255,255,255,0.2);
        display: inline-block;
        padding: 5px 15px;
        border-radius: 15px;
        margin-top: 10px;
        font-size: 0.9rem;
    }

    /* 單字膠囊樣式 */
    .vocab-pill {
        background: white;
        border-left: 5px solid #26A69A;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: transform 0.2s;
    }
    .vocab-pill:hover { transform: translateX(5px); }
    
    .vocab-amis { font-size: 18px; font-weight: 700; color: #004D40; }
    .vocab-zh { font-size: 14px; color: #555; }
    
    /* 對話氣泡樣式 (句子) */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    
    .chat-bubble {
        background: white;
        padding: 20px;
        border-radius: 20px 20px 20px 0;
        box-shadow: 0 3px 15px rgba(0,0,0,0.08);
        position: relative;
        border: 1px solid #E0F2F1;
    }
    
    .chat-avatar {
        font-size: 24px;
        margin-bottom: 5px;
    }
    
    .sentence-amis {
        font-size: 19px;
        font-weight: 700;
        color: #00796B;
        margin-bottom: 5px;
    }
    
    .sentence-zh {
        font-size: 15px;
        color: #757575;
        border-top: 1px dashed #B2DFDB;
        padding-top: 5px;
        margin-top: 5px;
    }

    /* 按鈕：清爽藍綠漸層 */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        font-size: 16px;
        font-weight: 600;
        background: linear-gradient(135deg, #26A69A 0%, #00897B 100%);
        color: white !important;
        border: none;
        padding: 10px 0;
        box-shadow: 0 4px 10px rgba(38, 166, 154, 0.3);
    }
    .stButton>button:hover {
        box-shadow: 0 6px 15px rgba(38, 166, 154, 0.5);
        transform: scale(1.01);
    }
    
    /* Tab 優化 */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 20px;
        padding: 10px 20px;
        color: #00695C !important;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00695C !important;
        color: white !important;
    }
    
    /* 測驗區塊 */
    .quiz-box {
        background: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border-top: 5px solid #26A69A;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據結構 ---

# 單字資料
VOCABULARY = [
    {"amis": "kapah",       "zh": "好",           "file": "v_kapah"},
    {"amis": "haw",         "zh": "嗎 (疑問詞)",   "file": "v_haw"},
    {"amis": "kisu",        "zh": "你",           "file": "v_kisu"},
    {"amis": "maan",        "zh": "什麼",         "file": "v_maan"},
    {"amis": "dademakan",   "zh": "辦事情/事項",   "file": "v_dademakan"},
    {"amis": "misu",        "zh": "你(的)",       "file": "v_misu"},
    {"amis": "cima",        "zh": "誰",           "file": "v_cima"},
    {"amis": "ngangan",     "zh": "名字",         "file": "v_ngangan"},
    {"amis": "pina",        "zh": "多少",         "file": "v_pina"},
    {"amis": "pina tu",     "zh": "多少了",       "file": "v_pinatu"},
    {"amis": "mihecaan",    "zh": "歲/年",        "file": "v_mihecaan"},
    {"amis": "hacuwa",      "zh": "何時",         "file": "v_hacuwa"},
    {"amis": "remiad",      "zh": "天/日子",      "file": "v_remiad"},
    {"amis": "kasuvucan",   "zh": "生日",         "file": "v_kasuvucan"}, # 顯示時可備註 kasubucan
]

# 句子資料
SENTENCES = [
    {"amis": "Kapah haw kisu?", "zh": "你好嗎？", "file": "s_kapah_haw"},
    {"amis": "A u maan ku dademakan nu misu?", "zh": "你要辦什麼事？", "file": "s_maan_dademakan"},
    {"amis": "Cima ku ngangan nu misu?", "zh": "你叫什麼名字？", "file": "s_cima_ngangan"},
    {"amis": "Pina tu ku mihecaan nu misu?", "zh": "你幾歲了?", "file": "s_pina_mihecaan"},
    {"amis": "Hacuwa a remiad ku kasuvucan nu misu?", "zh": "你的生日是何時？", "file": "s_hacuwa_kasuvucan"},
]

# 測驗題庫
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
        tts = gTTS(text=text, lang='id') # 使用印尼語模擬
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
    
    # Q1: 單字聽力
    q1_target = random.choice(VOCABULARY)
    others = [v for v in VOCABULARY if v['amis'] != q1_target['amis']]
    q1_options = random.sample(others, 2) + [q1_target]
    random.shuffle(q1_options)
    st.session_state.q1_data = {"target": q1_target, "options": q1_options}

    # Q2: 句子填空
    q2_data = random.choice(QUIZ_DATA)
    random.shuffle(q2_data['opts'])
    st.session_state.q2_data = q2_data

    # Q3: 句子翻譯
    q3_target = random.choice(SENTENCES)
    other_sentences = [s['zh'] for s in SENTENCES if s['zh'] != q3_target['zh']]
    q3_options = random.sample(other_sentences, 2) + [q3_target['zh']]
    random.shuffle(q3_options)
    st.session_state.q3_data = {"target": q3_target, "options": q3_options}

if 'q1_data' not in st.session_state:
    init_quiz()

# --- 3. 介面邏輯 ---

def show_learning_mode():
    st.markdown("### 💬 常用對話單字")
    
    # 單字區：使用 Grid + Pill 樣式
    cols = st.columns(2)
    for idx, item in enumerate(VOCABULARY):
        with cols[idx % 2]:
            display_text = item['amis']
            if item['amis'] == "kasuvucan":
                display_text += " (kasubucan)"
                
            st.markdown(f"""
            <div class="vocab-pill">
                <span class="vocab-amis">{display_text}</span>
                <span class="vocab-zh">{item['zh']}</span>
            </div>
            """, unsafe_allow_html=True)
            play_audio(item['amis'], filename_base=item['file'])
    
    st.markdown("---")
    st.markdown("### 🗣️ 對話練習")
    
    # 句子區：使用對話氣泡樣式
    for s in SENTENCES:
        st.markdown(f"""
        <div class="chat-bubble">
            <div class="chat-avatar">👤</div>
            <div class="sentence-amis">{s['amis']}</div>
            <div class="sentence-zh">{s['zh']}</div>
        </div>
        """, unsafe_allow_html=True)
        play_audio(s['amis'], filename_base=s['file'])
        st.write("") # Spacer

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; color: #00695C;'>🎯 小測驗</h3>", unsafe_allow_html=True)
    st.progress(st.session_state.current_q / 3)
    st.write("")

    # Q1: 單字聽力
    if st.session_state.current_q == 0:
        data = st.session_state.q1_data
        target = data['target']
        
        st.markdown(f"""
        <div class="quiz-box">
            <h4>👂 聽聽看，這是什麼意思？</h4>
            <p>請點擊播放按鈕</p>
        </div>
        """, unsafe_allow_html=True)
        play_audio(target['amis'], filename_base=target['file'])
        
        st.write("")
        cols = st.columns(3)
        for idx, opt in enumerate(data['options']):
            with cols[idx]:
                if st.button(opt['zh'], key=f"q1_{idx}"):
                    if opt['amis'] == target['amis']:
                        st.balloons()
                        st.success("答對了！")
                        time.sleep(1)
                        st.session_state.score += 1
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.error("再試試看！")

    # Q2: 句子填空
    elif st.session_state.current_q == 1:
        data = st.session_state.q2_data
        st.markdown(f"""
        <div class="quiz-box">
            <h4>✍️ 句子填空</h4>
            <h2 style="color:#00796B;">{data['q'].replace('______', '<span style="border-bottom:2px solid #FF5722; color:#FF5722;">______</span>')}</h2>
            <p>{data['zh']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        ans = st.radio("請選擇正確的單字：", data['opts'])
        if st.button("送出答案"):
            if ans == data['ans']:
                st.balloons()
                st.success("答對了！")
                time.sleep(1)
                st.session_state.score += 1
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("不對喔，再想一下！")

    # Q3: 句子翻譯
    elif st.session_state.current_q == 2:
        data = st.session_state.q3_data
        target = data['target']
        st.markdown(f"""
        <div class="quiz-box">
            <h4>🗣️ 這句話是什麼意思？</h4>
            <p>請聽語音</p>
        </div>
        """, unsafe_allow_html=True)
        play_audio(target['amis'], filename_base=target['file'])
        
        for opt in data['options']:
            if st.button(opt):
                if opt == target['zh']:
                    st.balloons()
                    st.success("太棒了！挑戰成功！🎉")
                    time.sleep(1)
                    st.session_state.score += 1
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.error("再聽一次看看！")

    # 結算
    else:
        st.markdown(f"""
        <div class="quiz-box">
            <h1 style='color: #00695C !important;'>🎉 完成挑戰！</h1>
            <p style='font-size: 18px;'>你已經學會基本的問候囉！</p>
            <div style='font-size: 60px; margin: 20px 0;'>👋</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 再玩一次"):
            init_quiz()
            st.rerun()

# --- 4. 主程式 ---
def main():
    # 標題區
    st.markdown("""
    <div class="header-box">
        <h1>Kapah haw kisu?</h1>
        <div style="font-size: 1.2rem; margin-top:5px;">你好嗎？</div>
        <div class="sub-info">講師：楊麗芳 | 教材提供者：楊麗芳</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📖 學習模式", "🎮 測驗挑戰"])
    
    with tab1:
        show_learning_mode()
    
    with tab2:
        show_quiz_mode()

if __name__ == "__main__":
    main()
