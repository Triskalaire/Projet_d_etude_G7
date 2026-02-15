from getBlueskyFeed import (
    load_token,
    get_ukrainian_feed,
    get_science_feed,
    get_hot_feed,
    get_verified_news_feed
)
from mongoConnect import get_db
from datetime import datetime, timezone
from pymongo.errors import BulkWriteError

def insert_feed_data(feed_data, collection_name):
    if not feed_data:
        print(f"Aucune donnée à insérer dans '{collection_name}'.")
        return

    db = get_db()
    collection = db[collection_name]

    # Ensure unique index on post.uri (on ne va pas ajouter plein de fois le même post)
    collection.create_index([("post.uri", 1)], unique=True)

    # Add timestamp
    for item in feed_data:
        item["inserted_at"] = datetime.now(timezone.utc)

    try:
        result = collection.insert_many(feed_data)
        print(f"{len(result.inserted_ids)} documents insérés dans '{collection_name}'.")
    except BulkWriteError as e: 
        # Duplicate errors are expected 
        inserted = e.details.get("nInserted", 0) 
        print(f"{inserted} nouveaux documents insérés dans '{collection_name}' (doublons ignorés).")
    except Exception as e: 
        print(f"Erreur inattendue dans '{collection_name}': {e}")

def main():
    token = load_token()
    if not token:
        return

    print("Récupération Hot...")
    hot = get_hot_feed(token)
    insert_feed_data(hot, "hot")

    print("Récupération Ukrainian War Posts...")
    ukrainian = get_ukrainian_feed(token)
    insert_feed_data(ukrainian, "ukrainian")

    print("Récupération Science...")
    science = get_science_feed(token)
    insert_feed_data(science, "science")

    print("Récupération Verified News...")
    verified_news = get_verified_news_feed(token)
    insert_feed_data(verified_news, "verified_news")


main()