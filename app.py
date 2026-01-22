import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 你好嗎？", 
    page_icon="🌊", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 極致美化 (島嶼晨曦風格 🌅) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;500;700;900&family=Quicksand:wght@700&display=swap');

    /* 全局背景：柔和晨曦漸層 */
    .stApp { 
        background: linear-gradient(135deg, #FFF8F0 0%, #FFF3E0 100%); 
        font-family: 'Noto Sans TC', sans-serif;
    }
    
    .block-container { padding-top: 1.5rem !important; padding-bottom: 5rem !important; }

    /* --- 頂部 Hero 區塊 --- */
    .hero-card {
        background: linear-gradient(120deg, #FF7043 0%, #FF5722 100%);
        padding: 40px 30px;
        border-radius: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(255, 87, 34, 0.3);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    
    /* 裝飾性背景圓圈 */
    .hero-card::before {
        content: "";
        position: absolute;
        top: -50px; left: -50px;
        width: 150px; height: 150px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
    }
    .hero-card::after {
        content: "";
        position: absolute;
        bottom: -30px; right: -20px;
        width: 100px; height: 100px;
        background: rgba(255,255,255,0.15);
        border-radius: 50%;
    }

    .hero-title {
        font-family: 'Quicksand', sans-serif;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
        letter-spacing: 1px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .hero-subtitle {
        font-size: 18px;
        font-weight: 500;
        opacity: 0.95;
        margin-bottom: 20px;
    }
    
    .teacher-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(5px);
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 14px;
        font-weight: 500;
        border: 1px solid rgba(255,255,255,0.4);
    }

    /* --- 單字卡片設計 --- */
    .vocab-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #FF7043;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .vocab-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(255, 112, 67, 0.15);
    }
    
    .v-amis {
        font-size: 20px;
        font-weight: 700;
        color: #37474F;
        margin-bottom: 4px;
    }
    
    .v-zh {
        font-size: 14px;
        color: #90A4AE;
        font-weight: 500;
    }

    /* --- 對話框設計 --- */
    .dialog-box {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        border: 1px solid #FFF3E0;
        position: relative;
    }
    
    .dialog-header {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .avatar {
        width: 40px; height: 40px;
        background: #FFCCBC;
        color: #D84315;
        border-radius: 50%;
        display: flex; 
        align-items: center; 
        justify-content: center;
        font-weight: bold;
        margin-right: 12px;
        font-size: 18px;
    }
    
    .s-amis {
        font-size: 18px;
        font-weight: 700;
        color: #263238;
        line-height: 1.4;
    }
    
    .s-zh {
        font-size: 15px;
        color: #78909C;
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px dashed #ECEFF1;
    }

    /* --- 按鈕美化 --- */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        background: #37474F;
        color: white !important;
        border: none;
        padding: 12px 0;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background: #455A64;
        box-shadow: 0 4px 12px rgba(55, 71, 79, 0.3);
    }
    
    /* --- Tab 選單美化 --- */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #FFFFFF;
        padding: 5px;
        border-radius: 30px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-around;
        margin-bottom: 25px;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        text-align: center;
        border-radius: 25px;
        padding: 8px 0;
        color: #78909C !important;
        font-weight: 600;
        border: none !important;
        background: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FF7043 !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(255, 112, 67, 0.4);
    }
    
    /* 測驗區塊 */
    .quiz-container {
        background: white;
        padding: 30px;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據結構 ---

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
    {"amis": "kasuvucan",   "zh": "生日",         "file": "v_kasuvucan"}, 
]

SENTENCES = [
    {"amis": "Kapah haw kisu?", "zh": "你好嗎？", "file": "s_kapah_haw"},
    {"amis": "A u maan ku dademakan nu misu?", "zh": "你要辦什麼事？", "file": "s_maan_dademakan"},
    {"amis": "Cima ku ngangan nu misu?", "zh": "你叫什麼名字？", "file": "s_cima_ngangan"},
    {"amis": "Pina tu ku mihecaan nu misu?", "zh": "你幾歲了?", "file": "s_pina_mihecaan"},
    {"amis": "Hacuwa a remiad ku kasuvucan nu misu?", "zh": "你的生日是何時？", "file": "s_hacuwa_kasuvucan"},
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

# --- 3. 介面邏輯 ---

def show_learning_mode():
    st.markdown("<h4 style='color:#546E7A; margin-bottom:15px;'>📝 核心單字</h4>", unsafe_allow_html=True)
    
    # 單字區：精緻卡片 Grid
    cols = st.columns(2)
    for idx, item in enumerate(VOCABULARY):
        with cols[idx % 2]:
            display_text = item['amis']
            if item['amis'] == "kasuvucan":
                display_text += "<br><span style='font-size:12px; color:#B0BEC5'>(kasubucan)</span>"
                
            st.markdown(f"""
            <div class="vocab-card">
                <div class="v-amis">{display_text}</div>
                <div class="v-zh">{item['zh']}</div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(item['amis'], filename_base=item['file'])
    
    st.markdown("---")
    st.markdown("<h4 style='color:#546E7A; margin-bottom:15px;'>💬 生活會話</h4>", unsafe_allow_html=True)
    
    # 句子區：對話框設計
    for i, s in enumerate(SENTENCES):
        st.markdown(f"""
        <div class="dialog-box">
            <div class="dialog-header">
                <div class="avatar">{i+1}</div>
                <div class="s-amis">{s['amis']}</div>
            </div>
            <div class="s-zh">{s['zh']}</div>
        </div>
        """, unsafe_allow_html=True)
        play_audio(s['amis'], filename_base=s['file'])

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; color: #FF7043; margin-bottom: 20px;'>✨ 挑戰開始</h3>", unsafe_allow_html=True)
    st.progress(st.session_state.current_q / 3)
    st.write("")

    # Q1
    if st.session_state.current_q == 0:
        data = st.session_state.q1_data
        target = data['target']
        
        st.markdown(f"""
        <div class="quiz-container">
            <div style="font-size:40px; margin-bottom:10px;">👂</div>
            <h4 style="color:#37474F">請聽語音，選出正確意思</h4>
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
                        st.error("再試一次！")

    # Q2
    elif st.session_state.current_q == 1:
        data = st.session_state.q2_data
        st.markdown(f"""
        <div class="quiz-container">
            <div style="font-size:40px; margin-bottom:10px;">✍️</div>
            <h4 style="color:#37474F">句子填空</h4>
            <h2 style="color:#FF7043; margin: 15px 0;">{data['q'].replace('______', '___?___')}</h2>
            <p style="color:#90A4AE">{data['zh']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        ans = st.radio("請選擇：", data['opts'])
        if st.button("確認答案"):
            if ans == data['ans']:
                st.balloons()
                st.success("Correct! 答對了！")
                time.sleep(1)
                st.session_state.score += 1
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("加油，再想一下！")

    # Q3
    elif st.session_state.current_q == 2:
        data = st.session_state.q3_data
        target = data['target']
        st.markdown(f"""
        <div class="quiz-container">
            <div style="font-size:40px; margin-bottom:10px;">🗣️</div>
            <h4 style="color:#37474F">這句話是什麼意思？</h4>
        </div>
        """, unsafe_allow_html=True)
        play_audio(target['amis'], filename_base=target['file'])
        
        for opt in data['options']:
            if st.button(opt):
                if opt == target['zh']:
                    st.balloons()
                    st.success("太棒了！全部通關！🎉")
                    time.sleep(1)
                    st.session_state.score += 1
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.error("再聽一次看看！")

    # 結算
    else:
        st.markdown(f"""
        <div class="quiz-container">
            <h1 style='color: #FF7043 !important;'>🎉 挑戰成功！</h1>
            <p style='font-size: 18px; color: #546E7A;'>你已經學會自我介紹囉！</p>
            <div style='font-size: 80px; margin: 20px 0;'>🌟</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 再玩一次"):
            init_quiz()
            st.rerun()

# --- 4. 主程式 ---
def main():
    # Hero Header
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Kapah haw kisu?</div>
        <div class="hero-subtitle">你好嗎？</div>
        <div class="teacher-badge">
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
