from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY or OPENAI_API_KEY == "your_api_key_here":
    raise ValueError("Please set your OPENAI_API_KEY in the .env file")

app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/api/check-product', methods=['POST'])
def check_product():
    try:
        data = request.json
        image_url = data.get('image_url')
        image_base64 = data.get('image_base64')
        
        if not image_url and not image_base64:
            return jsonify({'error': 'image_url or image_base64 is required'}), 400
        
        if image_base64:
            image_content = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }
            }
        else:
            image_content = {
                "type": "image_url",
                "image_url": {"url": image_url}
            }
        
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
                        image_content
                    ]
                }
            ]
        )
        
        result = response.choices[0].message.content
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

