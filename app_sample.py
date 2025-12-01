import streamlit as st
from gtts import gTTS
from io import BytesIO
import time

# 設定頁面配置
st.set_page_config(
    page_title="簡易文字轉語音系統",
    page_icon="🎙️",
    layout="centered"
)

def text_to_speech(text, lang, slow):
    """
    將文字轉換為語音並回傳音訊位元組數據
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
    
    # 語言選擇字典
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
            # 呼叫轉換函式
            audio_bytes = text_to_speech(text_input, lang_code, slow_speed)
            
            # 模擬一點延遲讓體驗更流暢 (可選)
            time.sleep(0.5)

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