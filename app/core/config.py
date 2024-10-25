import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

# ACCESS_KEY=os.environ.get("S3_ACCESS_KEY")
# SECRET_KEY=os.environ.get("S3_SECRET_KEY")
# BUCKET_NAME=os.environ.get("S3_BUCKET_NAME")
DB_HOST=os.environ.get("DB_HOST")
DB_PORT=os.environ.get("DB_PORT")
DB_USER=os.environ.get("DB_USER")
DB_PASS=os.environ.get("DB_PASS")
DB_NAME=os.environ.get("DB_NAME")

# DOCKER = os.environ.get("DOCKER", "True") == "True"


class Settings(BaseSettings):
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    app_title: str = "personal_task_manager"
    project_name: str = "API personal_task_manager"
    project_host: str = "127.0.0.1"
    project_port: int = 8000


settings = Settings()