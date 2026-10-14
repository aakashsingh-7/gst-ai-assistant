# 🧾 GST AI Assistant

A small AI-powered web app that helps with GST (India) questions. Built as a mini project for Module 5 (AI Tools & Mini Project).

## Features
- **Ask GST:** chat assistant for GST questions, answered in simple language with a built-in safety prompt (it says when it is unsure and points to official sources).
- **Invoice calculator:** deterministic GST maths, with inclusive/exclusive pricing and CGST+SGST vs IGST split.
- **Explain simply:** paste a notice or clause and get a plain-English summary with action items.

## Tech stack
Python · Streamlit · Google Gemini API (`google-genai`)

## Run locally
```bash
git clone <your-repo-url>
cd gst-ai-assistant
pip install -r requirements.txt
export GEMINI_API_KEY="your-key"   # Windows PowerShell: $env:GEMINI_API_KEY="your-key"
streamlit run app.py
```
Get a free API key from Google AI Studio. You can also paste the key in the app sidebar. Set `GEMINI_MODEL` to change the model.

## How I used AI tools
See [LEARNINGS.md](LEARNINGS.md).

## Limitations
- GST rates and rules change. Verify against official notifications.
- LLM answers can be wrong. This is an educational demo, not tax advice.

## Ideas for next steps
- Upload an invoice PDF and extract fields
- Retrieval over official GST FAQs for grounded answers
- GSTIN format validation
# gst-ai-assistant
