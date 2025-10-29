import { api } from '../lib/api';

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
  page_type: keyof typeof PageType;
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

class CompanyPageService {
  private getCompanyId(): string | null {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_id;
    } catch {
      return null;
    }
  }

  private getBaseUrl(): string {
    const companyId = this.getCompanyId();
    if (!companyId) {
      throw new Error('Company ID not found in token');
    }
    return `/api/company/${companyId}/pages`;
  }

  async getPages(filters: CompanyPageFilters = {}): Promise<CompanyPageListResponse> {
    const params = new URLSearchParams();
    
    if (filters.page_type) params.append('page_type', filters.page_type);
    if (filters.status) params.append('status', filters.status);
    if (filters.page) params.append('page', filters.page.toString());
    if (filters.page_size) params.append('page_size', filters.page_size.toString());

    const response = await api.authenticatedRequest(`${this.getBaseUrl()}?${params.toString()}`);
    return response as CompanyPageListResponse;
  }

  async getPageById(pageId: string): Promise<CompanyPage> {
    const response = await api.authenticatedRequest(`${this.getBaseUrl()}/${pageId}`);
    return response as CompanyPage;
  }

  async getPageByType(pageType: keyof typeof PageType): Promise<CompanyPage | null> {
    try {
      const response = await api.authenticatedRequest(`${this.getBaseUrl()}/by-type/${pageType}`);
      return response as CompanyPage;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null;
      }
      throw error;
    }
  }

  async createPage(data: CreateCompanyPageRequest): Promise<CompanyPage> {
    const response = await api.authenticatedRequest(this.getBaseUrl(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response as CompanyPage;
  }

  async updatePage(pageId: string, data: UpdateCompanyPageRequest): Promise<CompanyPage> {
    const response = await api.authenticatedRequest(`${this.getBaseUrl()}/${pageId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response as CompanyPage;
  }

  async publishPage(pageId: string): Promise<CompanyPage> {
    const response = await api.authenticatedRequest(`${this.getBaseUrl()}/${pageId}/publish`, {
      method: 'POST',
    });
    return response as CompanyPage;
  }

  async archivePage(pageId: string): Promise<CompanyPage> {
    const response = await api.authenticatedRequest(`${this.getBaseUrl()}/${pageId}/archive`, {
      method: 'POST',
    });
    return response as CompanyPage;
  }

  async setDefaultPage(pageId: string): Promise<CompanyPage> {
    const response = await api.authenticatedRequest(`${this.getBaseUrl()}/${pageId}/set-default`, {
      method: 'POST',
    });
    return response as CompanyPage;
  }

  async deletePage(pageId: string): Promise<void> {
    await api.authenticatedRequest(`${this.getBaseUrl()}/${pageId}`, {
      method: 'DELETE',
    });
  }

  // Methods for public pages (no authentication required)
  async getPublicPage(companyId: string, pageType: keyof typeof PageType): Promise<CompanyPage | null> {
    try {
      const response = await api.authenticatedRequest(`/api/public/companies/${companyId}/pages/${pageType}`);
      return response as CompanyPage;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null;
      }
      throw error;
    }
  }
}

export const companyPageService = new CompanyPageService();
