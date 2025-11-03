export interface CompanyPage {
  id: string;
  company_id: string;
  page_type: keyof typeof PageType;
  title: string;
  html_content: string;
  plain_text: string;
  word_count: number;
  meta_description?: string;
  meta_keywords: string[];
  language: string;
  status: keyof typeof PageStatus;
  is_default: boolean;
  version: number;
  created_at: string;
  updated_at: string;
  published_at?: string;
}

export const PageType = {
  PUBLIC_COMPANY_DESCRIPTION: 'public_company_description',
  JOB_POSITION_DESCRIPTION: 'job_position_description',
  DATA_PROTECTION: 'data_protection',
  TERMS_OF_USE: 'terms_of_use',
  THANK_YOU_APPLICATION: 'thank_you_application',
} as const;

export const PageStatus = {
  DRAFT: 'draft',
  PUBLISHED: 'published',
  ARCHIVED: 'archived',
} as const;

export interface CreateCompanyPageRequest {
  page_type: typeof PageType[keyof typeof PageType]; // Use the value (lowercase), not the key
  title: string;
  html_content: string;
  meta_description?: string;
  meta_keywords?: string[];
  language?: string;
  is_default?: boolean;
}

export interface UpdateCompanyPageRequest {
  title?: string;
  html_content?: string;
  meta_description?: string;
  meta_keywords?: string[];
  language?: string;
  is_default?: boolean;
}

export interface CompanyPageListResponse {
  pages: CompanyPage[];
  total: number;
  page: number;
  page_size: number;
}

export interface CompanyPageFilters {
  page_type?: keyof typeof PageType;
  status?: keyof typeof PageStatus;
  page?: number;
  page_size?: number;
}

// Options for selects
export const PAGE_TYPE_OPTIONS = [
  { value: PageType.PUBLIC_COMPANY_DESCRIPTION, label: 'Public Company Description' },
  { value: PageType.JOB_POSITION_DESCRIPTION, label: 'Job Position Description' },
  { value: PageType.DATA_PROTECTION, label: 'Data Protection' },
  { value: PageType.TERMS_OF_USE, label: 'Terms of Use' },
  { value: PageType.THANK_YOU_APPLICATION, label: 'Thank You Page' },
];

export const PAGE_STATUS_OPTIONS = [
  { value: PageStatus.DRAFT, label: 'Draft', color: 'gray' },
  { value: PageStatus.PUBLISHED, label: 'Published', color: 'green' },
  { value: PageStatus.ARCHIVED, label: 'Archived', color: 'red' },
];

export const LANGUAGE_OPTIONS = [
  { value: 'en', label: 'English' },
  { value: 'es', label: 'Spanish' },
  { value: 'fr', label: 'French' },
  { value: 'de', label: 'German' },
];
