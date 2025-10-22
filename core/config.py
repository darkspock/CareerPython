from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 2880  # 48 hours

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    RAPIDAPI_KEY: str = "your_rapidapi_key_here"

    # AI Service Configuration
    AI_AGENT: str = "xai"  # Options: "xai" or "groq"

    # xAI Configuration
    XAI_API_KEY: str = ""
    XAI_API_URL: str = "https://api.x.ai/v1"
    XAI_MODEL: str = "grok-3-mini"
    XAI_MAX_TOKENS: int = 4000
    XAI_TIMEOUT: int = 60

    # Groq Configuration
    GROQ_API_KEY: str = ""
    GROQ_API_URL: str = "https://api.groq.com/openai/v1"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_MAX_TOKENS: int = 4000
    GROQ_TIMEOUT: int = 60

    # Environment settings
    ENVIRONMENT: str = "development"

    # Email service selection (smtp or mailgun)
    EMAIL_SERVICE: str = "smtp"

    # SMTP settings (for development with Mailpit)
    SMTP_HOST: str = "mailpit"
    SMTP_PORT: int = 1025
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@careerpython.local"
    SMTP_USE_TLS: bool = False

    # Mailgun settings (for production)
    MAILGUN_API_KEY: str = ""
    MAILGUN_DOMAIN: str = ""
    MAILGUN_API_URL: str = "https://api.mailgun.net/v3"

    # Frontend and support settings
    FRONTEND_URL: str = "http://localhost:3000"
    SUPPORT_EMAIL: str = "support@careerpython.com"

    # Storage settings
    STORAGE_TYPE: str = "local"  # Options: "local" or "s3"

    # Local storage settings (for development)
    LOCAL_STORAGE_PATH: str = "uploads"
    LOCAL_STORAGE_URL: str = "http://localhost:8000/uploads"

    # AWS S3 storage settings (for production)
    AWS_S3_BUCKET: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"

    # Storage configuration
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_EXTENSIONS: str = ".pdf,.doc,.docx,.txt"

    auth: AuthSettings = AuthSettings()

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()