import React, { useCallback, useEffect } from 'react';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Image from '@tiptap/extension-image';
import Link from '@tiptap/extension-link';
import Placeholder from '@tiptap/extension-placeholder';
import './WysiwygEditor.css';

interface WysiwygEditorProps {
  value?: string;
  content?: string; // Alias for value for backward compatibility
  onChange: (content: string) => void;
  placeholder?: string;
  height?: number;
  minHeight?: string; // CSS string like "150px"
  disabled?: boolean;
  className?: string;
}

export const WysiwygEditor: React.FC<WysiwygEditorProps> = ({
  value,
  content,
  onChange,
  placeholder = 'Enter your content...',
  height = 300,
  minHeight,
  disabled = false,
  className = ''
}) => {
  const editorValue = value || content || '';
  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        // Exclude Link from StarterKit since we're configuring it separately
        link: false,
      }),
      Image.configure({
        inline: true,
        allowBase64: true, // Critical for base64 images
        HTMLAttributes: {
          class: 'wysiwyg-image',
        },
      }),
      Link.configure({
        openOnClick: false,
        HTMLAttributes: {
          class: 'wysiwyg-link',
        },
      }),
      Placeholder.configure({
        placeholder: placeholder,
      }),
    ],
    content: editorValue,
    editable: !disabled,
    onUpdate: ({ editor }) => {
      const html = editor.getHTML();
      // Log to verify base64 images are being saved
      if (html.includes('data:image')) {
        console.log('HTML contains base64 image, saving...');
      }
      onChange(html);
    },
    editorProps: {
      handlePaste: (_view, event) => {
        const items = Array.from(event.clipboardData?.items || []);
        
        // Check if any item is an image
        const hasImage = items.some(item => item.type.indexOf('image') === 0);
        
        if (hasImage) {
          event.preventDefault();
          
          items.forEach(item => {
            if (item.type.indexOf('image') === 0) {
              const file = item.getAsFile();
              
              if (file) {
                const reader = new FileReader();
                
                reader.onload = (readerEvent) => {
                  const base64 = readerEvent.target?.result;
                  
                  if (typeof base64 === 'string') {
                    // Insert image at cursor position using the editor
                    if (editor) {
                      editor.chain()
                        .focus()
                        .setImage({ src: base64 })
                        .run();
                    }
                  }
                };
                
                reader.onerror = (error) => {
                  console.error('Error reading image:', error);
                };
                
                // Convert to base64
                reader.readAsDataURL(file);
              }
            }
          });
          
          return true; // Prevent default paste behavior
        }
        
        return false; // Let Tiptap handle non-image paste events
      },
    },
  });

  // Update editor content when value/content changes externally (e.g., when loading from database)
  useEffect(() => {
    if (!editor || !editorValue) return;
    
    const currentContent = editor.getHTML();
    const newContent = editorValue;
    
    // Only update if content actually changed (avoid infinite loops)
    // Use a more lenient comparison for base64 images which might have whitespace differences
    const normalizedCurrent = currentContent.replace(/\s+/g, ' ').trim();
    const normalizedNew = newContent.replace(/\s+/g, ' ').trim();
    
    if (normalizedCurrent !== normalizedNew) {
      // Log to verify base64 images are being loaded
      if (newContent.includes('data:image')) {
        console.log('Loading HTML with base64 image...');
      }
      // Use setContent to load HTML including base64 images
      editor.commands.setContent(newContent);
      
      // Verify the image was loaded
      setTimeout(() => {
        const loadedHtml = editor.getHTML();
        if (newContent.includes('data:image') && !loadedHtml.includes('data:image')) {
          console.error('Base64 image was lost during load!');
          console.log('Original:', newContent.substring(0, 200));
          console.log('Loaded:', loadedHtml.substring(0, 200));
        }
      }, 100);
    }
  }, [editor, editorValue]);

  // Add drag and drop support for images
  useEffect(() => {
    if (!editor) return;

    let editorElement: HTMLElement | null = null;
    let timeoutId: ReturnType<typeof setTimeout> | null = null;
    let retryTimeoutId: ReturnType<typeof setTimeout> | null = null;

    const handleDrop = (event: DragEvent) => {
      event.preventDefault();
      
      // Verify editor is still available when drop event fires
      if (!editor || !editor.view || !editor.view.dom) {
        return;
      }
      
      const files = Array.from(event.dataTransfer?.files || []);
      
      files.forEach(file => {
        if (file.type.indexOf('image') === 0) {
          const reader = new FileReader();
          
          reader.onload = (e) => {
            const base64 = e.target?.result;
            
            if (typeof base64 === 'string' && editor && editor.view) {
              // Get drop position
              const coordinates = { left: event.clientX, top: event.clientY };
              const pos = editor.view.posAtCoords(coordinates);
              
              if (pos) {
                editor.chain()
                  .focus()
                  .insertContentAt(pos.pos, {
                    type: 'image',
                    attrs: { src: base64 },
                  })
                  .run();
              }
            }
          };
          
          reader.readAsDataURL(file);
        }
      });
    };

    // Wait for editor to be fully mounted before accessing view.dom
    const setupDropHandler = () => {
      try {
        if (!editor || !editor.view) {
          // Retry after a short delay if editor is not ready
          retryTimeoutId = setTimeout(setupDropHandler, 50);
          return;
        }

        // Check if view.dom exists
        if (editor.view.dom) {
          editorElement = editor.view.dom;
          editorElement.addEventListener('drop', handleDrop);
        } else {
          // Retry if dom is not ready yet
          retryTimeoutId = setTimeout(setupDropHandler, 50);
        }
      } catch (error) {
        // If there's an error accessing view.dom, retry
        console.warn('Editor view.dom not available yet:', error);
        retryTimeoutId = setTimeout(setupDropHandler, 50);
      }
    };

    // Initial setup with a small delay to ensure editor is mounted
    timeoutId = setTimeout(setupDropHandler, 100);

    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      if (retryTimeoutId) {
        clearTimeout(retryTimeoutId);
      }
      // Use the stored reference instead of accessing editor.view.dom again
      if (editorElement) {
        editorElement.removeEventListener('drop', handleDrop);
      }
    };
  }, [editor]);

  const setLink = useCallback(() => {
    const previousUrl = editor?.getAttributes('link').href;
    const url = window.prompt('URL', previousUrl);

    // cancelled
    if (url === null) {
      return;
    }

    // empty
    if (url === '') {
      editor?.chain().focus().extendMarkRange('link').unsetLink().run();
      return;
    }

    // update link
    editor?.chain().focus().extendMarkRange('link').setLink({ href: url }).run();
  }, [editor]);

  const addImage = useCallback(() => {
    const url = window.prompt('URL de la imagen');
    if (url) {
      editor?.chain().focus().setImage({ src: url }).run();
    }
  }, [editor]);

  if (!editor) {
    return null;
  }

  return (
    <div className={`wysiwyg-editor ${className}`}>
      {/* Toolbar */}
      <div className="wysiwyg-toolbar">
        <div className="toolbar-group">
          <button
            type="button"
            onClick={() => editor.chain().focus().toggleBold().run()}
            disabled={!editor.can().chain().focus().toggleBold().run()}
            className={editor.isActive('bold') ? 'is-active' : ''}
            title="Negrita"
          >
            <strong>B</strong>
          </button>
          <button
            type="button"
            onClick={() => editor.chain().focus().toggleItalic().run()}
            disabled={!editor.can().chain().focus().toggleItalic().run()}
            className={editor.isActive('italic') ? 'is-active' : ''}
            title="Cursiva"
          >
            <em>I</em>
          </button>
          <button
            type="button"
            onClick={() => editor.chain().focus().toggleStrike().run()}
            disabled={!editor.can().chain().focus().toggleStrike().run()}
            className={editor.isActive('strike') ? 'is-active' : ''}
            title="Tachado"
          >
            <s>S</s>
          </button>
        </div>

        <div className="toolbar-group">
          <button
            type="button"
            onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()}
            className={editor.isActive('heading', { level: 1 }) ? 'is-active' : ''}
            title="Título 1"
          >
            H1
          </button>
          <button
            type="button"
            onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}
            className={editor.isActive('heading', { level: 2 }) ? 'is-active' : ''}
            title="Título 2"
          >
            H2
          </button>
          <button
            type="button"
            onClick={() => editor.chain().focus().toggleHeading({ level: 3 }).run()}
            className={editor.isActive('heading', { level: 3 }) ? 'is-active' : ''}
            title="Título 3"
          >
            H3
          </button>
        </div>

        <div className="toolbar-group">
          <button
            type="button"
            onClick={() => editor.chain().focus().toggleBulletList().run()}
            className={editor.isActive('bulletList') ? 'is-active' : ''}
            title="Lista con viñetas"
          >
            • Lista
          </button>
          <button
            type="button"
            onClick={() => editor.chain().focus().toggleOrderedList().run()}
            className={editor.isActive('orderedList') ? 'is-active' : ''}
            title="Lista numerada"
          >
            1. Lista
          </button>
        </div>

        <div className="toolbar-group">
          <button
            type="button"
            onClick={() => editor.chain().focus().toggleBlockquote().run()}
            className={editor.isActive('blockquote') ? 'is-active' : ''}
            title="Cita"
          >
            "
          </button>
          <button
            type="button"
            onClick={() => editor.chain().focus().toggleCodeBlock().run()}
            className={editor.isActive('codeBlock') ? 'is-active' : ''}
            title="Bloque de código"
          >
            {'</>'}
          </button>
        </div>

        <div className="toolbar-group">
          <button
            type="button"
            onClick={setLink}
            className={editor.isActive('link') ? 'is-active' : ''}
            title="Enlace"
          >
            🔗
          </button>
          <button
            type="button"
            onClick={addImage}
            title="Imagen"
          >
            🖼️
          </button>
        </div>

        <div className="toolbar-group">
          <button
            type="button"
            onClick={() => editor.chain().focus().undo().run()}
            disabled={!editor.can().chain().focus().undo().run()}
            title="Deshacer"
          >
            ↶
          </button>
          <button
            type="button"
            onClick={() => editor.chain().focus().redo().run()}
            disabled={!editor.can().chain().focus().redo().run()}
            title="Rehacer"
          >
            ↷
          </button>
        </div>
      </div>

      {/* Editor Content */}
      <div 
        className="wysiwyg-content"
        style={minHeight ? { minHeight } : { height: `${height - 60}px` }}
      >
        <EditorContent editor={editor} />
      </div>
    </div>
  );
};

export default WysiwygEditor;