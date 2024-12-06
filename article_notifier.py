from bs4 import BeautifulSoup
from dotenv import load_dotenv

import time
import hashlib
import os
import requests

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
URL = os.getenv("URL")

def get_page_content(url):
    response = requests.get(url)
    return response.text

def get_articles(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('product-item-name')
    return articles

def send_discord_notification(title, message):
    data = {
        "content": f"**{title}**\n{message}"
    }
    requests.post(WEBHOOK_URL, json=data)

def main():
    previous_content_hash = None
    
    while True:
        try:
            current_content = get_page_content(URL)
            current_hash = hashlib.md5(current_content.encode()).hexdigest()
            
            if previous_content_hash and current_hash != previous_content_hash:
                articles = get_articles(current_content)
                if articles:
                    send_discord_notification(
                        "Nouvel article !",
                        f"Un nouvel article est disponible sur {URL}"
                    )
            
            previous_content_hash = current_hash
            
            time.sleep(300)
            
        except Exception as e:
            print(f"Erreur : {e}")
            time.sleep(60)

if __name__ == "__main__":
    main() 