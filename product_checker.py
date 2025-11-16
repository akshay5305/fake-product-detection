from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY or OPENAI_API_KEY == "your_api_key_here":
    raise ValueError("Please set your OPENAI_API_KEY in the .env file")

client = OpenAI(api_key=OPENAI_API_KEY)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": """Analyze this product image and provide a clear authenticity assessment. 

Please provide your response in the following structured format:

**VERDICT**: [Start with either "REAL" or "FAKE" or "UNCERTAIN" - be direct and clear]

**CONFIDENCE LEVEL**: [High/Medium/Low]

**DETAILED ANALYSIS**:
- Logo Analysis: [Examine the logo quality, positioning, and authenticity markers]
- Construction Quality: [Assess stitching, materials, craftsmanship, and build quality]
- Labels & Tags: [Review any visible labels, tags, size markings, model numbers, country of manufacture]
- Packaging: [If visible, analyze box quality, branding, fonts, and artwork]
- Overall Quality Indicators: [Any other visual cues that indicate authenticity or lack thereof]

**KEY EVIDENCE**:
[List 3-5 specific visual details that support your verdict]

**RECOMMENDATIONS**:
[Provide actionable advice based on your assessment]

Be specific, detailed, and focus on visual evidence you can observe in the image. If you cannot determine authenticity with confidence, clearly state what additional information or images would be helpful."""},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://thumbs.dreamstime.com/b/made-china-abibas-fake-adidas-brand-shoes-42741550.jpg"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)

