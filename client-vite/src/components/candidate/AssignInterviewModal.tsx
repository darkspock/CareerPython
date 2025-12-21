import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { AlertCircle, Plus } from 'lucide-react';
import { companyInterviewService } from '../../services/companyInterviewService';
import { companyInterviewTemplateService, type InterviewTemplate } from '../../services/companyInterviewTemplateService';
import { CompanyUserService } from '../../services/companyUserService';
import { api } from '../../lib/api';
import { useCompanyId } from '../../hooks/useCompanyId';
import type { WorkflowStage } from '../../types/workflow';
import type { CompanyRole } from '../../types/company';
import type { CompanyUser } from '../../types/companyUser';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import LoadingSpinner from '@/components/common/LoadingSpinner';
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
  companyCandidateId: _companyCandidateId,
  currentStageId,
  currentWorkflowId: _currentWorkflowId,
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

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && handleClose()}>
      <DialogContent className="max-w-5xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{t('company.interviews.assignInterview')}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Global form error */}
          {formError && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{formError}</AlertDescription>
            </Alert>
          )}

          {/* Two Column Layout */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Workflow Stage */}
            <div className="space-y-2">
              <Label>
                {t('company.interviews.form.stage')} <span className="text-destructive">*</span>
              </Label>
              <Select value={workflowStageId} onValueChange={setWorkflowStageId}>
                <SelectTrigger className={fieldErrors.workflowStageId ? 'border-destructive' : ''}>
                  <SelectValue placeholder={t('company.interviews.form.selectStage')} />
                </SelectTrigger>
                <SelectContent>
                  {availableStages.map((stage) => (
                    <SelectItem key={stage.id} value={stage.id}>
                      {stage.name}
                      {stage.id === currentStageId && ` (${t('company.interviews.current', { defaultValue: 'Current' })})`}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {fieldErrors.workflowStageId && (
                <p className="text-sm text-destructive">{fieldErrors.workflowStageId}</p>
              )}
            </div>

            {/* Interview Type */}
            <div className="space-y-2">
              <Label>
                {t('company.interviews.form.type')} <span className="text-destructive">*</span>
              </Label>
              <Select value={interviewType} onValueChange={setInterviewType}>
                <SelectTrigger className={fieldErrors.interviewType ? 'border-destructive' : ''}>
                  <SelectValue placeholder={t('company.interviews.form.selectType')} />
                </SelectTrigger>
                <SelectContent>
                  {INTERVIEW_TYPES.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {t(`company.interviews.types.${type.value}`, { defaultValue: type.label })}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {fieldErrors.interviewType && (
                <p className="text-sm text-destructive">{fieldErrors.interviewType}</p>
              )}
            </div>

            {/* Template (Conditional) */}
            {interviewType && (
              <div className="md:col-span-2 space-y-2">
                <Label>
                  {t('company.interviews.form.template')}
                  {availableTemplates.length > 1 && <span className="text-destructive">*</span>}
                </Label>
                {loadingTemplates ? (
                  <LoadingSpinner size="sm" text={t('common.loading')} />
                ) : availableTemplates.length === 0 ? (
                  <p className="text-sm text-muted-foreground">
                    {t('company.interviews.form.noTemplates', { defaultValue: 'No templates available for this type' })}
                  </p>
                ) : availableTemplates.length === 1 ? (
                  <div className="px-3 py-2 bg-muted rounded-lg">
                    <p className="text-sm text-foreground">{availableTemplates[0].name}</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {t('company.interviews.form.autoSelected', { defaultValue: 'Automatically selected' })}
                    </p>
                  </div>
                ) : (
                  <>
                    <Select value={templateId} onValueChange={setTemplateId}>
                      <SelectTrigger className={fieldErrors.templateId ? 'border-destructive' : ''}>
                        <SelectValue placeholder={t('company.interviews.form.selectTemplate')} />
                      </SelectTrigger>
                      <SelectContent>
                        {availableTemplates.map((template) => (
                          <SelectItem key={template.id} value={template.id}>
                            {template.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    {fieldErrors.templateId && (
                      <p className="text-sm text-destructive">{fieldErrors.templateId}</p>
                    )}
                  </>
                )}
              </div>
            )}

            {/* Scheduled Date */}
            <div className="md:col-span-2 space-y-2">
              <Label>{t('company.interviews.form.scheduledDate')}</Label>
              <Input
                type="datetime-local"
                value={scheduledAt}
                onChange={(e) => setScheduledAt(e.target.value)}
                className={fieldErrors.scheduledAt ? 'border-destructive' : ''}
              />
              {fieldErrors.scheduledAt && (
                <p className="text-sm text-destructive">{fieldErrors.scheduledAt}</p>
              )}
              <p className="text-xs text-muted-foreground">
                {t('company.interviews.form.scheduledDateHelp', { defaultValue: 'Optional - leave empty to schedule later' })}
              </p>
            </div>
          </div>

          {/* Role Assignments Section */}
          <div className="border-t pt-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-foreground">
                {t('company.interviews.form.roleAssignments', { defaultValue: 'Role Assignments' })} <span className="text-destructive">*</span>
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
              <LoadingSpinner size="sm" text={t('common.loading')} />
            ) : availableRoles.length === 0 ? (
              <p className="text-sm text-muted-foreground">{t('company.interviews.form.noRoles')}</p>
            ) : (
              <div className="space-y-4">
                {roleAssignments.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground border-2 border-dashed rounded-lg">
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
              <p className="mt-2 text-sm text-destructive">{fieldErrors.roleAssignments}</p>
            )}
            <p className="mt-2 text-xs text-muted-foreground">
              {t('company.interviews.form.roleAssignmentsHelp', { defaultValue: 'Assign at least one person to any role. You can leave roles empty and assign people later.' })}
            </p>
          </div>

          <DialogFooter>
            <Button type="button" variant="ghost" onClick={handleClose} disabled={submitting}>
              {t('common.cancel')}
            </Button>
            <Button type="submit" disabled={submitting || loadingTemplates || loadingRoles || loadingUsers}>
              {submitting && <LoadingSpinner size="sm" color="white" className="mr-2" />}
              {t('company.interviews.assignInterview')}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
