/**
 * Template Editor Component
 * Phase 7: Component for creating/editing email templates
 */

import React, { useState } from 'react';
import type {
  EmailTemplate,
  CreateEmailTemplateRequest,
  UpdateEmailTemplateRequest,
  TriggerEvent
} from '../../../types/emailTemplate';
import {
  getTriggerEventLabel,
  getTriggerEventDescription,
  DEFAULT_AVAILABLE_VARIABLES,
  getVariableDescription
} from '../../../types/emailTemplate';
import { EmailTemplateService } from '../../../services/emailTemplateService';

interface TemplateEditorProps {
  workflowId: string;
  template?: EmailTemplate | null;
  stageId?: string | null;
  onSave?: () => void;
  onCancel?: () => void;
}

export const TemplateEditor: React.FC<TemplateEditorProps> = ({
  workflowId,
  template,
  stageId = null,
  onSave,
  onCancel
}) => {
  const isEditMode = !!template;

  const [formData, setFormData] = useState({
    template_name: template?.template_name || '',
    template_key: template?.template_key || '',
    subject: template?.subject || '',
    body_html: template?.body_html || '',
    body_text: template?.body_text || '',
    trigger_event: template?.trigger_event || ('' as TriggerEvent),
    available_variables: template?.available_variables || DEFAULT_AVAILABLE_VARIABLES,
    is_active: template?.is_active ?? true
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Available trigger events
  const triggerEvents: TriggerEvent[] = [
    'application_created',
    'application_updated',
    'stage_entered',
    'stage_completed',
    'stage_changed',
    'status_accepted',
    'status_rejected',
    'status_withdrawn',
    'deadline_approaching',
    'deadline_passed',
    'manual'
  ] as TriggerEvent[];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (!formData.template_name || !formData.subject || !formData.body_html || !formData.trigger_event) {
      setError('Please fill in all required fields');
      return;
    }

    try {
      setIsLoading(true);

      if (isEditMode && template) {
        // Update existing template
        const updateData: UpdateEmailTemplateRequest = {
          template_name: formData.template_name,
          subject: formData.subject,
          body_html: formData.body_html,
          body_text: formData.body_text || null,
          available_variables: formData.available_variables
        };
        await EmailTemplateService.updateTemplate(template.id, updateData);
      } else {
        // Create new template
        const createData: CreateEmailTemplateRequest = {
          workflow_id: workflowId,
          stage_id: stageId,
          template_name: formData.template_name,
          template_key: formData.template_key,
          subject: formData.subject,
          body_html: formData.body_html,
          body_text: formData.body_text || null,
          trigger_event: formData.trigger_event,
          available_variables: formData.available_variables,
          is_active: formData.is_active
        };
        await EmailTemplateService.createTemplate(createData);
      }

      if (onSave) onSave();
    } catch (err: any) {
      setError(err.message || 'Failed to save template');
      console.error('Error saving template:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const insertVariable = (variable: string) => {
    const textarea = document.getElementById('body_html') as HTMLTextAreaElement;
    if (textarea) {
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const text = formData.body_html;
      const before = text.substring(0, start);
      const after = text.substring(end);
      const newValue = `${before}{{ ${variable} }}${after}`;

      setFormData({ ...formData, body_html: newValue });

      // Set cursor position after inserted variable
      setTimeout(() => {
        textarea.focus();
        textarea.selectionStart = textarea.selectionEnd = start + variable.length + 6;
      }, 0);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        {/* Header */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">
            {isEditMode ? 'Edit Email Template' : 'Create Email Template'}
          </h2>
          <p className="text-sm text-gray-600 mt-1">
            {isEditMode
              ? 'Update your email template settings'
              : 'Create a new automated email template'}
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Template Name */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Template Name *
            </label>
            <input
              type="text"
              value={formData.template_name}
              onChange={(e) => setFormData({ ...formData, template_name: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., Welcome Email"
              required
            />
          </div>

          {/* Template Key (only for create) */}
          {!isEditMode && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Template Key *
              </label>
              <input
                type="text"
                value={formData.template_key}
                onChange={(e) => setFormData({ ...formData, template_key: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., welcome_email"
                required
              />
              <p className="text-xs text-gray-500 mt-1">
                Unique identifier (lowercase, underscores, no spaces)
              </p>
            </div>
          )}

          {/* Trigger Event (only for create) */}
          {!isEditMode && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Trigger Event *
              </label>
              <select
                value={formData.trigger_event}
                onChange={(e) => setFormData({ ...formData, trigger_event: e.target.value as TriggerEvent })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select trigger event...</option>
                {triggerEvents.map((event) => (
                  <option key={event} value={event}>
                    {getTriggerEventLabel(event)}
                  </option>
                ))}
              </select>
              {formData.trigger_event && (
                <p className="text-xs text-gray-500 mt-1">
                  {getTriggerEventDescription(formData.trigger_event)}
                </p>
              )}
            </div>
          )}

          {/* Subject */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email Subject *
            </label>
            <input
              type="text"
              value={formData.subject}
              onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., Welcome to {{ company_name }}"
              required
            />
          </div>

          {/* Variables Palette */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Available Variables
            </label>
            <div className="flex flex-wrap gap-2 p-3 bg-gray-50 border border-gray-200 rounded-lg">
              {formData.available_variables.map((variable: string) => (
                <button
                  key={variable}
                  type="button"
                  onClick={() => insertVariable(variable)}
                  className="px-3 py-1 text-sm bg-white border border-gray-300 rounded hover:bg-blue-50 hover:border-blue-300 transition-colors"
                  title={getVariableDescription(variable)}
                >
                  {`{{ ${variable} }}`}
                </button>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Click a variable to insert it at cursor position
            </p>
          </div>

          {/* Body HTML */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email Body (HTML) *
            </label>
            <textarea
              id="body_html"
              value={formData.body_html}
              onChange={(e) => setFormData({ ...formData, body_html: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
              rows={12}
              placeholder="<p>Hello {{ candidate_name }},</p><p>Welcome to our process!</p>"
              required
            />
          </div>

          {/* Body Text (optional) */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email Body (Plain Text)
            </label>
            <textarea
              value={formData.body_text}
              onChange={(e) => setFormData({ ...formData, body_text: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
              rows={6}
              placeholder="Hello {{ candidate_name }}, Welcome to our process!"
            />
            <p className="text-xs text-gray-500 mt-1">
              Optional plain text version for email clients that don't support HTML
            </p>
          </div>

          {/* Active Toggle (only for create) */}
          {!isEditMode && (
            <div className="mb-6">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={formData.is_active}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                  className="mr-2"
                />
                <span className="text-sm font-medium text-gray-700">
                  Activate template immediately
                </span>
              </label>
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center gap-3 pt-4 border-t border-gray-200">
            <button
              type="submit"
              disabled={isLoading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {isLoading ? 'Saving...' : isEditMode ? 'Update Template' : 'Create Template'}
            </button>
            {onCancel && (
              <button
                type="button"
                onClick={onCancel}
                disabled={isLoading}
                className="px-6 py-2 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};
