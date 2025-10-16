# Design Document

## Overview

The Resume Management System implements a comprehensive solution for creating, editing, previewing, and downloading general resumes. The system leverages existing candidate profile data and integrates with the current AI-powered platform architecture. The design focuses on the first phase implementation (General resumes only) while preparing the database structure for future Position-specific and Role-based resume types.

## Architecture

### High-Level Architecture

The system follows the existing Clean Architecture pattern with Domain-Driven Design principles:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Resume API    │  │  WYSIWYG Editor │  │   Preview   │ │
│  │   Endpoints     │  │   Interface     │  │   Service   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Resume Commands │  │  Resume Queries │  │   Resume    │ │
│  │   & Handlers    │  │   & Handlers    │  │ Controllers │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                     Domain Layer                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │     Resume      │  │    Resume       │  │   Resume    │ │
│  │    Entities     │  │   Services      │  │ Repositories│ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   SQLAlchemy    │  │   AI Services   │  │   Export    │ │
│  │   Repository    │  │   Integration   │  │  Services   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Integration Points

- **Candidate System**: Leverages existing candidate profile data (experience, education, projects, skills)
- **AI Services**: Integrates with existing XAI service for content generation and enhancement
- **User Management**: Uses existing user authentication and subscription management
- **Export System**: Extends existing resume export functionality

## Components and Interfaces

### 1. Domain Layer

#### Resume Entity
```python
@dataclass
class Resume:
    id: str
    user_id: str
    candidate_id: str
    name: str
    resume_type: ResumeType  # GENERAL, POSITION, ROLE
    position_id: Optional[str] = None  # For future Position resumes
    role: Optional[str] = None  # For future Role resumes
    
    # Content sections
    general_data: Dict[str, Any]
    summary: Optional[str] = None
    key_aspects: List[str] = field(default_factory=list)
    intro_letter: Optional[str] = None
    
    # AI-generated content
    ai_generated_summary: Optional[str] = None
    ai_generated_key_aspects: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: datetime
    updated_at: datetime
    last_generated_at: Optional[datetime] = None
    
    # Custom content (WYSIWYG edits)
    custom_content: Dict[str, Any] = field(default_factory=dict)
    formatting_preferences: Dict[str, Any] = field(default_factory=dict)
```

#### Resume Content Value Objects
```python
@dataclass
class ResumeContent:
    sections: Dict[str, ResumeSection]
    formatting: FormattingOptions
    metadata: ContentMetadata

@dataclass
class ResumeSection:
    title: str
    content: str
    order: int
    is_ai_generated: bool
    is_customized: bool
    last_updated: datetime
```

#### Domain Services
- **ResumeGenerationService**: Orchestrates resume creation from candidate data
- **ResumeContentService**: Manages content updates and AI integration
- **ResumeValidationService**: Validates resume data and completeness

### 2. Application Layer

#### Commands
```python
class CreateGeneralResumeCommand:
    user_id: str
    candidate_id: str
    name: str
    include_ai_enhancement: bool = True

class UpdateResumeContentCommand:
    resume_id: str
    user_id: str
    content_updates: Dict[str, Any]
    preserve_ai_content: bool = True

class GenerateResumePreviewCommand:
    resume_id: str
    user_id: str
    format_type: str = "professional"
```

#### Queries
```python
class GetUserResumesQuery:
    user_id: str
    resume_type: Optional[ResumeType] = None

class GetResumeContentQuery:
    resume_id: str
    user_id: str
    include_ai_content: bool = True
```

#### Handlers
- **CreateGeneralResumeHandler**: Handles resume creation workflow
- **UpdateResumeContentHandler**: Manages content updates and AI integration
- **GenerateResumePreviewHandler**: Creates preview content for display

### 3. Infrastructure Layer

#### Database Models
```python
class ResumeModel(Base):
    __tablename__ = "resumes"
    
    id = Column(String, primary_key=True, default=generate_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    candidate_id = Column(String, ForeignKey("candidates.id"), nullable=False)
    name = Column(String, nullable=False)
    resume_type = Column(Enum(ResumeType), nullable=False, default=ResumeType.GENERAL)
    
    # Future expansion fields
    position_id = Column(String, nullable=True)  # For Position resumes
    role = Column(String, nullable=True)  # For Role resumes
    
    # Content storage
    content_data = Column(JSON, nullable=True)  # Structured resume content
    ai_content = Column(JSON, nullable=True)  # AI-generated content
    custom_content = Column(JSON, nullable=True)  # WYSIWYG customizations
    formatting_preferences = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_generated_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("UserModel", back_populates="resumes")
    candidate = relationship("CandidateModel", back_populates="resumes")

class ResumeVersionModel(Base):
    __tablename__ = "resume_versions"
    
    id = Column(String, primary_key=True, default=generate_id)
    resume_id = Column(String, ForeignKey("resumes.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    content_snapshot = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_action = Column(String, nullable=True)  # "ai_generation", "user_edit", etc.
```

#### Services Integration
```python
class AIResumeContentService:
    def __init__(self, xai_service: XAIService):
        self.xai_service = xai_service
    
    async def generate_summary(self, candidate_data: CandidateData) -> str
    async def generate_key_aspects(self, candidate_data: CandidateData) -> List[str]
    async def enhance_content(self, content: str, context: Dict[str, Any]) -> str

class ResumeExportService:
    def __init__(self, pdf_service: PDFGenerationService):
        self.pdf_service = pdf_service
    
    async def export_to_pdf(self, resume: Resume, options: ExportOptions) -> bytes
    async def export_to_word(self, resume: Resume, options: ExportOptions) -> bytes
    async def export_to_html(self, resume: Resume, options: ExportOptions) -> str
```

