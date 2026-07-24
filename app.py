import io
import streamlit as st
from groq import Groq
from gtts import gTTS

# 画面の基本設定
st.title("🎙️ 深夜のAI観察室")
st.caption("テーマを入力すると、AIが自動で討論し音声を生成します。")

# テーマの入力フォーム
theme = st.text_input("ディスカッションテーマ", value="なぜ人間は『時間』に支配されているのか？")

if st.button("対話を生成して音声を聴く"):
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

            # 音声の合成 (Google TTS)
            with st.spinner("音声を合成中..."):
                tts = gTTS(text=script_text, lang='ja')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)

            st.success("作成が完了しました！")
            st.audio(fp, format='audio/mp3')

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
