import React, { useState } from 'react';
import MDEditor from '@uiw/react-md-editor';
import './MarkdownEditor.css';

interface MarkdownEditorProps {
  value: string;
  onChange: (content: string) => void;
  placeholder?: string;
  height?: number;
  disabled?: boolean;
  className?: string;
}

export const MarkdownEditor: React.FC<MarkdownEditorProps> = ({
  value,
  onChange,
  placeholder = 'Enter your content...',
  height = 300,
  disabled = false,
  className = ''
}) => {
  const [isPreview, setIsPreview] = useState(false);

  const handleEditorChange = (val?: string) => {
    onChange(val || '');
  };

  return (
    <div className={`wysiwyg-editor ${className}`}>
      <div className="mb-2 flex justify-between items-center">
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setIsPreview(false)}
            className={`px-3 py-1 text-sm rounded ${
              !isPreview 
                ? 'bg-blue-500 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Edit
          </button>
          <button
            type="button"
            onClick={() => setIsPreview(true)}
            className={`px-3 py-1 text-sm rounded ${
              isPreview 
                ? 'bg-blue-500 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Preview
          </button>
        </div>
        <div className="text-xs text-gray-500">
          Markdown supported
        </div>
      </div>
      
      <div 
        className="border border-gray-300 rounded-lg overflow-hidden"
        style={{ height: `${height}px` }}
      >
        <MDEditor
          value={value}
          onChange={handleEditorChange}
          height={height - 2}
          preview={isPreview ? 'preview' : 'edit'}
          hideToolbar={disabled}
          data-color-mode="light"
          textareaProps={{
            placeholder: placeholder,
            disabled: disabled,
          }}
          // Configuración de herramientas personalizada
          commands={[
            // Grupo de formato básico
            'bold' as any,
            'italic' as any,
            'strikethrough' as any,
            'underline' as any,
            'divider' as any,
            
            // Grupo de títulos
            'title1' as any,
            'title2' as any,
            'title3' as any,
            'title4' as any,
            'title5' as any,
            'title6' as any,
            'divider' as any,
            
            // Grupo de listas
            'unorderedListCommand' as any,
            'orderedListCommand' as any,
            'checkedListCommand' as any,
            'divider' as any,
            
            // Grupo de enlaces e imágenes
            'link' as any,
            'image' as any,
            'divider' as any,
            
            // Grupo de código
            'codeBlock' as any,
            'code' as any,
            'quote' as any,
            'divider' as any,
            
            // Grupo de tabla
            'table' as any,
            'divider' as any,
            
            // Grupo de formato avanzado
            'fullscreen' as any,
            'preview' as any,
            'divider' as any,
            
            // Grupo de ayuda
            'help' as any,
          ]}
        />
      </div>
      
      <div className="mt-2 text-xs text-gray-500">
        <p>
          <strong>Markdown shortcuts:</strong> **bold**, *italic*, # heading, - list, [link](url), ![image](url)
        </p>
        <p>
          <strong>Images:</strong> Use markdown syntax: ![alt text](image-url) or drag & drop images
        </p>
      </div>
    </div>
  );
};

export default MarkdownEditor;