/**
 * Resume Preview Component
 *
 * Real-time preview of the resume with different template options
 * and responsive design support.
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Monitor,
  Smartphone,
  Tablet,
  Palette,
  Download,
  Share2,
  Settings,
  Eye,
  Calendar,
  MapPin,
  Mail,
  Phone,
  Globe
} from 'lucide-react';

import type { Resume } from '../../../types/resume';

interface ResumePreviewProps {
  resumeData: Resume;
  template?: 'professional' | 'modern' | 'minimal' | 'creative';
  className?: string;
  onTemplateChange?: (template: string) => void;
  onExport?: () => void;
  onShare?: () => void;
}

const ResumePreview: React.FC<ResumePreviewProps> = ({
  resumeData,
  template = 'professional',
  className = '',
  onTemplateChange,
  onExport,
  onShare
}) => {
  const [viewMode, setViewMode] = useState<'desktop' | 'tablet' | 'mobile'>('desktop');
  const [showSettings, setShowSettings] = useState(false);

  const getViewModeClasses = () => {
    switch (viewMode) {
      case 'mobile':
        return 'max-w-sm mx-auto';
      case 'tablet':
        return 'max-w-2xl mx-auto';
      default:
        return 'max-w-4xl mx-auto';
    }
  };

  const getTemplateClasses = () => {
    switch (template) {
      case 'modern':
        return 'bg-gradient-to-br from-blue-50 to-indigo-50 border-l-4 border-blue-500';
      case 'minimal':
        return 'bg-white border border-gray-200';
      case 'creative':
        return 'bg-gradient-to-r from-purple-50 to-pink-50 border-l-4 border-purple-500';
      default:
        return 'bg-white border border-gray-300 shadow-sm';
    }
  };

  const renderHeader = () => {
    // Use new general_data structure if available, fallback to legacy datos_personales
    const generalData = resumeData.content?.general_data;
    const personalData = resumeData.content?.datos_personales || {};

    return (
      <div className={`p-6 ${template === 'modern' ? 'bg-blue-600 text-white' : template === 'creative' ? 'bg-purple-600 text-white' : 'border-b border-gray-200'}`}>
        <div className="text-center">
          <h1 className={`text-2xl font-bold mb-1 ${template === 'modern' || template === 'creative' ? 'text-white' : 'text-gray-900'}`}>
            {generalData?.name || personalData.name || resumeData.name || 'Your Name'}
          </h1>
          <p className={`text-lg ${template === 'modern' || template === 'creative' ? 'text-blue-100' : 'text-gray-600'}`}>
            {generalData?.cv_title || 'Professional Title'}
          </p>

          <div className={`flex flex-wrap justify-center gap-4 mt-4 text-sm ${template === 'modern' || template === 'creative' ? 'text-blue-100' : 'text-gray-600'}`}>
            {(generalData?.email || personalData.email) && (
              <div className="flex items-center gap-1">
                <Mail className="w-4 h-4" />
                {generalData?.email || personalData.email}
              </div>
            )}
            {(generalData?.phone || personalData.phone) && (
              <div className="flex items-center gap-1">
                <Phone className="w-4 h-4" />
                {generalData?.phone || personalData.phone}
              </div>
            )}
            {personalData.location && (
              <div className="flex items-center gap-1">
                <MapPin className="w-4 h-4" />
                {personalData.location}
              </div>
            )}
            {personalData.linkedin_url && (
              <div className="flex items-center gap-1">
                <Globe className="w-4 h-4" />
                {personalData.linkedin_url}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  // Helper function to convert simple markdown to HTML
  const convertMarkdownToHtml = (markdown: string): string => {
    if (!markdown) return '';

    return markdown
      // Convert headers (### -> h3, ## -> h2, # -> h1)
      .replace(/^### (.*$)/gim, '<h3 class="text-lg font-semibold mt-4 mb-2">$1</h3>')
      .replace(/^## (.*$)/gim, '<h2 class="text-xl font-bold mt-6 mb-3">$1</h2>')
      .replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold mt-8 mb-4">$1</h1>')
      // Convert bold text (**text** -> <strong>text</strong>)
      .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
      // Convert italic text (*text* -> <em>text</em>)
      .replace(/\*(.*)\*/gim, '<em>$1</em>')
      // Convert bullet points (- item -> <li>item</li>)
      .replace(/^- (.*$)/gim, '<li>$1</li>')
      // Wrap consecutive <li> items in <ul>
      .replace(/(<li>.*<\/li>(?:\s*<li>.*<\/li>)*)/gim, '<ul class="list-disc list-inside space-y-1 my-2">$1</ul>')
      // Convert line breaks
      .replace(/\n/g, '<br>');
  };

  const renderSections = () => {
    if (!resumeData?.content) return null;

    const { content } = resumeData;
    let sections = [];

    // Use new variable_sections structure if available
    if (content.variable_sections && content.variable_sections.length > 0) {
      sections = content.variable_sections.map(section => ({
        id: section.key,
        title: section.title,
        content: section.content,
        order: section.order
      }));
    } else {
      // Fallback to legacy structure
      if (content.experiencia_profesional && content.experiencia_profesional.trim()) {
        sections.push({
          id: 'experiencia_profesional',
          title: 'Experiencia Profesional',
          content: content.experiencia_profesional,
          order: 1
        });
      }

      if (content.educacion && content.educacion.trim()) {
        sections.push({
          id: 'educacion',
          title: 'Educación',
          content: content.educacion,
          order: 2
        });
      }

      if (content.habilidades && content.habilidades.trim()) {
        sections.push({
          id: 'habilidades',
          title: 'Habilidades',
          content: content.habilidades,
          order: 3
        });
      }

      if (content.proyectos && content.proyectos.trim()) {
        sections.push({
          id: 'proyectos',
          title: 'Proyectos',
          content: content.proyectos,
          order: 4
        });
      }
    }

    const sortedSections = sections.sort((a, b) => a.order - b.order);

    return sortedSections.map((section) => (
      <div key={section.id} className="mb-6">
        <h2 className={`text-lg font-semibold mb-3 ${
          template === 'modern' ? 'text-blue-700 border-b-2 border-blue-200' :
          template === 'creative' ? 'text-purple-700 border-b-2 border-purple-200' :
          'text-gray-900 border-b border-gray-200'
        } pb-1`}>
          {section.title}
        </h2>
        <div
          className="prose prose-sm max-w-none text-gray-700"
          // Use innerHTML directly for new HTML content, convert markdown for legacy content
          dangerouslySetInnerHTML={{
            __html: content.variable_sections?.length > 0
              ? section.content  // New structure - already HTML
              : convertMarkdownToHtml(section.content)  // Legacy structure - convert markdown
          }}
        />
      </div>
    ));
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Preview Controls */}
      <div className="flex items-center justify-between bg-white border border-gray-200 rounded-lg p-4">
        <div className="flex items-center gap-2">
          <Eye className="w-5 h-5 text-gray-600" />
          <span className="font-medium text-gray-900">Preview</span>
        </div>

        <div className="flex items-center gap-4">
          {/* View Mode Controls */}
          <div className="flex items-center gap-1 border border-gray-200 rounded-lg p-1">
            <button
              onClick={() => setViewMode('desktop')}
              className={`p-2 rounded ${viewMode === 'desktop' ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'}`}
              title="Desktop View"
            >
              <Monitor className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('tablet')}
              className={`p-2 rounded ${viewMode === 'tablet' ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'}`}
              title="Tablet View"
            >
              <Tablet className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('mobile')}
              className={`p-2 rounded ${viewMode === 'mobile' ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'}`}
              title="Mobile View"
            >
              <Smartphone className="w-4 h-4" />
            </button>
          </div>

          {/* Template Selector */}
          <div className="relative">
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="flex items-center gap-2 px-3 py-2 border border-gray-200 rounded-lg hover:bg-gray-50"
            >
              <Palette className="w-4 h-4" />
              Template
            </button>

            {showSettings && (
              <div className="absolute right-0 top-full mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
                <div className="p-2">
                  {['professional', 'modern', 'minimal', 'creative'].map((templateOption) => (
                    <button
                      key={templateOption}
                      onClick={() => {
                        onTemplateChange?.(templateOption);
                        setShowSettings(false);
                      }}
                      className={`w-full text-left px-3 py-2 rounded hover:bg-gray-50 capitalize ${
                        template === templateOption ? 'bg-blue-50 text-blue-600' : ''
                      }`}
                    >
                      {templateOption}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-2">
            {onShare && (
              <button
                onClick={onShare}
                className="flex items-center gap-2 px-3 py-2 text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <Share2 className="w-4 h-4" />
                Share
              </button>
            )}

            {onExport && (
              <button
                onClick={onExport}
                className="flex items-center gap-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                <Download className="w-4 h-4" />
                Export
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Preview Container */}
      <div className="bg-gray-100 p-8 rounded-lg">
        <motion.div
          layout
          className={`${getViewModeClasses()} ${getTemplateClasses()} rounded-lg overflow-hidden transition-all duration-300`}
          style={{
            minHeight: '800px',
            transform: viewMode === 'mobile' ? 'scale(0.8)' : viewMode === 'tablet' ? 'scale(0.9)' : 'scale(1)',
            transformOrigin: 'top center'
          }}
        >
          {/* Resume Header */}
          {renderHeader()}

          {/* Resume Content */}
          <div className="p-6">
            {resumeData?.content ? (
              <>
                {renderSections()}
                {/* Check for empty content in both new and legacy structures */}
                {(() => {
                  const hasNewSections = resumeData.content.variable_sections?.some(section =>
                    section.content && section.content.trim()
                  );
                  const hasLegacySections = resumeData.content.experiencia_profesional ||
                    resumeData.content.educacion ||
                    resumeData.content.proyectos ||
                    resumeData.content.habilidades;

                  return !hasNewSections && !hasLegacySections ? (
                    <div className="text-center py-12 text-gray-500">
                      <Eye className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                      <p className="text-lg font-medium mb-2">No content to preview</p>
                      <p>Add some content to sections to see your resume preview</p>
                    </div>
                  ) : null;
                })()}
              </>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <Eye className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                <p className="text-lg font-medium mb-2">No content to preview</p>
                <p>Add some sections to see your resume preview</p>
              </div>
            )}
          </div>

          {/* Resume Footer */}
          <div className="px-6 pb-6 text-center text-xs text-gray-500">
            Generated on {new Date().toLocaleDateString()}
          </div>
        </motion.div>
      </div>

      {/* Click outside to close settings */}
      {showSettings && (
        <div
          className="fixed inset-0 z-0"
          onClick={() => setShowSettings(false)}
        />
      )}
    </div>
  );
};

export default ResumePreview;