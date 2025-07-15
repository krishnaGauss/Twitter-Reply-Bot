import tweepy
import os
import json
from dotenv import load_dotenv
import time
import re
from typing import List, Dict, Any
from datetime import datetime, timedelta

load_dotenv()

class HumanTweetFilter:
    
    def __init__(self):
        # Promotional/spam indicators
        self.promotional_keywords = [
            'buy now', 'limited time', 'sale', 'discount', 'promo code', 'coupon',
            'free shipping', 'order now', 'click here', 'sign up now', 'register now',
            'get yours', 'don\'t miss out', 'exclusive offer', 'special deal',
            'flash sale', 'today only', 'hurry up', 'act fast', 'while supplies last',
            
            'affiliate', 'sponsored', 'ad', '#ad', 'paid partnership', 'gifted',
            'promo', 'collaboration', 'brand partner', 'ambassador',
            
            'giveaway', 'contest', 'win', 'winner', 'prize', 'raffle',
            'follow and retweet', 'rt to win', 'tag friends', 'enter to win',
            
            # Generic promotional
            'check out', 'link in bio', 'swipe up', 'shop now', 'learn more',
            'book now', 'reserve now', 'download now', 'try now', 'get started',
            'join now', 'subscribe', 'follow for more', 'turn on notifications'
        ]
        
        # Bot/automated content patterns
        self.bot_patterns = [
            r'^(good morning|gm|good night|gn)\s*[!.]*\s*$',  
            r'^(thanks?|thank you)\s+(for\s+the\s+)?(follow|rt|retweet)\s*[!.]*\s*$',  
            r'^\d+/\d+$',  
            r'^(breaking|update|alert):\s*$',  
            r'^(this|that|it)\s+(is|was)\s+(amazing|great|awesome|incredible)\s*[!.]*\s*$',  
            r'^(wow|omg|amazing|incredible)\s*[!.]*\s*$',  # Single word reactions
            r'^(yes|no|maybe|true|false)\s*[!.]*\s*$',  # Single word responses
        ]
        
        # Human conversation indicators
        self.human_indicators = [
            # Personal experiences
            'i think', 'i feel', 'i believe', 'in my opinion', 'personally',
            'from my experience', 'i noticed', 'i remember', 'i used to',
            'i\'ve been', 'i\'ve seen', 'i\'ve tried', 'i\'ve found', 'we tried',
            
            # Conversational elements
            'what do you think', 'thoughts?', 'anyone else', 'has anyone',
            'does anyone know', 'can someone', 'help me understand',
            'am i the only one', 'maybe i\'m wrong', 'correct me if',
            
            # Emotional expressions
            'frustrated', 'excited', 'disappointed', 'surprised', 'confused',
            'worried', 'happy', 'annoyed', 'curious', 'concerned',
            
            'not sure', 'maybe', 'probably', 'i guess', 'i suppose',
            'could be wrong', 'might be', 'seems like', 'looks like',
            
            'why', 'how', 'what', 'when', 'where', 'who',
            'explain', 'understand', 'clarify', 'elaborate'
        ]
        
        self.genuine_patterns = [
            r'\b(just|recently|yesterday|today|this morning)\s+(experienced|tried|noticed|saw|found)\b',
            r'\b(has anyone|does anyone|can someone|would anyone)\b',
            r'\b(i\'m|i am)\s+(thinking|wondering|curious|confused|frustrated)\b',
            r'\?.*\?',  
            r'\b(update|edit|correction):\s*',  
            r'\b(tbh|honestly|ngl|imo|imho)\b',  
        ]
        
        
        self.reply_worthy_indicators = [
            'having trouble', 'problem with', 'issue with', 'can\'t figure out',
            'not working', 'broken', 'failed', 'error', 'bug',
            
            # Questions (natural conversation starters)
            'which should i', 'what would you', 'how do i', 'where can i',
            'anyone recommend', 'suggestions', 'advice', 'help',
            
            # Opinions/discussions
            'thoughts on', 'opinion about', 'what do you think about',
            'agree or disagree', 'am i right', 'change my mind',
            
            # Experiences (relatable content)
            'just tried', 'been using', 'switched to', 'moved from',
            'experience with', 'compared to', 'better than', 'worse than'
        ]
    
    def is_promotional(self, tweet_data: Dict[str, Any]) -> bool:
        """Check if tweet is promotional/spam content"""
        text = tweet_data['content'].lower()
        
        promo_score = sum(1 for keyword in self.promotional_keywords if keyword in text)
        if promo_score >= 2:
            return True
        
        promo_patterns = [
            r'\b\d+%\s*(off|discount|sale)\b',
            r'\$\d+.*\b(off|discount|sale)\b',
            r'\b(free|save)\s+\$\d+\b',
            r'\b(use code|promo code|coupon)\b',
            r'\b(limited time|ends soon|today only)\b',
            r'\b(link in bio|linktree|linktr\.ee)\b',
        ]
        
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in promo_patterns):
            return True
        
        if len(re.findall(r'#\w+', text)) > 4:
            return True
        
        # Excessive emojis
        emoji_count = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', text))
        if emoji_count > 6:
            return True
        
        # All caps (often spam)
        if len(re.findall(r'[A-Z]{4,}', tweet_data['content'])) > 2:
            return True
        
        return False
    
    def is_bot_content(self, tweet_data: Dict[str, Any]) -> bool:
        """Check if tweet appears to be automated/bot content"""
        text = tweet_data['content'].lower().strip()
        
        # Check against bot patterns
        for pattern in self.bot_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        # Very short, generic responses
        if len(text) < 10 and text in ['ok', 'yes', 'no', 'thanks', 'nice', 'cool', 'great']:
            return True
        
        # Just links/mentions (often automated)
        if re.match(r'^(@\w+\s*)+$', text) or re.match(r'^(https?://\S+\s*)+$', text):
            return True
        
        # Repetitive posting pattern (same user posting very similar content)
        words = text.split()
        if len(words) > 2 and len(set(words)) < len(words) * 0.5:  # High repetition
            return True
        
        return False
    
    def calculate_human_score(self, tweet_data: Dict[str, Any]) -> float:
        """Calculate how human/genuine the tweet appears (0-1)"""
        text = tweet_data['content'].lower()
        score = 0.3  # Base score
        
        # Human indicators
        human_matches = sum(1 for indicator in self.human_indicators if indicator in text)
        score += human_matches * 0.1
        
        # Genuine patterns
        pattern_matches = sum(1 for pattern in self.genuine_patterns if re.search(pattern, text, re.IGNORECASE))
        score += pattern_matches * 0.15
        
        # Natural language features
        # Contractions (very human)
        contractions = len(re.findall(r"\b\w+\'[a-z]+\b", text))
        score += min(contractions * 0.1, 0.2)
        
        # Questions (engagement)
        question_marks = text.count('?')
        score += min(question_marks * 0.05, 0.15)
        
        # Casual language markers
        casual_markers = ['tbh', 'ngl', 'imo', 'imho', 'lol', 'omg', 'btw', 'idk']
        casual_score = sum(1 for marker in casual_markers if marker in text)
        score += min(casual_score * 0.08, 0.2)
        
        # Personal pronouns (human touch)
        personal_pronouns = len(re.findall(r'\b(i|my|me|myself|we|us|our)\b', text))
        score += min(personal_pronouns * 0.05, 0.15)
        
        # Moderate length (too short often spam, too long often promotional)
        length = len(tweet_data['content'])
        if 20 <= length <= 200:
            score += 0.1
        elif 200 < length <= 280:
            score += 0.05
        
        return min(score, 1.0)
    
    def is_reply_worthy(self, tweet_data: Dict[str, Any]) -> bool:
        """Check if tweet is worth replying to"""
        text = tweet_data['content'].lower()
        
        # Check for reply-worthy indicators
        reply_worthy_matches = sum(1 for indicator in self.reply_worthy_indicators if indicator in text)
        
        # Questions are always reply-worthy
        if '?' in text:
            return True
        
        # Problems/issues are reply-worthy
        if reply_worthy_matches >= 1:
            return True
        
        # Avoid replying to retweets (usually not original content)
        if tweet_data['content'].startswith('RT @'):
            return False
        
        # Avoid very short tweets (often not conversational)
        if len(tweet_data['content']) < 15:
            return False
        
        return reply_worthy_matches > 0
    
    def filter_for_replies(self, tweets: List[Dict[str, Any]], min_human_score: float = 0.3) -> List[Dict[str, Any]]:
        """Filter tweets for those suitable for human-like replies"""
        filtered_tweets = []
        
        for tweet in tweets:
            # Skip promotional content
            if self.is_promotional(tweet):
                continue
            
            # Skip bot content
            if self.is_bot_content(tweet):
                continue
            
            # Calculate human score
            human_score = self.calculate_human_score(tweet)
            tweet['human_score'] = round(human_score, 2)
            
            # Check if reply-worthy
            tweet['reply_worthy'] = self.is_reply_worthy(tweet)
            
            # Keep only human-like, reply-worthy tweets
            if human_score >= min_human_score and tweet['reply_worthy']:
                filtered_tweets.append(tweet)
        
        # Sort by human score (most human-like first)
        filtered_tweets.sort(key=lambda x: x['human_score'], reverse=True)
        
        return filtered_tweets


