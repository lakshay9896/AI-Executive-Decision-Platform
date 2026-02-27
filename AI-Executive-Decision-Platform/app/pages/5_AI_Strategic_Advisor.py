#page 5
import streamlit as st
from langchain_community.llms import Ollama
from ui_theme import apply_corporate_theme
apply_corporate_theme()

st.title("AI Strategic Advisor")

llm = Ollama(model="mistral")

question = st.text_input("Enter Executive Strategic Question:")

if question:
    with st.spinner("Generating executive briefing..."):
        prompt = f"""
You are a Chief Strategy Officer.

Provide:
1. Executive Summary
2. Financial Interpretation
3. Risk Assessment
4. Strategic Recommendation
5. 90-Day Action Plan

Question:
{question}
"""
        response = llm.invoke(prompt)

    st.markdown(response)
