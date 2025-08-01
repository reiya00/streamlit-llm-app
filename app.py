import streamlit as st
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# .envから環境変数を読み込む
load_dotenv()

# OpenAI APIキーの取得
openai_api_key = os.getenv("OPENAI_API_KEY")

# 専門家の種類とシステムメッセージ
experts = {
    "医療": "あなたは医療分野の専門家です。医学的な知識に基づいて回答してください。",
    "法律": "あなたは法律分野の専門家です。法的な観点から回答してください。",
    "IT": "あなたはIT分野の専門家です。技術的な観点から回答してください。"
}

# LLM応答関数
def get_llm_response(user_input, expert_type):
    system_message = experts.get(expert_type, "あなたは一般的な知識を持つAIです。")
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", user_input)
    ])
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)
    return llm(prompt.format())

# Streamlit UI
st.title("LLM専門家相談アプリ")
st.write("""
このWebアプリは、医療・法律・ITの専門家としてLLM（大規模言語モデル）に質問できるサービスです。
下の入力フォームに相談内容を入力し、専門家の種類を選択して送信してください。
""")

expert_type = st.radio("専門家の種類を選択してください", list(experts.keys()))
user_input = st.text_area("相談内容を入力してください")

if st.button("送信"):
    if not user_input:
        st.warning("相談内容を入力してください。")
    else:
        with st.spinner("回答を生成中..."):
            response = get_llm_response(user_input, expert_type)
        st.success("回答:")
        st.write(response)