# article-analyzer
An API-integrated project with a Streamlit UI that analyzes URLs and lets you ask questions about the input URL.


#File 1:

import requests
from bs4 import BeautifulSoup

def fetch_article_text(url: str, max_chars: int = 10000) -> str:
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    )

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    paragraphs = soup.find_all("p")
    text = " ".join(p.get_text() for p in paragraphs)
    text = " ".join(text.split())

    return text[:max_chars]

#File 2:

import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from article_utils import fetch_article_text

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

            st.write(response.choices[0].message.content)
