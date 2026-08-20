import os
import re
from datetime import datetime
from dotenv import load_dotenv
from google import genai

load_dotenv()

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[\s_-]+', '-', text)

def generate_affiliate_article(topic: str, affiliate_link: str) -> str:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    prompt = f"""
    Write a 600-word product review and buying guide about '{topic}'.
    Target audience: Buyers looking for fast, reliable recommendations.
    
    Formatting rules:
    - Break into clear sections using standard Markdown formatting.
    - Highlight key pros, cons, and features in bullet points.
    - Place clear Call-to-Action (CTA) sentences encouraging readers to buy using this exact link: {affiliate_link}
    - Do NOT include an H1 title heading inside the body text.
    """
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    
    os.makedirs("output", exist_ok=True)
    filename = f"output/{slugify(topic)}.md"
    
    # Format with front-matter metadata for static site tools on AWS Amplify
    front_matter = f"""---
title: "{topic}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
draft: false
---

"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter + response.text)
        
    print(f"✅ Generated and saved: {filename}")
    return filename