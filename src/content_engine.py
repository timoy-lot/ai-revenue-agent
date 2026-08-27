import os
from google import genai

def generate_affiliate_article(topic: str, affiliate_link: str) -> str:
    # Google GenAI SDK automatically detects GEMINI_API_KEY from environment variables
    client = genai.Client()

    search_query = topic.replace(" ", "+")
    amazon_affiliate_url = f"https://www.amazon.com/s?k={search_query}&tag={affiliate_link}"

    prompt = f"""
    Write a comprehensive, highly engaging, SEO-optimized review article about "{topic}".
    
    Guidelines:
    - Include product highlights, key specs, pros & cons, and a buyer's recommendation.
    - Include a clear Call to Action (CTA) button/link formatted in Markdown.
    - Use this exact affiliate link for the CTA: [{topic} on Amazon]({amazon_affiliate_url})
    - Ensure the tone is helpful and objective.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    os.makedirs("output", exist_ok=True)
    filename = topic.lower().replace(" ", "-") + ".md"
    filepath = os.path.join("output", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response.text)

    return filepath
