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

def text_to_speech(text, lang, slow, tld='com'):
    """
    將文字轉換為語音並回傳音訊位元組數據
    tld: 頂級域名，不同域名有不同的聲音品質
    """
    try:
        # 初始化 gTTS 物件，使用 tld 參數可以獲得不同口音
        tts = gTTS(text=text, lang=lang, slow=slow, tld=tld)
        
        # 建立一個記憶體中的 BytesIO 物件來儲存音訊
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
    
    # 語言和口音選擇
    st.subheader("🌍 語言選擇")
    
    voice_options = {
        "中文 (台灣 🇹🇼)": ("zh", "com.tw"),
        "中文 (中國 🇨🇳)": ("zh-CN", "com"),
        "英文 (美國 🇺🇸)": ("en", "com"),
        "英文 (英國 🇬🇧)": ("en", "co.uk"),
        "英文 (澳洲 🇦🇺)": ("en", "com.au"),
        "英文 (印度 🇮🇳)": ("en", "co.in"),
        "日文 (🇯🇵)": ("ja", "co.jp"),
        "韓文 (🇰🇷)": ("ko", "co.kr"),
        "法文 (🇫🇷)": ("fr", "fr"),
        "德文 (🇩🇪)": ("de", "de"),
        "西班牙文 (🇪🇸)": ("es", "es"),
        "葡萄牙文 (🇧🇷)": ("pt", "com.br"),
    }
    
    selected_voice = st.selectbox(
        "選擇語言和口音",
        options=list(voice_options.keys()),
        help="不同地區的口音會有不同的聲音特色"
    )
    
    lang_code, tld_code = voice_options[selected_voice]
    
    # 語速設定
    st.subheader("🎚️ 語速控制")
    slow_speed = st.checkbox("🐌 慢速朗讀", help="適合學習語言時使用")

# 主要內容區
text_input = st.text_area(
    "請在下方輸入要轉換的文字：",
    height=200,
    placeholder="在此輸入您想聽到的文字..."
)

# 轉換按鈕與邏輯
if st.button("🔊 開始轉換", type="primary", use_container_width=True):
    if text_input.strip() == "":
        st.warning("⚠️ 請先輸入文字再進行轉換！")
    else:
        with st.spinner('🎵 正在生成語音...'):
            # 使用 gTTS 生成語音
            audio_bytes = text_to_speech(text_input, lang_code, slow_speed, tld_code)
            time.sleep(0.3)

        if audio_bytes:
            st.success("✅ 轉換成功！")
            
            # 顯示文字資訊
            col1, col2 = st.columns(2)
            with col1:
                st.metric("字數", len(text_input))
            with col2:
                st.metric("語言", selected_voice)
            
            # 播放音訊
            st.audio(audio_bytes, format='audio/mp3')
            
            # 提供下載按鈕
            st.download_button(
                label="📥 下載 MP3 檔案",
                data=audio_bytes,
                file_name=f"tts_{lang_code}_{int(time.time())}.mp3",
                mime="audio/mp3",
                use_container_width=True
            )
        else:
            st.error("❌ 轉換失敗，請檢查網路連接或稍後再試")

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