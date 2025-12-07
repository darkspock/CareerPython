/**
 * Candidate Report Modal
 * Modal for generating and viewing AI-powered candidate reports
 */

import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { X, FileText, Download, Loader2, RefreshCw, CheckCircle, AlertCircle } from 'lucide-react';
import { candidateReportService, type CandidateReportResponse } from '../../services/candidateReportService';
import { toast } from 'react-toastify';

interface CandidateReportModalProps {
  isOpen: boolean;
  onClose: () => void;
  companyCandidateId: string;
  candidateName: string;
}

type ModalState = 'idle' | 'generating' | 'viewing' | 'error';

export default function CandidateReportModal({
  isOpen,
  onClose,
  companyCandidateId,
  candidateName
}: CandidateReportModalProps) {
  const { t } = useTranslation();
  const [state, setState] = useState<ModalState>('idle');
  const [report, setReport] = useState<CandidateReportResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [downloadingPdf, setDownloadingPdf] = useState(false);

  // Reset state when modal opens/closes
  useEffect(() => {
    if (!isOpen) {
      setState('idle');
      setReport(null);
      setError(null);
    }
  }, [isOpen]);

  const handleGenerateReport = async () => {
    try {
      setState('generating');
      setError(null);

      const response = await candidateReportService.generateReport({
        company_candidate_id: companyCandidateId,
        include_comments: true,
        include_interviews: true,
        include_reviews: true
      });

      setReport(response);
      setState('viewing');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to generate report';
      setError(errorMessage);
      setState('error');
      toast.error(errorMessage);
    }
  };

  const handleDownloadPdf = async () => {
    if (!report) return;

    try {
      setDownloadingPdf(true);

      // For now, create a simple PDF-like download from the markdown
      // In a real implementation, this would call the backend PDF endpoint
      const blob = new Blob([report.report_markdown], { type: 'text/markdown' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${candidateName.replace(/\s+/g, '_')}_report_${new Date().toISOString().split('T')[0]}.md`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast.success(t('company.candidates.report.downloadSuccess', 'Report downloaded successfully'));
    } catch (err) {
      toast.error(t('company.candidates.report.downloadError', 'Failed to download report'));
    } finally {
      setDownloadingPdf(false);
    }
  };

  const handleRegenerate = () => {
    setReport(null);
    handleGenerateReport();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative w-full max-w-4xl bg-white rounded-xl shadow-xl max-h-[90vh] flex flex-col">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 flex-shrink-0">
            <div className="flex items-center gap-3">
              <FileText className="w-6 h-6 text-blue-600" />
              <div>
                <h2 className="text-xl font-semibold text-gray-900">
                  {t('company.candidates.report.title', 'Candidate Report')}
                </h2>
                <p className="text-sm text-gray-500">{candidateName}</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-500"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6">
            {/* Idle State - Show generate button */}
            {state === 'idle' && (
              <div className="text-center py-12">
                <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  {t('company.candidates.report.generateTitle', 'Generate AI Report')}
                </h3>
                <p className="text-gray-500 mb-6 max-w-md mx-auto">
                  {t('company.candidates.report.generateDescription',
                    'Generate a comprehensive AI-powered report based on comments, interviews, and reviews for this candidate.')}
                </p>
                <button
                  onClick={handleGenerateReport}
                  className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
                >
                  <FileText className="w-5 h-5" />
                  {t('company.candidates.report.generateButton', 'Generate Report')}
                </button>
              </div>
            )}

            {/* Generating State */}
            {state === 'generating' && (
              <div className="text-center py-12">
                <Loader2 className="w-16 h-16 text-blue-600 animate-spin mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  {t('company.candidates.report.generating', 'Generating Report...')}
                </h3>
                <p className="text-gray-500">
                  {t('company.candidates.report.generatingDescription',
                    'AI is analyzing candidate data. This may take a moment.')}
                </p>
              </div>
            )}

            {/* Error State */}
            {state === 'error' && (
              <div className="text-center py-12">
                <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  {t('company.candidates.report.errorTitle', 'Generation Failed')}
                </h3>
                <p className="text-gray-500 mb-6">{error}</p>
                <button
                  onClick={handleGenerateReport}
                  className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
                >
                  <RefreshCw className="w-5 h-5" />
                  {t('company.candidates.report.retryButton', 'Try Again')}
                </button>
              </div>
            )}

            {/* Viewing State - Show report */}
            {state === 'viewing' && report && (
              <div className="space-y-6">
                {/* Report Header */}
                <div className="flex items-center justify-between pb-4 border-b border-gray-200">
                  <div className="flex items-center gap-2 text-green-600">
                    <CheckCircle className="w-5 h-5" />
                    <span className="text-sm font-medium">
                      {t('company.candidates.report.generated', 'Report generated')} {' '}
                      {new Date(report.generated_at).toLocaleString()}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={handleRegenerate}
                      className="inline-flex items-center gap-2 px-3 py-1.5 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50"
                    >
                      <RefreshCw className="w-4 h-4" />
                      {t('company.candidates.report.regenerate', 'Regenerate')}
                    </button>
                    <button
                      onClick={handleDownloadPdf}
                      disabled={downloadingPdf}
                      className="inline-flex items-center gap-2 px-3 py-1.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                    >
                      {downloadingPdf ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        <Download className="w-4 h-4" />
                      )}
                      {t('company.candidates.report.download', 'Download')}
                    </button>
                  </div>
                </div>

                {/* Report Sections */}
                <div className="space-y-6">
                  {/* Summary */}
                  <section>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">
                      {t('company.candidates.report.summary', 'Summary')}
                    </h3>
                    <p className="text-gray-700 leading-relaxed">
                      {report.sections.summary}
                    </p>
                  </section>

                  {/* Strengths */}
                  <section>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">
                      {t('company.candidates.report.strengths', 'Strengths')}
                    </h3>
                    <ul className="space-y-2">
                      {report.sections.strengths.map((strength, idx) => (
                        <li key={idx} className="flex items-start gap-2">
                          <span className="text-green-500 mt-1">✓</span>
                          <span className="text-gray-700">{strength}</span>
                        </li>
                      ))}
                    </ul>
                  </section>

                  {/* Areas for Improvement */}
                  <section>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">
                      {t('company.candidates.report.areasForImprovement', 'Areas for Improvement')}
                    </h3>
                    <ul className="space-y-2">
                      {report.sections.areas_for_improvement.map((area, idx) => (
                        <li key={idx} className="flex items-start gap-2">
                          <span className="text-amber-500 mt-1">→</span>
                          <span className="text-gray-700">{area}</span>
                        </li>
                      ))}
                    </ul>
                  </section>

                  {/* Interview Insights */}
                  {report.sections.interview_insights && (
                    <section>
                      <h3 className="text-lg font-semibold text-gray-900 mb-3">
                        {t('company.candidates.report.interviewInsights', 'Interview Insights')}
                      </h3>
                      <p className="text-gray-700 leading-relaxed">
                        {report.sections.interview_insights}
                      </p>
                    </section>
                  )}

                  {/* Recommendation */}
                  <section className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-blue-900 mb-2">
                      {t('company.candidates.report.recommendation', 'Recommendation')}
                    </h3>
                    <p className="text-blue-800 leading-relaxed">
                      {report.sections.recommendation}
                    </p>
                  </section>
                </div>

                {/* Raw Markdown (collapsible) */}
                <details className="border border-gray-200 rounded-lg">
                  <summary className="px-4 py-3 cursor-pointer text-sm font-medium text-gray-600 hover:text-gray-900">
                    {t('company.candidates.report.viewRawMarkdown', 'View Raw Markdown')}
                  </summary>
                  <pre className="p-4 bg-gray-50 text-sm text-gray-700 overflow-x-auto whitespace-pre-wrap">
                    {report.report_markdown}
                  </pre>
                </details>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="flex items-center justify-end px-6 py-4 border-t border-gray-200 bg-gray-50 flex-shrink-0">
            <button
              onClick={onClose}
              className="px-4 py-2 text-gray-700 hover:text-gray-900"
            >
              {t('common.close', 'Close')}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
