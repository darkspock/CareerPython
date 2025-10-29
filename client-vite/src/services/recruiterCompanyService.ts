/**
 * Service for managing the recruiting company (company using the platform)
 */

import { ApiClient } from '../lib/api';
import type { RecruiterCompany, UpdateRecruiterCompanyRequest } from '../types/recruiter-company';

export const recruiterCompanyService = {
  /**
   * Get the current company's information
   */
  async getCompany(companyId: string): Promise<RecruiterCompany> {
    return ApiClient.get<RecruiterCompany>(`/companies/${companyId}`);
  },

  /**
   * Get company by slug
   */
  async getCompanyBySlug(slug: string): Promise<RecruiterCompany> {
    return ApiClient.get<RecruiterCompany>(`/companies/slug/${slug}`);
  },

  /**
   * Update the current company's information
   */
  async updateCompany(
    companyId: string,
    data: UpdateRecruiterCompanyRequest
  ): Promise<RecruiterCompany> {
    return ApiClient.put<RecruiterCompany>(`/companies/${companyId}`, data);
  },

  /**
   * Upload company logo
   */
  async uploadLogo(companyId: string, file: File): Promise<RecruiterCompany> {
    const formData = new FormData();
    formData.append('file', file);

    const token = localStorage.getItem('access_token');
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/companies/${companyId}/upload-logo`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to upload logo');
    }

    return response.json();
  },
};
