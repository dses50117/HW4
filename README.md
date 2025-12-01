# 🎙️ 文字轉語音系統 (Text-to-Speech App)

一個基於 Streamlit 和 gTTS 的簡易文字轉語音網頁應用程式，支援多種語言的語音合成。

## ✨ 功能特色

- 🌍 支援多種語言（中文、英文、日文、韓文、法文、德文等）
- 🎧 即時播放語音
- 📥 下載 MP3 音檔
- ⚡ 簡潔直覺的使用介面
- 🐌 可選慢速朗讀模式

## 🚀 線上 Demo

部署在 Streamlit Cloud：
```
https://your-app-name.streamlit.app
```

## 📋 需求

- Python 3.8 或更高版本
- 網路連線（gTTS 需要連接 Google 服務）

## 🛠️ 安裝步驟

### 1. 克隆此專案

```bash
git clone https://github.com/your-username/text-to-speech-app.git
cd text-to-speech-app
```

### 2. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 3. 執行應用程式

```bash
streamlit run app.py
```

應用程式將在瀏覽器中自動開啟，預設網址為 `http://localhost:8501`

## 📦 專案結構

```
HW4/
├── app.py                      # 主要應用程式
├── requirements.txt            # Python 套件依賴
├── README.md                   # 專案說明文件
├── .gitignore                  # Git 忽略文件
├── .streamlit/                 # Streamlit 配置
│   └── config.toml            # 主題和設定
└── Dia_文字轉語音.ipynb        # 開發筆記本（可選）
```

## 💡 使用方法

1. 在文字框中輸入想要轉換的文字
2. 從側邊欄選擇語言
3. （可選）啟用慢速朗讀模式
4. 點擊「🔊 開始轉換」按鈕
5. 播放或下載生成的音檔

## 🌐 部署到 Streamlit Cloud

1. 將專案推送到 GitHub
2. 前往 [Streamlit Cloud](https://streamlit.io/cloud)
3. 使用 GitHub 帳號登入
4. 點擊「New app」
5. 選擇您的 repository、branch 和 `app.py`
6. 點擊「Deploy」

## 🔧 技術棧

- **Streamlit**: Web 應用框架
- **gTTS (Google Text-to-Speech)**: 文字轉語音引擎
- **Python**: 主要程式語言

## 📝 注意事項

- gTTS 需要網路連線，因為它使用 Google Translate TTS API
- 對於非常長的文字，可能需要較長的處理時間
- 生成的語音品質取決於 Google TTS 服務

## 🤝 貢獻

歡迎提出 Issue 或 Pull Request！

## 📄 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

您的名字

## 🙏 致謝

- [Streamlit](https://streamlit.io/) - 優秀的 Web 應用框架
- [gTTS](https://gtts.readthedocs.io/) - Google Text-to-Speech API 包裝器
