"""
Nutshell - AI-Powered Content Summarizer
Main application entry point
"""
import streamlit as st
from config.settings import AppConfig, init_session_state
from core.validators import validate_inputs
from core.content_loader import load_content, get_content_info
from core.summarizer import summarize_content
from ui.components import (
    render_header, render_sidebar, render_url_input, 
    render_summary_result, render_content_info, render_history,
    show_error, show_success, show_info
)

def main():
    """Main application function"""
    
    # Configure page
    st.set_page_config(
        page_title="Nutshell - AI Content Summarizer",
        page_icon="🥜",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Render header
    render_header()
    
    # Render sidebar and get configuration
    api_key, model_name, format_type, word_limit = render_sidebar()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # URL input section
        url, process_button = render_url_input()
        
        # Process content when button is clicked
        if process_button:
            # Validate inputs
            valid, error_message = validate_inputs(api_key, url)
            
            if not valid:
                show_error(error_message)
            else:
                # Add https if missing
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                try:
                    # Load content
                    with st.spinner("🔍 Loading content..."):
                        documents, error = load_content(url)
                    
                    if error:
                        show_error(f"Failed to load content: {error}")
                    else:
                        show_success("Content loaded successfully!")
                        
                        # Get content info
                        content_info = get_content_info(documents)
                        render_content_info(content_info)
                        
                        # Summarize content
                        with st.spinner("🧠 Generating summary..."):
                            summary_data = summarize_content(
                                documents, api_key, model_name, format_type, word_limit
                            )
                        
                        # Display results
                        render_summary_result(summary_data)
                        
                        # Add to history
                        st.session_state.summary_history.append(summary_data)
                        st.session_state.usage_count += 1
                        
                        show_success("Summary generated successfully!")
                        
                except Exception as e:
                    show_error(f"An error occurred: {str(e)}")
    
    with col2:
        # Usage stats
        st.subheader("📊 Usage Stats")
        st.metric("Total Summaries", st.session_state.usage_count)
        
        # Model info
        st.subheader("🤖 Current Model")
        st.info(f"**{model_name}**\n\n{AppConfig.GROQ_MODELS[model_name]}")
        
        # Recent history
        render_history()
        
        # Tips
        st.subheader("💡 Tips")
        st.markdown("""
        **Supported Content:**
        - YouTube videos
        - News articles  
        - Blog posts
        - Research papers
        
        **Best Practices:**
        - Use structured format for detailed content
        - Try bullet points for quick overviews
        - Executive format works great for business content
        """)

if __name__ == "__main__":
    main()