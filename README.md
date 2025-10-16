# CareerPython 🚀

> **Advanced Career Management Platform** - A full-stack application showcasing Clean Architecture, Domain-Driven Design, and modern Python development practices.

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19.1.1-blue?logo=react)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8.3-blue?logo=typescript)](https://typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-containerized-blue?logo=docker)](https://docker.com)

## 🎯 Project Overview

CareerPython is a comprehensive career management platform that demonstrates advanced software engineering practices through a real-world application. Built with **Clean Architecture** principles and **Domain-Driven Design**, it showcases enterprise-level Python development skills ideal for technical recruiters and hiring managers.

### Key Features

- 👥 **Candidate Management** - Complete candidate lifecycle management with profiles, skills, and preferences
- 📄 **AI-Powered Resume Builder** - Generate tailored resumes with AI enhancement and multiple formats
- 💼 **Job Position Management** - Full job posting lifecycle with approval workflows and matching
- 🏢 **Company Administration** - Multi-tenant company management with role-based access
- 🎤 **Interview Templates** - Structured interview processes with customizable templates
- 📊 **Application Tracking** - End-to-end candidate application tracking system
- 🔔 **Notification System** - Real-time notifications and email communications
- 📱 **Responsive UI** - Modern React interface with internationalization (i18n)

## 🏗️ Architecture Highlights

This project demonstrates **professional-grade software architecture** patterns:

### Clean Architecture & DDD
```
├── Domain Layer (Business Logic)
│   ├── Entities (Candidate, JobPosition, Company, Resume)
│   ├── Value Objects (CandidateId, Email, SalaryRange)
│   ├── Domain Services & Events
│   └── Repository Interfaces
├── Application Layer (Use Cases)
│   ├── Commands (Write Operations)
│   ├── Queries (Read Operations)
│   ├── Handlers (Business Logic)
│   └── DTOs (Data Transfer)
├── Infrastructure Layer (External Concerns)
│   ├── Database (SQLAlchemy ORM)
│   ├── External APIs & Services
│   └── Repository Implementations
└── Presentation Layer (API & UI)
    ├── FastAPI Controllers
    ├── Request/Response Models
    └── React Frontend
```

### Advanced Patterns Implemented

- **🎯 CQRS (Command Query Responsibility Segregation)** - Separate read/write operations
- **🔄 Event-Driven Architecture** - Domain events with async processing
- **💉 Dependency Injection** - Full IoC container with dependency-injector
- **🏭 Factory & Builder Patterns** - Domain entity creation and resume building
- **📦 Repository Pattern** - Clean data access abstraction
- **🔌 Strategy Pattern** - Multiple resume generation strategies
- **🎪 Mediator Pattern** - Command/Query bus implementation
- **🎭 Adapter Pattern** - External service integrations

## 🛠️ Technical Stack

### Backend (Python)
- **FastAPI** - Modern, fast web framework with automatic API documentation
- **Python 3.13** - Latest Python features and performance improvements
- **SQLAlchemy** - Advanced ORM with relationship mapping
- **PostgreSQL** - Production-grade relational database
- **Redis** - Caching and session management
- **Dramatiq** - Background job processing with Redis broker
- **Alembic** - Database migrations and schema management
- **Pydantic** - Data validation and settings management
- **Dependency Injector** - Professional IoC container
- **PyJWT** - JWT token authentication
- **ReportLab & WeasyPrint** - PDF generation for resumes
- **Pytest** - Comprehensive testing framework

### Frontend (React/TypeScript)
- **React 19** - Latest React with concurrent features
- **TypeScript 5.8** - Type-safe development
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **TipTap** - Rich text editor for resume building
- **React Hook Form** - Form validation and management
- **Framer Motion** - Smooth animations and transitions
- **i18next** - Internationalization (English/Spanish)
- **React Router** - Client-side routing
- **DnD Kit** - Drag and drop functionality

### DevOps & Infrastructure
- **Docker** - Containerized development and deployment
- **Docker Compose** - Multi-service orchestration
- **GitHub Actions** - Complete CI/CD pipeline
- **Nginx** - Reverse proxy and static asset serving
- **UV** - Ultra-fast Python package management

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.13+ (for local development)
- Node.js 18+ (for frontend development)

### Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/CareerPython.git
cd CareerPython
```

2. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start with Docker (Recommended)**
```bash
make start          # Start all services
make logs           # View logs
make migrate        # Run database migrations
```

4. **Local Development**
```bash
# Backend
uv venv
uv sync
make rebuild-venv

# Frontend
cd client-vite
npm install
npm run dev
```

### Available Commands

```bash
# Docker Operations
make start          # Start development environment
make stop           # Stop all services
make build          # Build containers
make logs          # View service logs

# Database
make migrate        # Run migrations
make revision m="description"  # Create new migration

# Development
make test          # Run test suite
make bash          # Access container shell
```

## 🧪 Testing & Quality

This project demonstrates **professional testing practices**:

- **Unit Tests** - Domain logic and business rules
- **Integration Tests** - Database and external service interactions
- **Architecture Tests** - Enforce Clean Architecture boundaries
- **API Tests** - FastAPI endpoint testing
- **Frontend Tests** - React component testing
- **E2E Tests** - Full user workflow testing with Playwright

### Code Quality Tools
- **MyPy** - Static type checking
- **Flake8** - Code style and quality
- **Pytest Coverage** - Test coverage reporting
- **Pre-commit Hooks** - Automated code formatting
- **Bandit** - Security vulnerability scanning

## 📊 API Documentation

The API is fully documented with **OpenAPI/Swagger**:

- **Development**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key API Endpoints

```python
# Candidate Management
POST   /api/candidates                    # Create candidate
GET    /api/candidates/{id}               # Get candidate details
PUT    /api/candidates/{id}               # Update candidate
GET    /api/candidates                    # List candidates with filters

# Resume Operations
POST   /api/candidates/{id}/resumes       # Create resume
GET    /api/resumes/{id}                  # Get resume
PUT    /api/resumes/{id}                  # Update resume content
POST   /api/resumes/{id}/generate-pdf     # Generate PDF

# Job Management
POST   /api/admin/job-positions           # Create job position
GET    /api/admin/job-positions           # List job positions
PUT    /api/admin/job-positions/{id}      # Update job position
POST   /api/admin/job-positions/{id}/approve # Approve job posting

# Interview Templates
POST   /api/admin/interview-templates     # Create template
GET    /api/admin/interview-templates     # List templates
PUT    /api/admin/interview-templates/{id} # Update template
```

## 🎨 Frontend Features

The React frontend showcases **modern web development**:

- **Responsive Design** - Mobile-first approach with Tailwind CSS
- **Rich Text Editing** - Professional resume editing with TipTap
- **Real-time Updates** - Live form validation and feedback
- **Drag & Drop** - Intuitive resume section reordering
- **Internationalization** - English and Spanish support
- **Accessibility** - WCAG compliance and keyboard navigation
- **Performance** - Code splitting and lazy loading
- **State Management** - React hooks and context API

## 🔒 Security Features

- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - Argon2 password hashing
- **CORS Configuration** - Proper cross-origin resource sharing
- **Input Validation** - Pydantic models for request validation
- **SQL Injection Prevention** - SQLAlchemy ORM protection
- **Security Headers** - Comprehensive security header configuration

## 📈 Performance & Scalability

- **Database Optimization** - Indexed queries and connection pooling
- **Caching Strategy** - Redis caching for frequently accessed data
- **Background Processing** - Async job processing with Dramatiq
- **API Rate Limiting** - Request throttling and abuse prevention
- **Static Asset Optimization** - Nginx serving with compression
- **Database Migrations** - Safe schema evolution with Alembic

## 🌍 Production Ready

This application includes **production-grade features**:

- **Health Checks** - Application and database health monitoring
- **Logging** - Structured logging with different levels
- **Monitoring** - Application metrics and error tracking
- **Backup Systems** - Database backup and recovery procedures
- **Load Balancing** - Nginx reverse proxy configuration
- **SSL/TLS** - HTTPS encryption support
- **Environment Management** - Development, staging, and production configs

## 🔧 Development Workflow

The project follows **professional development practices**:

1. **Feature Branches** - Git flow with feature/bugfix branches
2. **Code Reviews** - Pull request reviews with GitHub
3. **Automated Testing** - CI/CD pipeline with GitHub Actions
4. **Code Quality Gates** - Automated linting and testing
5. **Database Migrations** - Safe schema evolution
6. **Documentation** - Comprehensive code and API documentation

## 🏛️ Why This Project Demonstrates Senior-Level Skills

### Architecture & Design
✅ **Clean Architecture** - Proper separation of concerns and dependency inversion
✅ **Domain-Driven Design** - Rich domain models with business logic encapsulation
✅ **SOLID Principles** - Single responsibility, open/closed, and dependency inversion
✅ **Design Patterns** - Multiple patterns applied appropriately

### Technical Proficiency
✅ **Modern Python** - Python 3.13 with advanced features and type hints
✅ **Async Programming** - Proper async/await usage and background processing
✅ **Database Design** - Complex relationships and optimized queries
✅ **API Design** - RESTful APIs with proper HTTP status codes and documentation

### Engineering Practices
✅ **Testing Strategy** - Unit, integration, and e2e testing
✅ **CI/CD Pipeline** - Automated testing, building, and deployment
✅ **Code Quality** - Linting, type checking, and security scanning
✅ **Documentation** - Comprehensive README and API docs

### Full-Stack Capabilities
✅ **Backend Development** - FastAPI with advanced Python patterns
✅ **Frontend Development** - Modern React with TypeScript
✅ **DevOps** - Docker, containerization, and deployment automation
✅ **Database Management** - PostgreSQL with migrations and optimization

## 📞 Contact

**Juan Macías**
📧 [extjmv@gmail.com](mailto:extjmv@gmail.com)
💼 [LinkedIn Profile](https://linkedin.com/in/juanmaciasvela)

---

⭐ **If this project demonstrates the kind of Python expertise you're looking for, let's connect!**

*This project showcases production-ready code, architectural best practices, and full-stack development capabilities that translate directly to enterprise software development roles.*