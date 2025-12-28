import { api } from '../lib/api';
import { API_BASE_URL } from '../config/api';
import { PageType, PageStatus, type CompanyPage, type CompanyPageFilters, type CompanyPageListResponse, type CreateCompanyPageRequest, type UpdateCompanyPageRequest } from '../types/companyPage';

class CompanyPageService {
  /**
   * Get the company slug from localStorage
   */
  private getCompanySlug(): string {
    const slug = localStorage.getItem('company_slug');
    if (!slug) {
      throw new Error('Company slug not found. Please log in again.');
    }
    return slug;
  }

  /**
   * Get the base path for company page endpoints (company-scoped)
   */
  private getBaseUrl(): string {
    return `/${this.getCompanySlug()}/admin/pages`;
  }

  async getPages(filters: CompanyPageFilters = {}): Promise<CompanyPageListResponse> {
    const params = new URLSearchParams();

    if (filters.page_type) {
      // Convert key to value (e.g., 'PUBLIC_COMPANY_DESCRIPTION' -> 'public_company_description')
      const pageTypeValue = PageType[filters.page_type];
      params.append('page_type', pageTypeValue);
    }
    if (filters.status) {
      // Convert key to value (e.g., 'DRAFT' -> 'draft')
      const statusValue = PageStatus[filters.status];
      params.append('status', statusValue);
    }
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
      // Convert key to value (e.g., 'PUBLIC_COMPANY_DESCRIPTION' -> 'public_company_description')
      const pageTypeValue = PageType[pageType];
      const response = await api.authenticatedRequest(`${this.getBaseUrl()}/by-type/${pageTypeValue}`);
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
  async getPublicPage(companySlug: string, pageType: keyof typeof PageType): Promise<CompanyPage | null> {
    try {
      // Convert key to value (e.g., 'PUBLIC_COMPANY_DESCRIPTION' -> 'public_company_description')
      const pageTypeValue = PageType[pageType];
      // Use public endpoint without authentication
      const response = await fetch(`${API_BASE_URL}/${companySlug}/pages/${pageTypeValue}`);

      if (!response.ok) {
        if (response.status === 404) {
          return null;
        }
        throw new Error(`Failed to fetch company page: ${response.statusText}`);
      }

      return await response.json() as CompanyPage;
    } catch (error: any) {
      if (error.message?.includes('404') || error.message?.includes('not found')) {
        return null;
      }
      throw error;
    }
  }
}

export const companyPageService = new CompanyPageService();
