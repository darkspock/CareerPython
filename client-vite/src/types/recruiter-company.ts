/**
 * Types for the recruiting company (the company using the platform)
 * This is different from the "company" entity that represents job applicant companies
 */

export interface RecruiterCompany {
  id: string;
  name: string;
  domain: string;
  slug: string | null;
  logo_url: string | null;
  settings: Record<string, any>;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface UpdateRecruiterCompanyRequest {
  name: string;
  domain: string;
  slug?: string | null;
  logo_url?: string | null;
  settings: Record<string, any>;
}
