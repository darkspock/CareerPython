/**
 * WYSIWYG Editor Component using Tiptap
 *
 * A rich text editor that outputs HTML content with basic sanitization
 * for use in resume sections.
 */

import React from 'react';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Link from '@tiptap/extension-link';
import BulletList from '@tiptap/extension-bullet-list';
import OrderedList from '@tiptap/extension-ordered-list';
import ListItem from '@tiptap/extension-list-item';
import '../../styles/tiptap.css';
import {
  Bold,
  Italic,
  Underline,
  List,
  ListOrdered,
  Link as LinkIcon,
  Unlink
} from 'lucide-react';

interface WysiwygEditorProps {
  content: string;
  onChange: (html: string) => void;
  placeholder?: string;
  className?: string;
  minHeight?: string;
  disabled?: boolean;
}

const WysiwygEditor: React.FC<WysiwygEditorProps> = ({
  content,
  onChange,
  placeholder = 'Start typing...',
  className = '',
  minHeight = '120px',
  disabled = false
}) => {
  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        // Disable some extensions we don't need
        blockquote: false,
        code: false,
        codeBlock: false,
        strike: false,
        dropcursor: false,
        gapcursor: false,
      }),
      Link.configure({
        openOnClick: false,
        HTMLAttributes: {
          target: '_blank',
          rel: 'noopener noreferrer',
        },
      }),
      BulletList.configure({
        HTMLAttributes: {
          class: 'bullet-list',
        },
      }),
      OrderedList.configure({
        HTMLAttributes: {
          class: 'ordered-list',
        },
      }),
      ListItem,
    ],
    content: content || '',
    editable: !disabled,
    onUpdate: ({ editor }) => {
      const html = editor.getHTML();
      onChange(html);
    },
    editorProps: {
      attributes: {
        class: `prose prose-sm max-w-none focus:outline-none ${className}`,
        style: `min-height: ${minHeight}`,
        placeholder: placeholder,
      },
    },
  });

  // Update editor content when prop changes
  React.useEffect(() => {
    if (editor && content !== editor.getHTML()) {
      editor.commands.setContent(content || '');
    }
  }, [content, editor]);

  const setLink = () => {
    if (!editor) return;

    const previousUrl = editor.getAttributes('link').href;
    const url = window.prompt('URL', previousUrl);

    // cancelled
    if (url === null) {
      return;
    }

    // empty
    if (url === '') {
      editor.chain().focus().extendMarkRange('link').unsetLink().run();
      return;
    }

    // update link
    editor.chain().focus().extendMarkRange('link').setLink({ href: url }).run();
  };

  const unsetLink = () => {
    if (!editor) return;
    editor.chain().focus().unsetLink().run();
  };

  if (!editor) {
    return (
      <div className="animate-pulse">
        <div className="border border-gray-300 rounded-lg">
          <div className="h-10 bg-gray-100 border-b border-gray-300 rounded-t-lg"></div>
          <div className="p-4" style={{ minHeight }}>
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="border border-gray-300 rounded-lg overflow-hidden bg-white">
      {/* Toolbar */}
      <div className="flex items-center gap-1 p-2 border-b border-gray-200 bg-gray-50 flex-wrap">
        {/* Text formatting */}
        <button
          onClick={() => editor.chain().focus().toggleBold().run()}
          disabled={!editor.can().chain().focus().toggleBold().run()}
          className={`p-2 rounded hover:bg-gray-200 transition-colors ${
            editor.isActive('bold') ? 'bg-blue-100 text-blue-600' : 'text-gray-600'
          } disabled:opacity-50 disabled:cursor-not-allowed`}
          title="Bold"
        >
          <Bold className="w-4 h-4" />
        </button>

        <button
          onClick={() => editor.chain().focus().toggleItalic().run()}
          disabled={!editor.can().chain().focus().toggleItalic().run()}
          className={`p-2 rounded hover:bg-gray-200 transition-colors ${
            editor.isActive('italic') ? 'bg-blue-100 text-blue-600' : 'text-gray-600'
          } disabled:opacity-50 disabled:cursor-not-allowed`}
          title="Italic"
        >
          <Italic className="w-4 h-4" />
        </button>

        {/* Divider */}
        <div className="w-px h-6 bg-gray-300 mx-1"></div>

        {/* Lists */}
        <button
          onClick={() => editor.chain().focus().toggleBulletList().run()}
          className={`p-2 rounded hover:bg-gray-200 transition-colors ${
            editor.isActive('bulletList') ? 'bg-blue-100 text-blue-600' : 'text-gray-600'
          }`}
          title="Bullet List"
        >
          <List className="w-4 h-4" />
        </button>

        <button
          onClick={() => editor.chain().focus().toggleOrderedList().run()}
          className={`p-2 rounded hover:bg-gray-200 transition-colors ${
            editor.isActive('orderedList') ? 'bg-blue-100 text-blue-600' : 'text-gray-600'
          }`}
          title="Numbered List"
        >
          <ListOrdered className="w-4 h-4" />
        </button>

        {/* Divider */}
        <div className="w-px h-6 bg-gray-300 mx-1"></div>

        {/* Links */}
        <button
          onClick={setLink}
          className={`p-2 rounded hover:bg-gray-200 transition-colors ${
            editor.isActive('link') ? 'bg-blue-100 text-blue-600' : 'text-gray-600'
          }`}
          title="Add Link"
        >
          <LinkIcon className="w-4 h-4" />
        </button>

        {editor.isActive('link') && (
          <button
            onClick={unsetLink}
            className="p-2 rounded hover:bg-gray-200 transition-colors text-gray-600"
            title="Remove Link"
          >
            <Unlink className="w-4 h-4" />
          </button>
        )}

        {/* Divider */}
        <div className="w-px h-6 bg-gray-300 mx-1"></div>

        {/* Headings */}
        <select
          onChange={(e) => {
            const level = parseInt(e.target.value);
            if (level === 0) {
              editor.chain().focus().setParagraph().run();
            } else {
              editor.chain().focus().toggleHeading({ level: level as 1 | 2 | 3 | 4 | 5 | 6 }).run();
            }
          }}
          value={
            editor.isActive('heading', { level: 1 }) ? 1 :
            editor.isActive('heading', { level: 2 }) ? 2 :
            editor.isActive('heading', { level: 3 }) ? 3 : 0
          }
          className="px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value={0}>Paragraph</option>
          <option value={1}>Heading 1</option>
          <option value={2}>Heading 2</option>
          <option value={3}>Heading 3</option>
        </select>
      </div>

      {/* Editor */}
      <div className="p-4">
        <EditorContent
          editor={editor}
          className="focus:outline-none"
          style={{ minHeight }}
        />
      </div>
    </div>
  );
};

export default WysiwygEditor;