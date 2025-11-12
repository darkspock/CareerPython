# Perfect Onboarding Process for ATS Monkey  
**Personal Project: AI-Powered Application Tracking System – CRM Philosophy**  
*Date:* 2025-11-09 | *Version:* 1.0  

---

## Overview  
The **perfect onboarding** must be **fast, smart, and personalized** based on company type.  
We apply **CRM philosophy**:  
- Build relationships (candidates as customers).  
- Intelligent automation (AI for suggestions).  
- Actionable data from Day 1.  
- Seamless, scalable user experience.  

The process is divided into **3 initialization levels**:  
1. **ONBOARDING** → Basic setup (roles + pages)  
2. **WORKFLOWS** → Default hiring workflows  
3. **SAMPLE DATA** → Optional sample data for evaluation  

> **AI Integration**: During creation, AI analyzes company name/description and **suggests type + initial content**.

---

## Step 0: Company Type Selection  
**Wizard question during company creation**:  
> *“What best describes your company?”*  

| Type | Characteristics | Example |
|------|------------------|---------|
| **Startup / Small Business** | 1–50 employees, fast hiring, multi-role users | Tech startup, local agency |
| **Mid-Size Company** | 51–500 employees, structured but flexible | Growing SaaS, retail chain |
| **Enterprise / Large Corporation** | 501+ employees, compliance-heavy, complex approvals | Fortune 500, global firm |
| **Recruitment Agency** | Any size, high-volume, client-focused | Staffing firm, headhunting |

> **Default**: Mid-Size Company  
> **AI Suggestion**: If user skips, AI predicts based on name (e.g., “TechFlow Inc.” → Startup).

---

## 1. ONBOARDING – Basic Configuration (Roles + Pages)

### Roles  
**CRM Focus**: Roles emphasize **candidate experience** and **relationship ownership**.

| Role | Responsibilities |
|------|------------------|
| **HR Manager** | Strategy, communication, offer stage |
| **Recruiter** | Sourcing, screening, engagement |
| **Tech Lead** | Technical assessments |
| **Hiring Manager** | Position-specific decisions |
| **Interviewer** | Conducts interviews |
| **Department Head** | High-level approvals |
| **CTO / C-Level** | Senior hires |

#### **Differentiation by Company Type**

| Type | Role Adjustments |
|------|------------------|
| **Startup/Small** | Combine HR Manager + Recruiter → **HR Generalist**<br>Add **Founder** for approvals |
| **Mid-Size** | Add **Talent Acquisition Specialist** |
| **Enterprise** | Add **Diversity & Inclusion Officer**, **Legal Reviewer** |
| **Agency** | Add **Client Manager**, **Sourcer** |

> **Implementation**: First user = Admin. AI suggests role assignments when inviting team.

---

### Default Pages  
5 pages auto-created. All support **HTML, SEO, versioning, multi-language**, and **Unlayer editor**.

| Page | Purpose | Public Endpoint |
|------|--------|-----------------|
| `public_company_description` | Public company overview | `/public/company/{id}/pages/public_company_description` |
| `job_position_description` | Benefits/culture in job posts | Same |
| `data_protection` | Privacy policy (GDPR/CCPA) | Same |
| `terms_of_use` | Platform legal terms | Same |
| `thank_you_application` | Post-apply message | Same |

#### **Behavior by Initialization**

| Mode | Status | Content |
|------|--------|--------|
| **Basic (no sample)** | DRAFT | Empty, ready to edit |
| **With Sample Data** | PUBLISHED (or DRAFT) | Pre-filled, customizable |

#### **Differentiation by Company Type**

| Type | Tone & Content |
|------|----------------|
| **Startup/Small** | Energetic, short, emojis: “Join our rocket ship!” |
| **Mid-Size** | Professional, growth-focused: “Career paths + benefits” |
| **Enterprise** | Formal, compliant: EEO, legal disclaimers |
| **Agency** | Client-centric: “Partner with us” + `{{client_name}}` placeholder |

> **AI Feature**: Auto-generate draft content:  
> _“Based on ‘Nexlify AI’, here’s your public description: ‘We’re building the future of…’”_

---

## 2. WORKFLOWS – Default Hiring Processes

Uses your **CompanyWorkflow + WorkflowStage** system.  
**CRM Focus**: Every stage builds **candidate trust** (emails, feedback, transparency).

### Job Position Workflow  
**Auto-created**: “Job Positions Workflow” (Kanban)

| Stage | Type | Emoji |
|-------|------|-------|
| Draft | INITIAL | 📝 |
| Under Review | PROGRESS | 🔍 |
| Approved | PROGRESS | ✅ |
| Published | SUCCESS | 🌐 |
| Closed | SUCCESS | 🔒 |
| Cancelled | FAIL | ❌ |

#### **Differentiation**

| Type | Adjustments |
|------|-------------|
| **Startup** | Skip “Under Review” → 4 stages |
| **Mid-Size** | Add “Budget Approval” |
| **Enterprise** | Add “Compliance Review” |
| **Agency** | Add “Client Approval” |

---

### Candidate Application Workflows  
**3 Phases** with **auto-transitions** on SUCCESS.

