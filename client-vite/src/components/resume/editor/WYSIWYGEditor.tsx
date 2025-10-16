/**
 * WYSIWYG Editor Component
 *
 * Rich text editor for resume content editing with formatting options
 * and real-time preview capabilities.
 */

import React, { useState, useCallback } from 'react';
import {
  Bold,
  Italic,
  Underline,
  List,
  ListOrdered,
  AlignLeft,
  AlignCenter,
  AlignRight,
  Link,
  Type,
  Save,
  Eye,
  EyeOff
} from 'lucide-react';
import { motion } from 'framer-motion';

interface WYSIWYGEditorProps {
  content: string;
  onChange: (content: string) => void;
  placeholder?: string;
  className?: string;
  showPreview?: boolean;
  onSave?: () => void;
  saving?: boolean;
}

interface EditorState {
  isBold: boolean;
  isItalic: boolean;
  isUnderline: boolean;
  alignment: 'left' | 'center' | 'right';
}

const WYSIWYGEditor: React.FC<WYSIWYGEditorProps> = ({
  content,
  onChange,
  placeholder = 'Start typing...',
  className = '',
  showPreview = false,
  onSave,
  saving = false
}) => {
  const [editorState, setEditorState] = useState<EditorState>({
    isBold: false,
    isItalic: false,
    isUnderline: false,
    alignment: 'left'
  });
  const [isPreviewMode, setIsPreviewMode] = useState(showPreview);
  const [focusedEditor, setFocusedEditor] = useState(false);

  const handleFormatting = useCallback((command: string, value?: string) => {
    document.execCommand(command, false, value);
    updateEditorState();
  }, []);

  const updateEditorState = () => {
    setEditorState({
      isBold: document.queryCommandState('bold'),
      isItalic: document.queryCommandState('italic'),
      isUnderline: document.queryCommandState('underline'),
      alignment: document.queryCommandValue('justifyLeft') ? 'left' :
                document.queryCommandValue('justifyCenter') ? 'center' :
                document.queryCommandValue('justifyRight') ? 'right' : 'left'
    });
  };

  const handleContentChange = (e: React.FormEvent<HTMLDivElement>) => {
    const newContent = e.currentTarget.innerHTML;
    onChange(newContent);
  };

  const insertLink = () => {
    const url = prompt('Enter URL:');
    if (url) {
      handleFormatting('createLink', url);
    }
  };

  const formatButtons = [
    { icon: Bold, command: 'bold', active: editorState.isBold, title: 'Bold' },
    { icon: Italic, command: 'italic', active: editorState.isItalic, title: 'Italic' },
    { icon: Underline, command: 'underline', active: editorState.isUnderline, title: 'Underline' },
    { icon: List, command: 'insertUnorderedList', active: false, title: 'Bullet List' },
    { icon: ListOrdered, command: 'insertOrderedList', active: false, title: 'Numbered List' },
    { icon: AlignLeft, command: 'justifyLeft', active: editorState.alignment === 'left', title: 'Align Left' },
    { icon: AlignCenter, command: 'justifyCenter', active: editorState.alignment === 'center', title: 'Align Center' },
    { icon: AlignRight, command: 'justifyRight', active: editorState.alignment === 'right', title: 'Align Right' },
  ];

  return (
    <div className={`border border-gray-300 rounded-lg overflow-hidden ${className}`}>
      {/* Toolbar */}
      <div className="bg-gray-50 border-b border-gray-200 p-2 flex items-center gap-1 flex-wrap">
        <div className="flex items-center gap-1">
          {formatButtons.map(({ icon: Icon, command, active, title }) => (
            <button
              key={command}
              type="button"
              onClick={() => handleFormatting(command)}
              className={`p-2 rounded hover:bg-gray-200 transition-colors ${
                active ? 'bg-blue-100 text-blue-600' : 'text-gray-600'
              }`}
              title={title}
            >
              <Icon className="w-4 h-4" />
            </button>
          ))}
        </div>

        <div className="w-px h-6 bg-gray-300 mx-1" />

        <div className="flex items-center gap-1">
          <button
            type="button"
            onClick={insertLink}
            className="p-2 rounded hover:bg-gray-200 transition-colors text-gray-600"
            title="Insert Link"
          >
            <Link className="w-4 h-4" />
          </button>

          <select
            onChange={(e) => handleFormatting('fontSize', e.target.value)}
            className="px-2 py-1 text-sm border border-gray-300 rounded focus:ring-1 focus:ring-blue-500"
            title="Font Size"
          >
            <option value="2">Small</option>
            <option value="3" selected>Normal</option>
            <option value="4">Large</option>
            <option value="5">Extra Large</option>
          </select>
        </div>

        <div className="w-px h-6 bg-gray-300 mx-1" />

        <div className="flex items-center gap-1 ml-auto">
          <button
            type="button"
            onClick={() => setIsPreviewMode(!isPreviewMode)}
            className={`p-2 rounded hover:bg-gray-200 transition-colors ${
              isPreviewMode ? 'bg-blue-100 text-blue-600' : 'text-gray-600'
            }`}
            title={isPreviewMode ? 'Hide Preview' : 'Show Preview'}
          >
            {isPreviewMode ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
          </button>

          {onSave && (
            <button
              type="button"
              onClick={onSave}
              disabled={saving}
              className="px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
              title="Save Changes"
            >
              {saving ? (
                <>
                  <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white"></div>
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" />
                  Save
                </>
              )}
            </button>
          )}
        </div>
      </div>

      {/* Editor Content */}
      <div className="flex">
        {/* Editor */}
        <div className={`${isPreviewMode ? 'w-1/2 border-r border-gray-200' : 'w-full'}`}>
          <div
            contentEditable
            suppressContentEditableWarning
            onInput={handleContentChange}
            onFocus={() => setFocusedEditor(true)}
            onBlur={() => setFocusedEditor(false)}
            onMouseUp={updateEditorState}
            onKeyUp={updateEditorState}
            dangerouslySetInnerHTML={{ __html: content }}
            className={`min-h-64 p-4 outline-none focus:ring-2 focus:ring-blue-500 focus:ring-inset prose prose-sm max-w-none ${
              !content ? 'text-gray-400' : ''
            }`}
            style={{ minHeight: '256px' }}
            data-placeholder={placeholder}
          />

          {!content && !focusedEditor && (
            <div className="absolute top-16 left-4 text-gray-400 pointer-events-none">
              {placeholder}
            </div>
          )}
        </div>

        {/* Preview */}
        {isPreviewMode && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="w-1/2 p-4 bg-gray-50"
          >
            <div className="text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
              <Eye className="w-4 h-4" />
              Preview
            </div>
            <div
              className="prose prose-sm max-w-none"
              dangerouslySetInnerHTML={{ __html: content }}
            />
            {!content && (
              <div className="text-gray-400 italic">
                Start typing to see a preview...
              </div>
            )}
          </motion.div>
        )}
      </div>

      {/* Editor Footer */}
      <div className="bg-gray-50 border-t border-gray-200 px-4 py-2 text-xs text-gray-500 flex items-center justify-between">
        <div>
          Use the toolbar above to format your text. Press Ctrl+S to save.
        </div>
        <div className="flex items-center gap-4">
          <span>{content.replace(/<[^>]*>/g, '').length} characters</span>
          <span>{content.split(/\s+/).filter(word => word.length > 0).length} words</span>
        </div>
      </div>
    </div>
  );
};

export default WYSIWYGEditor;