/**
 * Resume Editor Page Component
 *
 * Full-page resume editor with comprehensive editing capabilities
 * including WYSIWYG editing, section management, and real-time preview.
 */

import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import HybridResumeEditor from '../components/resume/editor/HybridResumeEditor';

const ResumeEditorPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  useEffect(() => {
    document.title = 'Resume Editor - ATSMonkey';
  }, []);

  const handleBack = () => {
    navigate('/candidate/profile/resumes');
  };

  const handleSave = (resumeData: any) => {
    // Handle successful save
    console.log('Resume saved:', resumeData);
    // You could show a success toast here
  };

  if (!id) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Resume Not Found</h1>
          <p className="text-gray-600 mb-6">The resume you're looking for doesn't exist or you don't have access to it.</p>
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
    <HybridResumeEditor
      resumeId={id}
      onBack={handleBack}
      onSave={handleSave}
    />
  );
};

export default ResumeEditorPage;