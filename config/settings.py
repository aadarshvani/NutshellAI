"""
Simple configuration for Nutshell application
"""
import streamlit as st

class AppConfig:
    """Basic app configuration"""
    
    APP_NAME = "🥜 Nutshell"
    APP_TAGLINE = "AI-Powered Content Summarizer"
    
    # Model options
    GROQ_MODELS = {
        "Gemma2-9b-it": "Fast and efficient",
        "llama-3.1-8b-instant": "Balanced performance", 
        "mixtral-8x7b-32768": "Best for long content"
    }
    
    # Summary formats
    SUMMARY_FORMATS = {
        "structured": "Organized sections",
        "bullet_points": "Clear bullet points",
        "paragraph": "Flowing paragraph",
        "executive": "Executive summary"
    }
    
    # Word limits
    WORD_LIMITS = [100, 200, 300, 500, 750, 1000]
    DEFAULT_WORD_LIMIT = 300
    
    # YouTube domains
    YOUTUBE_DOMAINS = ['youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com']

def get_api_key():
    """Get API key from secrets or input"""
    try:
        return st.secrets.get("GROQ_API_KEY", "")
    except:
        return ""

def init_session_state():
    """Initialize session state"""
    if 'summary_history' not in st.session_state:
        st.session_state.summary_history = []
    if 'usage_count' not in st.session_state:
        st.session_state.usage_count = 0