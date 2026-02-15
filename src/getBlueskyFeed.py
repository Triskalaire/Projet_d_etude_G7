import requests
import os
from dotenv import load_dotenv

load_dotenv()

BLUESKY_USERNAME = os.getenv("BSKY_IDENTIFIER")
BLUESKY_PASSWORD = os.getenv("BSKY_PASSWORD")

API_URL = "https://bsky.social/xrpc"

def load_token():
    """Authentifie l'utilisateur et retourne un token JWT Bluesky."""
    payload = {
        "identifier": BLUESKY_USERNAME,
        "password": BLUESKY_PASSWORD
    }

    r = requests.post(f"{API_URL}/com.atproto.server.createSession", json=payload)

    if r.status_code != 200:
        print("Erreur d'authentification Bluesky :", r.text)
        return None

    return r.json().get("accessJwt")


def _auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

# Note : How did I get those feed ? With f"{API_URL}/app.bsky.feed.getSuggestedFeeds" (examples of feed that I might like)
# And then I chose some with big likes number. Only the "What's Hot" feed is an official one
# I chose Verified News to get a "golden feed", and the Ukrainan feed to maybe get some false news/less verified news to compare

# -----------------------------
# 1. HOT FEED (What's Hot)
# -----------------------------
def get_hot_feed(token, limit=50):
    """What's Hot feed via feed generator."""
    params = {
        "feed": "at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.generator/whats-hot",
        "limit": limit
    }

    r = requests.get(
        f"{API_URL}/app.bsky.feed.getFeed",
        headers=_auth_headers(token),
        params=params
    )

    if r.status_code != 200:
        print("Erreur Hot:", r.text)
        return []

    return r.json().get("feed", [])

# -----------------------------
# 2. UKRAINIAN NEWS FEED
# -----------------------------
def get_ukrainian_feed(token, limit=50):
    """Posts from Ukrainians about Ukraine and their experience during the war. """
    params = {
        "feed": "at://did:plc:dvgliotey33vix3wlltybgkd/app.bsky.feed.generator/ukrainian-view",
        "limit": limit
    }

    r = requests.get(
        f"{API_URL}/app.bsky.feed.getFeed",
        headers=_auth_headers(token),
        params=params
    )

    if r.status_code != 200:
        print("Erreur Ukrainian News:", r.text)
        return []

    return r.json().get("feed", [])

# -----------------------------
# 3. SCIENCE FEED
# -----------------------------
def get_science_feed(token, limit=50):
    """Science feed via feed generator."""
    params = {
        "feed": "at://did:plc:jfhpnnst6flqway4eaeqzj2a/app.bsky.feed.generator/for-science",
        "limit": limit
    }

    r = requests.get(
        f"{API_URL}/app.bsky.feed.getFeed",
        headers=_auth_headers(token),
        params=params
    )

    if r.status_code != 200:
        print("Erreur Science:", r.text)
        return []

    return r.json().get("feed", [])

# -----------------------------
# 4. VERIFIED NEWS FEED
# -----------------------------
def get_verified_news_feed(token, limit=50):
    """Verified News feed via feed generator."""
    params = {
        "feed": "at://did:plc:kkf4naxqmweop7dv4l2iqqf5/app.bsky.feed.generator/verified-news",
        "limit": limit
    }

    r = requests.get(
        f"{API_URL}/app.bsky.feed.getFeed",
        headers=_auth_headers(token),
        params=params
    )

    if r.status_code != 200:
        print("Erreur Verified News:", r.text)
        return []

    return r.json().get("feed", [])

