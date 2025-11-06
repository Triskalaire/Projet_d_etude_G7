from getBlueskyFeed import load_token, get_feed, get_timeline
from mongoConnect import db
from datetime import datetime, timezone
from pymongo.errors import BulkWriteError

def insert_feed_data(feed_data, collection_name):
    if not feed_data:
        print(f"Aucune donnée à insérer dans '{collection_name}'.")
        return

    collection = db[collection_name]
    print(collection_name)

    # Add timestamp
    for item in feed_data:
        item["inserted_at"] = datetime.now(timezone.utc)
        print(item)

    try:
        result = collection.insert_many(feed_data)
        print(f"{len(result.inserted_ids)} documents insérés dans '{collection_name}'.")
    except BulkWriteError as e:
        print("Erreur lors de l'insertion :", e.details)

def main():
    token = load_token()
    if not token:
        return

    print("Récupération du feed 'What's Hot'...")
    feed, feed_cursor = get_feed(token)
    print("Nombre de posts dans le feed:", len(feed))
    insert_feed_data(feed, "feed")

    print("\nRécupération du timeline utilisateur...")
    timeline, timeline_cursor = get_timeline(token)
    print("Nombre de posts dans la timeline:", len(timeline))
    insert_feed_data(timeline, "timeline")

if __name__ == "__main__":
    main()