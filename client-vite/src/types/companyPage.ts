export interface CompanyPage {
  id: string;
  company_id: string;
  page_type: keyof typeof PageType | typeof PageType[keyof typeof PageType]; // Can be either key or value
  title: string;
  html_content: string;
  plain_text: string;
  word_count: number;
  meta_description?: string;
  meta_keywords: string[];
  language: string;
  status: keyof typeof PageStatus | typeof PageStatus[keyof typeof PageStatus]; // Can be either key or value
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

// Helper functions for translations
export function getPageTypeLabel(pageType: keyof typeof PageType | string): string {
  // Create reverse mapping from value to key
  const valueToKey: Record<string, keyof typeof PageType> = {
    'public_company_description': 'PUBLIC_COMPANY_DESCRIPTION',
    'job_position_description': 'JOB_POSITION_DESCRIPTION',
    'data_protection': 'DATA_PROTECTION',
    'terms_of_use': 'TERMS_OF_USE',
    'thank_you_application': 'THANK_YOU_APPLICATION',
  };
  
  // Check if it's a value (exists in values)
  const isValue = Object.values(PageType).includes(pageType as typeof PageType[keyof typeof PageType]);
  
  // If it's already a key, use it directly; otherwise convert from value to key
  const key = isValue ? valueToKey[pageType] : (pageType in PageType ? pageType as keyof typeof PageType : undefined);
  
  const labels: Record<keyof typeof PageType, string> = {
    PUBLIC_COMPANY_DESCRIPTION: 'Descripción Pública de Empresa',
    JOB_POSITION_DESCRIPTION: 'Descripción de Posición',
    DATA_PROTECTION: 'Protección de Datos',
    TERMS_OF_USE: 'Términos de Uso',
    THANK_YOU_APPLICATION: 'Página de Agradecimiento',
  };
  
  return key ? labels[key] : pageType;
}

export function getPageStatusLabel(status: keyof typeof PageStatus | typeof PageStatus[keyof typeof PageStatus]): string {
  // Create reverse mapping from value to key
  const valueToKey: Record<string, keyof typeof PageStatus> = {
    'draft': 'DRAFT',
    'published': 'PUBLISHED',
    'archived': 'ARCHIVED',
  };
  
  // If it's already a key, use it directly; otherwise convert from value to key
  const key = (status in PageStatus) ? status as keyof typeof PageStatus : valueToKey[status];
  
  const labels: Record<keyof typeof PageStatus, string> = {
    DRAFT: 'Borrador',
    PUBLISHED: 'Publicado',
    ARCHIVED: 'Archivado',
  };
  
  return key ? labels[key] : status;
}

export function getPageStatusColor(status: keyof typeof PageStatus | typeof PageStatus[keyof typeof PageStatus]): string {
  // Create reverse mapping from value to key
  const valueToKey: Record<string, keyof typeof PageStatus> = {
    'draft': 'DRAFT',
    'published': 'PUBLISHED',
    'archived': 'ARCHIVED',
  };
  
  // If it's already a key, use it directly; otherwise convert from value to key
  const key = (status in PageStatus) ? status as keyof typeof PageStatus : valueToKey[status];
  
  const colors: Record<keyof typeof PageStatus, string> = {
    DRAFT: 'bg-gray-100 text-gray-800',
    PUBLISHED: 'bg-green-100 text-green-800',
    ARCHIVED: 'bg-red-100 text-red-800',
  };
  
  return key ? colors[key] : 'bg-gray-100 text-gray-800';
}

// Helper function to normalize status to value for comparisons
export function normalizePageStatus(status: keyof typeof PageStatus | typeof PageStatus[keyof typeof PageStatus]): typeof PageStatus[keyof typeof PageStatus] {
  // If it's already a value, return it
  if (Object.values(PageStatus).includes(status as typeof PageStatus[keyof typeof PageStatus])) {
    return status as typeof PageStatus[keyof typeof PageStatus];
  }
  // Otherwise it's a key, convert to value
  return PageStatus[status as keyof typeof PageStatus];
}

// Helper function to normalize page type to value for comparisons
export function normalizePageType(pageType: keyof typeof PageType | typeof PageType[keyof typeof PageType]): typeof PageType[keyof typeof PageType] {
  // If it's already a value, return it
  if (Object.values(PageType).includes(pageType as typeof PageType[keyof typeof PageType])) {
    return pageType as typeof PageType[keyof typeof PageType];
  }
  // Otherwise it's a key, convert to value
  return PageType[pageType as keyof typeof PageType];
}

// Options for selects
export const PAGE_TYPE_OPTIONS = [
  { value: PageType.PUBLIC_COMPANY_DESCRIPTION, label: 'Descripción Pública de Empresa' },
  { value: PageType.JOB_POSITION_DESCRIPTION, label: 'Descripción de Posición' },
  { value: PageType.DATA_PROTECTION, label: 'Protección de Datos' },
  { value: PageType.TERMS_OF_USE, label: 'Términos de Uso' },
  { value: PageType.THANK_YOU_APPLICATION, label: 'Página de Agradecimiento' },
];

export const PAGE_STATUS_OPTIONS = [
  { value: PageStatus.DRAFT, label: 'Borrador', color: 'gray' },
  { value: PageStatus.PUBLISHED, label: 'Publicado', color: 'green' },
  { value: PageStatus.ARCHIVED, label: 'Archivado', color: 'red' },
];

export const LANGUAGE_OPTIONS = [
  { value: 'en', label: 'English' },
  { value: 'es', label: 'Spanish' },
  { value: 'fr', label: 'French' },
  { value: 'de', label: 'German' },
];
