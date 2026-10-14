import os

import streamlit as st
from google import genai
from google.genai import types

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = """You are a GST (Goods and Services Tax, India) assistant for small business owners
and students. Explain in simple, plain English with short examples. If you are unsure, or if the
answer depends on the latest notification or rate change, say so clearly and tell the user to
verify on the official GST portal (gst.gov.in) or with a Chartered Accountant. Never invent
section numbers, rates or deadlines. Keep answers concise."""

# Rate slabs change over time. Verify against the latest GST notifications before relying on them.
GST_RATES = [0, 5, 18, 40]


def get_client():
    key = os.getenv("GEMINI_API_KEY") or st.session_state.get("api_key")
    if not key:
        return None
    return genai.Client(api_key=key)


def ask_model(history, user_text=None):
    client = get_client()
    if client is None:
        return "Add your Gemini API key in the sidebar first."
    contents = [
        types.Content(role=m["role"], parts=[types.Part(text=m["text"])]) for m in history
    ]
    if user_text:
        contents.append(types.Content(role="user", parts=[types.Part(text=user_text)]))
    try:
        resp = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        return resp.text or "(empty response)"
    except Exception as e:
        return f"API error: {e}"


def calculate_gst(amount, rate, inclusive, inter_state):
    if inclusive:
        base = amount / (1 + rate / 100)
    else:
        base = amount
    tax = base * rate / 100
    result = {"Base amount": base, "Total GST": tax, "Invoice total": base + tax}
    if inter_state:
        result["IGST"] = tax
    else:
        result["CGST"] = tax / 2
        result["SGST"] = tax / 2
    return result


st.set_page_config(page_title="GST AI Assistant", page_icon="🧾")
st.title("🧾 GST AI Assistant")
st.caption("Mini project: AI-powered help for GST questions, built with Streamlit + Gemini.")

with st.sidebar:
    st.header("Setup")
    st.text_input("Gemini API key", type="password", key="api_key",
                  help="Free key from Google AI Studio. Or set GEMINI_API_KEY in your environment.")
    st.caption(f"Model: {MODEL}")
    st.warning("Educational tool only. Not tax or legal advice.")

tab_chat, tab_calc, tab_explain = st.tabs(["Ask GST", "Invoice calculator", "Explain simply"])

with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message("assistant" if m["role"] == "model" else "user"):
            st.write(m["text"])
    if prompt := st.chat_input("e.g. When do I need to register for GST?"):
        with st.chat_message("user"):
            st.write(prompt)
        with st.spinner("Thinking..."):
            answer = ask_model(st.session_state.messages, prompt)
        st.session_state.messages.append({"role": "user", "text": prompt})
        st.session_state.messages.append({"role": "model", "text": answer})
        with st.chat_message("assistant"):
            st.write(answer)

with tab_calc:
    st.subheader("GST calculator (no AI, plain maths)")
    amount = st.number_input("Amount (₹)", min_value=0.0, value=1000.0, step=100.0)
    rate = st.selectbox("GST rate (%)", GST_RATES, index=2)
    inclusive = st.checkbox("Amount already includes GST")
    inter_state = st.checkbox("Inter-state sale (IGST)")
    for label, value in calculate_gst(amount, rate, inclusive, inter_state).items():
        st.write(f"**{label}:** ₹{value:,.2f}")

with tab_explain:
    st.subheader("Paste GST text, get a plain-English explanation")
    text = st.text_area("Notice, clause or circular text", height=200)
    if st.button("Explain") and text.strip():
        with st.spinner("Explaining..."):
            st.write(ask_model([], "Explain this in simple words and list any action items:\n\n" + text))
