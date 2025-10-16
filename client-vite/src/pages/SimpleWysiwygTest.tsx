/**
 * Simple WYSIWYG Test Page
 *
 * Very basic test to verify WYSIWYG editor works
 */

import React, { useState } from 'react';
import WysiwygEditor from '../components/common/WysiwygEditor';

const SimpleWysiwygTest: React.FC = () => {
  const [content, setContent] = useState('<h3>Test Content</h3><p><strong>Bold text</strong> and <em>italic text</em></p><ul><li>List item 1</li><li>List item 2</li></ul>');

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            🧪 Simple WYSIWYG Test
          </h1>
          <p className="text-gray-600 mb-6">
            If you can see a rich text editor below with formatting toolbar, the WYSIWYG is working correctly.
          </p>

          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
            <h3 className="font-medium text-green-900 mb-2">✅ What you should see:</h3>
            <ul className="text-green-800 space-y-1">
              <li>• A toolbar with formatting buttons (Bold, Italic, Lists, Links, Headings)</li>
              <li>• Rich text content that you can edit directly</li>
              <li>• No markdown syntax visible</li>
              <li>• Proper formatting (headings, bold, italic, lists)</li>
            </ul>
          </div>

          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <h3 className="font-medium text-red-900 mb-2">❌ If you see this instead:</h3>
            <ul className="text-red-800 space-y-1">
              <li>• A plain textarea with HTML/markdown syntax</li>
              <li>• No formatting toolbar</li>
              <li>• Raw HTML code visible</li>
              <li>• Error messages in the console</li>
            </ul>
            <p className="text-red-800 mt-2">...then there's a problem with the WYSIWYG installation.</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">WYSIWYG Editor Test</h2>

          <WysiwygEditor
            content={content}
            onChange={setContent}
            placeholder="Try editing this content..."
            minHeight="200px"
          />

          <div className="mt-6 pt-6 border-t border-gray-200">
            <h3 className="text-lg font-medium text-gray-900 mb-3">Generated HTML Output:</h3>
            <pre className="bg-gray-100 p-4 rounded-lg text-sm overflow-x-auto text-gray-700">
              {content}
            </pre>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <h3 className="text-lg font-medium text-gray-900 mb-3">Rendered Result:</h3>
            <div
              className="border border-gray-200 rounded-lg p-4 prose prose-sm max-w-none"
              dangerouslySetInnerHTML={{ __html: content }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimpleWysiwygTest;