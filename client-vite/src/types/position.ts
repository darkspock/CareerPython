// Position/Job Opening types

// Work location type options
export const WORK_LOCATION_OPTIONS = [
  { value: 'on_site', label: 'On-site' },
  { value: 'remote', label: 'Remote' },
  { value: 'hybrid', label: 'Hybrid' },
  { value: 'flexible', label: 'Flexible' }
] as const;

// Language options
export const LANGUAGE_OPTIONS = [
  { value: 'spanish', label: 'Spanish' },
  { value: 'english', label: 'English' },
  { value: 'french', label: 'French' },
  { value: 'german', label: 'German' },
  { value: 'portuguese', label: 'Portuguese' },
  { value: 'italian', label: 'Italian' },
  { value: 'chinese', label: 'Chinese' },
  { value: 'japanese', label: 'Japanese' }
] as const;

// Language level options (matching backend LanguageLevelEnum)
export const LANGUAGE_LEVEL_OPTIONS = [
  { value: 'none', label: 'None' },
  { value: 'basic', label: 'Basic' },
  { value: 'conversational', label: 'Conversational' },
  { value: 'professional', label: 'Professional' }
] as const;

// Desired role options (matching backend PositionRoleEnum)
export const DESIRED_ROLE_OPTIONS = [
  { value: 'manage_people', label: 'Manage People' },
  { value: 'lead_initiatives', label: 'Lead Initiatives' },
  { value: 'technology', label: 'Technology' },
  { value: 'sales', label: 'Sales' },
  { value: 'financial', label: 'Financial' },
  { value: 'hr', label: 'HR' },
  { value: 'executive', label: 'Executive' },
  { value: 'operations', label: 'Operations' },
  { value: 'marketing', label: 'Marketing' },
  { value: 'product', label: 'Product' },
  { value: 'legal_compliance', label: 'Legal & Compliance' },
  { value: 'customer_success', label: 'Customer Success' }
] as const;
export interface Position {
  id: string;
  company_id: string;
  company_name?: string; // Populated when fetching with company info
  title: string;
  description?: string;
  department?: string;
  location?: string;
  work_location_type: 'on_site' | 'remote' | 'hybrid' | 'flexible';
  salary_range?: {
    min_amount: number;
    max_amount: number;
    currency: string;
  };
  contract_type: 'full_time' | 'part_time' | 'contract' | 'internship';
  requirements?: Record<string, any>;
  job_category: string;
  position_level?: 'junior' | 'mid' | 'senior' | 'lead';
  number_of_openings: number;
  application_instructions?: string;
  benefits?: string[];
  working_hours?: string;
  travel_required?: boolean;
  languages_required?: Array<{language: string, level: string}>;
  visa_sponsorship: boolean;
  contact_person?: string;
  reports_to?: string;
  status: 'pending' | 'approved' | 'rejected' | 'open' | 'closed' | 'paused';
  desired_roles?: string[]; // Desired role types for candidates
  open_at?: string;
  application_deadline?: string;
  skills?: string[];
  application_url?: string;
  application_email?: string;
  created_at?: string;
  updated_at?: string;
  // Legacy fields for backward compatibility
  employment_type?: 'full_time' | 'part_time' | 'contract' | 'internship' | 'freelance';
  experience_level?: 'entry' | 'mid' | 'senior' | 'executive';
  salary_min?: number;
  salary_max?: number;
  salary_currency?: string;
  is_remote?: boolean;
  is_active?: boolean;
}

export interface CreatePositionRequest {
  company_id: string;
  title: string;
  description?: string;
  department?: string;
  location?: string;
  employment_type?: 'full_time' | 'part_time' | 'contract' | 'internship' | 'freelance';
  experience_level?: 'entry' | 'mid' | 'senior' | 'executive';
  salary_min?: number;
  salary_max?: number;
  salary_currency?: string;
  requirements?: string[];
  benefits?: string[];
  skills?: string[];
  is_remote?: boolean;
  application_deadline?: string;
  application_url?: string;
  application_email?: string;
  // New fields
  working_hours?: string;
  travel_required?: number;
  visa_sponsorship?: boolean;
  contact_person?: string;
  reports_to?: string;
  number_of_openings?: number;
  job_category?: string;
  languages_required?: Record<string, string>;
  desired_roles?: string[];
}

export interface UpdatePositionRequest {
  title?: string;
  description?: string;
  department?: string;
  location?: string;
  employment_type?: 'full_time' | 'part_time' | 'contract' | 'internship' | 'freelance';
  experience_level?: 'entry' | 'mid' | 'senior' | 'executive';
  salary_min?: number;
  salary_max?: number;
  salary_currency?: string;
  requirements?: string[];
  benefits?: string[];
  skills?: string[];
  is_remote?: boolean;
  application_deadline?: string;
  application_url?: string;
  application_email?: string;
  // New fields
  working_hours?: string;
  travel_required?: number;
  visa_sponsorship?: boolean;
  contact_person?: string;
  reports_to?: string;
  number_of_openings?: number;
  job_category?: string;
  languages_required?: Record<string, string>;
  desired_roles?: string[];
}

export interface PositionFilters {
  company_id?: string;
  search_term?: string;
  department?: string;
  location?: string;
  employment_type?: string;
  experience_level?: string;
  is_remote?: boolean;
  is_active?: boolean;
  page?: number;
  page_size?: number;
}

export interface PositionListResponse {
  positions: Position[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface PositionStats {
  total_positions: number;
  active_positions: number;
  inactive_positions: number;
  positions_by_type: Record<string, number>;
  positions_by_level: Record<string, number>;
  positions_by_company: Record<string, number>;
}

export interface PositionActionResponse {
  message: string;
  position?: Position;
}

export interface PositionFormData {
  company_id: string;
  title: string;
  description: string;
  department: string;
  location: string;
  work_location_type: 'on_site' | 'remote' | 'hybrid' | 'flexible';
  employment_type: 'full_time' | 'part_time' | 'contract' | 'internship' | 'freelance';
  experience_level: 'entry' | 'mid' | 'senior' | 'executive';
  salary_min: string;
  salary_max: string;
  salary_currency: string;
  requirements: string;
  benefits: string;
  skills: string;
  application_deadline: string;
  application_url: string;
  application_email: string;
  contact_person: string;
  // Updated fields
  working_hours: string;
  travel_required: boolean;
  visa_sponsorship: boolean;
  reports_to: string;
  number_of_openings: string;
  job_category: string;
  languages_required: Array<{language: string, level: string}>; // Language dropdown pairs
  desired_roles: string[]; // Multiselect desired roles
}