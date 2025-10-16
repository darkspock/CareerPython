/**
 * Resume Export Modal Component
 *
 * Advanced export modal with format selection, template options,
 * custom settings, and download tracking.
 */

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  X,
  Download,
  FileText,
  Image,
  Globe,
  Settings,
  Eye,
  Check,
  AlertTriangle,
  Clock,
  Palette,
  Layout,
  Zap
} from 'lucide-react';
import { api } from '../../../lib/api';

interface ResumeExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  resumeId: string;
  resumeName: string;
}

interface ExportOptions {
  format: 'pdf' | 'docx' | 'html' | 'png';
  template: 'professional' | 'modern' | 'minimal' | 'creative';
  includeMetadata: boolean;
  customizeColors: boolean;
  primaryColor: string;
  paperSize: 'A4' | 'Letter' | 'A3';
  includePhoto: boolean;
  fontSize: 'small' | 'medium' | 'large';
  lineSpacing: 'compact' | 'normal' | 'relaxed';
}

interface ExportHistory {
  id: string;
  format: string;
  template: string;
  downloadedAt: string;
  downloadUrl?: string;
}

const ResumeExportModal: React.FC<ResumeExportModalProps> = ({
  isOpen,
  onClose,
  resumeId,
  resumeName
}) => {
  const [exportOptions, setExportOptions] = useState<ExportOptions>({
    format: 'pdf',
    template: 'professional',
    includeMetadata: true,
    customizeColors: false,
    primaryColor: '#3B82F6',
    paperSize: 'A4',
    includePhoto: false,
    fontSize: 'medium',
    lineSpacing: 'normal'
  });

  const [exporting, setExporting] = useState(false);
  const [exportProgress, setExportProgress] = useState(0);
  const [exportHistory, setExportHistory] = useState<ExportHistory[]>([]);
  const [activeStep, setActiveStep] = useState<'options' | 'preview' | 'download'>('options');
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      loadExportHistory();
    }
  }, [isOpen, resumeId]);

  const loadExportHistory = async () => {
    try {
      const history = await api.getResumeExportHistory(resumeId, 30) as ExportHistory[];
      setExportHistory(history.slice(0, 5)); // Show last 5 exports
    } catch (error) {
      console.error('Failed to load export history:', error);
    }
  };

  const handleExport = async () => {
    try {
      setExporting(true);
      setExportProgress(0);
      setError(null);
      setActiveStep('download');

      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setExportProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 10;
        });
      }, 200);

      const response = await api.exportResume(resumeId, {
        format: exportOptions.format,
        template: exportOptions.template,
        include_metadata: exportOptions.includeMetadata,
        customize_colors: exportOptions.customizeColors,
        primary_color: exportOptions.primaryColor,
        paper_size: exportOptions.paperSize,
        include_photo: exportOptions.includePhoto,
        font_size: exportOptions.fontSize,
        line_spacing: exportOptions.lineSpacing
      });

      clearInterval(progressInterval);
      setExportProgress(100);

      // Handle successful export
      if (response.download_url) {
        // Download the file
        const link = document.createElement('a');
        link.href = response.download_url;
        link.download = `${resumeName}.${exportOptions.format}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // Refresh export history
        loadExportHistory();

        // Close modal after successful download
        setTimeout(() => {
          onClose();
        }, 1500);
      }
    } catch (error: any) {
      console.error('Export failed:', error);
      setError(error.message || 'Export failed. Please try again.');
      setActiveStep('options');
    } finally {
      setExporting(false);
      setExportProgress(0);
    }
  };

  const handlePreview = async () => {
    try {
      setActiveStep('preview');
      const response = await api.getResumePreviewHtml(resumeId, {
        template: exportOptions.template,
        customize_colors: exportOptions.customizeColors,
        primary_color: exportOptions.primaryColor
      });

      if (response.preview_html) {
        const blob = new Blob([response.preview_html], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        setPreviewUrl(url);
      }
    } catch (error) {
      console.error('Preview failed:', error);
      setError('Failed to generate preview');
    }
  };

  const formatOptions = [
    {
      value: 'pdf',
      label: 'PDF Document',
      icon: FileText,
      description: 'Best for printing and professional sharing',
      recommended: true
    },
    {
      value: 'docx',
      label: 'Word Document',
      icon: FileText,
      description: 'Editable format for further customization'
    },
    {
      value: 'html',
      label: 'HTML Page',
      icon: Globe,
      description: 'Web-friendly format for online sharing'
    },
    {
      value: 'png',
      label: 'Image',
      icon: Image,
      description: 'High-quality image for social media'
    }
  ];

  const templateOptions = [
    {
      value: 'professional',
      label: 'Professional',
      description: 'Clean and corporate design',
      preview: 'bg-white border-l-4 border-gray-400'
    },
    {
      value: 'modern',
      label: 'Modern',
      description: 'Contemporary with blue accents',
      preview: 'bg-blue-50 border-l-4 border-blue-500'
    },
    {
      value: 'minimal',
      label: 'Minimal',
      description: 'Simple and elegant layout',
      preview: 'bg-gray-50 border border-gray-200'
    },
    {
      value: 'creative',
      label: 'Creative',
      description: 'Colorful and artistic design',
      preview: 'bg-gradient-to-r from-purple-50 to-pink-50 border-l-4 border-purple-500'
    }
  ];

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Download className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Export Resume</h2>
                  <p className="text-sm text-gray-600">{resumeName}</p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>

            {/* Step Indicator */}
            <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
              <div className="flex items-center gap-4">
                {['options', 'preview', 'download'].map((step, index) => (
                  <div key={step} className="flex items-center">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                      activeStep === step ? 'bg-blue-600 text-white' :
                      index < ['options', 'preview', 'download'].indexOf(activeStep) ? 'bg-green-600 text-white' :
                      'bg-gray-200 text-gray-600'
                    }`}>
                      {index < ['options', 'preview', 'download'].indexOf(activeStep) ? (
                        <Check className="w-4 h-4" />
                      ) : (
                        index + 1
                      )}
                    </div>
                    <span className={`ml-2 text-sm font-medium ${
                      activeStep === step ? 'text-blue-600' : 'text-gray-500'
                    }`}>
                      {step === 'options' ? 'Options' :
                       step === 'preview' ? 'Preview' : 'Download'}
                    </span>
                    {index < 2 && (
                      <div className={`w-12 h-0.5 ml-4 ${
                        index < ['options', 'preview', 'download'].indexOf(activeStep) ? 'bg-green-600' : 'bg-gray-200'
                      }`} />
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Content */}
            <div className="p-6 overflow-y-auto max-h-[60vh]">
              {activeStep === 'options' && (
                <div className="space-y-8">
                  {/* Error Display */}
                  {error && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
                      <AlertTriangle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="text-red-800 font-medium">Export Failed</p>
                        <p className="text-red-600 text-sm mt-1">{error}</p>
                      </div>
                    </div>
                  )}

                  {/* Format Selection */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                      <FileText className="w-5 h-5" />
                      Export Format
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {formatOptions.map((format) => (
                        <button
                          key={format.value}
                          onClick={() => setExportOptions(prev => ({ ...prev, format: format.value as any }))}
                          className={`relative p-4 border-2 rounded-lg text-left transition-all ${
                            exportOptions.format === format.value
                              ? 'border-blue-500 bg-blue-50'
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          {format.recommended && (
                            <div className="absolute top-2 right-2">
                              <span className="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded">
                                Recommended
                              </span>
                            </div>
                          )}
                          <div className="flex items-start gap-3">
                            <format.icon className={`w-6 h-6 flex-shrink-0 ${
                              exportOptions.format === format.value ? 'text-blue-600' : 'text-gray-600'
                            }`} />
                            <div>
                              <h4 className="font-medium text-gray-900">{format.label}</h4>
                              <p className="text-sm text-gray-600 mt-1">{format.description}</p>
                            </div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Template Selection */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                      <Palette className="w-5 h-5" />
                      Template
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {templateOptions.map((template) => (
                        <button
                          key={template.value}
                          onClick={() => setExportOptions(prev => ({ ...prev, template: template.value as any }))}
                          className={`p-4 border-2 rounded-lg text-left transition-all ${
                            exportOptions.template === template.value
                              ? 'border-blue-500 bg-blue-50'
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          <div className="flex items-start gap-3">
                            <div className={`w-12 h-16 rounded ${template.preview} flex-shrink-0`}></div>
                            <div>
                              <h4 className="font-medium text-gray-900">{template.label}</h4>
                              <p className="text-sm text-gray-600 mt-1">{template.description}</p>
                            </div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Advanced Options */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                      <Settings className="w-5 h-5" />
                      Advanced Options
                    </h3>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="text-sm font-medium text-gray-900">Include Metadata</label>
                          <p className="text-xs text-gray-600">Add creation date and resume ID</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={exportOptions.includeMetadata}
                            onChange={(e) => setExportOptions(prev => ({ ...prev, includeMetadata: e.target.checked }))}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Paper Size
                          </label>
                          <select
                            value={exportOptions.paperSize}
                            onChange={(e) => setExportOptions(prev => ({ ...prev, paperSize: e.target.value as any }))}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          >
                            <option value="A4">A4 (210 × 297 mm)</option>
                            <option value="Letter">Letter (8.5 × 11 in)</option>
                            <option value="A3">A3 (297 × 420 mm)</option>
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Font Size
                          </label>
                          <select
                            value={exportOptions.fontSize}
                            onChange={(e) => setExportOptions(prev => ({ ...prev, fontSize: e.target.value as any }))}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          >
                            <option value="small">Small</option>
                            <option value="medium">Medium</option>
                            <option value="large">Large</option>
                          </select>
                        </div>
                      </div>

                      {exportOptions.customizeColors && (
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Primary Color
                          </label>
                          <input
                            type="color"
                            value={exportOptions.primaryColor}
                            onChange={(e) => setExportOptions(prev => ({ ...prev, primaryColor: e.target.value }))}
                            className="w-20 h-10 border border-gray-300 rounded-lg"
                          />
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Export History */}
                  {exportHistory.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                        <Clock className="w-5 h-5" />
                        Recent Exports
                      </h3>
                      <div className="space-y-2">
                        {exportHistory.map((export_item) => (
                          <div key={export_item.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                            <div className="flex items-center gap-3">
                              <FileText className="w-4 h-4 text-gray-600" />
                              <div>
                                <p className="text-sm font-medium text-gray-900">
                                  {export_item.format.toUpperCase()} • {export_item.template}
                                </p>
                                <p className="text-xs text-gray-600">
                                  {new Date(export_item.downloadedAt).toLocaleDateString()}
                                </p>
                              </div>
                            </div>
                            {export_item.downloadUrl && (
                              <button
                                onClick={() => window.open(export_item.downloadUrl, '_blank')}
                                className="text-blue-600 hover:text-blue-700 text-sm font-medium"
                              >
                                Download Again
                              </button>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {activeStep === 'preview' && (
                <div className="text-center py-8">
                  <div className="inline-flex items-center gap-2 text-blue-600 mb-4">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                    Generating preview...
                  </div>
                  {previewUrl && (
                    <iframe
                      src={previewUrl}
                      className="w-full h-96 border border-gray-200 rounded-lg"
                      title="Resume Preview"
                    />
                  )}
                </div>
              )}

              {activeStep === 'download' && (
                <div className="text-center py-8">
                  <div className="inline-flex items-center gap-2 text-blue-600 mb-4">
                    <Zap className="w-6 h-6" />
                    {exporting ? 'Exporting your resume...' : 'Export completed!'}
                  </div>

                  {exporting && (
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
                      <div
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${exportProgress}%` }}
                      ></div>
                    </div>
                  )}

                  <p className="text-gray-600 mb-6">
                    {exporting
                      ? `Processing your ${exportOptions.format.toUpperCase()} export...`
                      : 'Your resume has been exported successfully!'
                    }
                  </p>

                  {!exporting && (
                    <div className="flex items-center justify-center gap-2 text-green-600">
                      <Check className="w-5 h-5" />
                      Download started automatically
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
              <button
                onClick={onClose}
                className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                disabled={exporting}
              >
                {activeStep === 'download' && !exporting ? 'Close' : 'Cancel'}
              </button>

              <div className="flex gap-3">
                {activeStep === 'options' && (
                  <>
                    <button
                      onClick={handlePreview}
                      className="flex items-center gap-2 px-4 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
                    >
                      <Eye className="w-4 h-4" />
                      Preview
                    </button>
                    <button
                      onClick={handleExport}
                      disabled={exporting}
                      className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      <Download className="w-4 h-4" />
                      {exporting ? 'Exporting...' : 'Export'}
                    </button>
                  </>
                )}

                {activeStep === 'preview' && (
                  <button
                    onClick={() => setActiveStep('options')}
                    className="px-4 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
                  >
                    Back to Options
                  </button>
                )}
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

export default ResumeExportModal;