import os
import requests
import streamlit as st
from groq import Groq

# 画面の基本設定
st.title("🎙️ 深夜のAI観察室")
st.caption("テーマを入力すると、AIが自動で討論し音声を生成します。")

# テーマの入力フォーム
theme = st.text_input("ディスカッションテーマ", value="なぜ人間は『時間』に支配されているのか？")

if st.button("対話を生成して音声を聴く"):
    # SecretsからAPIキーを取得（安全な取得方法に変更）
    groq_api_key = st.secrets.get("GROQ_API_KEY")
    
    if not groq_api_key:
        st.error("GROQ_API_KEY がSecretsに設定されていません。")
    else:
        try:
            client = Groq(api_key=groq_api_key)

            # 会話の生成 (Groq API)
            with st.spinner("AIが対話を考案中..."):
                prompt = f"以下のテーマについて、NOVA(司会)、LOGOS(論理)、LUNA(感情)、ZERO(哲学)の4体で短く日本語で議論してください。テーマ: {theme}"
                
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                script_text = response.choices[0].message.content
                st.write("### 生成された台本")
                st.text(script_text)

            # 音声の合成 (Web版 VOICEVOX API)
            with st.spinner("音声を合成中..."):
                speaker_id = 1
                tts_url = f"https://api.ttsquest.app/v2/voicevox/synthesis?text={script_text[:100]}&speaker={speaker_id}"
                
                res = requests.get(tts_url).json()
                audio_url = res.get("retryAfterUrl") or res.get("mp3StreamingUrl")

            if audio_url:
                st.success("作成が完了しました！")
                st.audio(audio_url)
            else:
                st.error("音声の生成に失敗しました。")

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
