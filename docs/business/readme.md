# ATS Monkey - Business Requirements Documentation

**Version:** 1.0
**Last Updated:** 2025-01-XX
**Status:** Active

---

## About ATS Monkey

ATS Monkey is an open-source enterprise-grade Applicant Tracking System (ATS) designed to serve organizations of all sizes—from early-stage startups to multinational corporations.

### Key Features

- **Customizable Workflows**: Fully configurable hiring processes per company
- **AI-Powered Intelligence**: Smart suggestions, automated screening, interview assistance
- **CRM Philosophy**: Treating candidates as valued customers with relationship-focused interactions
- **Multi-tenant Architecture**: From small teams to enterprise deployments
- **Open Source**: Full transparency, no vendor lock-in, community-driven

### Target Market

| Segment | Size | Key Needs |
|---------|------|-----------|
| Startup / Small Business | 1-50 employees | Speed, simplicity, cost-efficiency |
| Mid-Size Company | 51-500 employees | Scalability, structured processes |
| Enterprise / Large Corporation | 501+ employees | Compliance, complex workflows |
| Recruitment Agency | Any size | Multi-client management, high volume |

---

## Platform Modules

### Company Area
Complete recruitment management suite for organizations:
- Job position lifecycle management
- Candidate pipeline and workflow management
- Interview scheduling and evaluation
- Team collaboration and role-based access
- Analytics and reporting

### Job Listing Area
Public-facing job portal for talent attraction:
- Company career pages with branding
- Global job board across all companies
- SEO-optimized job listings
- Mobile-responsive application process

### Candidate Area
Comprehensive career platform for job seekers:
- Application tracking and management
- CV/Resume generation and AI optimization
- Interview preparation tools
- Training and coaching resources

### Admin Area
Internal platform administration:
- System metrics and analytics
- Company and candidate oversight
- Configuration management
- Impersonation for support

---

## Documentation Index

This business requirements documentation is organized as follows:

| Document | Description |
|----------|-------------|
| [00-executive-summary.md](./00-executive-summary.md) | High-level overview, vision, and market positioning |
| [01-company-module.md](./01-company-module.md) | Company area functional requirements |
| [02-job-listing-module.md](./02-job-listing-module.md) | Job portal and career pages requirements |
| [03-candidate-module.md](./03-candidate-module.md) | Candidate platform requirements |
| [04-admin-module.md](./04-admin-module.md) | Platform administration requirements |
| [05-interview-system.md](./05-interview-system.md) | Interview management system |
| [06-workflow-system.md](./06-workflow-system.md) | Unified workflow engine |
| [07-onboarding-system.md](./07-onboarding-system.md) | Company onboarding process |
| [08-feature-catalog.md](./08-feature-catalog.md) | Detailed feature implementation reference |
| [09-global-flows.md](./09-global-flows.md) | **End-to-end user journeys and process flows** |

---

## Key Business Capabilities

### Workflow System
- **Phases**: Macro-level stages (Sourcing, Evaluation, Offer)
- **Workflows**: Customizable pipelines within each phase
- **Stages**: Individual steps with validation and automation
- **Automatic Transitions**: Rule-based movement between stages

### Interview Management
- **Templates**: Reusable interview structures
- **Scoring**: Absolute scoring (higher is better)
- **Formats**: Self-conducted, AI-assisted, interviewer-led
- **External Interviewers**: Guest access for evaluators

### Customization System
- **Custom Fields**: Company-specific data capture
- **Validation Rules**: JsonLogic-based business rules
- **Automated Actions**: Stage-based triggers
- **Page Templates**: Customizable public content

---

## HR Expert Additions

Each document includes HR expert recommendations covering:

- **Candidate Experience**: Mobile-first, transparent processes, quick feedback
- **Diversity & Inclusion**: Blind screening, inclusive language, diversity metrics
- **Compliance & Legal**: GDPR/CCPA, EEO compliance, audit trails
- **Modern Hiring Practices**: Skills-based hiring, structured interviews, collaborative decisions

---

## Document Status

| Document | Status | Last Review |
|----------|--------|-------------|
| Executive Summary | Complete | 2025-01 |
| Company Module | Complete | 2025-01 |
| Job Listing Module | Complete | 2025-01 |
| Candidate Module | Complete | 2025-01 |
| Admin Module | Complete | 2025-01 |
| Interview System | Complete | 2025-01 |
| Workflow System | Complete | 2025-01 |
| Onboarding System | Complete | 2025-01 |
| Feature Catalog | Complete | 2025-01 |
| Global Flows | Complete | 2025-12 |

---

## Contributing

These are living documents. Contributions welcome for:
- Requirement clarifications
- Additional use cases
- HR industry best practices
- Compliance updates

---

**Document Owner**: Product Team
**Review Cycle**: Quarterly
