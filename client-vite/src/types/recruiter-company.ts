/**
 * Types for the recruiting company (the company using the platform)
 * This is different from the "company" entity that represents job applicant companies
 */

export type CompanyType = 
  | 'startup_small'
  | 'mid_size'
  | 'enterprise'
  | 'recruitment_agency';

export interface RecruiterCompany {
  id: string;
  name: string;
  domain: string;
  slug: string | null;
  logo_url: string | null;
  settings: Record<string, any>;
  status: string;
  company_type?: CompanyType;
  created_at: string;
  updated_at: string;
}

export interface UpdateRecruiterCompanyRequest {
  name: string;
  domain: string;
  slug?: string | null;
  logo_url?: string | null;
  settings: Record<string, any>;
  company_type?: CompanyType;
}

// Constants for UI
export const COMPANY_TYPE_OPTIONS = [
  { 
    value: 'startup_small', 
    label: 'Startup / Small Business',
    description: '1–50 employees, fast hiring, multi-role users'
  },
  { 
    value: 'mid_size', 
    label: 'Mid-Size Company',
    description: '51–500 employees, structured but flexible'
  },
  { 
    value: 'enterprise', 
    label: 'Enterprise / Large Corporation',
    description: '501+ employees, compliance-heavy, complex approvals'
  },
  { 
    value: 'recruitment_agency', 
    label: 'Recruitment Agency',
    description: 'Any size, high-volume, client-focused'
  }
] as const;
