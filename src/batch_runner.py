from content_engine import generate_affiliate_article

# Define your target topics and affiliate destination links
CAMPAIGN_TOPICS = [
    {
        "topic": "Top Ergonomic Keyboards for Programmers",
        "link": "https://example.com/affiliate/keyboards"
    },
    {
        "topic": "Best Ultrawide Monitors for Coding Productivity",
        "link": "https://example.com/affiliate/monitors"
    },
    {
        "topic": "Must-Have Noise-Canceling Headphones for Remote Developers",
        "link": "https://example.com/affiliate/headphones"
    }
]

def run_campaign():
    print("🚀 Starting Automated Content Generation...")
    for item in CAMPAIGN_TOPICS:
        generate_affiliate_article(item["topic"], item["link"])
    print("\n🎉 All articles generated and ready in the 'output/' folder!")

if __name__ == "__main__":
    run_campaign()