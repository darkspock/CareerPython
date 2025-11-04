import { api } from '../lib/api';
import { API_BASE_URL } from '../config/api';
import { PageType, PageStatus, type CompanyPage, type CompanyPageFilters, type CompanyPageListResponse, type CreateCompanyPageRequest, type UpdateCompanyPageRequest } from '../types/companyPage';

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
    // Use the endpoint without company_id: /api/company/pages/{page_id}
    const response = await api.authenticatedRequest(`/api/company/pages/${pageId}`);
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
    // Use the endpoint without company_id: /api/company/pages/{page_id}
    const response = await api.authenticatedRequest(`/api/company/pages/${pageId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response as CompanyPage;
  }

  async publishPage(pageId: string): Promise<CompanyPage> {
    // Use the endpoint without company_id: /api/company/pages/{page_id}/publish
    const response = await api.authenticatedRequest(`/api/company/pages/${pageId}/publish`, {
      method: 'POST',
    });
    return response as CompanyPage;
  }

  async archivePage(pageId: string): Promise<CompanyPage> {
    // Use the endpoint without company_id: /api/company/pages/{page_id}/archive
    const response = await api.authenticatedRequest(`/api/company/pages/${pageId}/archive`, {
      method: 'POST',
    });
    return response as CompanyPage;
  }

  async setDefaultPage(pageId: string): Promise<CompanyPage> {
    // Use the endpoint without company_id: /api/company/pages/{page_id}/set-default
    const response = await api.authenticatedRequest(`/api/company/pages/${pageId}/set-default`, {
      method: 'POST',
    });
    return response as CompanyPage;
  }

  async deletePage(pageId: string): Promise<void> {
    // Use the endpoint without company_id: /api/company/pages/{page_id}
    await api.authenticatedRequest(`/api/company/pages/${pageId}`, {
      method: 'DELETE',
    });
  }

  // Methods for public pages (no authentication required)
  async getPublicPage(companyId: string, pageType: keyof typeof PageType): Promise<CompanyPage | null> {
    try {
      // Convert key to value (e.g., 'PUBLIC_COMPANY_DESCRIPTION' -> 'public_company_description')
      const pageTypeValue = PageType[pageType];
      // Use public endpoint without authentication
      const response = await fetch(`${API_BASE_URL}/api/public/company/${companyId}/pages/${pageTypeValue}`);
      
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
