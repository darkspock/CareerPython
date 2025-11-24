import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { X, AlertCircle, Plus } from 'lucide-react';
import { companyInterviewService } from '../../services/companyInterviewService';
import { companyInterviewTemplateService, type InterviewTemplate } from '../../services/companyInterviewTemplateService';
import { CompanyUserService } from '../../services/companyUserService';
import { api } from '../../lib/api';
import { useCompanyId } from '../../hooks/useCompanyId';
import type { WorkflowStage } from '../../types/workflow';
import type { CompanyRole } from '../../types/company';
import type { CompanyUser } from '../../types/companyUser';
import { Button } from '@/components/ui/button';
import RoleAssignmentSelector, { type RoleAssignment } from '../interviews/RoleAssignmentSelector';

// Interview types enum (must match backend InterviewTypeEnum)
const INTERVIEW_TYPES = [
  { value: 'CUSTOM', label: 'Custom' },
  { value: 'TECHNICAL', label: 'Technical' },
  { value: 'BEHAVIORAL', label: 'Behavioral' },
  { value: 'CULTURAL_FIT', label: 'Cultural Fit' },
  { value: 'KNOWLEDGE_CHECK', label: 'Knowledge Check' },
  { value: 'EXPERIENCE_CHECK', label: 'Experience Check' },
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
  const [interviewType, setInterviewType] = useState<string>('');
  const [templateId, setTemplateId] = useState<string>('');
  const [roleAssignments, setRoleAssignments] = useState<RoleAssignment[]>([]);
  const [scheduledAt, setScheduledAt] = useState<string>('');

  // workflowStageId - directly use currentStageId or allow override
  const [workflowStageId, setWorkflowStageId] = useState<string>('');

  // Initialize workflowStageId when modal opens
  useEffect(() => {
    if (isOpen) {
      // Check if currentStageId is in availableStages
      const isCurrentStageAvailable = currentStageId && availableStages.some(s => s.id === currentStageId);

      // If current stage is available, use it; otherwise use empty string
      const initialStageId = isCurrentStageAvailable ? currentStageId || '' : '';

      setWorkflowStageId(initialStageId);
      setInterviewType('');
      setTemplateId('');
      setRoleAssignments([]);
      setScheduledAt('');
      setFormError(null);
      setFieldErrors({});
    }
  }, [isOpen, currentStageId, availableStages]);

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

    // Validate job position (required by backend)
    if (!jobPositionId) {
      setFormError(t('company.interviews.errors.jobPositionRequired', { 
        defaultValue: 'This candidate must be associated with a job position to assign interviews' 
      }));
      return false;
    }

    if (!workflowStageId) {
      errors.workflowStageId = t('company.interviews.errors.stageRequired', { defaultValue: 'Stage is required' });
    }

    if (!interviewType) {
      errors.interviewType = t('company.interviews.errors.typeRequired', { defaultValue: 'Interview type is required' });
    }

    if (availableTemplates.length > 1 && !templateId) {
      errors.templateId = t('company.interviews.errors.templateRequired', { defaultValue: 'Please select a template' });
    }

    // Check if at least one role assignment exists with a valid roleId
    const validAssignments = roleAssignments.filter(a => a.roleId);
    if (validAssignments.length === 0) {
      errors.roleAssignments = t('company.interviews.errors.rolesRequired', { defaultValue: 'At least one role is required' });
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

      // Extract required_roles (roleIds) and interviewers (all userIds)
      const validAssignments = roleAssignments.filter(a => a.roleId && a.roleId.trim() !== '');
      const requiredRoles = validAssignments.map(a => a.roleId).filter(Boolean);
      const allInterviewers = validAssignments
        .flatMap(a => a.userIds)
        .filter(Boolean)
        .filter((id, index, self) => self.indexOf(id) === index); // Remove duplicates

      console.log('Sending interview data:', {
        requiredRoles,
        allInterviewers,
        roleAssignments: validAssignments
      });

      // Call create interview service through companyInterviewService
      await companyInterviewService.createInterview({
        candidate_id: candidateId,
        workflow_stage_id: workflowStageId,
        interview_type: interviewType as any, // Type assertion - backend expects specific enum
        interview_mode: 'MANUAL', // Default to MANUAL mode
        interview_template_id: templateId || undefined,
        required_roles: requiredRoles,
        scheduled_at: scheduledAt || undefined,
        interviewers: allInterviewers.length > 0 ? allInterviewers : undefined,
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
    // Just close - form will be reset by useEffect when reopened
    onClose();
  };

  const addRoleAssignment = () => {
    const newAssignment: RoleAssignment = {
      id: `assignment-${Date.now()}`,
      roleId: '',
      userIds: [],
    };
    setRoleAssignments(prev => [...prev, newAssignment]);
  };

  const updateRoleAssignment = (id: string, updated: RoleAssignment) => {
    setRoleAssignments(prev =>
      prev.map(assignment => (assignment.id === id ? updated : assignment))
    );
  };

  const removeRoleAssignment = (id: string) => {
    setRoleAssignments(prev => prev.filter(assignment => assignment.id !== id));
  };

  // Get IDs of roles that are already used
  const usedRoleIds = roleAssignments.map(a => a.roleId).filter(Boolean);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-5xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 sticky top-0 bg-white z-10">
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

          {/* Two Column Layout */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                    {stage.id === currentStageId && ` (${t('company.interviews.current', { defaultValue: 'Current' })})`}
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
              <div className="md:col-span-2">
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

            {/* Scheduled Date */}
            <div className="md:col-span-2">
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
          </div>

          {/* Role Assignments Section */}
          <div className="border-t pt-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                {t('company.interviews.form.roleAssignments', { defaultValue: 'Role Assignments' })} <span className="text-red-600">*</span>
              </h3>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={addRoleAssignment}
                disabled={loadingRoles || loadingUsers}
              >
                <Plus className="h-4 w-4 mr-1" />
                {t('company.interviews.form.addRole', { defaultValue: 'Add Role' })}
              </Button>
            </div>
            
            {loadingRoles || loadingUsers ? (
              <div className="flex items-center gap-2 text-gray-600">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-gray-400 border-t-transparent"></div>
                <span className="text-sm">{t('common.loading')}</span>
              </div>
            ) : availableRoles.length === 0 ? (
              <p className="text-sm text-gray-500">{t('company.interviews.form.noRoles')}</p>
            ) : (
              <div className="space-y-4">
                {roleAssignments.length === 0 ? (
                  <div className="text-center py-8 text-gray-500 border-2 border-dashed rounded-lg">
                    <p className="text-sm">
                      {t('company.interviews.form.noRolesAssigned', { defaultValue: 'No roles assigned yet' })}
                    </p>
                    <p className="text-xs mt-1">
                      {t('company.interviews.form.clickAddRole', { defaultValue: 'Click "Add Role" to start' })}
                    </p>
                  </div>
                ) : (
                  roleAssignments.map((assignment) => (
                    <RoleAssignmentSelector
                      key={assignment.id}
                      assignment={assignment}
                      availableRoles={availableRoles}
                      availableUsers={availableUsers}
                      onChange={(updated) => updateRoleAssignment(assignment.id, updated)}
                      onRemove={() => removeRoleAssignment(assignment.id)}
                      usedRoleIds={usedRoleIds.filter(id => id !== assignment.roleId)}
                    />
                  ))
                )}
              </div>
            )}
            
            {fieldErrors.roleAssignments && (
              <p className="mt-2 text-sm text-red-600">{fieldErrors.roleAssignments}</p>
            )}
            <p className="mt-2 text-xs text-gray-500">
              {t('company.interviews.form.roleAssignmentsHelp', { defaultValue: 'Assign at least one person to any role. You can leave roles empty and assign people later.' })}
            </p>
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
