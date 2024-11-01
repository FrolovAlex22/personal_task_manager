import dotenv
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# ACCESS_KEY=os.environ.get("S3_ACCESS_KEY")
# SECRET_KEY=os.environ.get("S3_SECRET_KEY")
# BUCKET_NAME=os.environ.get("S3_BUCKET_NAME")
# DB_HOST=os.getenv("DB_HOST")
# DB_PORT=os.getenv("DB_PORT")
# DB_USER=os.getenv("DB_USER")
# DB_PASS=os.getenv("DB_PASS")
# DB_NAME=os.getenv("DB_NAME")

# DOCKER = os.environ.get("DOCKER", "True") == "True"


class PostgresqlSettings(BaseModel):
    URL: str

class AuthSettings(BaseModel):
    KEY: str

class MainSettings(BaseModel):
    HOST: str
    PORT: int

class Settings(BaseSettings):
    DB: PostgresqlSettings
    AUTH: AuthSettings
    MAIN: MainSettings
    # DB_HOST: str
    # DB_PORT: str
    # DB_USER: str
    # DB_PASS: str
    # DB_NAME: str
    # DATABASE_URL: str = (
    #     f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    #     )
    app_title: str = "personal_task_manager"
    # project_name: str = "API personal_task_manager"
    # HOST: str = "127.0.0.1"
    # PORT: int = 8000

    # @property
    # def DATABASE_URL(self):
    #     # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
    #     return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=dotenv.find_dotenv(".env"),
        env_nested_delimiter="_",
    )


settings = Settings()