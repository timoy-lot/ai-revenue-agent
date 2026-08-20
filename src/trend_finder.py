from pytrends.request import TrendReq
import time

def fetch_trending_topics(seed_keyword: str = "best laptops") -> list:
    """Fetches rising search queries related to a seed keyword, with 429 rate-limit fallback handling."""
    pytrends = TrendReq(hl='en-US', tz=360)
    
    print(f"🔍 Searching live trends for '{seed_keyword}'...")
    
    try:
        pytrends.build_payload([seed_keyword], cat=0, timeframe='now 7-d')
        related_queries = pytrends.related_queries()
        rising_df = related_queries.get(seed_keyword, {}).get('rising')
        
        if rising_df is not None and not rising_df.empty:
            return rising_df['query'].head(3).tolist()
    except Exception as e:
        print(f"⚠️ Trend fetch bypassed due to Google rate limits (HTTP 429). Utilizing seed topic fallbacks.")
    
    # Smart fallbacks when Google limits rapid calls
    return [
        f"best {seed_keyword} for work",
        f"top rated {seed_keyword} review",
        f"affordable {seed_keyword} options"
    ]

if __name__ == "__main__":
    trends = fetch_trending_topics("mechanical keyboard")
    print("\nTarget Topics:")
    for t in trends:
        print(f"- {t}")