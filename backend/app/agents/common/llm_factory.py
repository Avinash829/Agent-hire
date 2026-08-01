from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.settings import get_settings
from app.logging.logger import get_logger

logger = get_logger(__name__)

def get_gemini_llm_with_fallbacks(temperature: float = 0.2):
    """
    Creates a ChatGoogleGenerativeAI model with built-in fallbacks.
    If the primary model fails (e.g. 429 quota limit or 404), 
    it automatically attempts the secondary models.
    """
    settings = get_settings()
    
    # 1. Define your primary model (e.g., the standard Flash model)
    primary_llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash", 
        google_api_key=settings.gemini_api_key,
        temperature=temperature,
        max_retries=1 # Keep low so it falls back quickly
    )

    # 2. Define your fallback models
    # If 3.6-flash hits a rate limit, it will try 3.5-flash-lite, etc.
    fallback_1 = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite", 
        google_api_key=settings.gemini_api_key,
        temperature=temperature,
        max_retries=1
    )
    
    fallback_2 = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash", 
        google_api_key=settings.gemini_api_key,
        temperature=temperature,
        max_retries=1
    )

    # 3. Chain them together using with_fallbacks
    # If primary_llm fails, it tries fallback_1. If that fails, it tries fallback_2.
    llm_with_fallbacks = primary_llm.with_fallbacks(
        fallbacks=[fallback_1, fallback_2]
    )
    
    return llm_with_fallbacks