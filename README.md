# Product Authenticity Checker

An AI-powered application that helps you verify the authenticity of products using OpenAI's GPT-4 Vision model.

## Features

- 📷 Upload images via URL, file upload, or camera
- 🤖 AI-powered authenticity analysis
- 📊 Detailed assessment with evidence points
- 🎨 Clean dark theme interface

## Local Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
5. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- OpenAI API key

### Steps

1. **Push your code to GitHub:**
   - Create a new repository on GitHub
   - Push your code (make sure `.env` is in `.gitignore` - never commit API keys!)

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository and branch
   - Set the main file path to: `streamlit_app.py`
   - Click "Deploy"

3. **Add your API key as a secret:**
   - In your Streamlit Cloud app dashboard, go to "Settings" → "Secrets"
   - Add the following:
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```
   - Click "Save"

4. **Your app will automatically redeploy!**

## Important Notes

- ✅ The app already handles Streamlit secrets properly
- ✅ Never commit your `.env` file or API keys to GitHub
- ✅ Use Streamlit Cloud secrets for production deployment
- ✅ The app works with both local `.env` files and Streamlit Cloud secrets

## Requirements

- Python 3.9+
- OpenAI API key
- See `requirements.txt` for Python dependencies

## File Structure

```
fake-detection/
├── streamlit_app.py      # Main Streamlit app (deploy this)
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
├── README.md            # This file
├── app.py               # Flask API (optional)
└── product_checker.py   # Test script (optional)
```

## Support

For issues or questions, please open an issue on GitHub.

