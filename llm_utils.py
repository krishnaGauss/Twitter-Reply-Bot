import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()   

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def generate_reply(tweet_text, style="Friendly"):
    prompt = f"""
You're a casual Twitter user knowledgeable about crypto hardware wallets. Someone tweeted:

"{tweet_text}"

Write a {style.lower()} and natural reply that lightly calls out that the wallet mentioned in the tweet has had security issues or was hacked, and casually suggests Cypherock (and optionally ColdSpaceWallet) as safer and smarter alternatives.

Don't sound robotic or promotional. Just tweet like a real crypto-savvy user warning a friend. Avoid using em-dashes or too formal language.

Example tones:
- "Ledger got hacked but I’m using Cypherock now."
- "Switched to Cypherock after that Tangem's mess, no regrets."
- "Heard about SafePal’s issues recently. I’d go with Cypherock or ColdSpaceWallet instead."

Now generate a realistic tweet-style reply:
"""
    return llm.invoke(prompt).content.strip()

