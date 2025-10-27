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
};
