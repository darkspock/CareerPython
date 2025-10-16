/**
 * Resume Export Page
 *
 * Dedicated page for exporting resumes with comprehensive
 * format options and download management.
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Download,
  ArrowLeft,
  FileText,
  Globe,
  Image,
  Settings,
  Clock,
  Check,
  AlertTriangle,
  Zap
} from 'lucide-react';
import ResumeExportModal from '../components/resume/export/ResumeExportModal';
import { api } from '../lib/api';

interface ResumeData {
  id: string;
  name: string;
  candidate_id: string;
  created_at: string;
  updated_at: string;
}

const ResumeExportPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [resumeData, setResumeData] = useState<ResumeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showExportModal, setShowExportModal] = useState(false);
  const [exportHistory, setExportHistory] = useState([]);
  const [quickExporting, setQuickExporting] = useState(false);

  // Get URL parameters for quick export
  const quickFormat = searchParams.get('format') as 'pdf' | 'docx' | 'html' | null;
  const quickTemplate = searchParams.get('template') || 'professional';

  useEffect(() => {
    document.title = 'Export Resume - CareerPython';
    if (id) {
      loadResumeData();
      loadExportHistory();
    }
  }, [id]);

  useEffect(() => {
    // Auto-trigger export if format is specified in URL
    if (resumeData && quickFormat && !showExportModal) {
      handleQuickExport();
    }
  }, [resumeData, quickFormat]);

  const loadResumeData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getResume(id!) as ResumeData;
      setResumeData(data);
    } catch (error) {
      console.error('Error loading resume:', error);
      setError('Failed to load resume data');
    } finally {
      setLoading(false);
    }
  };

  const loadExportHistory = async () => {
    try {
      const history = await api.getResumeExportHistory(id!, 30);
      setExportHistory(history || []);
    } catch (error) {
      console.error('Failed to load export history:', error);
    }
  };

  const handleQuickExport = async () => {
    if (!quickFormat || !resumeData) return;

    try {
      setQuickExporting(true);

      const response = await api.exportResume(id!, {
        format: quickFormat,
        template: quickTemplate,
        include_metadata: true
      });

      if (response.download_url) {
        // Download the file
        const link = document.createElement('a');
        link.href = response.download_url;
        link.download = `${resumeData.name}.${quickFormat}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // Refresh export history
        loadExportHistory();
      }
    } catch (error) {
      console.error('Quick export failed:', error);
      setError('Export failed. Please try again.');
    } finally {
      setQuickExporting(false);
    }
  };

  const handleBack = () => {
    navigate('/candidate/profile/resumes');
  };

  if (!id) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Export Not Available</h1>
          <p className="text-gray-600 mb-6">No resume specified for export.</p>
          <button
            onClick={handleBack}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Back to Resumes
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading resume data...</p>
        </div>
      </div>
    );
  }

  if (error || !resumeData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Export Error</h1>
          <p className="text-gray-600 mb-6">{error || 'Resume not found'}</p>
          <div className="flex gap-3 justify-center">
            <button
              onClick={loadResumeData}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Try Again
            </button>
            <button
              onClick={handleBack}
              className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Back to Resumes
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-4">
              <button
                onClick={handleBack}
                className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Download className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <h1 className="text-lg font-semibold text-gray-900">Export Resume</h1>
                  <p className="text-sm text-gray-600">{resumeData.name}</p>
                </div>
              </div>
            </div>

            <button
              onClick={() => setShowExportModal(true)}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Download className="w-4 h-4 mr-2" />
              Export Resume
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Quick Export Processing */}
        {quickExporting && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8"
          >
            <div className="flex items-center gap-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <div>
                <h3 className="text-lg font-semibold text-blue-900">Processing Export</h3>
                <p className="text-blue-700">
                  Generating your {quickFormat?.toUpperCase()} export with {quickTemplate} template...
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Quick Export Options */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <Zap className="w-6 h-6 text-yellow-500" />
            <h2 className="text-xl font-semibold text-gray-900">Quick Export</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              {
                format: 'pdf',
                icon: FileText,
                label: 'PDF Document',
                description: 'Most popular format for job applications',
                color: 'text-red-600 bg-red-50 border-red-200'
              },
              {
                format: 'docx',
                icon: FileText,
                label: 'Word Document',
                description: 'Editable format for customization',
                color: 'text-blue-600 bg-blue-50 border-blue-200'
              },
              {
                format: 'html',
                icon: Globe,
                label: 'HTML Page',
                description: 'Web-friendly online sharing',
                color: 'text-green-600 bg-green-50 border-green-200'
              }
            ].map((option) => (
              <button
                key={option.format}
                onClick={() => {
                  const url = new URL(window.location.href);
                  url.searchParams.set('format', option.format);
                  url.searchParams.set('template', 'professional');
                  window.location.href = url.toString();
                }}
                disabled={quickExporting}
                className={`p-4 border-2 rounded-lg text-left transition-all hover:shadow-md disabled:opacity-50 ${option.color}`}
              >
                <div className="flex items-start gap-3">
                  <option.icon className="w-6 h-6 flex-shrink-0" />
                  <div>
                    <h3 className="font-semibold">{option.label}</h3>
                    <p className="text-sm opacity-80 mt-1">{option.description}</p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Advanced Export */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <Settings className="w-6 h-6 text-gray-600" />
              <h2 className="text-xl font-semibold text-gray-900">Advanced Export</h2>
            </div>
            <button
              onClick={() => setShowExportModal(true)}
              className="inline-flex items-center px-4 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
            >
              <Settings className="w-4 h-4 mr-2" />
              Customize Export
            </button>
          </div>

          <div className="text-gray-600">
            <p className="mb-4">
              Use advanced export options to customize your resume with:
            </p>
            <ul className="space-y-2 text-sm">
              <li className="flex items-center gap-2">
                <Check className="w-4 h-4 text-green-600" />
                Multiple professional templates
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-4 h-4 text-green-600" />
                Custom color schemes
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-4 h-4 text-green-600" />
                Paper size options (A4, Letter, A3)
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-4 h-4 text-green-600" />
                Font size and spacing control
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-4 h-4 text-green-600" />
                Metadata inclusion options
              </li>
            </ul>
          </div>
        </div>

        {/* Export History */}
        {exportHistory.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-6">
              <Clock className="w-6 h-6 text-gray-600" />
              <h2 className="text-xl font-semibold text-gray-900">Export History</h2>
            </div>

            <div className="space-y-3">
              {exportHistory.slice(0, 5).map((export_item: any) => (
                <div
                  key={export_item.id}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-white rounded border">
                      <FileText className="w-4 h-4 text-gray-600" />
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900">
                        {export_item.format.toUpperCase()} Export
                      </h4>
                      <p className="text-sm text-gray-600">
                        {export_item.template} template • {new Date(export_item.downloadedAt).toLocaleDateString()}
                      </p>
                    </div>
                  </div>

                  {export_item.downloadUrl && (
                    <button
                      onClick={() => window.open(export_item.downloadUrl, '_blank')}
                      className="px-3 py-2 text-blue-600 hover:text-blue-700 font-medium text-sm"
                    >
                      Download Again
                    </button>
                  )}
                </div>
              ))}
            </div>

            {exportHistory.length > 5 && (
              <div className="mt-4 text-center">
                <button className="text-blue-600 hover:text-blue-700 font-medium text-sm">
                  View All Exports ({exportHistory.length})
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Export Modal */}
      <ResumeExportModal
        isOpen={showExportModal}
        onClose={() => setShowExportModal(false)}
        resumeId={id}
        resumeName={resumeData.name}
      />
    </div>
  );
};

export default ResumeExportPage;