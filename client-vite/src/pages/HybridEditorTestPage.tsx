/**
 * Hybrid Editor Test Page
 *
 * Test page for the new HybridResumeEditor with mock data
 */

import React from 'react';
import HybridResumeEditor from '../components/resume/editor/HybridResumeEditor';

const HybridEditorTestPage: React.FC = () => {
  const mockResumeId = "test-resume-123";

  const handleBack = () => {
    console.log('Back clicked');
  };

  const handleSave = (resumeData: any) => {
    console.log('Save clicked:', resumeData);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="p-4">
        <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-sm p-6 mb-4">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            🧪 Hybrid Resume Editor Test
          </h1>
          <p className="text-gray-600 mb-4">
            This is a test page for the new HybridResumeEditor with WYSIWYG functionality.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-medium text-blue-900 mb-2">Expected Features:</h3>
            <ul className="text-blue-800 space-y-1">
              <li>• Two tabs: "General Information" and "Resume Sections"</li>
              <li>• WYSIWYG editors for each resume section (no more markdown textareas)</li>
              <li>• Rich text formatting toolbar</li>
              <li>• Real-time preview on the right side</li>
              <li>• Auto-save functionality</li>
            </ul>
          </div>
        </div>

        <HybridResumeEditor
          resumeId={mockResumeId}
          onBack={handleBack}
          onSave={handleSave}
        />
      </div>
    </div>
  );
};

export default HybridEditorTestPage;