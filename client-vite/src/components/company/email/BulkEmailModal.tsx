/**
 * Bulk Email Modal Component
 * Phase 8: Allows sending emails to multiple candidates using templates
 */

import React, { useState, useEffect } from 'react';
import { Mail, Users, Send, AlertCircle, CheckCircle } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { EmailTemplate } from '../../../types/emailTemplate';
import type { CompanyCandidate } from '../../../types/companyCandidate';
import { EmailTemplateService } from '../../../services/emailTemplateService';
import { formatVariableForDisplay } from '../../../types/emailTemplate';

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

  useEffect(() => {
    if (isOpen && workflowId) {
      loadTemplates();
    }
  }, [isOpen, workflowId]);

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
      const allTemplates = await EmailTemplateService.listTemplatesByWorkflow(workflowId, true);
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
      })).filter(r => r.email);

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

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3">
            <Mail className="w-6 h-6 text-blue-600" />
            Send Bulk Email
          </DialogTitle>
        </DialogHeader>

        {/* Recipients Summary */}
        <div className="flex items-center gap-2 text-sm text-blue-700 bg-blue-50 px-4 py-2 rounded-lg border border-blue-100">
          <Users className="w-4 h-4" />
          <span>
            Sending to <strong>{candidates.length}</strong> candidate{candidates.length !== 1 ? 's' : ''}
          </span>
        </div>

        <div className="py-4">
          {/* Error Alert */}
          {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertCircle className="w-4 h-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Step: Select Template */}
          {step === 'select-template' && (
            <div className="space-y-4">
              <h3 className="text-lg font-medium">Select Email Template</h3>

              {isLoading ? (
                <div className="flex justify-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
              ) : templates.length === 0 ? (
                <Card className="bg-gray-50">
                  <CardContent className="pt-6 text-center">
                    <Mail className="w-12 h-12 text-muted-foreground mx-auto mb-3" />
                    <p className="text-muted-foreground">No manual email templates available.</p>
                    <p className="text-sm text-muted-foreground mt-1">
                      Create a template with "Manual" trigger to send bulk emails.
                    </p>
                  </CardContent>
                </Card>
              ) : (
                <div className="space-y-3">
                  {templates.map(template => (
                    <Card
                      key={template.id}
                      className="cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors"
                      onClick={() => handleSelectTemplate(template)}
                    >
                      <CardContent className="pt-4">
                        <div className="font-medium">{template.template_name}</div>
                        <div className="text-sm text-muted-foreground mt-1">{template.subject}</div>
                        <div className="flex flex-wrap gap-2 mt-2">
                          {template.available_variables.slice(0, 5).map(v => (
                            <Badge key={v} variant="secondary" className="text-xs">
                              {formatVariableForDisplay(v)}
                            </Badge>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Step: Preview */}
          {step === 'preview' && selectedTemplate && (
            <div className="space-y-4">
              <h3 className="text-lg font-medium">Preview Email</h3>

              {/* Template Info */}
              <Card className="bg-gray-50">
                <CardContent className="pt-4">
                  <div className="text-sm text-muted-foreground">Template</div>
                  <div className="font-medium">{selectedTemplate.template_name}</div>
                </CardContent>
              </Card>

              {/* Subject Preview */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Subject</label>
                <Card>
                  <CardContent className="pt-4">
                    {selectedTemplate.subject}
                  </CardContent>
                </Card>
              </div>

              {/* Body Preview */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Body Preview</label>
                <Card className="max-h-64 overflow-y-auto">
                  <CardContent className="pt-4">
                    <div dangerouslySetInnerHTML={{ __html: renderPreviewBody() }} />
                  </CardContent>
                </Card>
              </div>

              {/* Variables Info */}
              <Alert className="border-yellow-200 bg-yellow-50">
                <AlertDescription className="text-yellow-800 text-sm">
                  <strong>Note:</strong> Variables like {'{'}{'{'} candidate_name {'}'}{'}'}  will be
                  replaced with actual candidate data for each recipient.
                </AlertDescription>
              </Alert>
            </div>
          )}

          {/* Step: Sending */}
          {step === 'sending' && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-muted-foreground">Sending emails...</p>
              <p className="text-sm text-muted-foreground mt-1">Please wait while we process your request.</p>
            </div>
          )}

          {/* Step: Complete */}
          {step === 'complete' && sendResult && (
            <div className="text-center py-8">
              <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Emails Sent!</h3>
              <p className="text-muted-foreground mb-4">{sendResult.message}</p>
              <Badge variant="secondary" className="text-green-700 bg-green-50">
                {sendResult.queued} queued
              </Badge>
            </div>
          )}
        </div>

        <DialogFooter>
          <Button
            variant="ghost"
            onClick={step === 'preview' ? () => setStep('select-template') : onClose}
          >
            {step === 'preview' ? 'Back' : 'Cancel'}
          </Button>

          {step === 'preview' && (
            <Button onClick={handleSendEmails}>
              <Send className="w-4 h-4" />
              Send to {candidates.length} Candidate{candidates.length !== 1 ? 's' : ''}
            </Button>
          )}

          {step === 'complete' && (
            <Button onClick={onClose}>
              Done
            </Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
