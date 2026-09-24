from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    chroma_path: str = "./chroma_data"

    min_fit_to_tailor: int = 20


settings = Settings()