def get_recent_tweets(handle, max_results=10, save_path="tweets.json", filter_for_replies=True, min_human_score=0.3):
    """
    Fetch recent tweets from a specific handle with filtering for reply-worthy content
    
    Args:
        handle: Twitter handle (with or without @)
        max_results: Maximum number of tweets to fetch
        save_path: Path to save tweets JSON file (optional)
        filter_for_replies: Whether to filter for reply-worthy content
        min_human_score: Minimum human score to keep tweet (0-1)
    """
    try:
        # Clean handle
        handle = handle.replace('@', '')
        
        client = tweepy.Client(bearer_token=os.getenv("BEARER_TOKEN"))
        
        # Get user info first
        user = client.get_user(username=handle)
        if not user.data:
            print(f"User @{handle} not found.")
            return []
        
        user_id = user.data.id
        
        # Get user's tweets
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=max_results,
            tweet_fields=["created_at", "public_metrics", "context_annotations", "conversation_id"],
            expansions=["referenced_tweets.id"],
            exclude=["retweets", "replies"]  # Focus on original content
        )
        
        if not tweets.data:
            print(f"No tweets found for @{handle}.")
            return []
        
        # Process tweets
        tweet_data_list = []
        for tweet in tweets.data:
            # Skip if it's a reply to someone else
            if tweet.text.startswith('@') and tweet.conversation_id != tweet.id:
                continue
                
            tweet_data = {
                "id": tweet.id,
                "created_at": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "username": handle,
                "content": tweet.text,
                "retweet_count": getattr(tweet, 'public_metrics', {}).get('retweet_count', 0),
                "like_count": getattr(tweet, 'public_metrics', {}).get('like_count', 0),
                "reply_count": getattr(tweet, 'public_metrics', {}).get('reply_count', 0),
                "url": f"https://twitter.com/{handle}/status/{tweet.id}",
                "is_original": tweet.conversation_id == tweet.id  # True if original tweet
            }
            tweet_data_list.append(tweet_data)
        
        print(f"Fetched {len(tweet_data_list)} tweets from @{handle}")
        
        # Apply filtering for reply-worthy content
        if filter_for_replies:
            tweet_filter = HumanTweetFilter()
            original_count = len(tweet_data_list)
            tweet_data_list = tweet_filter.filter_for_replies(tweet_data_list, min_human_score)
            filtered_count = len(tweet_data_list)
            
            print(f"Filtered out {original_count - filtered_count} promotional/bot/non-reply-worthy tweets")
            print(f"Found {filtered_count} tweets suitable for replies")
        
        # Save to JSON if path provided
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(tweet_data_list, f, indent=2, ensure_ascii=False)
            print(f"Saved to {save_path}")
        
        return tweet_data_list
        
    except tweepy.Unauthorized:
        print("Error: Unauthorized. Check your bearer token.")
        return []
    except tweepy.NotFound:
        print(f"Error: User @{handle} not found.")
        return []
    except tweepy.TooManyRequests:
        print("Rate limit exceeded. Waiting for 15 minutes...")
        time.sleep(900)
        return get_recent_tweets(handle, max_results, save_path, filter_for_replies, min_human_score)
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return []


    
    
    
    