import tweepy
import os
import json
from dotenv import load_dotenv
import time

load_dotenv()

# For finding recent tweets based on a keyword


def get_recent_tweets(keyword,  max_results=20, save_path="tweets.json"):
    try:
        client = tweepy.Client(bearer_token=os.getenv("BEARER_TOKEN"))
        tweets = client.search_recent_tweets(query=keyword, max_results=max_results, tweet_fields=["created_at"],
                                             expansions=["author_id"],
                                             user_fields=["username", "name"])
        if not tweets.data:
            print("No tweets found for the given keyword.")
            return []

        user_map = {}
        if tweets.includes and "users" in tweets.includes:
            for user in tweets.includes["users"]:
                user_map[user.id] = {
                    "username": user.username,
                    "name": user.name
                }

        tweet_data_list = []
        for tweet in tweets.data:
            user_info = user_map.get(tweet.author_id, {})
            tweet_data = {
                "id": tweet.id,
                "created_at": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "username": user_info.get("username", "unknown"),
                "display_name": user_info.get("name", "unknown"),
                "content": tweet.text,
                "url": f"https://twitter.com/{user_info.get('username', 'unknown')}/status/{tweet.id}"
            }
            tweet_data_list.append(tweet_data)

        # Save to JSON file
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(tweet_data_list, f, indent=2, ensure_ascii=False)

        return tweet_data_list

    except tweepy.TooManyRequests as e:
        print("Rate limit exceeded. Waiting for 15 minutes...")
        time.sleep(900)
        return get_recent_tweets(keyword)
