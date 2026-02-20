import requests
from bs4 import BeautifulSoup

def get_website_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # remove script and style
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text(separator=" ")
        return text

    except:
        return "Error fetching website"
