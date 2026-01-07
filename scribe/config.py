import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from current directory or project root
load_dotenv()

# Also try to load from ~/.scriberc
home_config = Path.home() / ".scriberc"
if home_config.exists():
    load_dotenv(home_config)


def get_api_key(provider="deepseek"):
    """Get API key for the specified provider"""
    if provider == "deepseek":
        key = os.getenv("DEEPSEEK_API_KEY")
        if not key:
            raise ValueError(
                "DEEPSEEK_API_KEY not found. Set it in .env or ~/.scriberc"
            )
        return key
    elif provider == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError(
                "OPENAI_API_KEY not found. Set it in .env or ~/.scriberc"
            )
        return key
    else:
        raise ValueError(f"Unknown provider: {provider}")


def get_base_url(provider="deepseek"):
    """Get base URL for the specified provider"""
    if provider == "deepseek":
        return "https://api.deepseek.com"
    elif provider == "openai":
        return None  # OpenAI client uses default
    else:
        raise ValueError(f"Unknown provider: {provider}")


def get_model(provider="deepseek"):
    """Get model name for the specified provider"""
    if provider == "deepseek":
        return "deepseek-chat"
    elif provider == "openai":
        return "gpt-4o-mini"
    else:
        raise ValueError(f"Unknown provider: {provider}")
