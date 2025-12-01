import streamlit as st
from gtts import gTTS
from io import BytesIO
import time
import edge_tts
import asyncio
import tempfile
import os

# 設定頁面配置
st.set_page_config(
    page_title="簡易文字轉語音系統",
    page_icon="🎙️",
    layout="centered"
)

async def text_to_speech_edge(text, voice, rate):
    """
    使用 Edge TTS 將文字轉換為語音（更自然）
    """
    try:
        # 建立臨時文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_path = tmp_file.name
        
        # 設定語速
        rate_str = f"{int((rate - 1) * 100):+d}%"
        
        # 生成語音
        communicate = edge_tts.Communicate(text, voice, rate=rate_str)
        await communicate.save(tmp_path)
        
        # 讀取文件
        with open(tmp_path, 'rb') as f:
            audio_bytes = f.read()
        
        # 刪除臨時文件
        os.unlink(tmp_path)
        
        return BytesIO(audio_bytes)
    except Exception as e:
        st.error(f"Edge TTS 轉換發生錯誤: {e}")
        return None

def text_to_speech(text, lang, slow):
    """
    將文字轉換為語音並回傳音訊位元組數據（使用 gTTS）
    """
    try:
        # 初始化 gTTS 物件
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # 建立一個記憶體中的 BytesIO 物件來儲存音訊，避免頻繁寫入硬碟
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        
        # 將指針重置到開頭
        mp3_fp.seek(0)
        return mp3_fp
    except Exception as e:
        st.error(f"轉換發生錯誤: {e}")
        return None

# --- 使用者介面 (UI) ---

st.title("🎙️ 文字轉語音轉換器 (TTS)")
st.markdown("輸入文字，選擇語言，即刻生成語音檔案！")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    
    # TTS 引擎選擇
    tts_engine = st.radio(
        "選擇 TTS 引擎",
        ["Edge TTS (推薦 - 更自然)", "gTTS (Google)"],
        help="Edge TTS 提供更自然的人聲"
    )
    
    if tts_engine.startswith("Edge"):
        # Edge TTS 語音選項（更自然的聲音）
        st.subheader("語音選擇")
        voice_options = {
            "中文女聲 (曉曉 - 活潑)": "zh-CN-XiaoxiaoNeural",
            "中文女聲 (曉伊 - 溫柔)": "zh-CN-XiaoyiNeural", 
            "中文男聲 (雲希 - 沉穩)": "zh-CN-YunxiNeural",
            "中文男聲 (雲陽 - 新聞)": "zh-CN-YunyangNeural",
            "台灣女聲 (曉臻)": "zh-TW-HsiaoChenNeural",
            "台灣男聲 (雲哲)": "zh-TW-YunJheNeural",
            "英文女聲 (Jenny - 美國)": "en-US-JennyNeural",
            "英文男聲 (Guy - 美國)": "en-US-GuyNeural",
            "英文女聲 (Sonia - 英國)": "en-GB-SoniaNeural",
        }
        
        selected_voice_label = st.selectbox(
            "選擇聲音",
            options=list(voice_options.keys())
        )
        voice_code = voice_options[selected_voice_label]
        
        # 語速設定
        speed_rate = st.slider("語速", 0.5, 2.0, 1.0, 0.1)
        
    else:
        # gTTS 語言選擇字典
        languages = {
            "中文 (台灣)": "zh-tw",
            "中文 (簡體)": "zh-cn",
            "英文 (美國)": "en",
            "日文": "ja",
            "韓文": "ko",
            "法文": "fr",
            "德文": "de"
        }
        
        selected_lang_label = st.selectbox(
            "選擇語言",
            options=list(languages.keys())
        )
        lang_code = languages[selected_lang_label]
        
        # 語速設定
        st.write("語速設定")
        slow_speed = st.checkbox("慢速朗讀 (Slow Mode)")

# 主要內容區
text_input = st.text_area(
    "請在下方輸入要轉換的文字：",
    height=200,
    placeholder="在此輸入您想聽到的文字..."
)

# 轉換按鈕與邏輯
if st.button("🔊 開始轉換", type="primary"):
    if text_input.strip() == "":
        st.warning("⚠️ 請先輸入文字再進行轉換！")
    else:
        with st.spinner('正在生成語音...'):
            if tts_engine.startswith("Edge"):
                # 使用 Edge TTS
                audio_bytes = asyncio.run(text_to_speech_edge(text_input, voice_code, speed_rate))
            else:
                # 使用 gTTS
                audio_bytes = text_to_speech(text_input, lang_code, slow_speed)
            
            # 模擬一點延遲讓體驗更流暢 (可選)
            time.sleep(0.3)

        if audio_bytes:
            st.success("✅ 轉換成功！")
            
            # 播放音訊
            st.audio(audio_bytes, format='audio/mp3')
            
            # 提供下載按鈕
            st.download_button(
                label="📥 下載 MP3 檔案",
                data=audio_bytes,
                file_name=f"tts_output_{int(time.time())}.mp3",
                mime="audio/mp3"
            )

# 頁尾資訊
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: small;'>
        Created with Streamlit & gTTS Library
    </div>
    """,
    unsafe_allow_html=True
)