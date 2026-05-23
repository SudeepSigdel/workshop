from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_hostname: str
    db_port: str
    db_name: str

    db_string: str

    secret_key: str
    algorithm: str
    token_expiration_time: int

    class Config:
        env_file = ".env"

settings = Settings() #type: ignore