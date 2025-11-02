/**
 * Resume Preview Page
 *
 * Dedicated page for viewing resume previews with full-screen support,
 * export functionality, and sharing capabilities.
 */

import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ResumePreviewPage from '../components/resume/preview/ResumePreviewPage';

const ResumePreviewPageRoute: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  useEffect(() => {
    document.title = 'Resume Preview - ATSMonkey';
  }, []);

  const handleBack = () => {
    navigate('/candidate/profile/resumes');
  };

  if (!id) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Preview Not Found</h1>
          <p className="text-gray-600 mb-6">The resume preview you're looking for doesn't exist.</p>
          <button
            onClick={handleBack}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Back to Resumes
          </button>
        </div>
      </div>
    );
  }

  return (
    <ResumePreviewPage
      resumeId={id}
      onBack={handleBack}
    />
  );
};

export default ResumePreviewPageRoute;