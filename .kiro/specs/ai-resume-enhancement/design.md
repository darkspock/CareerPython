# Design Document

## Overview

The AI Resume Enhancement Platform is a web application that leverages artificial intelligence to improve users' resumes through automated data extraction, conversational interviews, and personalized content generation. The system follows Domain-Driven Design (DDD), Command Query Responsibility Segregation (CQRS), and Hexagonal Architecture principles to ensure maintainability, scalability, and clear separation of concerns.

The platform integrates with xAI for intelligent content processing and supports a tiered subscription model with different feature access levels. The frontend is built with React (located in `/client`), while the backend uses FastAPI with SQLAlchemy for data persistence.

## Architecture

### Hexagonal Architecture Implementation

The system follows hexagonal architecture with clear boundaries between layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   React Client  │  │  FastAPI Routes │                  │
│  │   (Frontend)    │  │   (Controllers) │                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                         │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Use Cases     │  │   Command/Query │                  │
│  │   (Services)    │  │    Handlers     │                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Domain Layer                            │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │    Entities     │  │  Domain Events  │                  │
│  │  Value Objects  │  │  Business Rules │                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                       │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Repositories  │  │   External APIs │                  │
│  │   (SQLAlchemy)  │  │   (xAI, Email)  │                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### CQRS Implementation

Commands and Queries are separated to optimize read and write operations:

**Commands (Write Operations):**
- CreateUserCommand
- UploadResumeCommand
- UpdateCandidateDataCommand
- StartInterviewCommand
- SubmitAnswerCommand
- GenerateResumeCommand
- ProcessPaymentCommand

**Queries (Read Operations):**
- GetCandidateProfileQuery
- GetInterviewProgressQuery
- GetResumePreviewQuery
- GetSubscriptionStatusQuery
- GetJobApplicationHistoryQuery

## Components and Interfaces

### Core Domain Entities

#### User Aggregate
```python
class User:
    - id: ULID
    - email: EmailAddress
    - password_hash: str
    - subscription: Subscription
    - created_at: datetime
    - is_active: bool
```

#### Candidate Aggregate
```python
class Candidate:
    - id: ULID
    - user_id: ULID
    - personal_info: PersonalInfo
    - experiences: List[Experience]
    - education: List[Education]
    - projects: List[Project]
    - job_categories: List[JobCategory]
    - profile_sections: Dict[SectionType, ProfileSection]
```

#### Interview Aggregate
```python
class Interview:
    - id: ULID
    - candidate_id: ULID
    - template: InterviewTemplate
    - status: InterviewStatus
    - answers: List[InterviewAnswer]
    - progress: InterviewProgress
    - created_at: datetime
    - completed_at: Optional[datetime]
```

#### Subscription Aggregate
```python
class Subscription:
    - id: ULID
    - user_id: ULID
    - tier: SubscriptionTier (FREE, STANDARD, PREMIUM)
    - status: SubscriptionStatus
    - expires_at: Optional[datetime]
    - usage_limits: UsageLimits
```

### External Service Interfaces

#### AI Service Interface
```python
class AIServiceInterface(ABC):
    @abstractmethod
    async def extract_resume_data(self, pdf_content: bytes) -> CandidateData
    
    @abstractmethod
    async def generate_interview_questions(self, context: InterviewContext) -> List[Question]
    
    @abstractmethod
    async def normalize_interview_responses(self, responses: List[Answer]) -> NormalizedProfile
    
    @abstractmethod
    async def generate_resume(self, profile: CandidateProfile) -> ResumeDocument
    
    @abstractmethod
    async def adapt_resume_to_job(self, profile: CandidateProfile, job_description: str) -> AdaptedResume
```

#### Payment Service Interface
```python
class PaymentServiceInterface(ABC):
    @abstractmethod
    async def process_payment(self, payment_data: PaymentData) -> PaymentResult
    
    @abstractmethod
    async def create_subscription(self, user_id: str, plan: SubscriptionPlan) -> Subscription
    
    @abstractmethod
    async def cancel_subscription(self, subscription_id: str) -> bool
```

