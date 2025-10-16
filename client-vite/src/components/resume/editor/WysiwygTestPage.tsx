/**
 * WYSIWYG Test Page
 *
 * Simple test component to verify WYSIWYG editor integration
 * and HTML sanitization functionality.
 */

import React, { useState } from 'react';
import WysiwygEditor from '../../common/WysiwygEditor';

const WysiwygTestPage: React.FC = () => {
  const [content1, setContent1] = useState('<h3>Work Experience</h3><p><strong>Senior Developer</strong></p><p>Tech Company Inc.</p><p><em>2020 - Present</em></p><ul><li>Developed web applications</li><li>Led technical teams</li><li>Implemented best practices</li></ul>');
  const [content2, setContent2] = useState('<h3>Skills</h3><ul><li>JavaScript</li><li>TypeScript</li><li>React</li><li>Node.js</li><li>Python</li></ul>');
  const [content3, setContent3] = useState('');

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">WYSIWYG Editor Test</h1>

          <div className="space-y-8">
            {/* Test 1: Experience Section */}
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-3">Test 1: Experience Section</h2>
              <WysiwygEditor
                content={content1}
                onChange={setContent1}
                placeholder="Enter your work experience..."
                minHeight="200px"
              />
              <div className="mt-4 p-4 bg-gray-50 rounded border">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Generated HTML:</h4>
                <pre className="text-xs text-gray-600 overflow-x-auto">{content1}</pre>
              </div>
            </div>

            {/* Test 2: Skills Section */}
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-3">Test 2: Skills Section</h2>
              <WysiwygEditor
                content={content2}
                onChange={setContent2}
                placeholder="Enter your skills..."
                minHeight="150px"
              />
              <div className="mt-4 p-4 bg-gray-50 rounded border">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Generated HTML:</h4>
                <pre className="text-xs text-gray-600 overflow-x-auto">{content2}</pre>
              </div>
            </div>

            {/* Test 3: Empty Editor */}
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-3">Test 3: Empty Editor</h2>
              <WysiwygEditor
                content={content3}
                onChange={setContent3}
                placeholder="Start typing to test the editor..."
                minHeight="150px"
              />
              <div className="mt-4 p-4 bg-gray-50 rounded border">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Generated HTML:</h4>
                <pre className="text-xs text-gray-600 overflow-x-auto">{content3 || '<empty>'}</pre>
              </div>
            </div>

            {/* Combined Preview */}
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-3">Combined Preview</h2>
              <div className="border border-gray-300 rounded-lg p-6 bg-white">
                <div className="prose prose-sm max-w-none">
                  <div dangerouslySetInnerHTML={{ __html: content1 }} />
                  {content2 && <div dangerouslySetInnerHTML={{ __html: content2 }} />}
                  {content3 && <div dangerouslySetInnerHTML={{ __html: content3 }} />}
                </div>
              </div>
            </div>

            {/* Instructions */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-blue-900 mb-3">Test Instructions</h3>
              <ul className="space-y-2 text-blue-800">
                <li>• Try formatting text with bold, italic, and headings</li>
                <li>• Create bullet and numbered lists</li>
                <li>• Add links to test link functionality</li>
                <li>• Test the toolbar buttons and keyboard shortcuts</li>
                <li>• Check that HTML output looks correct in the preview</li>
                <li>• Verify that the content persists when switching between editors</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WysiwygTestPage;