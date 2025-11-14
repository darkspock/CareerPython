// Types for company registration
import type { CompanyType } from './recruiter-company';

export interface CompanyRegistrationRequest {
  // User data
  email: string;
  password: string;
  full_name: string;
  
  // Company data
  company_name: string;
  domain: string;
  logo_url?: string;
  contact_phone?: string;
  address?: string;
  company_type?: CompanyType;  // Company type for onboarding customization
  
  // Options
  initialize_workflows: boolean;      // Whether to initialize default workflows
  include_example_data: boolean;       // Whether to include sample data
  accept_terms: boolean;
  accept_privacy: boolean;
}

export interface CompanyRegistrationResponse {
  company_id: string;
  user_id: string;
  message: string;
  redirect_url?: string;
}

export interface LinkUserRequest {
  email: string;
  password: string;
  // Company data
  company_name: string;
  domain: string;
  logo_url?: string;
  contact_phone?: string;
  address?: string;
  company_type?: CompanyType;  // Company type for onboarding customization
  
  // Options
  initialize_workflows: boolean;      // Whether to initialize default workflows
  include_example_data: boolean;       // Whether to include sample data
  accept_terms: boolean;
  accept_privacy: boolean;
}

export interface LinkUserResponse {
  company_id: string;
  user_id: string;
  message: string;
  redirect_url?: string;
}

export interface CheckEmailResponse {
  exists: boolean;
  can_link: boolean; // If user exists and can be linked
}

