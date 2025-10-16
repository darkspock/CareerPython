// Company API service
import { api } from '../lib/api';
import type {
  Company,
  CompanyFilters,
  CompanyStats,
  CreateCompanyRequest,
  UpdateCompanyRequest,
  CompanyListResponse,
  CompanyActionResponse
} from '../types/company';

export class CompanyService {
  private static readonly BASE_PATH = '/admin/companies';

  /**
   * Get list of companies with optional filters
   */
  static async getCompanies(filters?: CompanyFilters): Promise<CompanyListResponse> {
    const queryParams = new URLSearchParams();

    if (filters?.search_term) queryParams.append('search_term', filters.search_term);
    if (filters?.status) queryParams.append('status', filters.status);
    if (filters?.industry) queryParams.append('industry', filters.industry);
    if (filters?.size) queryParams.append('size', filters.size);
    if (filters?.location) queryParams.append('location', filters.location);
    if (filters?.page) queryParams.append('page', filters.page.toString());
    if (filters?.page_size) queryParams.append('page_size', filters.page_size.toString());

    const endpoint = `${this.BASE_PATH}${queryParams.toString() ? `?${queryParams}` : ''}`;

    try {
      const response = await api.authenticatedRequest(endpoint);
      return {
        companies: response.companies || [],
        total: response.total || 0,
        page: response.page || 1,
        page_size: response.page_size || 10,
        total_pages: response.total_pages || 0
      };
    } catch (error) {
      console.error('Error fetching companies:', error);
      throw error;
    }
  }

  /**
   * Get company statistics
   */
  static async getCompanyStats(): Promise<CompanyStats> {
    try {
      const response = await api.authenticatedRequest(`${this.BASE_PATH}/stats`);
      return {
        total_companies: response.total_companies || 0,
        pending_approval: response.pending_approval || 0,
        approved_companies: response.approved_companies || 0,
        active_companies: response.active_companies || 0,
        rejected_companies: response.rejected_companies || 0,
        inactive_companies: response.inactive_companies || 0
      };
    } catch (error) {
      console.error('Error fetching company stats:', error);
      throw error;
    }
  }

  /**
   * Get single company by ID
   */
  static async getCompanyById(companyId: string): Promise<Company> {
    try {
      const response = await api.authenticatedRequest(`${this.BASE_PATH}/${companyId}`);
      return response;
    } catch (error) {
      console.error(`Error fetching company ${companyId}:`, error);
      throw error;
    }
  }

  /**
   * Create new company
   */
  static async createCompany(companyData: any): Promise<Company> {
    try {
      const response = await api.authenticatedRequest(this.BASE_PATH, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(companyData)
      });
      return response;
    } catch (error) {
      console.error('Error creating company:', error);
      throw error;
    }
  }

  /**
   * Update existing company
   */
  static async updateCompany(companyId: string, companyData: UpdateCompanyRequest): Promise<Company> {
    try {
      const response = await api.authenticatedRequest(`${this.BASE_PATH}/${companyId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(companyData)
      });
      return response;
    } catch (error) {
      console.error(`Error updating company ${companyId}:`, error);
      throw error;
    }
  }

  /**
   * Delete company
   */
  static async deleteCompany(companyId: string): Promise<CompanyActionResponse> {
    try {
      const response = await api.authenticatedRequest(`${this.BASE_PATH}/${companyId}`, {
        method: 'DELETE'
      });
      return response;
    } catch (error) {
      console.error(`Error deleting company ${companyId}:`, error);
      throw error;
    }
  }

  /**
   * Approve pending company
   */
  static async approveCompany(companyId: string): Promise<CompanyActionResponse> {
    try {
      const response = await api.authenticatedRequest(`${this.BASE_PATH}/${companyId}/approve`, {
        method: 'POST'
      });
      return response;
    } catch (error) {
      console.error(`Error approving company ${companyId}:`, error);
      throw error;
    }
  }

  /**
   * Reject pending company
   */
  static async rejectCompany(companyId: string, reason: string): Promise<CompanyActionResponse> {
    try {
      const response = await api.authenticatedRequest(`${this.BASE_PATH}/${companyId}/reject`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ reason })
      });
      return response;
    } catch (error) {
      console.error(`Error rejecting company ${companyId}:`, error);
      throw error;
    }
  }

  /**
   * Activate approved company
   */
  static async activateCompany(companyId: string): Promise<CompanyActionResponse> {
    try {
      const response = await api.authenticatedRequest(`${this.BASE_PATH}/${companyId}/activate`, {
        method: 'POST'
      });
      return response;
    } catch (error) {
      console.error(`Error activating company ${companyId}:`, error);
      throw error;
    }
  }

  /**
   * Deactivate active company
   */
  static async deactivateCompany(companyId: string): Promise<CompanyActionResponse> {
    try {
      const response = await api.authenticatedRequest(`${this.BASE_PATH}/${companyId}/deactivate`, {
        method: 'POST'
      });
      return response;
    } catch (error) {
      console.error(`Error deactivating company ${companyId}:`, error);
      throw error;
    }
  }

  /**
   * Bulk operations
   */
  static async bulkApproveCompanies(companyIds: string[]): Promise<CompanyActionResponse> {
    try {
      const response = await api.authenticatedRequest(`${this.BASE_PATH}/bulk/approve`, {
        method: 'POST',
        body: JSON.stringify({ company_ids: companyIds })
      });
      return response;
    } catch (error) {
      console.error('Error bulk approving companies:', error);
      throw error;
    }
  }

  static async bulkRejectCompanies(companyIds: string[], reason: string): Promise<CompanyActionResponse> {
    try {
      const response = await api.authenticatedRequest(`${this.BASE_PATH}/bulk/reject`, {
        method: 'POST',
        body: JSON.stringify({ company_ids: companyIds, reason })
      });
      return response;
    } catch (error) {
      console.error('Error bulk rejecting companies:', error);
      throw error;
    }
  }

  static async bulkActivateCompanies(companyIds: string[]): Promise<CompanyActionResponse> {
    try {
      const response = await api.authenticatedRequest(`${this.BASE_PATH}/bulk/activate`, {
        method: 'POST',
        body: JSON.stringify({ company_ids: companyIds })
      });
      return response;
    } catch (error) {
      console.error('Error bulk activating companies:', error);
      throw error;
    }
  }

  static async bulkDeactivateCompanies(companyIds: string[]): Promise<CompanyActionResponse> {
    try {
      const response = await api.authenticatedRequest(`${this.BASE_PATH}/bulk/deactivate`, {
        method: 'POST',
        body: JSON.stringify({ company_ids: companyIds })
      });
      return response;
    } catch (error) {
      console.error('Error bulk deactivating companies:', error);
      throw error;
    }
  }

  /**
   * Export companies data
   */
  static async exportCompanies(filters?: CompanyFilters, format: 'csv' | 'excel' = 'csv'): Promise<Blob> {
    const queryParams = new URLSearchParams();

    if (filters?.search_term) queryParams.append('search_term', filters.search_term);
    if (filters?.status) queryParams.append('status', filters.status);
    if (filters?.industry) queryParams.append('industry', filters.industry);
    if (filters?.size) queryParams.append('size', filters.size);
    if (filters?.location) queryParams.append('location', filters.location);
    queryParams.append('format', format);

    const endpoint = `${this.BASE_PATH}/export${queryParams.toString() ? `?${queryParams}` : ''}`;

    try {
      const response = await api.authenticatedRequest(endpoint, {
        responseType: 'blob'
      });
      return response;
    } catch (error) {
      console.error('Error exporting companies:', error);
      throw error;
    }
  }
}

export default CompanyService;