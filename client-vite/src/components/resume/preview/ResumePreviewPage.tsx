/**
 * Resume Preview Page Component
 *
 * Full-screen resume preview with advanced template options,
 * export functionality, and sharing capabilities.
 */

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Download,
  Share2,
  Printer,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Settings,
  Eye,
  ArrowLeft,
  Check,
  FileText,
  Globe
} from 'lucide-react';
import { api } from '../../../lib/api';

interface ResumePreviewPageProps {
  resumeId: string;
  onBack?: () => void;
  className?: string;
  embed?: boolean;
}

interface ResumeData {
  id: string;
  name: string;
  candidate_id: string;
  resume_type: string;
  status: string;
  ai_enhancement_status: string;
  content: {
    experiencia_profesional: string;
    educacion: string;
    proyectos: string;
    habilidades: string;
    datos_personales: Record<string, any>;
  };
  ai_generated_content: any;
  formatting_preferences: {
    template: string;
    color_scheme: string;
    font_family: string;
    include_photo: boolean;
    sections_order: string[];
  };
  general_data: Record<string, any>;
  custom_content: Record<string, any>;
  created_at: string;
  updated_at: string;
}

const ResumePreviewPage: React.FC<ResumePreviewPageProps> = ({
  resumeId,
  onBack,
  className = '',
  embed = false
}) => {
  const [resumeData, setResumeData] = useState<ResumeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [template, setTemplate] = useState('professional');
  const [zoom, setZoom] = useState(100);
  const [showSettings, setShowSettings] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [exportFormat, setExportFormat] = useState<'pdf' | 'docx' | 'html'>('pdf');
  const [shareUrl, setShareUrl] = useState('');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    loadResumeData();
    generateShareUrl();
  }, [resumeId]);

  const loadResumeData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getResume(resumeId) as ResumeData;
      setResumeData(data);
      setTemplate(data.formatting_preferences?.template || 'professional');
    } catch (error) {
      console.error('Error loading resume:', error);
      setError('Failed to load resume preview');
    } finally {
      setLoading(false);
    }
  };

  const generateShareUrl = () => {
    const baseUrl = window.location.origin;
    const url = `${baseUrl}/candidate/profile/resumes/${resumeId}/preview`;
    setShareUrl(url);
  };

  const handleExport = async (format: 'pdf' | 'docx' | 'html') => {
    try {
      setExporting(true);
      setExportFormat(format);

      const response = await api.exportResume(resumeId, {
        format_type: format,
        template,
        include_ai_enhancement: true
      }) as { download_url?: string };

      // Handle the export response
      if (response && typeof response === 'object' && 'download_url' in response && response.download_url) {
        // Open download URL in new tab
        window.open(response.download_url, '_blank');
      } else {
        // Fallback: navigate to export page
        window.open(`/candidate/profile/resumes/${resumeId}/export?format=${format}&template=${template}`, '_blank');
      }
    } catch (error) {
      console.error('Export failed:', error);
      setError('Failed to export resume. Please try again.');
    } finally {
      setExporting(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const handleShare = async () => {
    try {
      await navigator.clipboard.writeText(shareUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy URL:', error);
    }
  };

  const handleZoomIn = () => {
    setZoom(prev => Math.min(prev + 25, 200));
  };

  const handleZoomOut = () => {
    setZoom(prev => Math.max(prev - 25, 50));
  };

  const handleResetZoom = () => {
    setZoom(100);
  };

  const getTemplateStyles = () => {
    const baseStyles = 'bg-white shadow-lg rounded-lg overflow-hidden mx-auto transition-all duration-300';

    switch (template) {
      case 'modern':
        return `${baseStyles} border-l-8 border-blue-500`;
      case 'minimal':
        return `${baseStyles} border border-gray-200`;
      case 'creative':
        return `${baseStyles} border-l-8 border-purple-500 bg-gradient-to-br from-white to-purple-50`;
      default:
        return `${baseStyles} border border-gray-300`;
    }
  };

  const renderPersonalInfo = () => {
    if (!resumeData) return null;

    const headerBg = template === 'modern' ? 'bg-blue-600 text-white' :
                    template === 'creative' ? 'bg-purple-600 text-white' :
                    'bg-gray-50 border-b border-gray-200';

    // Extract candidate info from content.datos_personales according to RESUME.md
    const personalData = resumeData.content?.datos_personales || {};
    const personalInfo = {
      name: personalData.name || 'Professional Name',
      title: personalData.job_title || personalData.position || 'Professional Title',
      email: personalData.email || '',
      phone: personalData.phone || '',
      location: personalData.location || '',
      website: personalData.linkedin_url || personalData.website || ''
    };

    return (
      <div className={`p-8 ${headerBg}`}>
        <div className="text-center">
          <h1 className={`text-3xl font-bold mb-2 ${
            template === 'modern' || template === 'creative' ? 'text-white' : 'text-gray-900'
          }`}>
            {personalInfo.name}
          </h1>
          {personalInfo.title && (
            <p className={`text-xl mb-4 ${
              template === 'modern' || template === 'creative' ? 'text-blue-100' : 'text-gray-600'
            }`}>
              {personalInfo.title}
            </p>
          )}

          <div className={`flex flex-wrap justify-center gap-6 text-sm ${
            template === 'modern' || template === 'creative' ? 'text-blue-100' : 'text-gray-600'
          }`}>
            {personalInfo.email && (
              <div className="flex items-center gap-2">
                <span>📧</span>
                {personalInfo.email}
              </div>
            )}
            {personalInfo.phone && (
              <div className="flex items-center gap-2">
                <span>📱</span>
                {personalInfo.phone}
              </div>
            )}
            {personalInfo.location && (
              <div className="flex items-center gap-2">
                <span>📍</span>
                {personalInfo.location}
              </div>
            )}
            {personalInfo.website && (
              <div className="flex items-center gap-2">
                <span>🌐</span>
                {personalInfo.website}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  const renderSections = () => {
    if (!resumeData?.content) return null;

    const { content } = resumeData;
    const sections = [];

    // Experiencia Profesional section
    if (content.experiencia_profesional && content.experiencia_profesional.trim()) {
      sections.push({
        id: 'experiencia_profesional',
        title: 'Experiencia Profesional',
        content: content.experiencia_profesional,
        order: 1
      });
    }

    // Educación section
    if (content.educacion && content.educacion.trim()) {
      sections.push({
        id: 'educacion',
        title: 'Educación',
        content: content.educacion,
        order: 2
      });
    }

    // Habilidades section
    if (content.habilidades && content.habilidades.trim()) {
      sections.push({
        id: 'habilidades',
        title: 'Habilidades',
        content: content.habilidades,
        order: 3
      });
    }

    // Proyectos section
    if (content.proyectos && content.proyectos.trim()) {
      sections.push({
        id: 'proyectos',
        title: 'Proyectos',
        content: content.proyectos,
        order: 4
      });
    }

    const sortedSections = sections.sort((a, b) => a.order - b.order);

    return (
      <div className="p-8 space-y-8">
        {sortedSections.map((section) => (
          <div key={section.id}>
            <h2 className={`text-xl font-bold mb-4 ${
              template === 'modern' ? 'text-blue-700 border-b-2 border-blue-200' :
              template === 'creative' ? 'text-purple-700 border-b-2 border-purple-200' :
              'text-gray-900 border-b border-gray-200'
            } pb-2`}>
              {section.title}
            </h2>
            <div
              className="prose prose-lg max-w-none text-gray-700 leading-relaxed"
              dangerouslySetInnerHTML={{ __html: convertMarkdownToHtml(section.content) }}
            />
          </div>
        ))}
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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading resume preview...</p>
        </div>
      </div>
    );
  }

  if (error || !resumeData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Preview Not Available</h1>
          <p className="text-gray-600 mb-6">{error || 'Resume not found'}</p>
          {onBack && (
            <button
              onClick={onBack}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Back to Resumes
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen bg-gray-100 ${className}`}>
      {/* Header Controls */}
      {!embed && (
        <div className="bg-white border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              {/* Left side */}
              <div className="flex items-center gap-4">
                {onBack && (
                  <button
                    onClick={onBack}
                    className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
                  >
                    <ArrowLeft className="w-5 h-5" />
                  </button>
                )}

                <div className="flex items-center gap-2">
                  <Eye className="w-5 h-5 text-blue-600" />
                  <h1 className="text-lg font-semibold text-gray-900">
                    {resumeData.name} - Preview
                  </h1>
                </div>
              </div>

              {/* Center - Zoom Controls */}
              <div className="flex items-center gap-2 bg-gray-50 rounded-lg p-1">
                <button
                  onClick={handleZoomOut}
                  className="p-2 hover:bg-gray-200 rounded"
                  title="Zoom Out"
                >
                  <ZoomOut className="w-4 h-4" />
                </button>
                <span className="px-3 py-2 text-sm font-medium">{zoom}%</span>
                <button
                  onClick={handleZoomIn}
                  className="p-2 hover:bg-gray-200 rounded"
                  title="Zoom In"
                >
                  <ZoomIn className="w-4 h-4" />
                </button>
                <button
                  onClick={handleResetZoom}
                  className="p-2 hover:bg-gray-200 rounded"
                  title="Reset Zoom"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
              </div>

              {/* Right side - Actions */}
              <div className="flex items-center gap-2">
                {/* Template Selector */}
                <div className="relative">
                  <button
                    onClick={() => setShowSettings(!showSettings)}
                    className="flex items-center gap-2 px-3 py-2 border border-gray-200 rounded-lg hover:bg-gray-50"
                  >
                    <Settings className="w-4 h-4" />
                    Template
                  </button>

                  {showSettings && (
                    <div className="absolute right-0 top-full mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
                      <div className="p-2">
                        {['professional', 'modern', 'minimal', 'creative'].map((templateOption) => (
                          <button
                            key={templateOption}
                            onClick={() => {
                              setTemplate(templateOption);
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

                {/* Share Button */}
                <button
                  onClick={handleShare}
                  className="flex items-center gap-2 px-3 py-2 text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50"
                >
                  {copied ? <Check className="w-4 h-4 text-green-600" /> : <Share2 className="w-4 h-4" />}
                  {copied ? 'Copied!' : 'Share'}
                </button>

                {/* Print Button */}
                <button
                  onClick={handlePrint}
                  className="flex items-center gap-2 px-3 py-2 text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50"
                >
                  <Printer className="w-4 h-4" />
                  Print
                </button>

                {/* Export Dropdown */}
                <div className="relative">
                  <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    <Download className="w-4 h-4" />
                    Export
                  </button>

                  <div className="absolute right-0 top-full mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
                    <div className="p-2">
                      {[
                        { format: 'pdf' as const, icon: FileText, label: 'PDF Document' },
                        { format: 'docx' as const, icon: FileText, label: 'Word Document' },
                        { format: 'html' as const, icon: Globe, label: 'HTML Page' }
                      ].map(({ format, icon: Icon, label }) => (
                        <button
                          key={format}
                          onClick={() => handleExport(format)}
                          disabled={exporting}
                          className="w-full text-left px-3 py-2 rounded hover:bg-gray-50 flex items-center gap-2 disabled:opacity-50"
                        >
                          <Icon className="w-4 h-4" />
                          {exporting && exportFormat === format ? 'Exporting...' : label}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Preview Content */}
      <div className="py-8 px-4 sm:px-6 lg:px-8">
        <motion.div
          className="max-w-4xl mx-auto"
          style={{
            transform: `scale(${zoom / 100})`,
            transformOrigin: 'top center'
          }}
        >
          <div className={getTemplateStyles()} style={{ minHeight: '1056px' }}>
            {/* Personal Information Header */}
            {renderPersonalInfo()}

            {/* Resume Sections */}
            {renderSections()}

            {/* Footer */}
            <div className="px-8 pb-8 text-center text-xs text-gray-500">
              Generated on {new Date().toLocaleDateString()} • Resume ID: {resumeId}
            </div>
          </div>
        </motion.div>
      </div>

      {/* Share URL Input (Hidden) */}
      <input
        type="text"
        value={shareUrl}
        readOnly
        className="sr-only"
        aria-label="Share URL"
      />

      {/* Click outside to close dropdowns */}
      {showSettings && (
        <div
          className="fixed inset-0 z-0"
          onClick={() => setShowSettings(false)}
        />
      )}
    </div>
  );
};

export default ResumePreviewPage;