#### Email Service Interface
```python
class EmailServiceInterface(ABC):
    @abstractmethod
    async def send_password_reset(self, email: str, reset_token: str) -> bool
    
    @abstractmethod
    async def send_welcome_email(self, email: str, user_name: str) -> bool
    
    @abstractmethod
    async def send_subscription_confirmation(self, email: str, subscription: Subscription) -> bool
```

### Application Services

#### Resume Processing Service
```python
class ResumeProcessingService:
    def __init__(self, ai_service: AIServiceInterface, candidate_repo: CandidateRepository):
        self.ai_service = ai_service
        self.candidate_repo = candidate_repo
    
    async def process_uploaded_resume(self, user_id: str, pdf_content: bytes) -> ProcessingResult:
        # Extract data using AI
        # Create/update candidate profile
        # Store original PDF in user_assets
        # Return processing results
```

#### Interview Service
```python
class InterviewService:
    def __init__(self, ai_service: AIServiceInterface, interview_repo: InterviewRepository):
        self.ai_service = ai_service
        self.interview_repo = interview_repo
    
    async def start_interview(self, candidate_id: str, template_type: InterviewTemplateType) -> Interview:
        # Initialize interview session
        # Generate first set of questions
        # Return interview instance
    
    async def process_answer(self, interview_id: str, answer: str) -> NextQuestion:
        # Store answer
        # Generate next question based on context
        # Update progress
```

#### Subscription Service
```python
class SubscriptionService:
    def __init__(self, payment_service: PaymentServiceInterface, user_repo: UserRepository):
        self.payment_service = payment_service
        self.user_repo = user_repo
    
    async def upgrade_subscription(self, user_id: str, plan: SubscriptionPlan) -> SubscriptionResult:
        # Process payment
        # Update user subscription
        # Send confirmation
    
    def check_usage_limits(self, user_id: str, action: UsageAction) -> bool:
        # Check current usage against limits
        # Return whether action is allowed
```

## Data Models

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id VARCHAR(26) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    subscription_tier VARCHAR(20) DEFAULT 'FREE',
    subscription_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### User Assets Table
