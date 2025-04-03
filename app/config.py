from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    mistral_api_key: str
    mistral_model: str = "mistral-large-latest"
    temperature: float = 0.1        


    model_config = ConfigDict(env_file=".env")

settings = Settings()
