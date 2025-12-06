/**
 * Bulk Email Modal Component
 * Phase 8: Allows sending emails to multiple candidates using templates
 */

import React, { useState, useEffect } from 'react';
import { X, Mail, Users, Send, AlertCircle, CheckCircle } from 'lucide-react';
import type { EmailTemplate } from '../../../types/emailTemplate';
import type { CompanyCandidate } from '../../../types/companyCandidate';
import { EmailTemplateService } from '../../../services/emailTemplateService';
import { DEFAULT_AVAILABLE_VARIABLES, formatVariableForDisplay } from '../../../types/emailTemplate';

interface BulkEmailModalProps {
  isOpen: boolean;
  onClose: () => void;
  candidates: CompanyCandidate[];
  workflowId: string;
  companyName?: string;
  positionTitle?: string;
}

type ModalStep = 'select-template' | 'preview' | 'sending' | 'complete';

interface SendResult {
  success: boolean;
  total: number;
  queued: number;
  message: string;
}

export const BulkEmailModal: React.FC<BulkEmailModalProps> = ({
  isOpen,
  onClose,
  candidates,
  workflowId,
  companyName = 'Company',
  positionTitle = 'Position'
}) => {
  const [step, setStep] = useState<ModalStep>('select-template');
  const [templates, setTemplates] = useState<EmailTemplate[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<EmailTemplate | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sendResult, setSendResult] = useState<SendResult | null>(null);

  // Load templates when modal opens
  useEffect(() => {
    if (isOpen && workflowId) {
      loadTemplates();
    }
  }, [isOpen, workflowId]);

  // Reset state when modal closes
  useEffect(() => {
    if (!isOpen) {
      setStep('select-template');
      setSelectedTemplate(null);
      setError(null);
      setSendResult(null);
    }
  }, [isOpen]);

  const loadTemplates = async () => {
    try {
      setIsLoading(true);
      setError(null);
      // Load templates with MANUAL trigger for bulk sending
      const allTemplates = await EmailTemplateService.listTemplatesByWorkflow(workflowId, true);
      // Filter to only show MANUAL trigger templates
      const manualTemplates = allTemplates.filter(t => t.trigger_event === 'manual');
      setTemplates(manualTemplates);
    } catch (err) {
      setError('Failed to load email templates');
      console.error('Error loading templates:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectTemplate = (template: EmailTemplate) => {
    setSelectedTemplate(template);
    setStep('preview');
  };

  const handleSendEmails = async () => {
    if (!selectedTemplate) return;

    try {
      setStep('sending');
      setError(null);

      // Build recipients list with template data
      const recipients = candidates.map(candidate => ({
        email: candidate.candidate_email || '',
        name: candidate.candidate_name || 'Candidate',
        template_data: {
          candidate_name: candidate.candidate_name || 'Candidate',
          candidate_email: candidate.candidate_email || '',
          position_title: candidate.job_position_title || positionTitle,
          company_name: companyName,
          stage_name: candidate.stage_name || '',
          application_id: candidate.id
        }
      })).filter(r => r.email); // Filter out candidates without email

      if (recipients.length === 0) {
        setError('No candidates with valid email addresses');
        setStep('preview');
        return;
      }

      const result = await EmailTemplateService.sendBulkEmail(
        selectedTemplate.id,
        recipients
      );

      setSendResult({
        success: true,
        total: result.total,
        queued: result.queued,
        message: result.message
      });
      setStep('complete');

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send emails');
      setStep('preview');
    }
  };

  const renderPreviewBody = () => {
    if (!selectedTemplate) return '';

    // Replace variables with example values for preview
    let preview = selectedTemplate.body_html;
    const exampleData: Record<string, string> = {
      candidate_name: candidates[0]?.candidate_name || 'John Doe',
      candidate_email: candidates[0]?.candidate_email || 'john@example.com',
      position_title: candidates[0]?.job_position_title || positionTitle,
      company_name: companyName,
      stage_name: candidates[0]?.stage_name || 'Application Review',
      application_id: candidates[0]?.id || 'APP-001'
    };

    for (const [key, value] of Object.entries(exampleData)) {
      preview = preview.replace(new RegExp(`\\{\\{${key}\\}\\}`, 'g'), value);
    }

    return preview;
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
        <div className="relative w-full max-w-3xl bg-white rounded-xl shadow-xl">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
            <div className="flex items-center gap-3">
              <Mail className="w-6 h-6 text-blue-600" />
              <h2 className="text-xl font-semibold text-gray-900">Send Bulk Email</h2>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-500"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Recipients Summary */}
          <div className="px-6 py-3 bg-blue-50 border-b border-blue-100">
            <div className="flex items-center gap-2 text-sm text-blue-700">
              <Users className="w-4 h-4" />
              <span>
                Sending to <strong>{candidates.length}</strong> candidate{candidates.length !== 1 ? 's' : ''}
              </span>
            </div>
          </div>

          {/* Content */}
          <div className="p-6">
            {/* Error Alert */}
            {error && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-red-800">Error</p>
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              </div>
            )}

            {/* Step: Select Template */}
            {step === 'select-template' && (
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Select Email Template</h3>

                {isLoading ? (
                  <div className="flex justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  </div>
                ) : templates.length === 0 ? (
                  <div className="text-center py-8 bg-gray-50 rounded-lg">
                    <Mail className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                    <p className="text-gray-600">No manual email templates available.</p>
                    <p className="text-sm text-gray-500 mt-1">
                      Create a template with "Manual" trigger to send bulk emails.
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {templates.map(template => (
                      <button
                        key={template.id}
                        onClick={() => handleSelectTemplate(template)}
                        className="w-full text-left p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
                      >
                        <div className="font-medium text-gray-900">{template.template_name}</div>
                        <div className="text-sm text-gray-600 mt-1">{template.subject}</div>
                        <div className="flex flex-wrap gap-2 mt-2">
                          {template.available_variables.slice(0, 5).map(v => (
                            <span
                              key={v}
                              className="px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded"
                            >
                              {formatVariableForDisplay(v)}
                            </span>
                          ))}
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Step: Preview */}
            {step === 'preview' && selectedTemplate && (
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Preview Email</h3>

                {/* Template Info */}
                <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                  <div className="text-sm text-gray-600">Template</div>
                  <div className="font-medium text-gray-900">{selectedTemplate.template_name}</div>
                </div>

                {/* Subject Preview */}
                <div className="mb-4">
                  <div className="text-sm font-medium text-gray-700 mb-1">Subject</div>
                  <div className="p-3 bg-white border border-gray-200 rounded-lg text-gray-900">
                    {selectedTemplate.subject}
                  </div>
                </div>

                {/* Body Preview */}
                <div className="mb-4">
                  <div className="text-sm font-medium text-gray-700 mb-1">Body Preview</div>
                  <div
                    className="p-4 bg-white border border-gray-200 rounded-lg max-h-64 overflow-y-auto"
                    dangerouslySetInnerHTML={{ __html: renderPreviewBody() }}
                  />
                </div>

                {/* Variables Info */}
                <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-800">
                  <strong>Note:</strong> Variables like {'{'}{'{'} candidate_name {'}'}{'}'}  will be
                  replaced with actual candidate data for each recipient.
                </div>
              </div>
            )}

            {/* Step: Sending */}
            {step === 'sending' && (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p className="text-gray-600">Sending emails...</p>
                <p className="text-sm text-gray-500 mt-1">Please wait while we process your request.</p>
              </div>
            )}

            {/* Step: Complete */}
            {step === 'complete' && sendResult && (
              <div className="text-center py-8">
                <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Emails Sent!</h3>
                <p className="text-gray-600 mb-4">{sendResult.message}</p>
                <div className="inline-flex items-center gap-4 text-sm">
                  <div className="px-4 py-2 bg-green-50 rounded-lg">
                    <span className="text-green-700 font-medium">{sendResult.queued}</span>
                    <span className="text-green-600 ml-1">queued</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="flex items-center justify-between px-6 py-4 border-t border-gray-200 bg-gray-50">
            <button
              onClick={step === 'preview' ? () => setStep('select-template') : onClose}
              className="px-4 py-2 text-gray-700 hover:text-gray-900"
            >
              {step === 'preview' ? 'Back' : 'Cancel'}
            </button>

            {step === 'preview' && (
              <button
                onClick={handleSendEmails}
                className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
              >
                <Send className="w-4 h-4" />
                Send to {candidates.length} Candidate{candidates.length !== 1 ? 's' : ''}
              </button>
            )}

            {step === 'complete' && (
              <button
                onClick={onClose}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
              >
                Done
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
