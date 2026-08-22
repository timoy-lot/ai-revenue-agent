import sys
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.trend_finder import fetch_trending_topics
from src.content_engine import generate_affiliate_article
from src.publisher import publish_article

def run_agent(seed_keyword: str, affiliate_tag: str):
    print("🤖 AI Revenue Agent Started...\n")
    
    # 1. Discover Trends
    topics = fetch_trending_topics(seed_keyword)
    print(f"\n🎯 Identified {len(topics)} target topics for campaign.")
    
    # 2. Generate Content & Publish
    for topic in topics:
        print(f"\n📝 Generating article for: '{topic}'")
        filepath = generate_affiliate_article(topic=topic, affiliate_link=affiliate_tag)
        
        print(f"🚀 Publishing article...")
        publish_article()

if __name__ == "__main__":
    # Pull affiliate tag from environment variable with fallback
    AFFILIATE_TAG = os.getenv("AFFILIATE_TAG", "yourtag-20")
    
    run_agent(
        seed_keyword="mechanical keyboard",
        affiliate_tag=AFFILIATE_TAG
    )