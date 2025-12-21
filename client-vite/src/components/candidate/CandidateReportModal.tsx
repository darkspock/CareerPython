/**
 * Candidate Report Modal
 * Modal for generating and viewing AI-powered candidate reports
 */

import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { FileText, Download, Loader2, RefreshCw, CheckCircle, AlertCircle } from 'lucide-react';
import { candidateReportService, type CandidateReportResponse } from '../../services/candidateReportService';
import { toast } from 'react-toastify';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import EmptyState from '@/components/common/EmptyState';

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

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <div className="flex items-center gap-3">
            <FileText className="w-6 h-6 text-primary" />
            <div>
              <DialogTitle>
                {t('company.candidates.report.title', 'Candidate Report')}
              </DialogTitle>
              <DialogDescription>{candidateName}</DialogDescription>
            </div>
          </div>
        </DialogHeader>

        <div className="py-4">
          {/* Idle State - Show generate button */}
          {state === 'idle' && (
            <EmptyState
              icon={FileText}
              title={t('company.candidates.report.generateTitle', 'Generate AI Report')}
              description={t('company.candidates.report.generateDescription',
                'Generate a comprehensive AI-powered report based on comments, interviews, and reviews for this candidate.')}
              actionLabel={t('company.candidates.report.generateButton', 'Generate Report')}
              onAction={handleGenerateReport}
              actionIcon={FileText}
              size="lg"
            />
          )}

          {/* Generating State */}
          {state === 'generating' && (
            <div className="text-center py-12">
              <LoadingSpinner size="xl" color="blue" />
              <h3 className="text-lg font-medium text-foreground mt-4 mb-2">
                {t('company.candidates.report.generating', 'Generating Report...')}
              </h3>
              <p className="text-muted-foreground">
                {t('company.candidates.report.generatingDescription',
                  'AI is analyzing candidate data. This may take a moment.')}
              </p>
            </div>
          )}

          {/* Error State */}
          {state === 'error' && (
            <div className="text-center py-12">
              <AlertCircle className="w-16 h-16 text-destructive mx-auto mb-4" />
              <h3 className="text-lg font-medium text-foreground mb-2">
                {t('company.candidates.report.errorTitle', 'Generation Failed')}
              </h3>
              <p className="text-muted-foreground mb-6">{error}</p>
              <Button onClick={handleGenerateReport}>
                <RefreshCw className="w-4 h-4 mr-2" />
                {t('company.candidates.report.retryButton', 'Try Again')}
              </Button>
            </div>
          )}

          {/* Viewing State - Show report */}
          {state === 'viewing' && report && (
            <div className="space-y-6">
              {/* Report Header */}
              <div className="flex items-center justify-between pb-4 border-b">
                <div className="flex items-center gap-2 text-green-600">
                  <CheckCircle className="w-5 h-5" />
                  <span className="text-sm font-medium">
                    {t('company.candidates.report.generated', 'Report generated')} {' '}
                    {new Date(report.generated_at).toLocaleString()}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Button variant="outline" size="sm" onClick={handleRegenerate}>
                    <RefreshCw className="w-4 h-4 mr-2" />
                    {t('company.candidates.report.regenerate', 'Regenerate')}
                  </Button>
                  <Button size="sm" onClick={handleDownloadPdf} disabled={downloadingPdf}>
                    {downloadingPdf ? (
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    ) : (
                      <Download className="w-4 h-4 mr-2" />
                    )}
                    {t('company.candidates.report.download', 'Download')}
                  </Button>
                </div>
              </div>

              {/* Report Sections */}
              <div className="space-y-6">
                {/* Summary */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">
                      {t('company.candidates.report.summary', 'Summary')}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground leading-relaxed">
                      {report.sections.summary}
                    </p>
                  </CardContent>
                </Card>

                {/* Strengths */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">
                      {t('company.candidates.report.strengths', 'Strengths')}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {report.sections.strengths.map((strength, idx) => (
                        <li key={idx} className="flex items-start gap-2">
                          <span className="text-green-500 mt-1">&#10003;</span>
                          <span className="text-muted-foreground">{strength}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                {/* Areas for Improvement */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">
                      {t('company.candidates.report.areasForImprovement', 'Areas for Improvement')}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {report.sections.areas_for_improvement.map((area, idx) => (
                        <li key={idx} className="flex items-start gap-2">
                          <span className="text-amber-500 mt-1">&rarr;</span>
                          <span className="text-muted-foreground">{area}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                {/* Interview Insights */}
                {report.sections.interview_insights && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-base">
                        {t('company.candidates.report.interviewInsights', 'Interview Insights')}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-muted-foreground leading-relaxed">
                        {report.sections.interview_insights}
                      </p>
                    </CardContent>
                  </Card>
                )}

                {/* Recommendation */}
                <Alert className="bg-primary/10 border-primary/20">
                  <AlertDescription>
                    <h3 className="text-base font-semibold text-primary mb-2">
                      {t('company.candidates.report.recommendation', 'Recommendation')}
                    </h3>
                    <p className="text-primary/80 leading-relaxed">
                      {report.sections.recommendation}
                    </p>
                  </AlertDescription>
                </Alert>
              </div>

              {/* Raw Markdown (collapsible) */}
              <details className="border rounded-lg">
                <summary className="px-4 py-3 cursor-pointer text-sm font-medium text-muted-foreground hover:text-foreground">
                  {t('company.candidates.report.viewRawMarkdown', 'View Raw Markdown')}
                </summary>
                <pre className="p-4 bg-muted text-sm text-muted-foreground overflow-x-auto whitespace-pre-wrap">
                  {report.report_markdown}
                </pre>
              </details>
            </div>
          )}
        </div>

        <DialogFooter>
          <Button variant="ghost" onClick={onClose}>
            {t('common.close', 'Close')}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
