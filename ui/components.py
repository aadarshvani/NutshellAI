"""
Simple UI components for Nutshell
"""
import streamlit as st
from config.settings import AppConfig

def render_header():
    """Render app header"""
    st.title(AppConfig.APP_NAME)
    st.markdown(f"*{AppConfig.APP_TAGLINE}*")
    st.markdown("---")

def render_sidebar():
    """Render sidebar with configuration options"""
    st.sidebar.header("⚙️ Configuration")
    
    # API Key input
    st.sidebar.subheader("🔑 API Key")
    api_key = st.sidebar.text_input(
        "Groq API Key", 
        value=st.session_state.get('api_key', ''),
        type='password',
        help="Get your free API key from console.groq.com"
    )
    
    if api_key:
        st.session_state['api_key'] = api_key
    
    # Model selection
    st.sidebar.subheader("🤖 AI Model")
    model_name = st.sidebar.selectbox(
        "Choose Model",
        options=list(AppConfig.GROQ_MODELS.keys()),
        help="Different models have different strengths"
    )
    
    # Summary format
    st.sidebar.subheader("📝 Summary Format")
    format_type = st.sidebar.selectbox(
        "Output Format",
        options=list(AppConfig.SUMMARY_FORMATS.keys()),
        format_func=lambda x: AppConfig.SUMMARY_FORMATS[x]
    )
    
    # Word limit
    word_limit = st.sidebar.selectbox(
        "Word Limit",
        options=AppConfig.WORD_LIMITS,
        index=AppConfig.WORD_LIMITS.index(AppConfig.DEFAULT_WORD_LIMIT)
    )
    
    # Quick link
    st.sidebar.markdown("---")
    st.sidebar.markdown("[Get Groq API Key →](https://console.groq.com/keys)")
    
    return api_key, model_name, format_type, word_limit

def render_url_input():
    """Render URL input section"""
    st.subheader("🔗 Content Source")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url = st.text_input(
            "Enter URL (YouTube video or web article)",
            placeholder="https://www.youtube.com/watch?v=... or https://example.com/article",
            help="Paste any YouTube video URL or web article URL"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
        process_button = st.button("🚀 Summarize", type="primary", use_container_width=True)
    
    return url, process_button

def render_summary_result(summary_data):
    """Render summary results"""
    st.subheader("📋 Summary")
    
    # Display summary
    st.markdown(summary_data["summary"])
    
    # Display metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Word Count", summary_data["word_count"])
    with col2:
        st.metric("Format", summary_data["format_type"].title())
    with col3:
        st.metric("Model", summary_data["model_used"])

def render_content_info(content_info):
    """Render content information"""
    if not content_info:
        return
    
    st.subheader("ℹ️ Content Info")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Type:** {content_info.get('content_type', 'Unknown')}")
        st.info(f"**Words:** {content_info.get('total_words', 0):,}")
    with col2:
        if content_info.get('title'):
            st.info(f"**Title:** {content_info['title'][:50]}...")

def render_history():
    """Render summary history"""
    if not st.session_state.summary_history:
        return
    
    st.subheader("📚 Recent Summaries")
    
    for i, item in enumerate(reversed(st.session_state.summary_history[-5:])):  # Show last 5
        with st.expander(f"Summary {len(st.session_state.summary_history) - i}"):
            st.markdown(item["summary"][:200] + "..." if len(item["summary"]) > 200 else item["summary"])
            st.caption(f"Model: {item['model_used']} | Format: {item['format_type']} | Words: {item['word_count']}")

def show_error(message):
    """Show error message"""
    st.error(f"❌ {message}")

def show_success(message):
    """Show success message"""
    st.success(f"✅ {message}")

def show_info(message):
    """Show info message"""
    st.info(f"ℹ️ {message}")

def show_warning(message):
    """Show warning message"""
    st.warning(f"⚠️ {message}")