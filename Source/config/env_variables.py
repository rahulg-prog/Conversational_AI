from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # OpenAI configurations
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME")
    
    #langsmith config
    LANGSMITH_TRACING: bool = os.getenv("LANGSMITH_TRACING", "true")
    LANGSMITH_ENDPOINT: str = os.getenv("LANGSMITH_ENDPOINT")
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT_NAME")
    
    #CONFIG PATH
    CONFIG_PATH: str = os.getenv("CONFIG_PATH")
    class Config:
        env_file = ".env"
        
settings = Settings()