import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from trend_finder import fetch_trending_topics
from content_engine import generate_affiliate_article
from publisher import publish_article

def run_agent(seed_keyword: str, affiliate_link: str):
    print("🤖 AI Revenue Agent Started...\n")
    
    # 1. Discover Trends
    topics = fetch_trending_topics(seed_keyword)
    print(f"\n🎯 Identified {len(topics)} target topics for campaign.")
    
    # 2. Generate Content & Publish
    for topic in topics:
        print(f"\n📝 Generating article for: '{topic}'")
        filepath = generate_affiliate_article(topic=topic, affiliate_link=affiliate_link)
        
        print(f"📤 Publishing article...")
        publish_article(filepath)
        
    print("\n🎉 Full End-to-End Execution Complete!")

if __name__ == "__main__":
    run_agent(
        seed_keyword="mechanical keyboard",
        affiliate_link="https://amazon.com/dp/your-affiliate-id"
    )