### 4. Presentation Layer

#### API Endpoints
```python
# Resume Management
POST /api/resumes/general  # Create general resume
GET /api/resumes  # List user resumes
GET /api/resumes/{resume_id}  # Get resume details
PUT /api/resumes/{resume_id}  # Update resume content
DELETE /api/resumes/{resume_id}  # Delete resume

# Preview and Export
GET /api/resumes/{resume_id}/preview  # Get preview content
GET /api/resumes/{resume_id}/preview/html  # Get HTML preview
POST /api/resumes/{resume_id}/export  # Export resume
GET /api/resumes/{resume_id}/download/{format}  # Download resume

# WYSIWYG Editor Support
PUT /api/resumes/{resume_id}/sections/{section_id}  # Update section
POST /api/resumes/{resume_id}/ai-enhance  # Trigger AI enhancement
```

#### WYSIWYG Editor Integration
- **Rich Text Editor**: Integration with modern WYSIWYG editor (e.g., TinyMCE, Quill)
- **Real-time Preview**: Live preview updates as user edits content
- **Section Management**: Drag-and-drop section reordering
- **AI Assistance**: Inline AI suggestions and content enhancement

## Data Models

### Resume Content Structure
```json
{
  "resume_id": "resume_123",
  "content_data": {
    "personal_info": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "location": "City, Country"
    },
    "summary": {
      "content": "Professional summary...",
      "is_ai_generated": true,
      "last_updated": "2024-01-15T10:00:00Z"
    },
    "experience": [
      {
        "id": "exp_1",
        "job_title": "Software Engineer",
        "company": "Tech Corp",
        "description": "Job description...",
        "start_date": "2020-01-01",
        "end_date": "2023-12-31",
        "is_customized": false
      }
    ],
    "education": [...],
    "projects": [...],
    "skills": [...],
    "key_aspects": [
      "Strong problem-solving skills",
      "Experience with modern frameworks"
    ],
    "intro_letter": "Dear Hiring Manager..."
  },
  "formatting_preferences": {
    "template": "professional",
    "color_scheme": "blue",
    "font_family": "Arial",
    "section_order": ["summary", "experience", "education", "projects", "skills"]
  }
}
```

### AI Content Integration
```json
{
  "ai_content": {
    "generated_summary": "AI-generated professional summary...",
    "generated_key_aspects": [
      "Leadership in cross-functional teams",
      "Expertise in scalable system design"
    ],
    "content_suggestions": {
      "experience": [
        {
          "section_id": "exp_1",
          "suggestions": ["Consider highlighting specific achievements", "Add quantifiable results"]
        }
      ]
    },
    "last_ai_update": "2024-01-15T10:00:00Z",
    "ai_confidence_scores": {
      "summary": 0.95,
      "key_aspects": 0.88
    }
  }
}
```

## Error Handling

### Domain Exceptions
```python
class ResumeNotFoundException(DomainException):
    pass

class ResumeAccessDeniedException(DomainException):
    pass

class ResumeContentValidationException(DomainException):
    pass

class ResumeGenerationException(DomainException):
    pass
```

### Error Response Format
```json
{
  "error": {
    "code": "RESUME_GENERATION_FAILED",
    "message": "Failed to generate resume content",
    "details": {
      "missing_sections": ["experience"],
      "validation_errors": ["Name is required"]
    },
    "timestamp": "2024-01-15T10:00:00Z"
  }
}
```

## Testing Strategy

### Unit Tests
- **Domain Entities**: Test resume creation, validation, and business rules
- **Domain Services**: Test resume generation and content management logic
- **Application Handlers**: Test command and query processing
- **Infrastructure Services**: Test AI integration and export functionality

### Integration Tests
- **API Endpoints**: Test complete request/response cycles
- **Database Operations**: Test resume CRUD operations
- **AI Service Integration**: Test content generation and enhancement
- **Export Functionality**: Test PDF, Word, and HTML generation

### End-to-End Tests
- **Resume Creation Workflow**: Test complete resume creation process
- **WYSIWYG Editing**: Test content editing and preview functionality
- **Export and Download**: Test complete export and download workflow
- **Subscription Limits**: Test download limits and subscription enforcement

## Performance Considerations

### Caching Strategy
- **Resume Content**: Cache generated resume content for quick access
- **AI Responses**: Cache AI-generated content to reduce API calls
- **Preview Content**: Cache HTML previews for faster display

### Optimization Techniques
- **Lazy Loading**: Load resume sections on demand
- **Batch Processing**: Process multiple AI requests together
- **Async Operations**: Use async processing for AI content generation
- **Database Indexing**: Index frequently queried fields (user_id, candidate_id, resume_type)

### Scalability Considerations
- **Horizontal Scaling**: Design for multiple application instances
- **Database Partitioning**: Consider partitioning by user_id for large datasets
- **CDN Integration**: Use CDN for serving static resume templates and assets
- **Queue Processing**: Use message queues for heavy AI processing tasks

## Security Considerations

### Access Control
- **User Authorization**: Ensure users can only access their own resumes
- **Role-Based Access**: Support different access levels (view, edit, delete)
- **API Rate Limiting**: Implement rate limiting for resume operations

### Data Protection
- **Sensitive Data**: Encrypt sensitive resume content at rest
- **Audit Logging**: Log all resume access and modification events
- **Data Retention**: Implement data retention policies for deleted resumes

### AI Content Security
- **Content Validation**: Validate AI-generated content for appropriateness
- **Prompt Injection Protection**: Protect against malicious AI prompts
- **Content Filtering**: Filter potentially harmful or inappropriate content