```sql
CREATE TABLE user_assets (
    id VARCHAR(26) PRIMARY KEY,
    user_id VARCHAR(26) REFERENCES users(id),
    asset_type VARCHAR(50) NOT NULL,
    file_name VARCHAR(255),
    file_content BYTEA,
    text_content TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Candidates Table (Enhanced)
```sql
CREATE TABLE candidates (
    id VARCHAR(26) PRIMARY KEY,
    user_id VARCHAR(26) REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    date_of_birth DATE,
    city VARCHAR(100),
    country VARCHAR(100),
    job_category VARCHAR(50),
    expected_salary INTEGER,
    currency VARCHAR(10),
    relocation BOOLEAN,
    work_modality JSONB,
    languages JSONB,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    type VARCHAR(20) DEFAULT 'ENHANCED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Profile Sections Table
```sql
CREATE TABLE profile_sections (
    id VARCHAR(26) PRIMARY KEY,
    candidate_id VARCHAR(26) REFERENCES candidates(id),
    section_type VARCHAR(50) NOT NULL,
    completion_status VARCHAR(20) DEFAULT 'NOT_STARTED',
    content JSONB,
    ai_generated_content JSONB,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Interviews Table (Enhanced)
```sql
CREATE TABLE interviews (
    id VARCHAR(26) PRIMARY KEY,
    candidate_id VARCHAR(26) REFERENCES candidates(id),
    template_id VARCHAR(26) REFERENCES interview_templates(id),
    status VARCHAR(20) DEFAULT 'IN_PROGRESS',
    progress_percentage INTEGER DEFAULT 0,
    current_section VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Usage Tracking Table
```sql
CREATE TABLE usage_tracking (
    id VARCHAR(26) PRIMARY KEY,
    user_id VARCHAR(26) REFERENCES users(id),
    action_type VARCHAR(50) NOT NULL,
    action_date DATE NOT NULL,
    count INTEGER DEFAULT 1,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Value Objects

#### Subscription Tier
```python
class SubscriptionTier(Enum):
    FREE = "FREE"
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"

class UsageLimits:
    def __init__(self, tier: SubscriptionTier):
        self.tier = tier
        self.resume_downloads_per_week = self._get_download_limit()
        self.job_applications_per_day = self._get_application_limit()
    
    def _get_download_limit(self) -> int:
        limits = {
            SubscriptionTier.FREE: 1,
            SubscriptionTier.STANDARD: 10,
            SubscriptionTier.PREMIUM: -1  # Unlimited
        }
        return limits[self.tier]
    
    def _get_application_limit(self) -> int:
        limits = {
            SubscriptionTier.FREE: 0,
            SubscriptionTier.STANDARD: 3,
            SubscriptionTier.PREMIUM: 30
        }
        return limits[self.tier]
```

#### Interview Progress
```python
class InterviewProgress:
    def __init__(self):
        self.sections_completed: List[str] = []
        self.current_section: Optional[str] = None
        self.total_questions: int = 0
        self.answered_questions: int = 0
        self.completion_percentage: float = 0.0
    
    def calculate_progress(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return (self.answered_questions / self.total_questions) * 100
```

## Error Handling

### Domain Exceptions
```python
class DomainException(Exception):
    """Base exception for domain-related errors"""
    pass

class SubscriptionLimitExceededException(DomainException):
    """Raised when user exceeds subscription limits"""
    pass

class InvalidInterviewStateException(DomainException):
    """Raised when interview operation is invalid for current state"""
    pass

class AIProcessingException(DomainException):
    """Raised when AI service fails to process content"""
    pass

class PaymentProcessingException(DomainException):
    """Raised when payment processing fails"""
    pass
```

### Error Response Format
```python
class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime
    request_id: str
```

### Global Exception Handler
```python
@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error_code=exc.__class__.__name__,
            message=str(exc),
            timestamp=datetime.utcnow(),
            request_id=str(uuid.uuid4())
        ).dict()
    )
```

## Testing Strategy

### Unit Testing
- **Domain Entities**: Test business logic and invariants
- **Value Objects**: Test validation and behavior
- **Application Services**: Test use case orchestration
- **Command/Query Handlers**: Test CQRS implementation

### Integration Testing
- **Repository Layer**: Test database operations
- **External Services**: Test AI, payment, and email integrations
- **API Endpoints**: Test HTTP request/response handling

### End-to-End Testing
- **User Workflows**: Test complete user journeys
- **Subscription Flows**: Test payment and upgrade processes
- **AI Integration**: Test resume processing and interview flows

### Test Structure
```python
# Domain Tests
class TestCandidateAggregate:
    def test_create_candidate_with_valid_data(self):
        # Test candidate creation
        pass
    
    def test_add_experience_updates_profile(self):
        # Test experience addition
        pass

# Application Tests
class TestResumeProcessingService:
    @pytest.mark.asyncio
    async def test_process_uploaded_resume_success(self):
        # Test successful resume processing
        pass
    
    @pytest.mark.asyncio
    async def test_process_uploaded_resume_ai_failure(self):
        # Test AI service failure handling
        pass

# Integration Tests
class TestInterviewAPI:
    @pytest.mark.asyncio
    async def test_start_interview_endpoint(self):
        # Test interview start endpoint
        pass
```

### Mocking Strategy
- **AI Service**: Mock xAI responses for consistent testing
- **Payment Service**: Mock payment processing for subscription tests
- **Email Service**: Mock email sending for notification tests
- **Database**: Use in-memory SQLite for fast test execution

This design provides a robust foundation for the AI Resume Enhancement Platform, ensuring scalability, maintainability, and clear separation of concerns while supporting the complex business requirements of subscription management, AI integration, and multi-step user workflows.