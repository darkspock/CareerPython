"""Shared Container - Core services shared across all bounded contexts"""
from dependency_injector import containers, providers
from core.database import SQLAlchemyDatabase
from core.event_bus import EventBus
from core.config import settings
from src.notification_bc.notification.infrastructure.services.mailgun_service import MailgunService
from src.notification_bc.notification.infrastructure.services.smtp_email_service import SMTPEmailService
from src.framework.domain.infrastructure.storage_service_interface import StorageConfig
from src.framework.infrastructure.storage.storage_factory import StorageFactory
from src.framework.infrastructure.repositories.async_job_repository import AsyncJobRepository
from src.framework.infrastructure.jobs.async_job_service import AsyncJobService
from src.auth_bc.user.infrastructure.services.pdf_processing_service import PDFProcessingService
from src.notification_bc.notification.application.handlers.send_email_command_handler import SendEmailCommandHandler


class SharedContainer(containers.DeclarativeContainer):
    """Container para servicios compartidos (Database, EventBus, Email, AI, Storage)"""
    
    # Configuration
    config = providers.Configuration()
    
    # Load configuration from environment variables
    config.email_service.from_env("EMAIL_SERVICE", as_=str, default="smtp")
    config.ai_agent.from_env("AI_AGENT", as_=str, default="xai")
    config.storage_type.from_env("STORAGE_TYPE", as_=str, default="local")
    config.max_file_size_mb.from_env("MAX_FILE_SIZE_MB", as_=int, default=10)
    config.allowed_file_extensions.from_env("ALLOWED_FILE_EXTENSIONS", as_=str, default="pdf,doc,docx")
    
    # Core Services (Singletons)
    database = providers.Singleton(SQLAlchemyDatabase)
    event_bus = providers.Singleton(EventBus)
    
    # Email Service Factory
    @staticmethod
    def _get_email_service(email_service_type: str = None):
        """Factory method to create the appropriate email service based on configuration"""
        service_type = email_service_type or settings.EMAIL_SERVICE
        if service_type == "mailgun":
            return MailgunService()
        else:
            return SMTPEmailService()
    
    email_service = providers.Singleton(
        _get_email_service,
        email_service_type=config.email_service
    )

    # Email Command Handler
    send_email_command_handler = providers.Factory(
        SendEmailCommandHandler,
        email_service=email_service
    )

    # AI Service Factory
    @staticmethod
    def _get_ai_service(ai_agent: str = None):
        """Factory method to create the appropriate AI service based on configuration"""
        agent = ai_agent or settings.AI_AGENT
        if agent.lower() == "groq":
            from src.framework.infrastructure.services.ai.groq_service import GroqResumeAnalysisService
            return GroqResumeAnalysisService()
        else:
            from src.framework.infrastructure.services.ai.xai_service import XAIResumeAnalysisService
            return XAIResumeAnalysisService()
    
    ai_service = providers.Singleton(
        _get_ai_service,
        ai_agent=config.ai_agent
    )
    
    # Storage Service Factory
    @staticmethod
    def _get_storage_service(storage_type: str = None, max_file_size_mb: int = None, allowed_file_extensions: str = None):
        """Factory method to create the appropriate storage service based on configuration"""
        storage = storage_type or settings.STORAGE_TYPE
        max_size = max_file_size_mb or settings.MAX_FILE_SIZE_MB
        extensions = allowed_file_extensions or settings.ALLOWED_FILE_EXTENSIONS
        
        allowed_extensions = [ext.strip() for ext in extensions.split(',')]
        config = StorageConfig(
            max_file_size_mb=max_size,
            allowed_extensions=allowed_extensions
        )
        
        return StorageFactory.create_storage_service(
            storage_type=storage,
            config=config
        )
    
    storage_service = providers.Singleton(
        _get_storage_service,
        storage_type=config.storage_type,
        max_file_size_mb=config.max_file_size_mb,
        allowed_file_extensions=config.allowed_file_extensions
    )
    
    # Async Job Services
    async_job_repository = providers.Factory(
        AsyncJobRepository,
        database=database
    )
    
    async_job_service = providers.Factory(
        AsyncJobService,
        repository=async_job_repository
    )
    
    # PDF Processing Service
    pdf_processing_service = providers.Factory(
        PDFProcessingService
    )

