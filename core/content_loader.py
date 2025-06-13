"""
Simple content loading for YouTube and web content
"""
import streamlit as st
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from core.validators import is_youtube_url

@st.cache_data(ttl=3600, show_spinner=False)
def load_content(url):
    """Load content from URL with caching"""
    try:
        if is_youtube_url(url):
            # Load YouTube content
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        else:
            # Load web content
            loader = UnstructuredURLLoader(
                urls=[url],
                ssl_verify=True,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            )
        
        documents = loader.load()
        
        if not documents:
            raise Exception("No content found at the provided URL")
        
        return documents, None
        
    except Exception as e:
        return None, str(e)

def get_content_info(documents):
    """Get basic info about loaded content"""
    if not documents:
        return {}
    
    total_words = sum(len(doc.page_content.split()) for doc in documents)
    metadata = documents[0].metadata
    
    info = {
        "total_words": total_words,
        "content_type": "YouTube Video" if is_youtube_url(metadata.get("source", "")) else "Web Article",
        "title": metadata.get("title", "Unknown")
    }
    
    return info