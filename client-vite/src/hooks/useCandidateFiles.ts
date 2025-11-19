import { useState, useCallback } from 'react';
import { fileUploadService, type AttachedFile } from '../services/fileUploadService';

interface UseCandidateFilesOptions {
  candidateId: string | undefined;
}

export function useCandidateFiles({ candidateId }: UseCandidateFilesOptions) {
  const [attachedFiles, setAttachedFiles] = useState<AttachedFile[]>([]);
  const [uploadingFile, setUploadingFile] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadFiles = useCallback(async () => {
    if (!candidateId) return;

    try {
      const files = await fileUploadService.getCandidateFiles(candidateId);
      setAttachedFiles(files);
    } catch (fileErr) {
      console.warn('Could not load attached files:', fileErr);
      setAttachedFiles([]);
    }
  }, [candidateId]);

  const handleFileUpload = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file || !candidateId) return;

    try {
      setUploadingFile(true);
      const uploadedFile = await fileUploadService.uploadCandidateFile(candidateId, file);

      const newFile: AttachedFile = {
        id: uploadedFile.id,
        filename: uploadedFile.filename,
        original_name: uploadedFile.original_name,
        size: uploadedFile.size,
        content_type: uploadedFile.content_type,
        url: uploadedFile.url,
        uploaded_at: uploadedFile.uploaded_at,
        description: (uploadedFile as { description?: string }).description || '',
      };

      setAttachedFiles((prev) => [...prev, newFile]);
      setError(null);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to upload file';
      setError(errorMessage);
      console.error('Error uploading file:', err);
    } finally {
      setUploadingFile(false);
    }
  }, [candidateId]);

  const handleDeleteFile = useCallback(async (fileId: string) => {
    if (!candidateId) return;

    try {
      await fileUploadService.deleteCandidateFile(candidateId, fileId);
      setAttachedFiles((prev) => prev.filter((file) => file.id !== fileId));
      setError(null);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete file';
      setError(errorMessage);
      console.error('Error deleting file:', err);
    }
  }, [candidateId]);

  const handleDownloadFile = useCallback(async (file: AttachedFile) => {
    if (!candidateId) return;

    try {
      const blob = await fileUploadService.downloadFile(candidateId, file.id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = file.original_name;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to download file';
      setError(errorMessage);
      console.error('Error downloading file:', err);
    }
  }, [candidateId]);

  return {
    attachedFiles,
    uploadingFile,
    error,
    loadFiles,
    handleFileUpload,
    handleDeleteFile,
    handleDownloadFile,
  };
}

