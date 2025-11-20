import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { X, AlertCircle } from 'lucide-react';
import { companyInterviewService } from '../../services/companyInterviewService';
import { companyInterviewTemplateService, type InterviewTemplate } from '../../services/companyInterviewTemplateService';
import { CompanyUserService } from '../../services/companyUserService';
import { api } from '../../lib/api';
import { useCompanyId } from '../../hooks/useCompanyId';
import type { WorkflowStage } from '../../types/workflow';
import type { CompanyRole } from '../../types/company';
import type { CompanyUser } from '../../types/companyUser';

// Interview types enum (must match backend)
const INTERVIEW_TYPES = [
  { value: 'EXTENDED_PROFILE', label: 'Extended Profile' },
  { value: 'POSITION_INTERVIEW', label: 'Position Interview' },
  { value: 'TECHNICAL', label: 'Technical' },
  { value: 'BEHAVIORAL', label: 'Behavioral' },
  { value: 'CULTURAL_FIT', label: 'Cultural Fit' },
];

interface AssignInterviewModalProps {
  candidateId: string;
  companyCandidateId: string;
  currentStageId: string | null | undefined;
  currentWorkflowId: string | null | undefined;
  availableStages: WorkflowStage[];
  jobPositionId?: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function AssignInterviewModal({
  candidateId,
  companyCandidateId,
  currentStageId,
  currentWorkflowId,
  availableStages,
  jobPositionId,
  isOpen,
  onClose,
  onSuccess,
}: AssignInterviewModalProps) {
  const { t } = useTranslation();
  const companyId = useCompanyId();

  // Form state
  const [workflowStageId, setWorkflowStageId] = useState<string>(currentStageId || '');
  const [interviewType, setInterviewType] = useState<string>('');
  const [templateId, setTemplateId] = useState<string>('');
  const [requiredRoles, setRequiredRoles] = useState<string[]>([]);
  const [scheduledAt, setScheduledAt] = useState<string>('');
  const [participants, setParticipants] = useState<string[]>([]);

  // Loading states
  const [loadingTemplates, setLoadingTemplates] = useState(false);
  const [loadingRoles, setLoadingRoles] = useState(false);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  // Data
  const [availableTemplates, setAvailableTemplates] = useState<InterviewTemplate[]>([]);
  const [availableRoles, setAvailableRoles] = useState<CompanyRole[]>([]);
  const [availableUsers, setAvailableUsers] = useState<CompanyUser[]>([]);

  // Errors
  const [formError, setFormError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  // Pre-select current stage on mount and when it changes
  useEffect(() => {
    if (currentStageId) {
      setWorkflowStageId(currentStageId);
    }
  }, [currentStageId]);

  // Load available roles on mount
  useEffect(() => {
    loadRoles();
  }, []);

  // Load available users on mount
  useEffect(() => {
    loadUsers();
  }, []);

  // Load templates when interview type changes
  useEffect(() => {
    if (interviewType) {
      loadTemplates(interviewType);
    } else {
      setAvailableTemplates([]);
      setTemplateId('');
    }
  }, [interviewType]);

  // Auto-select template if only one available
  useEffect(() => {
    if (availableTemplates.length === 1) {
      setTemplateId(availableTemplates[0].id);
    }
  }, [availableTemplates]);

  const loadTemplates = async (type: string) => {
    try {
      setLoadingTemplates(true);
      // Load templates filtered by type
      const templates = await companyInterviewTemplateService.listTemplates({
        type: type,
        status: 'ENABLED',
      });
      setAvailableTemplates(templates);
    } catch (err) {
      console.error('Error loading templates:', err);
      setAvailableTemplates([]);
    } finally {
      setLoadingTemplates(false);
    }
  };

  const loadRoles = async () => {
    if (!companyId) return;

    try {
      setLoadingRoles(true);
      const rolesData = await api.listCompanyRoles(companyId, true); // Only active roles
      setAvailableRoles(rolesData as CompanyRole[]);
    } catch (err) {
      console.error('Error loading roles:', err);
      setAvailableRoles([]);
    } finally {
      setLoadingRoles(false);
    }
  };

  const loadUsers = async () => {
    if (!companyId) return;

    try {
      setLoadingUsers(true);
      const usersData = await CompanyUserService.getCompanyUsers(companyId, { active_only: true });
      setAvailableUsers(usersData);
    } catch (err) {
      console.error('Error loading users:', err);
      setAvailableUsers([]);
    } finally {
      setLoadingUsers(false);
    }
  };

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};

    if (!workflowStageId) {
      errors.workflowStageId = t('company.interviews.errors.stageRequired', { defaultValue: 'Stage is required' });
    }

    if (!interviewType) {
      errors.interviewType = t('company.interviews.errors.typeRequired', { defaultValue: 'Interview type is required' });
    }

    if (availableTemplates.length > 1 && !templateId) {
      errors.templateId = t('company.interviews.errors.templateRequired', { defaultValue: 'Please select a template' });
    }

    if (requiredRoles.length === 0) {
      errors.requiredRoles = t('company.interviews.errors.rolesRequired', { defaultValue: 'At least one role is required' });
    }

    if (scheduledAt) {
      const scheduledDate = new Date(scheduledAt);
      const now = new Date();
      if (scheduledDate < now) {
        errors.scheduledAt = t('company.interviews.errors.dateInPast', { defaultValue: 'Scheduled date must be in the future' });
      }
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    if (!validateForm()) {
      return;
    }

    try {
      setSubmitting(true);

      // Call create interview service through companyInterviewService
      await companyInterviewService.createInterview({
        candidate_id: candidateId,
        workflow_stage_id: workflowStageId,
        interview_type: interviewType as any, // Type assertion - backend expects specific enum
        interview_mode: 'MANUAL', // Default to MANUAL mode
        interview_template_id: templateId || undefined,
        required_roles: requiredRoles,
        scheduled_at: scheduledAt || undefined,
        interviewers: participants.length > 0 ? participants : undefined,
        job_position_id: jobPositionId,
      });

      // Call success callback to reload interviews
      onSuccess();
      handleClose();
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create interview';
      setFormError(errorMessage);
      console.error('Error creating interview:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleClose = () => {
    // Reset form
    setWorkflowStageId(currentStageId || '');
    setInterviewType('');
    setTemplateId('');
    setRequiredRoles([]);
    setScheduledAt('');
    setParticipants([]);
    setFormError(null);
    setFieldErrors({});
    onClose();
  };

  const toggleRole = (roleId: string) => {
    setRequiredRoles(prev =>
      prev.includes(roleId)
        ? prev.filter(id => id !== roleId)
        : [...prev, roleId]
    );
  };

  const toggleParticipant = (userId: string) => {
    setParticipants(prev =>
      prev.includes(userId)
        ? prev.filter(id => id !== userId)
        : [...prev, userId]
    );
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 sticky top-0 bg-white">
          <h2 className="text-xl font-semibold text-gray-900">
            {t('company.interviews.assignInterview')}
          </h2>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Global form error */}
          {formError && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-red-600">{formError}</p>
              </div>
            </div>
          )}

          {/* Workflow Stage (Obligatorio) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('company.interviews.form.stage')} <span className="text-red-600">*</span>
            </label>
            <select
              value={workflowStageId}
              onChange={(e) => setWorkflowStageId(e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                fieldErrors.workflowStageId ? 'border-red-500' : 'border-gray-300'
              }`}
            >
              <option value="">{t('company.interviews.form.selectStage')}</option>
              {availableStages.map((stage) => (
                <option key={stage.id} value={stage.id}>
                  {stage.name}
                  {stage.id === currentStageId && ` (${t('company.interviews.current')})`}
                </option>
              ))}
            </select>
            {fieldErrors.workflowStageId && (
              <p className="mt-1 text-sm text-red-600">{fieldErrors.workflowStageId}</p>
            )}
          </div>

          {/* Interview Type (Obligatorio) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('company.interviews.form.type')} <span className="text-red-600">*</span>
            </label>
            <select
              value={interviewType}
              onChange={(e) => setInterviewType(e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                fieldErrors.interviewType ? 'border-red-500' : 'border-gray-300'
              }`}
            >
              <option value="">{t('company.interviews.form.selectType')}</option>
              {INTERVIEW_TYPES.map((type) => (
                <option key={type.value} value={type.value}>
                  {t(`company.interviews.types.${type.value}`, { defaultValue: type.label })}
                </option>
              ))}
            </select>
            {fieldErrors.interviewType && (
              <p className="mt-1 text-sm text-red-600">{fieldErrors.interviewType}</p>
            )}
          </div>

          {/* Template (Conditional) */}
          {interviewType && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('company.interviews.form.template')}
                {availableTemplates.length > 1 && <span className="text-red-600">*</span>}
              </label>
              {loadingTemplates ? (
                <div className="flex items-center gap-2 text-gray-600">
                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-gray-400 border-t-transparent"></div>
                  <span className="text-sm">{t('common.loading')}</span>
                </div>
              ) : availableTemplates.length === 0 ? (
                <p className="text-sm text-gray-500">
                  {t('company.interviews.form.noTemplates', { defaultValue: 'No templates available for this type' })}
                </p>
              ) : availableTemplates.length === 1 ? (
                <div className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg">
                  <p className="text-sm text-gray-700">{availableTemplates[0].name}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {t('company.interviews.form.autoSelected', { defaultValue: 'Automatically selected' })}
                  </p>
                </div>
              ) : (
                <>
                  <select
                    value={templateId}
                    onChange={(e) => setTemplateId(e.target.value)}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                      fieldErrors.templateId ? 'border-red-500' : 'border-gray-300'
                    }`}
                  >
                    <option value="">{t('company.interviews.form.selectTemplate')}</option>
                    {availableTemplates.map((template) => (
                      <option key={template.id} value={template.id}>
                        {template.name}
                      </option>
                    ))}
                  </select>
                  {fieldErrors.templateId && (
                    <p className="mt-1 text-sm text-red-600">{fieldErrors.templateId}</p>
                  )}
                </>
              )}
            </div>
          )}

          {/* Required Roles (Obligatorio) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('company.interviews.form.requiredRoles')} <span className="text-red-600">*</span>
            </label>
            {loadingRoles ? (
              <div className="flex items-center gap-2 text-gray-600">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-gray-400 border-t-transparent"></div>
                <span className="text-sm">{t('common.loading')}</span>
              </div>
            ) : (
              <>
                <div className="border border-gray-300 rounded-lg p-3 max-h-48 overflow-y-auto">
                  {availableRoles.length === 0 ? (
                    <p className="text-sm text-gray-500">{t('company.interviews.form.noRoles')}</p>
                  ) : (
                    <div className="space-y-2">
                      {availableRoles.map((role) => (
                        <label key={role.id} className="flex items-center gap-2 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={requiredRoles.includes(role.id)}
                            onChange={() => toggleRole(role.id)}
                            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          />
                          <span className="text-sm text-gray-700">{role.name}</span>
                        </label>
                      ))}
                    </div>
                  )}
                </div>
                {fieldErrors.requiredRoles && (
                  <p className="mt-1 text-sm text-red-600">{fieldErrors.requiredRoles}</p>
                )}
                <p className="mt-1 text-xs text-gray-500">
                  {t('company.interviews.form.rolesHelp', { defaultValue: 'Select at least one role' })}
                </p>
              </>
            )}
          </div>

          {/* Scheduled Date (Opcional) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('company.interviews.form.scheduledDate')}
            </label>
            <input
              type="datetime-local"
              value={scheduledAt}
              onChange={(e) => setScheduledAt(e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                fieldErrors.scheduledAt ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {fieldErrors.scheduledAt && (
              <p className="mt-1 text-sm text-red-600">{fieldErrors.scheduledAt}</p>
            )}
            <p className="mt-1 text-xs text-gray-500">
              {t('company.interviews.form.scheduledDateHelp', { defaultValue: 'Optional - leave empty to schedule later' })}
            </p>
          </div>

          {/* Participants (Opcional) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('company.interviews.form.participants')}
            </label>
            {loadingUsers ? (
              <div className="flex items-center gap-2 text-gray-600">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-gray-400 border-t-transparent"></div>
                <span className="text-sm">{t('common.loading')}</span>
              </div>
            ) : (
              <>
                <div className="border border-gray-300 rounded-lg p-3 max-h-48 overflow-y-auto">
                  {availableUsers.length === 0 ? (
                    <p className="text-sm text-gray-500">{t('company.interviews.form.noUsers')}</p>
                  ) : (
                    <div className="space-y-2">
                      {availableUsers.map((user) => (
                        <label key={user.id} className="flex items-center gap-2 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={participants.includes(user.id)}
                            onChange={() => toggleParticipant(user.id)}
                            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          />
                          <span className="text-sm text-gray-700">
                            {user.email || user.id}
                          </span>
                        </label>
                      ))}
                    </div>
                  )}
                </div>
                <p className="mt-1 text-xs text-gray-500">
                  {t('company.interviews.form.participantsHelp', { defaultValue: 'Optional - select interviewers' })}
                </p>
              </>
            )}
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={handleClose}
              disabled={submitting}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50"
            >
              {t('common.cancel')}
            </button>
            <button
              type="submit"
              disabled={submitting || loadingTemplates || loadingRoles || loadingUsers}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {submitting && (
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
              )}
              {t('company.interviews.assignInterview')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

