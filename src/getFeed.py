import json
import requests
from login import login

# Load access token from token.json
def load_token():
    try:
        with open("token.json", "r", encoding="utf-8") as f:
            tokens = json.load(f)
            return tokens.get("accessJwt")
    except FileNotFoundError:
        print("Erreur : token.json introuvable. Veuillez d'abord exécuter login.py.")
        return None

def get_feed(access_token, preferred_languages="fr"):
    url = "https://bsky.social/xrpc/app.bsky.feed.getFeed"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept-Language": preferred_languages
    }
    params = {
        "feed": "at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.generator/whats-hot",
        "limit": 30
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        feed = data.get("feed", [])
        next_page = data.get("cursor")
        print("Feed reçu avec succès.")
        return feed, next_page
    else:
        print("Erreur lors de la récupération du feed :", response.text)
        return None, None

if __name__ == "__main__":
    token = load_token()
    if token:
        feed, cursor = get_feed(token)
        print("Nombre de posts:", len(feed))