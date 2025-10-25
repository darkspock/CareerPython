// Company-related types and interfaces

export type CompanyStatus =
  | 'pending'
  | 'approved'
  | 'rejected'
  | 'active'
  | 'inactive';

export type CompanySize =
  | 'startup'    // 1-10 employees
  | 'small'      // 11-50 employees
  | 'medium'     // 51-200 employees
  | 'large'      // 201-1000 employees
  | 'enterprise'; // 1000+ employees

export interface Company {
  id: string;
  name: string;
  description: string;
  website: string;
  industry: string;
  size: CompanySize;
  location: string;
  status: CompanyStatus;
  logo_url?: string;
  founded_year?: number;
  employee_count?: number;
  contact_email?: string;
  contact_phone?: string;
  created_at: string;
  updated_at: string;
  created_by?: string;
  updated_by?: string;
}

export type CompanyIndustry =
  | 'Technology'
  | 'Finance'
  | 'Healthcare'
  | 'Education'
  | 'Manufacturing'
  | 'Retail'
  | 'Consulting'
  | 'Marketing'
  | 'Real Estate'
  | 'Construction'
  | 'Transportation'
  | 'Food & Beverage'
  | 'Entertainment'
  | 'Non-Profit'
  | 'Government'
  | 'Other';

export interface CompanyFilters {
  search_term?: string;
  status?: CompanyStatus;
  industry?: CompanyIndustry;
  size?: CompanySize;
  location?: string;
  page?: number;
  page_size?: number;
}

export interface CompanyStats {
  total_companies: number;
  pending_approval: number;
  approved_companies: number;
  active_companies: number;
  rejected_companies: number;
  inactive_companies: number;
}

export interface CreateCompanyRequest {
  name: string;
  description: string;
  website: string;
  industry: CompanyIndustry;
  size: CompanySize;
  location: string;
  logo_url?: string;
  founded_year?: number;
  employee_count?: number;
  contact_email?: string;
  contact_phone?: string;
}

export interface UpdateCompanyRequest {
  name?: string;
  description?: string;
  website?: string;
  industry?: CompanyIndustry;
  size?: CompanySize;
  location?: string;
  logo_url?: string;
  founded_year?: number;
  employee_count?: number;
  contact_email?: string;
  contact_phone?: string;
}

export interface CompanyListResponse {
  companies: Company[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface CompanyActionResponse {
  message: string;
  company?: Company;
}

// Form-related types
export interface CompanyFormData {
  name: string;
  description: string;
  website: string;
  industry: CompanyIndustry | '';
  size: CompanySize;
  location: string;
  logo_url: string;
  founded_year: string;
  employee_count: string;
  contact_email: string;
  contact_phone: string;
}

export interface CompanyValidationErrors {
  name?: string;
  description?: string;
  website?: string;
  industry?: string;
  size?: string;
  location?: string;
  logo_url?: string;
  founded_year?: string;
  employee_count?: string;
  contact_email?: string;
  contact_phone?: string;
}

// Constants for UI
export const COMPANY_STATUS_OPTIONS = [
  { value: '', label: 'All Status' },
  { value: 'pending', label: 'Pending Approval' },
  { value: 'approved', label: 'Approved' },
  { value: 'rejected', label: 'Rejected' },
  { value: 'active', label: 'Active' },
  { value: 'inactive', label: 'Inactive' }
];

export const COMPANY_INDUSTRY_OPTIONS = [
  { value: '', label: 'All Industries' },
  { value: 'Technology', label: 'Technology' },
  { value: 'Finance', label: 'Finance' },
  { value: 'Healthcare', label: 'Healthcare' },
  { value: 'Education', label: 'Education' },
  { value: 'Manufacturing', label: 'Manufacturing' },
  { value: 'Retail', label: 'Retail' },
  { value: 'Consulting', label: 'Consulting' },
  { value: 'Marketing', label: 'Marketing' },
  { value: 'Real Estate', label: 'Real Estate' },
  { value: 'Construction', label: 'Construction' },
  { value: 'Transportation', label: 'Transportation' },
  { value: 'Food & Beverage', label: 'Food & Beverage' },
  { value: 'Entertainment', label: 'Entertainment' },
  { value: 'Non-Profit', label: 'Non-Profit' },
  { value: 'Government', label: 'Government' },
  { value: 'Other', label: 'Other' }
];

export const COMPANY_SIZE_OPTIONS = [
  { value: '', label: 'All Sizes' },
  { value: 'startup', label: 'Startup (1-10)' },
  { value: 'small', label: 'Small (11-50)' },
  { value: 'medium', label: 'Medium (51-200)' },
  { value: 'large', label: 'Large (201-1000)' },
  { value: 'enterprise', label: 'Enterprise (1000+)' }
];

// Helper functions
export const getCompanyStatusColor = (status: CompanyStatus): string => {
  switch (status) {
    case 'pending': return 'bg-yellow-100 text-yellow-800';
    case 'approved': return 'bg-blue-100 text-blue-800';
    case 'active': return 'bg-green-100 text-green-800';
    case 'rejected': return 'bg-red-100 text-red-800';
    case 'inactive': return 'bg-gray-100 text-gray-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export const getCompanyStatusIcon = (status: CompanyStatus): string => {
  switch (status) {
    case 'pending': return '⏳';
    case 'approved': return '✅';
    case 'active': return '🟢';
    case 'rejected': return '❌';
    case 'inactive': return '⏸️';
    default: return '❓';
  }
};

export const formatCompanySize = (size: CompanySize): string => {
  const sizeMap = {
    startup: 'Startup (1-10)',
    small: 'Small (11-50)',
    medium: 'Medium (51-200)',
    large: 'Large (201-1000)',
    enterprise: 'Enterprise (1000+)'
  };
  return sizeMap[size] || size;
};

// Company Role types
export interface CompanyRole {
  id: string;
  company_id: string;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateRoleRequest {
  name: string;
  description?: string;
}

export interface UpdateRoleRequest {
  name: string;
  description?: string;
}

export interface RoleFormData {
  name: string;
  description: string;
}

export interface RoleValidationErrors {
  name?: string;
  description?: string;
}