import streamlit as st
import re
from langchain.schema import Document
from langchain_community.document_loaders import UnstructuredURLLoader

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    st.error("youtube-transcript-api is not installed.")
    raise

def is_youtube_url(url):
    return "youtube.com" in url or "youtu.be" in url

def extract_video_id(url):
    """Extracts video ID from YouTube URL"""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def load_youtube_transcript(url):
    """Loads YouTube transcript as LangChain Document"""
    video_id = extract_video_id(url)
    if not video_id:
        return None, "Invalid YouTube URL"

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ' '.join([t['text'] for t in transcript])
        doc = Document(page_content=text, metadata={"source": url, "video_id": video_id})
        return [doc], None
    except Exception as e:
        return None, f"Transcript fetch failed: {e}"

@st.cache_data(ttl=3600)
def load_content(url):
    """Loads content from YouTube or web"""
    if is_youtube_url(url):
        return load_youtube_transcript(url)
    else:
        try:
            loader = UnstructuredURLLoader(urls=[url])
            docs = loader.load()
            return docs, None
        except Exception as e:
            return None, f"Web content load failed: {e}"

def get_content_info(documents):
    if not documents:
        return {}
    total_words = sum(len(doc.page_content.split()) for doc in documents)
    return {
        "total_words": total_words,
        "source": documents[0].metadata.get("source", ""),
        "video_id": documents[0].metadata.get("video_id", "")
    }
