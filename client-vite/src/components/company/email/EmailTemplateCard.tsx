/**
 * Email Template Card Component
 * Phase 7: Card component to display email template information
 */

import React from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
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
    <Card className={`hover:shadow-md transition-shadow ${template.is_active ? '' : 'opacity-75'}`}>
      <CardHeader>
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle>{template.template_name}</CardTitle>
            <p className="text-sm text-gray-500 mt-1">Key: {template.template_key}</p>
          </div>
          <div className="flex items-center gap-2">
            {/* Active Badge */}
            <Badge variant={template.is_active ? "default" : "secondary"}>
              {template.is_active ? 'Active' : 'Inactive'}
            </Badge>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        {/* Trigger Event */}
        <div>
          <Badge variant="outline">
            {getTriggerEventLabel(template.trigger_event)}
          </Badge>
          {template.stage_id && (
            <span className="ml-2 text-xs text-gray-600">
              Stage-specific
            </span>
          )}
        </div>

        {/* Subject Preview */}
        <div>
          <p className="text-sm font-medium text-gray-700 mb-1">Subject:</p>
          <p className="text-sm text-gray-600 line-clamp-1">{template.subject}</p>
        </div>

        {/* Body Preview */}
        <div>
          <p className="text-sm font-medium text-gray-700 mb-1">Body Preview:</p>
          <div
            className="text-sm text-gray-600 line-clamp-2"
            dangerouslySetInnerHTML={{ __html: template.body_html }}
          />
        </div>

        {/* Variables */}
        <div>
          <p className="text-sm font-medium text-gray-700 mb-2">Variables:</p>
          <div className="flex flex-wrap gap-1">
            {template.available_variables.slice(0, 5).map((variable: string) => (
              <Badge key={variable} variant="secondary">
                {`{{ ${variable} }}`}
              </Badge>
            ))}
            {template.available_variables.length > 5 && (
              <span className="text-xs text-gray-500 self-center">
                +{template.available_variables.length - 5} more
              </span>
            )}
          </div>
        </div>

        {/* Timestamps */}
        <div className="text-xs text-gray-500">
          <p>Created: {new Date(template.created_at).toLocaleDateString()}</p>
          {template.updated_at !== template.created_at && (
            <p>Updated: {new Date(template.updated_at).toLocaleDateString()}</p>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2 pt-3 border-t border-gray-200">
          {onEdit && (
            <Button
              onClick={handleEdit}
              disabled={isLoading}
              variant="secondary"
              className="flex-1"
            >
              Edit
            </Button>
          )}

          {onToggleActive && (
            <Button
              onClick={handleToggleActive}
              disabled={isLoading}
              variant={template.is_active ? "secondary" : "default"}
              className="flex-1"
            >
              {template.is_active ? 'Deactivate' : 'Activate'}
            </Button>
          )}

          {onDelete && (
            <Button
              onClick={handleDelete}
              disabled={isLoading}
              variant="destructive"
            >
              Delete
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
