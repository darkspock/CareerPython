/**
 * Editor Diagnostic Page
 *
 * Helps diagnose which editor component is actually loading
 */

import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import HybridResumeEditor from '../components/resume/editor/HybridResumeEditor';

const EditorDiagnosticPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  useEffect(() => {
    console.log('🔍 EditorDiagnosticPage loaded');
    console.log('📝 Resume ID:', id);
    console.log('🧩 HybridResumeEditor imported successfully');
    document.title = 'Diagnostic Resume Editor - CareerPython';
  }, [id]);

  const handleBack = () => {
    navigate('/candidate/profile/resumes');
  };

  const handleSave = (resumeData: any) => {
    console.log('💾 Save triggered:', resumeData);
  };

  if (!id) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center max-w-2xl mx-auto p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">🔍 Editor Diagnostic</h1>
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
            <h2 className="text-lg font-semibold text-red-900 mb-2">❌ No Resume ID Found</h2>
            <p className="text-red-700">
              This diagnostic page requires a resume ID in the URL.
              Try: <code className="bg-red-100 px-2 py-1 rounded">/diagnostic-editor/test-123</code>
            </p>
          </div>
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
    <div className="min-h-screen bg-gray-50">
      {/* Diagnostic Header */}
      <div className="bg-yellow-50 border-b border-yellow-200 p-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🔍</span>
            <div>
              <h1 className="text-lg font-semibold text-yellow-900">
                Diagnostic Mode: Resume Editor
              </h1>
              <p className="text-yellow-700 text-sm">
                This should load the NEW HybridResumeEditor with WYSIWYG functionality
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Status Indicators */}
      <div className="max-w-7xl mx-auto p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h3 className="font-semibold text-green-900 mb-2">✅ Component Status</h3>
            <p className="text-green-700 text-sm">HybridResumeEditor imported successfully</p>
          </div>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-semibold text-blue-900 mb-2">📝 Resume ID</h3>
            <p className="text-blue-700 text-sm font-mono">{id}</p>
          </div>
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <h3 className="font-semibold text-purple-900 mb-2">🧭 Expected Features</h3>
            <p className="text-purple-700 text-sm">Tabs + WYSIWYG editors</p>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-4 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">🎯 What to Look For:</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-medium text-green-700 mb-2">✅ If Working Correctly:</h3>
              <ul className="text-sm text-green-600 space-y-1">
                <li>• Two tabs: "General Information" and "Resume Sections"</li>
                <li>• WYSIWYG editors with formatting toolbars</li>
                <li>• No markdown syntax visible</li>
                <li>• Rich text editing capabilities</li>
                <li>• Real-time preview panel</li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium text-red-700 mb-2">❌ If Old Editor Shows:</h3>
              <ul className="text-sm text-red-600 space-y-1">
                <li>• Single page with "Contenido (Markdown)" labels</li>
                <li>• Plain textareas instead of rich editors</li>
                <li>• Markdown syntax visible in editors</li>
                <li>• No formatting toolbars</li>
                <li>• No tab navigation</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* The Actual Editor */}
      <HybridResumeEditor
        resumeId={id}
        onBack={handleBack}
        onSave={handleSave}
      />
    </div>
  );
};

export default EditorDiagnosticPage;