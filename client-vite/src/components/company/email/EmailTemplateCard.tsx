/**
 * Email Template Card Component
 * Phase 7: Card component to display email template information
 */

import React from 'react';
import type { EmailTemplate } from '../../../types/emailTemplate';
import { getTriggerEventLabel } from '../../../types/emailTemplate';

interface EmailTemplateCardProps {
  template: EmailTemplate;
  onEdit?: (template: EmailTemplate) => void;
  onDelete?: (templateId: string) => void;
  onToggleActive?: (templateId: string, isActive: boolean) => void;
  isLoading?: boolean;
}

export const EmailTemplateCard: React.FC<EmailTemplateCardProps> = ({
  template,
  onEdit,
  onDelete,
  onToggleActive,
  isLoading = false
}) => {
  const handleEdit = () => {
    if (!isLoading && onEdit) {
      onEdit(template);
    }
  };

  const handleDelete = () => {
    if (!isLoading && onDelete && confirm(`Delete template "${template.template_name}"?`)) {
      onDelete(template.id);
    }
  };

  const handleToggleActive = () => {
    if (!isLoading && onToggleActive) {
      onToggleActive(template.id, template.is_active);
    }
  };

  return (
    <div className={`bg-white rounded-lg border ${template.is_active ? 'border-gray-200' : 'border-gray-300 opacity-75'} shadow-sm hover:shadow-md transition-shadow`}>
      <div className="p-4">
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900">{template.template_name}</h3>
            <p className="text-sm text-gray-500 mt-1">Key: {template.template_key}</p>
          </div>
          <div className="flex items-center gap-2">
            {/* Active Badge */}
            <span
              className={`px-2 py-1 text-xs font-medium rounded ${
                template.is_active
                  ? 'bg-green-100 text-green-800 border border-green-200'
                  : 'bg-gray-100 text-gray-800 border border-gray-200'
              }`}
            >
              {template.is_active ? 'Active' : 'Inactive'}
            </span>
          </div>
        </div>

        {/* Trigger Event */}
        <div className="mb-3">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200">
            {getTriggerEventLabel(template.trigger_event)}
          </span>
          {template.stage_id && (
            <span className="ml-2 text-xs text-gray-600">
              Stage-specific
            </span>
          )}
        </div>

        {/* Subject Preview */}
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-700 mb-1">Subject:</p>
          <p className="text-sm text-gray-600 line-clamp-1">{template.subject}</p>
        </div>

        {/* Body Preview */}
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-700 mb-1">Body Preview:</p>
          <div
            className="text-sm text-gray-600 line-clamp-2"
            dangerouslySetInnerHTML={{ __html: template.body_html }}
          />
        </div>

        {/* Variables */}
        <div className="mb-4">
          <p className="text-sm font-medium text-gray-700 mb-2">Variables:</p>
          <div className="flex flex-wrap gap-1">
            {template.available_variables.slice(0, 5).map((variable: string) => (
              <span
                key={variable}
                className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-gray-100 text-gray-700 border border-gray-200"
              >
                {`{{ ${variable} }}`}
              </span>
            ))}
            {template.available_variables.length > 5 && (
              <span className="text-xs text-gray-500 self-center">
                +{template.available_variables.length - 5} more
              </span>
            )}
          </div>
        </div>

        {/* Timestamps */}
        <div className="text-xs text-gray-500 mb-3">
          <p>Created: {new Date(template.created_at).toLocaleDateString()}</p>
          {template.updated_at !== template.created_at && (
            <p>Updated: {new Date(template.updated_at).toLocaleDateString()}</p>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2 pt-3 border-t border-gray-200">
          {onEdit && (
            <button
              onClick={handleEdit}
              disabled={isLoading}
              className="flex-1 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Edit
            </button>
          )}

          {onToggleActive && (
            <button
              onClick={handleToggleActive}
              disabled={isLoading}
              className={`flex-1 px-3 py-2 text-sm font-medium rounded border disabled:opacity-50 disabled:cursor-not-allowed ${
                template.is_active
                  ? 'text-gray-700 bg-white border-gray-300 hover:bg-gray-50'
                  : 'text-green-700 bg-green-50 border-green-300 hover:bg-green-100'
              }`}
            >
              {template.is_active ? 'Deactivate' : 'Activate'}
            </button>
          )}

          {onDelete && (
            <button
              onClick={handleDelete}
              disabled={isLoading}
              className="px-3 py-2 text-sm font-medium text-red-700 bg-white border border-red-300 rounded hover:bg-red-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Delete
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
