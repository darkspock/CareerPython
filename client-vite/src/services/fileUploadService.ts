/**
 * Service for file upload operations
 */

import { ApiClient } from '../lib/api';

export interface FileUploadResponse {
  id: string;
  filename: string;
  original_name: string;
  size: number;
  content_type: string;
  url: string;
  uploaded_at: string;
}

export interface AttachedFile {
  id: string;
  filename: string;
  original_name: string;
  size: number;
  content_type: string;
  url: string;
  uploaded_at: string;
  description?: string;
}

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    Authorization: `Bearer ${token}`,
  };
};

export const fileUploadService = {
  /**
   * Upload a file for a candidate
   */
  async uploadCandidateFile(
    candidateId: string,
    file: File,
    description?: string
  ): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    if (description) {
      formData.append('description', description);
    }

    const response = await fetch(
      `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/candidates/${candidateId}/files`,
      {
        method: 'POST',
        headers: getAuthHeaders(),
        body: formData,
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to upload file');
    }

    return response.json();
  },

  /**
   * Get attached files for a candidate
   */
  async getCandidateFiles(candidateId: string): Promise<AttachedFile[]> {
    return ApiClient.get(`/api/candidates/${candidateId}/files`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * Delete an attached file
   */
  async deleteCandidateFile(candidateId: string, fileId: string): Promise<void> {
    return ApiClient.delete(`/api/candidates/${candidateId}/files/${fileId}`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * Download a file
   */
  async downloadFile(candidateId: string, fileId: string): Promise<Blob> {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/candidates/${candidateId}/files/${fileId}/download`,
      {
        headers: getAuthHeaders(),
      }
    );

    if (!response.ok) {
      throw new Error('Failed to download file');
    }

    return response.blob();
  },
};
