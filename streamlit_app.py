import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from PIL import Image
import io

# Try to get API key from Streamlit secrets (for deployment) or .env (for local)
load_dotenv()
try:
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
except:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY or OPENAI_API_KEY == "your_api_key_here":
    st.error("Please set your OPENAI_API_KEY in Streamlit secrets (for deployment) or .env file (for local)")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(page_title="Product Authenticity Checker", page_icon="🔍", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for dark theme - black background with white text
st.markdown("""
<style>
    /* Black background */
    .stApp {
        background-color: #000000;
    }
    
    /* Main content container - well organized */
    .main .block-container {
        padding: 3rem 2rem;
        max-width: 1200px;
        background-color: #000000;
    }
    
    /* Header styling - white text with red accent */
    h1 {
        color: #ffffff !important;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        padding-bottom: 1rem;
        border-bottom: 4px solid #dc3545;
    }
    
    h2 {
        color: #ffffff !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #dc3545;
    }
    
    h3 {
        color: #ffffff !important;
        text-align: center;
        font-weight: 500 !important;
        margin-bottom: 2rem !important;
        font-size: 1.2rem !important;
    }
    
    /* Tabs styling - dark theme with red accent */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: #1a1a1a;
        border-bottom: 2px solid #333333;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a1a;
        border-radius: 6px 6px 0 0;
        padding: 14px 28px;
        font-weight: 600;
        color: #cccccc !important;
        border-right: 1px solid #333333;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2a2a2a;
        color: #ffffff !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #dc3545 !important;
        color: #ffffff !important;
        border-right: 1px solid #dc3545;
    }
    
    /* Input fields - dark theme with better UX */
    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        border-radius: 6px !important;
        border: 2px solid #444444 !important;
        padding: 14px 18px !important;
        font-size: 16px !important;
        color: #ffffff !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #dc3545 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.2) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #888888 !important;
    }
    
    /* File uploader - dark theme with better UX */
    .stFileUploader {
        background-color: #1a1a1a !important;
        border-radius: 6px;
        padding: 35px;
        border: 2px dashed #444444;
        transition: all 0.2s ease;
    }
    
    .stFileUploader:hover {
        border-color: #dc3545;
        background-color: #222222;
    }
    
    .stFileUploader label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    /* Buttons - red primary buttons */
    .stButton > button {
        background-color: #dc3545 !important;
        color: #ffffff !important;
        border: 2px solid #dc3545 !important;
        border-radius: 6px !important;
        padding: 14px 36px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(220, 53, 69, 0.3) !important;
    }
    
    .stButton > button:hover {
        background-color: #c82333 !important;
        border-color: #c82333 !important;
        box-shadow: 0 4px 12px rgba(220, 53, 69, 0.5) !important;
        transform: translateY(-1px);
    }
    
    /* Success message - dark theme with green accent */
    .stSuccess {
        background-color: #1a1a1a !important;
        border-left: 4px solid #28a745 !important;
        border-radius: 6px !important;
        padding: 18px 22px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        margin: 1rem 0 !important;
    }
    
    /* Error message - dark theme with red accent */
    .stError {
        background-color: #1a1a1a !important;
        border-left: 4px solid #dc3545 !important;
        border-radius: 6px !important;
        padding: 18px 22px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        margin: 1rem 0 !important;
    }
    
    /* Warning message - dark theme with yellow accent */
    .stWarning {
        background-color: #1a1a1a !important;
        border-left: 4px solid #ffc107 !important;
        border-radius: 6px !important;
        padding: 18px 22px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        margin: 1rem 0 !important;
    }
    
    /* Info/Expander - dark theme with better UX */
    .streamlit-expanderHeader {
        background-color: #1a1a1a !important;
        border-radius: 6px !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: 14px 18px !important;
        border: 1px solid #333333 !important;
        transition: all 0.2s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #222222 !important;
        border-color: #dc3545 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #1a1a1a !important;
        border-radius: 6px !important;
        padding: 22px !important;
        margin-top: 10px !important;
        border: 1px solid #333333 !important;
    }
    
    /* Images - white borders */
    img {
        border-radius: 4px !important;
        border: 2px solid #333333 !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 2px !important;
        background-color: #ffffff !important;
        margin: 2rem 0 !important;
    }
    
    /* Markdown content - dark theme with better readability */
    .stMarkdown {
        background-color: #1a1a1a !important;
        padding: 24px !important;
        border-radius: 6px !important;
        margin: 1.5rem 0 !important;
        border: 1px solid #333333 !important;
        line-height: 1.8 !important;
    }
    
    .stMarkdown p, .stMarkdown li {
        color: #e0e0e0 !important;
        line-height: 1.9 !important;
        margin-bottom: 1rem !important;
        font-size: 15px !important;
    }
    
    .stMarkdown h4 {
        color: #ffffff !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
        font-size: 1.3rem !important;
    }
    
    .stMarkdown strong {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    .stMarkdown ul {
        margin-left: 1.5rem !important;
        margin-top: 0.5rem !important;
    }
    
    /* Caption text - dark theme */
    .stImage > div > div > img + div {
        color: #cccccc !important;
        font-weight: 500 !important;
        background-color: #1a1a1a !important;
        padding: 8px 12px !important;
        border-radius: 4px !important;
    }
    
    /* Camera input - dark theme */
    .stCameraInput {
        border-radius: 4px !important;
        border: 2px solid #333333 !important;
    }
    
    /* Spinner - white */
    .stSpinner > div {
        border-top-color: #ffffff !important;
    }
    
    /* Better spacing */
    .element-container {
        margin-bottom: 1.5rem;
    }
    
    /* Ensure all text is white */
    p, li, span, div, label {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🔍 Product Authenticity Checker")
st.markdown("### AI-Powered Product Verification System")

# Project Description
with st.expander("📖 About This Project", expanded=False):
    st.markdown("""
    **Product Authenticity Checker** is an AI-powered application that helps you verify the authenticity of products, 
    particularly focusing on branded items like Nike shoes, electronics, luxury goods, and more.
    
    **How it works:**
    - Upload an image of the product you want to verify
    - Our AI analyzes visual details including logos, stitching, materials, labels, and packaging
    - Get a detailed authenticity assessment with specific evidence points
    
    **What to look for:**
    - **Logo Quality**: Correct styling, positioning, and clarity
    - **Construction**: Stitching quality, material consistency, and overall craftsmanship
    - **Labels & Tags**: Size, model numbers, country of manufacture, and font consistency
    - **Packaging**: Branded boxes, artwork quality, and typography
    - **Price Indicators**: Suspiciously low prices may indicate counterfeits
    
    **Note**: This tool provides an AI-based assessment. For complete certainty, consider purchasing from authorized retailers or official brand websites.
    """)

st.divider()

tab1, tab2, tab3 = st.tabs(["📷 Image URL", "📁 Upload File", "🎥 Camera"])

def check_product(image_url=None, image_base64=None):
    try:
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
        
        with st.spinner("Analyzing product image..."):
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
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

with tab1:
    st.header("Enter Image URL")
    image_url = st.text_input("Image URL", placeholder="https://example.com/image.jpg")
    
    if image_url:
        try:
            st.image(image_url, caption="Preview", use_container_width=True)
            if st.button("Check Product", type="primary", use_container_width=True):
                result = check_product(image_url=image_url)
                if result:
                    result_lower = result.lower()
                    if result_lower.startswith("**verdict**: fake") or result_lower.startswith("verdict: fake"):
                        st.error("⚠️ **VERDICT: FAKE**")
                    elif result_lower.startswith("**verdict**: real") or result_lower.startswith("verdict: real"):
                        st.success("✅ **VERDICT: REAL**")
                    elif "uncertain" in result_lower[:200]:
                        st.warning("⚠️ **VERDICT: UNCERTAIN**")
                    else:
                        # Fallback for old format
                        is_fake = "fake" in result_lower[:200]
                        if is_fake:
                            st.error("⚠️ Likely Fake")
                        else:
                            st.success("✅ Likely Real")
                    st.markdown("---")
                    st.markdown(result)
        except Exception as e:
            st.error(f"Could not load image: {str(e)}")

with tab2:
    st.header("Upload Image File")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "webp"])
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Preview", use_container_width=True)
            
            if st.button("Check Product", type="primary", use_container_width=True):
                image_base64 = image_to_base64(image)
                result = check_product(image_base64=image_base64)
                if result:
                    result_lower = result.lower()
                    if result_lower.startswith("**verdict**: fake") or result_lower.startswith("verdict: fake"):
                        st.error("⚠️ **VERDICT: FAKE**")
                    elif result_lower.startswith("**verdict**: real") or result_lower.startswith("verdict: real"):
                        st.success("✅ **VERDICT: REAL**")
                    elif "uncertain" in result_lower[:200]:
                        st.warning("⚠️ **VERDICT: UNCERTAIN**")
                    else:
                        # Fallback for old format
                        is_fake = "fake" in result_lower[:200]
                        if is_fake:
                            st.error("⚠️ Likely Fake")
                        else:
                            st.success("✅ Likely Real")
                    st.markdown("---")
                    st.markdown(result)
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

with tab3:
    st.header("Capture from Camera")
    camera_input = st.camera_input("Take a photo")
    
    if camera_input is not None:
        try:
            image = Image.open(camera_input)
            st.image(image, caption="Captured Image", use_container_width=True)
            
            if st.button("Check Product", type="primary", use_container_width=True):
                image_base64 = image_to_base64(image)
                result = check_product(image_base64=image_base64)
                if result:
                    result_lower = result.lower()
                    if result_lower.startswith("**verdict**: fake") or result_lower.startswith("verdict: fake"):
                        st.error("⚠️ **VERDICT: FAKE**")
                    elif result_lower.startswith("**verdict**: real") or result_lower.startswith("verdict: real"):
                        st.success("✅ **VERDICT: REAL**")
                    elif "uncertain" in result_lower[:200]:
                        st.warning("⚠️ **VERDICT: UNCERTAIN**")
                    else:
                        # Fallback for old format
                        is_fake = "fake" in result_lower[:200]
                        if is_fake:
                            st.error("⚠️ Likely Fake")
                        else:
                            st.success("✅ Likely Real")
                    st.markdown("---")
                    st.markdown(result)
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