---

#### **Phase 1: Sourcing** (Kanban)  
*Objective: Screening & lead qualification*

| Stage | Type | Emoji |
|-------|------|-------|
| Pending | INITIAL | 📋 |
| Screening | PROGRESS | 🔍 |
| Qualified | SUCCESS → Phase 2 | ✅ |
| Not Suitable | FAIL | ❌ |
| On Hold | PROGRESS | ⏸️ |

---

#### **Phase 2: Evaluation** (Kanban)  
*Objective: Interviews & assessments*

| Stage | Type | Emoji |
|-------|------|-------|
| HR Interview | INITIAL | 👥 |
| Manager Interview | PROGRESS | 💼 |
| Assessment Test | PROGRESS | 📝 |
| Executive Interview | PROGRESS | 🎯 |
| Selected | SUCCESS → Phase 3 | ✅ |
| Rejected | FAIL | ❌ |

---

#### **Phase 3: Offer & Pre-Onboarding** (List View)  
*Objective: Close the deal*

| Stage | Type | Emoji |
|-------|------|-------|
| Offer Proposal | INITIAL | 💌 |
| Negotiation | PROGRESS | 🤝 |
| Document Submission | PROGRESS | 📄 |
| Document Verification | SUCCESS | ✅ |
| Lost | FAIL | ❌ |

---

#### **Differentiation by Company Type**

| Type | Sourcing | Evaluation | Offer |
|------|----------|------------|-------|
| **Startup** | 3 stages (fast) | 4 stages | 3 stages |
| **Mid-Size** | Standard | + Team Fit Interview | Standard |
| **Enterprise** | + Background Check | + Panel + Reference | + Contract Review |
| **Agency** | + Client Matching | + Client Interview | + Placement Fee |

---

#### **Stage Configuration (Per WORKFLOW2.md / WORKFLOW3.md)**

| Config | Details |
|--------|--------|
| **Roles** | e.g., HR in Sourcing, Tech Lead in Assessment |
| **Emails** | Auto-send on stage entry (Unlayer templates) |
| **Deadline** | e.g., 3 days (Sourcing), 7 days (Evaluation) |
| **Cost** | e.g., $100 (interview), $50 (test) |
| **Custom Fields** | See below |

---

### Recommended Custom Fields (CRM-Driven)

| Category | Field | Type | Visibility | Suggested Stage |
|---------|-------|------|------------|-----------------|
| **Compensation** | Salary Range | Text/Number | Internal | All |
| | Current Salary | Number | Internal | Sourcing |
| | Salary Expectation | Number | Internal | Offer |
| **Availability** | Start Date | Date | Internal | Offer |
| | Notice Period | Text | Internal | Offer |
| **Evaluation** | Technical Score | Number (0–100) | Internal | Assessment |
| | Cultural Fit Score | Number (0–100) | Internal | Interviews |
| | Feedback | Textarea | Internal | All |
| **Offer** | Salary Offer | Number | Internal | Offer |
| | Benefits Package | Textarea | Internal | Offer |
| | Start Date | Date | Internal | Offer |
| **Documents** | Document Status | Select | Internal | Verification |
| | Missing Docs | Text | Internal | Submission |
| **Source** | Recruitment Source | Select | Internal | Sourcing |
| | Recruiter Notes | Textarea | Internal | All |

#### **Type-Specific Fields**

| Type | Extra Fields |
|------|--------------|
| **Startup** | **Equity Offer** (Number/%) |
| **Mid-Size** | **Relocation Assistance** (Yes/No + Details) |
| **Enterprise** | **Diversity Metrics** (Select: Underrepresented) – *Mandatory in Sourcing* |
| **Agency** | **Client Fit Score**, **Bill Rate** (Currency) |

> **AI Suggestion**: “For your startup, add ‘Equity’ field in Offer stage?”

---

## 3. SAMPLE DATA – Optional Evaluation Mode

| Item | Quantity | Details |
|------|----------|--------|
| Candidates | 50 | Varied stages, sources, scores |
| Job Positions | 10 | Draft → Published |
| Users | 10 | With roles, tasks, comments |
| Applications | 10 | Linked to positions + users |

#### **Differentiation**

| Type | Scale | Focus |
|------|-------|-------|
| **Startup** | 20 candidates, 5 positions | Agile, quick hires |
| **Mid-Size** | Standard | Diverse analytics |
| **Enterprise** | 100 candidates | Compliance scenarios |
| **Agency** | Standard + client tags | Multi-client pipelines |

> **AI-Generated**: Realistic names, resumes, comments  
> **Opt-In**: Checkbox: “Load sample data?”  
> **Cleanup**: `Reset Company Data` command

---

## Onboarding Flow (User Journey)

```mermaid
graph TD
    A[Create Company] --> B[Select Type <br> (AI suggests)]
    B --> C[Auto-Create Roles + Pages]
    C --> D[Auto-Create Workflows]
    D --> E[Offer Sample Data?]
    E -->|Yes| F[Load AI-Generated Data]
    E -->|No| G[Go to Dashboard]
    G --> H[Guided Tour: "Edit your first workflow"]