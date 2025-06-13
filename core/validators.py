"""
Simple input validation for Nutshell
"""
import validators
from urllib.parse import urlparse
from config.settings import AppConfig

def validate_api_key(api_key):
    """Validate API key"""
    if not api_key or len(api_key.strip()) < 10:
        return False, "Please provide a valid API key"
    return True, None

def validate_url(url):
    """Validate URL format"""
    if not url:
        return False, "Please provide a URL"
    
    # Add https if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    if not validators.url(url):
        return False, "Please provide a valid URL"
    
    return True, None

def is_youtube_url(url):
    """Check if URL is YouTube"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace('www.', '')
        return domain in AppConfig.YOUTUBE_DOMAINS
    except:
        return False

def validate_inputs(api_key, url):
    """Validate all inputs"""
    # Check API key
    valid, error = validate_api_key(api_key)
    if not valid:
        return False, error
    
    # Check URL
    valid, error = validate_url(url)
    if not valid:
        return False, error
    
    return True, None