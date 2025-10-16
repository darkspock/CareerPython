/**
 * Save Test Page
 *
 * Test page to verify that the save functionality works correctly
 * with the new HybridResumeEditor
 */

import React, { useState } from 'react';
import { api } from '../lib/api';

const SaveTestPage: React.FC = () => {
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testSaveFunction = async () => {
    setLoading(true);
    setResult('');

    try {
      // NEW HYBRID FORMAT - This should work with backend
      const testData = {
        general_data: {
          cv_title: 'Test CV - New Hybrid Format',
          name: 'Test User',
          email: 'test@example.com',
          phone: '+1234567890'
        },
        variable_sections: [
          {
            key: 'experience',
            title: 'Experiencia Profesional',
            content: '<h3>Senior Developer</h3><p><strong>Tech Company</strong></p><p><em>2020 - Present</em></p><p>Developed amazing applications</p>',
            order: 1
          },
          {
            key: 'education',
            title: 'Educación',
            content: '<h3>Computer Science</h3><p><strong>University</strong></p><p><em>2016 - 2020</em></p><p>Bachelor degree</p>',
            order: 2
          },
          {
            key: 'skills',
            title: 'Habilidades',
            content: '<ul><li>JavaScript</li><li>TypeScript</li><li>React</li><li>Node.js</li></ul>',
            order: 3
          },
          {
            key: 'projects',
            title: 'Proyectos',
            content: '<h3>Awesome Project</h3><p><em>2022</em></p><p>Built a great project with React and Node.js</p>',
            order: 4
          }
        ],
        preserve_ai_content: true
      };

      console.log('🧪 Testing save with NEW HYBRID FORMAT:', testData);

      // Use a test resume ID
      const testResumeId = 'test-resume-123';

      await api.updateResumeContent(testResumeId, testData);

      setResult('✅ Save successful! The new hybrid format works correctly.');
    } catch (error: any) {
      console.error('❌ Save failed:', error);
      setResult(`❌ Save failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">
            🧪 Hybrid Format Save Test
          </h1>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <h3 className="font-medium text-blue-900 mb-2">Test Purpose:</h3>
            <p className="text-blue-800">
              This test verifies that the updateResumeContent API function works correctly
              with the NEW HYBRID resume structure (general_data + variable_sections)
              and should resolve the "Section with key 'skills' not found" error.
            </p>
          </div>

          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
            <h3 className="font-medium text-green-900 mb-2">✅ Expected Result:</h3>
            <ul className="text-green-800 space-y-1">
              <li>• Backend should accept the new hybrid format ✅</li>
              <li>• No more "Section not found" errors ✅</li>
              <li>• HybridResumeEditor auto-save should work ✅</li>
              <li>• Content-Type headers are properly set ✅</li>
            </ul>
          </div>

          <button
            onClick={testSaveFunction}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium mb-6"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Testing Save...
              </div>
            ) : (
              '🚀 Test Save Function'
            )}
          </button>

          {result && (
            <div className={`p-4 rounded-lg border ${
              result.includes('✅')
                ? 'bg-green-50 border-green-200 text-green-800'
                : 'bg-red-50 border-red-200 text-red-800'
            }`}>
              <h3 className="font-medium mb-2">Test Result:</h3>
              <pre className="text-sm whitespace-pre-wrap">{result}</pre>
            </div>
          )}

          <div className="mt-8 pt-6 border-t border-gray-200">
            <h3 className="text-lg font-medium text-gray-900 mb-3">NEW Hybrid Format Structure:</h3>
            <pre className="bg-gray-100 p-4 rounded-lg text-sm overflow-x-auto">
{`{
  "general_data": {
    "cv_title": "Test CV - New Hybrid Format",
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+1234567890"
  },
  "variable_sections": [
    {
      "key": "experience",
      "title": "Experiencia Profesional",
      "content": "<h3>Senior Developer</h3><p>...</p>",
      "order": 1
    },
    {
      "key": "skills",
      "title": "Habilidades",
      "content": "<ul><li>JavaScript</li>...</ul>",
      "order": 3
    }
    // ... more sections
  ],
  "preserve_ai_content": true
}`}
            </pre>
          </div>

          <div className="mt-6 text-center text-sm text-gray-500">
            <p>Check the browser console for detailed logs</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SaveTestPage;