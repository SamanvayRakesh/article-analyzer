import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from article_analyzer import fetch_article_text

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Ask the News")
st.write("Ask questions about any news article.")


url = st.text_input("Enter news article URL")

if st.button("Fetch Article"):
    if not url:
        st.warning("Please enter a URL.")
    else:
        try:
            article = fetch_article_text(url)

            if len(article) < 500:
                st.error("Could not extract enough article content.")
            else:
                st.session_state.article_text = article
                st.success("Article loaded successfully.")

        except Exception:
            st.error("Failed to fetch article.")


if "article_text" in st.session_state:
    question = st.text_input("Ask a question about the article")

    if st.button("Get Answer"):
        If not question:
            st.warning("Please enter a question.")
        else:
            prompt = f" Answer using only this article. If missing, say: 'The article does not provide this information.'\n\n{st.session_state.article_text}\n\nQuestion: {question}"

            response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0.2)
