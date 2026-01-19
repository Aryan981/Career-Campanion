import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    # Comma-separated list of model IDs to try in order
    model_ids: str = os.getenv(
        "MODEL_IDS", 
        "meta-llama/llama-3.3-70b-instruct:free,google/gemini-2.0-flash-exp:free,mistralai/mistral-small-3.1-24b-instruct:free,google/gemma-3-27b-it:free"
    )
    
    @property
    def model_list(self) -> list[str]:
        return [m.strip() for m in self.model_ids.split(",") if m.strip()]

    # Pydantic AI specific
    log_level: str = "INFO"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
