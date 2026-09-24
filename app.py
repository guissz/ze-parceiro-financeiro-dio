import os
import json
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Chave GEMINI_API_KEY não encontrada! Configure o arquivo .env.")
    st.stop()

client = genai.Client(api_key=api_key)

st.set_page_config(page_title="Assistente Financeiro - Gen Z", page_icon="💸", layout="centered")

st.title("💸 Zé - Parceiro Financeiro da Gen Z")
st.write("Seu parceiro para monitorar a grana sem julgamentos e sem burocracia.")

def carregar_dados():
    try:
        with open("data/transacoes.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"saldo_atual": 0.0, "transacoes": []}

def carregar_diretrizes():
    try:
        with open("data/diretrizes.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Você é um assistente financeiro amigável para a Geração Z."

dados_usuario = carregar_dados()
diretrizes_sistema = carregar_diretrizes()

system_instruction = f"""
{diretrizes_sistema}

DADOS ATUAIS DA CARTEIRA DO USUÁRIO (JSON):
{json.dumps(dados_usuario, ensure_ascii=False, indent=2)}
"""

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "model", 
        "parts": [{"text": "E aí! Acabei de chegar por aqui... Qual é a boa? Quanto tá a grana ou quer registrar um rolê pra gente começar?"}]
    })

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        for part in message["parts"]:
            st.markdown(part["text"])

if prompt := st.chat_input("Ex: Gastei 45 conto no iFood"):
    st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})
    with st.chat_message("user"):
        st.markdown(prompt)

    contents = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        for part in msg["parts"]:
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=part["text"])]))

    resposta_ia = None
    with st.spinner("Calculando a grana..."):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                ),
            )
            resposta_ia = response.text
        except Exception as e:
            resposta_ia = f"Ops, deu instabilidade no servidor agora há pouco. Tenta mandar a mensagem de novo! (Detalhe: {e})"

    with st.chat_message("model"):
        st.markdown(resposta_ia)
    
    st.session_state.messages.append({"role": "model", "parts": [{"text": resposta_ia}]})