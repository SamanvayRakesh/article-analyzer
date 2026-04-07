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




            st.write(response.choices[0].message.content)
