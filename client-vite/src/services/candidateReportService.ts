/**
 * Candidate Report Service
 * Service for generating AI-powered candidate reports
 */

import { api } from '../lib/api';

export interface CandidateReportRequest {
  company_candidate_id: string;
  include_comments?: boolean;
  include_interviews?: boolean;
  include_reviews?: boolean;
}

export interface CandidateReportResponse {
  report_id: string;
  company_candidate_id: string;
  candidate_name: string;
  generated_at: string;
  report_markdown: string;
  sections: {
    summary: string;
    strengths: string[];
    areas_for_improvement: string[];
    interview_insights?: string;
    recommendation: string;
  };
}

export interface ReportGenerationStatus {
  status: 'pending' | 'generating' | 'completed' | 'failed';
  progress?: number;
  message?: string;
}

/**
 * Get the company slug from localStorage
 */
function getCompanySlug(): string {
  const slug = localStorage.getItem('company_slug');
  if (!slug) {
    throw new Error('Company slug not found. Please log in again.');
  }
  return slug;
}

/**
 * Get the base path for candidate report endpoints (company-scoped)
 */
function getBasePath(): string {
  return `/${getCompanySlug()}/admin/candidates/reports`;
}

export const candidateReportService = {
  /**
   * Generate a new candidate report
   */
  async generateReport(request: CandidateReportRequest): Promise<CandidateReportResponse> {
    return await api.authenticatedRequest<CandidateReportResponse>(
      `${getBasePath()}/generate`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request)
      }
    );
  },

  /**
   * Get an existing report by ID
   */
  async getReport(reportId: string): Promise<CandidateReportResponse> {
    return await api.authenticatedRequest<CandidateReportResponse>(
      `${getBasePath()}/${reportId}`
    );
  },

  /**
   * Get all reports for a candidate
   */
  async getReportsForCandidate(companyCandidateId: string): Promise<CandidateReportResponse[]> {
    const slug = getCompanySlug();
    return await api.authenticatedRequest<CandidateReportResponse[]>(
      `/${slug}/admin/candidates/${companyCandidateId}/reports`
    );
  },

  /**
   * Download report as PDF
   */
  async downloadReportPdf(reportId: string): Promise<Blob> {
    const response = await api.authenticatedRequest<Response>(
      `${getBasePath()}/${reportId}/pdf`,
      {
        method: 'GET',
        headers: { 'Accept': 'application/pdf' }
      }
    );

    // If the API returns a blob directly
    if (response instanceof Blob) {
      return response;
    }

    // Otherwise convert to blob
    return new Blob([JSON.stringify(response)], { type: 'application/pdf' });
  }
};
