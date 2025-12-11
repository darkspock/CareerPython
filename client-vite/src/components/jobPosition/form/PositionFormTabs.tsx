/**
 * PositionFormTabs Component
 * Multi-tab form for creating/editing job positions with publishing flow
 */
import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, Lock, Info, Plus, Trash2, ChevronUp, ChevronDown, Pencil, Eye, EyeOff } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { WysiwygEditor } from '@/components/common';
import { StatusBadge, LockedFieldIndicator } from '../publishing';
import { SimpleFieldConfigEditor } from './SimpleFieldConfigEditor';
import { KillerQuestionsTab } from './KillerQuestionsTab';
import type { FieldType } from '@/types/workflow';

import type {
  Position,
  CreatePositionRequest,
  UpdatePositionRequest,
  JobPositionWorkflow,
  CustomFieldDefinition,
  LanguageRequirement,
} from '@/types/position';

import {
  JobPositionStatus,
  EmploymentType,
  ExperienceLevel,
  WorkLocationType,
  SalaryPeriod,
  isFieldLocked,
  getEmploymentTypeLabel,
  getExperienceLevelLabel,
  getWorkLocationTypeLabel,
  getSalaryPeriodLabel,
  LANGUAGE_OPTIONS,
} from '@/types/position';

interface PositionFormTabsProps {
  mode: 'create' | 'edit';
  position?: Position | null;
  workflow?: JobPositionWorkflow | null;
  onSave: (data: CreatePositionRequest | UpdatePositionRequest) => Promise<void>;
  isLoading?: boolean;
  canEditBudget?: boolean;
}

export function PositionFormTabs({
  mode,
  position,
  workflow,
  onSave,
  isLoading = false,
  canEditBudget = true,
}: PositionFormTabsProps) {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('basic');
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const status = position?.status || JobPositionStatus.DRAFT;

  // Form state
  const [formData, setFormData] = useState<CreatePositionRequest | UpdatePositionRequest>({
    title: '',
    description: '',
    job_category: 'Other',
    visibility: 'hidden',
    // Publishing flow fields
    employment_type: undefined,
    experience_level: undefined,
    work_location_type: undefined,
    office_locations: [],
    remote_restrictions: undefined,
    number_of_openings: 1,
    requisition_id: undefined,
    // Salary
    salary_currency: 'USD',
    salary_min: undefined,
    salary_max: undefined,
    salary_period: undefined,
    show_salary: false,
    budget_max: undefined,
    // Skills & Languages
    skills: [],
    languages: [],
    // Team
    hiring_manager_id: undefined,
    recruiter_id: undefined,
    // Custom fields
    custom_fields_values: {},
    custom_fields_config: [],
    // Screening
    screening_template_id: undefined,
    // Killer questions
    killer_questions: [],
    // Dates
    application_deadline: undefined,
    open_at: undefined,
  });

  // Skills input state
  const [skillInput, setSkillInput] = useState('');

  // Language input state
  const [languageInput, setLanguageInput] = useState<LanguageRequirement>({
    language: '',
    level: 'B1',
  });

  // Office location input
  const [locationInput, setLocationInput] = useState('');

  // Track if form has been initialized to prevent re-initialization on position reference changes
  const initializedRef = useRef(false);

  // Initialize form data from position (only once)
  useEffect(() => {
    if (position && !initializedRef.current) {
      initializedRef.current = true;
      setFormData({
        title: position.title || '',
        description: position.description || '',
        job_category: position.job_category || 'Other',
        visibility: position.visibility || 'hidden',
        employment_type: position.employment_type || undefined,
        experience_level: position.experience_level || undefined,
        work_location_type: position.work_location_type || undefined,
        office_locations: position.office_locations || [],
        remote_restrictions: position.remote_restrictions || undefined,
        number_of_openings: position.number_of_openings || 1,
        requisition_id: position.requisition_id || undefined,
        salary_currency: position.salary_currency || 'USD',
        salary_min: position.salary_min || undefined,
        salary_max: position.salary_max || undefined,
        salary_period: position.salary_period || undefined,
        show_salary: position.show_salary || false,
        budget_max: position.budget_max || undefined,
        skills: position.skills || [],
        languages: position.languages || [],
        hiring_manager_id: position.hiring_manager_id || undefined,
        recruiter_id: position.recruiter_id || undefined,
        custom_fields_values: position.custom_fields_values || {},
        custom_fields_config: position.custom_fields_config || [],
        killer_questions: position.killer_questions || [],
        application_deadline: position.application_deadline || undefined,
        open_at: position.open_at || undefined,
        department_id: position.department_id || undefined,
        candidate_pipeline_id: position.candidate_pipeline_id || undefined,
        screening_template_id: position.screening_template_id || undefined,
        job_position_workflow_id: position.job_position_workflow_id || undefined,
        stage_id: position.stage_id || undefined,
        phase_workflows: position.phase_workflows || {},
      });
    }
  }, [position]);

  const updateField = <K extends keyof typeof formData>(
    field: K,
    value: (typeof formData)[K]
  ) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const isLocked = (fieldName: string) => isFieldLocked(status, fieldName);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!formData.title?.trim()) {
      setError('Title is required');
      setActiveTab('basic');
      return;
    }

    // Validate salary range
    if (formData.salary_min && formData.salary_max) {
      if (formData.salary_min > formData.salary_max) {
        setError('Minimum salary cannot be greater than maximum salary');
        setActiveTab('compensation');
        return;
      }
    }

    // Validate budget vs salary
    if (formData.budget_max && formData.salary_max) {
      if (formData.salary_max > formData.budget_max) {
        setError('Maximum salary cannot exceed budget');
        setActiveTab('compensation');
        return;
      }
    }

    try {
      setSaving(true);
      await onSave(formData);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to save position';
      setError(errorMessage);
    } finally {
      setSaving(false);
    }
  };

  const addSkill = () => {
    const skill = skillInput.trim();
    if (skill && !formData.skills?.includes(skill)) {
      updateField('skills', [...(formData.skills || []), skill]);
    }
    setSkillInput('');
  };

  const removeSkill = (skill: string) => {
    updateField('skills', (formData.skills || []).filter((s) => s !== skill));
  };

  const addLanguage = () => {
    if (languageInput.language) {
      const existing = formData.languages || [];
      const exists = existing.some((l) => l.language === languageInput.language);
      if (!exists) {
        updateField('languages', [...existing, { ...languageInput }]);
      }
      setLanguageInput({ language: '', level: 'B1' });
    }
  };

  const removeLanguage = (language: string) => {
    updateField(
      'languages',
      (formData.languages || []).filter((l) => l.language !== language)
    );
  };

  const addLocation = () => {
    const loc = locationInput.trim();
    if (loc && !formData.office_locations?.includes(loc)) {
      updateField('office_locations', [...(formData.office_locations || []), loc]);
    }
    setLocationInput('');
  };

  const removeLocation = (location: string) => {
    updateField(
      'office_locations',
      (formData.office_locations || []).filter((l) => l !== location)
    );
  };

  // Custom fields state for inline editor
  const [isAddingField, setIsAddingField] = useState(false);
  const [editingFieldIndex, setEditingFieldIndex] = useState<number | null>(null);
  const [fieldFormData, setFieldFormData] = useState({
    field_name: '',
    field_key: '',
    field_type: 'TEXT' as FieldType,
    field_config: {} as Record<string, any>,
    is_required: false,
  });

  const FIELD_TYPES: FieldType[] = [
    'TEXT', 'TEXTAREA', 'NUMBER', 'CURRENCY', 'DATE',
    'DROPDOWN', 'MULTI_SELECT', 'RADIO', 'CHECKBOX',
    'FILE', 'URL', 'EMAIL', 'PHONE'
  ];

  const getFieldTypeLabel = (type: FieldType): string => {
    const labels: Record<FieldType, string> = {
      TEXT: 'Text',
      TEXTAREA: 'Text Area',
      NUMBER: 'Number',
      CURRENCY: 'Currency',
      DATE: 'Date',
      DROPDOWN: 'Dropdown',
      MULTI_SELECT: 'Multi-Select',
      RADIO: 'Radio Buttons',
      CHECKBOX: 'Checkbox',
      FILE: 'File Upload',
      URL: 'URL',
      EMAIL: 'Email',
      PHONE: 'Phone',
    };
    return labels[type] || type;
  };

  const generateFieldKey = (): string => {
    // Generate a unique UUID-based key
    return `field_${crypto.randomUUID().replace(/-/g, '').substring(0, 12)}`;
  };

  const handleFieldNameChange = (value: string) => {
    setFieldFormData(prev => ({
      ...prev,
      field_name: value,
      // Don't auto-generate field_key from name anymore - will be generated on save
    }));
  };

  const handleAddFieldClick = () => {
    setIsAddingField(true);
    setEditingFieldIndex(null);
    setFieldFormData({
      field_name: '',
      field_key: '',
      field_type: 'TEXT',
      field_config: {},
      is_required: false,
    });
  };

  const handleEditField = (index: number) => {
    const field = formData.custom_fields_config?.[index];
    if (!field) return;

    setEditingFieldIndex(index);
    setIsAddingField(false);

    // Merge options into field_config for FieldConfigEditor compatibility
    const fieldConfig = { ...(field.validation_rules || {}) };
    if (field.options && field.options.length > 0) {
      fieldConfig.options = field.options;
    }

    setFieldFormData({
      field_name: field.label,
      field_key: field.field_key,
      field_type: (field.field_type === 'SELECT' ? 'DROPDOWN' : field.field_type === 'MULTISELECT' ? 'MULTI_SELECT' : field.field_type) as FieldType,
      field_config: fieldConfig,
      is_required: field.is_required,
    });
  };

  const handleCancelFieldEdit = () => {
    setIsAddingField(false);
    setEditingFieldIndex(null);
    setFieldFormData({
      field_name: '',
      field_key: '',
      field_type: 'TEXT',
      field_config: {},
      is_required: false,
    });
  };

  const handleSaveField = () => {
    if (!fieldFormData.field_name.trim()) {
      setError('Field name is required');
      return;
    }

    // Use existing key or generate a new UUID-based key
    const fieldKey = fieldFormData.field_key.trim() || generateFieldKey();
    const currentConfig = formData.custom_fields_config || [];

    // Map workflow field types to position field types
    const mapFieldType = (type: FieldType): CustomFieldDefinition['field_type'] => {
      if (type === 'DROPDOWN') return 'SELECT';
      if (type === 'MULTI_SELECT') return 'MULTISELECT';
      if (['TEXT', 'NUMBER', 'DATE', 'BOOLEAN', 'URL'].includes(type)) {
        return type as CustomFieldDefinition['field_type'];
      }
      return 'TEXT';
    };

    const newField: CustomFieldDefinition = {
      field_key: fieldKey,
      label: fieldFormData.field_name,
      field_type: mapFieldType(fieldFormData.field_type),
      options: fieldFormData.field_config.options || null,
      is_required: fieldFormData.is_required,
      candidate_visible: true,
      validation_rules: Object.keys(fieldFormData.field_config).length > 0 ? fieldFormData.field_config : null,
      sort_order: isAddingField ? currentConfig.length : (editingFieldIndex ?? 0),
      is_active: true,
    };

    if (isAddingField) {
      // Check for duplicate key
      if (currentConfig.some(f => f.field_key === fieldKey)) {
        setError(`Field with key "${fieldKey}" already exists`);
        return;
      }
      updateField('custom_fields_config', [...currentConfig, newField]);
    } else if (editingFieldIndex !== null) {
      const updatedConfig = [...currentConfig];
      updatedConfig[editingFieldIndex] = { ...newField, field_key: currentConfig[editingFieldIndex].field_key };
      updateField('custom_fields_config', updatedConfig);
    }

    handleCancelFieldEdit();
    setError(null);
  };

  const handleDeleteField = (index: number) => {
    const currentConfig = formData.custom_fields_config || [];
    const fieldKey = currentConfig[index]?.field_key;

    updateField('custom_fields_config', currentConfig.filter((_, i) => i !== index));

    // Also remove the value
    if (fieldKey) {
      const currentValues = { ...formData.custom_fields_values };
      delete currentValues[fieldKey];
      updateField('custom_fields_values', currentValues);
    }
  };

  const handleMoveField = (index: number, direction: 'up' | 'down') => {
    const currentConfig = [...(formData.custom_fields_config || [])];
    const newIndex = direction === 'up' ? index - 1 : index + 1;

    if (newIndex < 0 || newIndex >= currentConfig.length) return;

    [currentConfig[index], currentConfig[newIndex]] = [currentConfig[newIndex], currentConfig[index]];
    currentConfig.forEach((f, i) => f.sort_order = i);
    updateField('custom_fields_config', currentConfig);
  };

  const toggleFieldActive = (index: number) => {
    const currentConfig = [...(formData.custom_fields_config || [])];
    currentConfig[index] = { ...currentConfig[index], is_active: !currentConfig[index].is_active };
    updateField('custom_fields_config', currentConfig);
  };

  const renderLockIcon = (fieldName: string) => {
    if (!isLocked(fieldName)) return null;
    return (
      <LockedFieldIndicator
        status={status}
        fieldName={fieldName}
        size="sm"
        className="ml-1"
      />
    );
  };

  return (
    <div className="space-y-6">
      {/* Header with Status */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            type="button"
            variant="ghost"
            onClick={() => navigate(-1)}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {mode === 'create' ? 'Create Job Position' : 'Edit Job Position'}
            </h1>
            {workflow && (
              <p className="text-sm text-muted-foreground">
                Workflow: {workflow.name}
              </p>
            )}
          </div>
        </div>
        {mode === 'edit' && position && (
          <StatusBadge status={status} size="lg" showIcon />
        )}
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Status Banner (for edit mode) */}
      {mode === 'edit' && position && status !== JobPositionStatus.DRAFT && (
        <Alert className="border-blue-200 bg-blue-50">
          <Info className="h-4 w-4" />
          <AlertDescription className="text-blue-800">
            Some fields may be locked based on the current status. Fields marked with{' '}
            <Lock className="inline h-3 w-3" /> cannot be edited.
          </AlertDescription>
        </Alert>
      )}

      <form onSubmit={handleSubmit}>
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
          <TabsList className="grid w-full grid-cols-7">
            <TabsTrigger value="basic">Basic Info</TabsTrigger>
            <TabsTrigger value="details">Job Details</TabsTrigger>
            <TabsTrigger value="compensation">Compensation</TabsTrigger>
            <TabsTrigger value="pipeline">Pipeline</TabsTrigger>
            <TabsTrigger value="killer">Killer Questions</TabsTrigger>
            <TabsTrigger value="custom">Custom Fields</TabsTrigger>
            <TabsTrigger value="team">Team</TabsTrigger>
          </TabsList>

          {/* Tab 1: Basic Info */}
          <TabsContent value="basic">
            <Card>
              <CardHeader>
                <CardTitle>Basic Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Title */}
                  <div className="md:col-span-2 space-y-2">
                    <Label htmlFor="title">
                      Job Title <span className="text-red-500">*</span>
                      {renderLockIcon('title')}
                    </Label>
                    <Input
                      id="title"
                      value={formData.title || ''}
                      onChange={(e) => updateField('title', e.target.value)}
                      placeholder="e.g., Senior Software Engineer"
                      disabled={isLocked('title')}
                      required
                    />
                  </div>

                  {/* Requisition ID */}
                  <div className="space-y-2">
                    <Label htmlFor="requisition_id">
                      Requisition ID
                      {renderLockIcon('requisition_id')}
                    </Label>
                    <Input
                      id="requisition_id"
                      value={formData.requisition_id || ''}
                      onChange={(e) => updateField('requisition_id', e.target.value || undefined)}
                      placeholder="e.g., REQ-2024-001"
                      disabled={isLocked('requisition_id')}
                    />
                    <p className="text-xs text-muted-foreground">
                      Internal tracking code
                    </p>
                  </div>

                  {/* Job Category */}
                  <div className="space-y-2">
                    <Label htmlFor="job_category">
                      Job Category
                      {renderLockIcon('job_category')}
                    </Label>
                    <Select
                      value={formData.job_category || 'Other'}
                      onValueChange={(value) => updateField('job_category', value)}
                      disabled={isLocked('job_category')}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select category" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Technology">Technology</SelectItem>
                        <SelectItem value="Operations">Operations</SelectItem>
                        <SelectItem value="Sales">Sales</SelectItem>
                        <SelectItem value="Marketing">Marketing</SelectItem>
                        <SelectItem value="Administration">Administration</SelectItem>
                        <SelectItem value="Human Resources">Human Resources</SelectItem>
                        <SelectItem value="Finance">Finance</SelectItem>
                        <SelectItem value="Customer Service">Customer Service</SelectItem>
                        <SelectItem value="Other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Description */}
                  <div className="md:col-span-2 space-y-2">
                    <Label htmlFor="description">
                      Job Description
                      {renderLockIcon('description')}
                    </Label>
                    <div className="border rounded-lg overflow-hidden">
                      <WysiwygEditor
                        value={formData.description || ''}
                        onChange={(content) => updateField('description', content)}
                        placeholder="Describe the role, responsibilities, and what you're looking for..."
                        height={350}
                        className="w-full"
                      />
                    </div>
                  </div>

                  {/* Visibility */}
                  <div className="md:col-span-2 space-y-2">
                    <Label>
                      Visibility
                      {renderLockIcon('visibility')}
                    </Label>
                    <div className="flex flex-wrap gap-6">
                      {(['hidden', 'internal', 'public'] as const).map((vis) => (
                        <div key={vis} className="flex items-center gap-2">
                          <input
                            type="radio"
                            id={`visibility-${vis}`}
                            name="visibility"
                            value={vis}
                            checked={formData.visibility === vis}
                            onChange={() => updateField('visibility', vis)}
                            disabled={isLocked('visibility')}
                            className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                          />
                          <Label htmlFor={`visibility-${vis}`} className="font-normal capitalize">
                            {vis === 'hidden' && 'Hidden - Only accessible by direct link'}
                            {vis === 'internal' && 'Internal - Visible to company users'}
                            {vis === 'public' && 'Public - Visible on job board'}
                          </Label>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Tab 2: Job Details */}
          <TabsContent value="details">
            <Card>
              <CardHeader>
                <CardTitle>Job Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Employment Type */}
                  <div className="space-y-2">
                    <Label htmlFor="employment_type">
                      Employment Type
                      {renderLockIcon('employment_type')}
                    </Label>
                    <Select
                      value={formData.employment_type || ''}
                      onValueChange={(value) =>
                        updateField('employment_type', value as EmploymentType || undefined)
                      }
                      disabled={isLocked('employment_type')}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select type" />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.values(EmploymentType).map((type) => (
                          <SelectItem key={type} value={type}>
                            {getEmploymentTypeLabel(type)}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Experience Level */}
                  <div className="space-y-2">
                    <Label htmlFor="experience_level">
                      Experience Level
                      {renderLockIcon('experience_level')}
                    </Label>
                    <Select
                      value={formData.experience_level || ''}
                      onValueChange={(value) =>
                        updateField('experience_level', value as ExperienceLevel || undefined)
                      }
                      disabled={isLocked('experience_level')}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select level" />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.values(ExperienceLevel).map((level) => (
                          <SelectItem key={level} value={level}>
                            {getExperienceLevelLabel(level)}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Work Location Type */}
                  <div className="space-y-2">
                    <Label htmlFor="work_location_type">
                      Work Location
                      {renderLockIcon('work_location_type')}
                    </Label>
                    <Select
                      value={formData.work_location_type || ''}
                      onValueChange={(value) =>
                        updateField('work_location_type', value as WorkLocationType || undefined)
                      }
                      disabled={isLocked('work_location_type')}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select location type" />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.values(WorkLocationType).map((type) => (
                          <SelectItem key={type} value={type}>
                            {getWorkLocationTypeLabel(type)}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Number of Openings */}
                  <div className="space-y-2">
                    <Label htmlFor="number_of_openings">
                      Number of Openings
                      {renderLockIcon('number_of_openings')}
                    </Label>
                    <Input
                      id="number_of_openings"
                      type="number"
                      min={1}
                      value={formData.number_of_openings || 1}
                      onChange={(e) =>
                        updateField('number_of_openings', parseInt(e.target.value) || 1)
                      }
                      disabled={isLocked('number_of_openings')}
                    />
                  </div>

                  {/* Application Deadline */}
                  <div className="space-y-2">
                    <Label htmlFor="application_deadline">
                      Application Deadline
                      {renderLockIcon('application_deadline')}
                    </Label>
                    <Input
                      id="application_deadline"
                      type="date"
                      value={formData.application_deadline || ''}
                      onChange={(e) =>
                        updateField('application_deadline', e.target.value || undefined)
                      }
                      disabled={isLocked('application_deadline')}
                    />
                  </div>
                </div>

                {/* Office Locations (show if on-site or hybrid) */}
                {(formData.work_location_type === WorkLocationType.ON_SITE ||
                  formData.work_location_type === WorkLocationType.HYBRID) && (
                  <div className="space-y-2">
                    <Label>
                      Office Locations
                      {renderLockIcon('office_locations')}
                    </Label>
                    <div className="flex gap-2">
                      <Input
                        value={locationInput}
                        onChange={(e) => setLocationInput(e.target.value)}
                        placeholder="e.g., New York, NY"
                        disabled={isLocked('office_locations')}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            e.preventDefault();
                            addLocation();
                          }
                        }}
                      />
                      <Button
                        type="button"
                        variant="outline"
                        onClick={addLocation}
                        disabled={isLocked('office_locations')}
                      >
                        Add
                      </Button>
                    </div>
                    {formData.office_locations && formData.office_locations.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-2">
                        {formData.office_locations.map((loc) => (
                          <span
                            key={loc}
                            className="inline-flex items-center gap-1 px-2 py-1 bg-gray-100 rounded-md text-sm"
                          >
                            {loc}
                            {!isLocked('office_locations') && (
                              <button
                                type="button"
                                onClick={() => removeLocation(loc)}
                                className="text-gray-500 hover:text-red-500"
                              >
                                &times;
                              </button>
                            )}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* Remote Restrictions (show if hybrid or remote) */}
                {(formData.work_location_type === WorkLocationType.HYBRID ||
                  formData.work_location_type === WorkLocationType.REMOTE) && (
                  <div className="space-y-2">
                    <Label htmlFor="remote_restrictions">
                      Remote Restrictions
                      {renderLockIcon('remote_restrictions')}
                    </Label>
                    <Input
                      id="remote_restrictions"
                      value={formData.remote_restrictions || ''}
                      onChange={(e) =>
                        updateField('remote_restrictions', e.target.value || undefined)
                      }
                      placeholder="e.g., US time zones only, Must be able to work EST hours"
                      disabled={isLocked('remote_restrictions')}
                    />
                  </div>
                )}

                {/* Skills */}
                <div className="space-y-2">
                  <Label>
                    Skills / Tags
                    {renderLockIcon('skills')}
                  </Label>
                  <div className="flex gap-2">
                    <Input
                      value={skillInput}
                      onChange={(e) => setSkillInput(e.target.value)}
                      placeholder="Type a skill and press Enter"
                      disabled={isLocked('skills')}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          addSkill();
                        }
                      }}
                    />
                    <Button
                      type="button"
                      variant="outline"
                      onClick={addSkill}
                      disabled={isLocked('skills')}
                    >
                      Add
                    </Button>
                  </div>
                  {formData.skills && formData.skills.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-2">
                      {formData.skills.map((skill) => (
                        <span
                          key={skill}
                          className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 rounded-md text-sm"
                        >
                          {skill}
                          {!isLocked('skills') && (
                            <button
                              type="button"
                              onClick={() => removeSkill(skill)}
                              className="text-blue-600 hover:text-red-500"
                            >
                              &times;
                            </button>
                          )}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Languages */}
                <div className="space-y-2">
                  <Label>
                    Language Requirements
                    {renderLockIcon('languages')}
                  </Label>
                  <div className="flex gap-2">
                    <Select
                      value={languageInput.language}
                      onValueChange={(value) =>
                        setLanguageInput((prev) => ({ ...prev, language: value }))
                      }
                      disabled={isLocked('languages')}
                    >
                      <SelectTrigger className="w-40">
                        <SelectValue placeholder="Language" />
                      </SelectTrigger>
                      <SelectContent>
                        {LANGUAGE_OPTIONS.map((lang) => (
                          <SelectItem key={lang.value} value={lang.value}>
                            {lang.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <Select
                      value={languageInput.level}
                      onValueChange={(value) =>
                        setLanguageInput((prev) => ({
                          ...prev,
                          level: value as LanguageRequirement['level'],
                        }))
                      }
                      disabled={isLocked('languages')}
                    >
                      <SelectTrigger className="w-32">
                        <SelectValue placeholder="Level" />
                      </SelectTrigger>
                      <SelectContent>
                        {['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'Native'].map((level) => (
                          <SelectItem key={level} value={level}>
                            {level}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <Button
                      type="button"
                      variant="outline"
                      onClick={addLanguage}
                      disabled={isLocked('languages') || !languageInput.language}
                    >
                      Add
                    </Button>
                  </div>
                  {formData.languages && formData.languages.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-2">
                      {formData.languages.map((lang) => (
                        <span
                          key={lang.language}
                          className="inline-flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-800 rounded-md text-sm"
                        >
                          {LANGUAGE_OPTIONS.find((l) => l.value === lang.language)?.label ||
                            lang.language}{' '}
                          ({lang.level})
                          {!isLocked('languages') && (
                            <button
                              type="button"
                              onClick={() => removeLanguage(lang.language)}
                              className="text-purple-600 hover:text-red-500"
                            >
                              &times;
                            </button>
                          )}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Tab 3: Compensation */}
          <TabsContent value="compensation">
            <Card>
              <CardHeader>
                <CardTitle>Compensation</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Salary Section */}
                <div className="space-y-4">
                  <h3 className="text-sm font-medium text-gray-700">Salary Range</h3>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    {/* Currency */}
                    <div className="space-y-2">
                      <Label htmlFor="salary_currency">
                        Currency
                        {renderLockIcon('salary_currency')}
                      </Label>
                      <Select
                        value={formData.salary_currency || 'USD'}
                        onValueChange={(value) => updateField('salary_currency', value)}
                        disabled={isLocked('salary_currency')}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="USD">USD ($)</SelectItem>
                          <SelectItem value="EUR">EUR (€)</SelectItem>
                          <SelectItem value="GBP">GBP (£)</SelectItem>
                          <SelectItem value="CAD">CAD ($)</SelectItem>
                          <SelectItem value="AUD">AUD ($)</SelectItem>
                          <SelectItem value="MXN">MXN ($)</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    {/* Min Salary */}
                    <div className="space-y-2">
                      <Label htmlFor="salary_min">
                        Minimum
                        {renderLockIcon('salary_min')}
                      </Label>
                      <Input
                        id="salary_min"
                        type="number"
                        min={0}
                        value={formData.salary_min || ''}
                        onChange={(e) =>
                          updateField('salary_min', e.target.value ? Number(e.target.value) : undefined)
                        }
                        placeholder="0"
                        disabled={isLocked('salary_min')}
                      />
                    </div>

                    {/* Max Salary */}
                    <div className="space-y-2">
                      <Label htmlFor="salary_max">
                        Maximum
                        {renderLockIcon('salary_max')}
                      </Label>
                      <Input
                        id="salary_max"
                        type="number"
                        min={0}
                        value={formData.salary_max || ''}
                        onChange={(e) =>
                          updateField('salary_max', e.target.value ? Number(e.target.value) : undefined)
                        }
                        placeholder="0"
                        disabled={isLocked('salary_max')}
                      />
                    </div>

                    {/* Period */}
                    <div className="space-y-2">
                      <Label htmlFor="salary_period">
                        Period
                        {renderLockIcon('salary_period')}
                      </Label>
                      <Select
                        value={formData.salary_period || ''}
                        onValueChange={(value) =>
                          updateField('salary_period', value as SalaryPeriod || undefined)
                        }
                        disabled={isLocked('salary_period')}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select period" />
                        </SelectTrigger>
                        <SelectContent>
                          {Object.values(SalaryPeriod).map((period) => (
                            <SelectItem key={period} value={period}>
                              {getSalaryPeriodLabel(period)}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  {/* Show Salary to Candidates */}
                  <div className="flex items-center gap-2">
                    <Checkbox
                      id="show_salary"
                      checked={formData.show_salary || false}
                      onCheckedChange={(checked) => updateField('show_salary', checked === true)}
                      disabled={isLocked('show_salary')}
                    />
                    <Label htmlFor="show_salary" className="font-normal">
                      Show salary range to candidates
                    </Label>
                  </div>
                </div>

                {/* Budget Section (only if user has permission) */}
                {canEditBudget && (
                  <div className="space-y-4 pt-4 border-t">
                    <div className="flex items-center gap-2">
                      <h3 className="text-sm font-medium text-gray-700">Internal Budget</h3>
                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger>
                            <Info className="h-4 w-4 text-gray-400" />
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>This value is never shown to candidates</p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {/* Budget Max */}
                      <div className="space-y-2">
                        <Label htmlFor="budget_max">
                          Maximum Budget
                          {renderLockIcon('budget_max')}
                        </Label>
                        <Input
                          id="budget_max"
                          type="number"
                          min={0}
                          value={formData.budget_max || ''}
                          onChange={(e) =>
                            updateField('budget_max', e.target.value ? Number(e.target.value) : undefined)
                          }
                          placeholder="0"
                          disabled={isLocked('budget_max')}
                        />
                        <p className="text-xs text-muted-foreground">
                          This will never be shown to candidates
                        </p>
                      </div>

                      {/* Approved Budget (read-only if approved) */}
                      {position?.approved_budget_max && (
                        <div className="space-y-2">
                          <Label>Approved Budget</Label>
                          <Input
                            value={position.approved_budget_max}
                            disabled
                            className="bg-green-50"
                          />
                          <p className="text-xs text-green-600">
                            Approved on{' '}
                            {position.approved_at
                              ? new Date(position.approved_at).toLocaleDateString()
                              : 'N/A'}
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Validation warning */}
                    {formData.salary_max && formData.budget_max && formData.salary_max > formData.budget_max && (
                      <Alert variant="destructive">
                        <AlertDescription>
                          Maximum salary cannot exceed the budget. Please adjust the salary or budget.
                        </AlertDescription>
                      </Alert>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Tab 4: Pipeline & Screening */}
          <TabsContent value="pipeline">
            <Card>
              <CardHeader>
                <CardTitle>Pipeline & Screening</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Alert>
                  <Info className="h-4 w-4" />
                  <AlertDescription>
                    Pipeline and screening configuration is managed through the workflow settings.
                    Select a workflow when creating the position to configure the candidate pipeline.
                  </AlertDescription>
                </Alert>

                {workflow && (
                  <div className="space-y-4">
                    <div>
                      <Label className="text-sm font-medium">Current Workflow</Label>
                      <p className="text-gray-700">{workflow.name}</p>
                    </div>

                    {workflow.stages && workflow.stages.length > 0 && (
                      <div>
                        <Label className="text-sm font-medium">Stages</Label>
                        <div className="flex flex-wrap gap-2 mt-2">
                          {workflow.stages.map((stage, index) => (
                            <span
                              key={stage.id}
                              className="inline-flex items-center gap-1 px-2 py-1 rounded-md text-sm"
                              style={{
                                backgroundColor: stage.background_color || '#e5e7eb',
                                color: stage.text_color || '#374151',
                              }}
                            >
                              {index + 1}. {stage.name}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {!workflow && (
                  <p className="text-muted-foreground">
                    No workflow assigned to this position.
                  </p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Tab 5: Killer Questions */}
          <TabsContent value="killer">
            <KillerQuestionsTab
              screeningTemplateId={formData.screening_template_id}
              onTemplateChange={(templateId) => updateField('screening_template_id', templateId || undefined)}
              questions={formData.killer_questions || []}
              onQuestionsChange={(questions) => updateField('killer_questions', questions)}
              disabled={isLocked('killer_questions')}
            />
          </TabsContent>

          {/* Tab 6: Custom Fields */}
          <TabsContent value="custom">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>Custom Fields</CardTitle>
                {!isLocked('custom_fields_config') && !isAddingField && editingFieldIndex === null && (
                  <Button type="button" variant="outline" size="sm" onClick={handleAddFieldClick}>
                    <Plus className="w-4 h-4 mr-2" />
                    Add Field
                  </Button>
                )}
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Add/Edit Field Form */}
                {(isAddingField || editingFieldIndex !== null) && (
                  <div className="p-4 border rounded-lg bg-gray-50 space-y-4">
                    <h4 className="font-semibold">
                      {isAddingField ? 'Add New Field' : 'Edit Field'}
                    </h4>

                    <div className="space-y-4">
                      <div>
                        <Label>Field Name *</Label>
                        <Input
                          value={fieldFormData.field_name}
                          onChange={(e) => handleFieldNameChange(e.target.value)}
                          placeholder="e.g., Expected Salary"
                        />
                      </div>

                      {/* Hidden field key - auto-generated from field name */}
                      <input
                        type="hidden"
                        value={fieldFormData.field_key}
                        onChange={(e) => setFieldFormData(prev => ({ ...prev, field_key: e.target.value }))}
                      />

                      <div>
                        <Label>Field Type *</Label>
                        <select
                          value={fieldFormData.field_type}
                          onChange={(e) => setFieldFormData(prev => ({
                            ...prev,
                            field_type: e.target.value as FieldType,
                            field_config: {}
                          }))}
                          className="w-full px-3 py-2 border rounded"
                        >
                          {FIELD_TYPES.map(type => (
                            <option key={type} value={type}>
                              {getFieldTypeLabel(type)}
                            </option>
                          ))}
                        </select>
                      </div>

                      {/* Field Configuration Editor - for options, validation, etc. */}
                      <SimpleFieldConfigEditor
                        fieldType={fieldFormData.field_type}
                        config={fieldFormData.field_config}
                        onChange={(newConfig) => setFieldFormData(prev => ({ ...prev, field_config: newConfig }))}
                      />

                      <div className="flex items-center gap-2">
                        <input
                          type="checkbox"
                          id="field_required"
                          checked={fieldFormData.is_required}
                          onChange={(e) => setFieldFormData(prev => ({ ...prev, is_required: e.target.checked }))}
                          className="rounded"
                        />
                        <Label htmlFor="field_required" className="cursor-pointer">Required field</Label>
                      </div>

                      <div className="flex gap-2">
                        <Button
                          type="button"
                          onClick={handleSaveField}
                          disabled={!fieldFormData.field_name.trim()}
                          size="sm"
                        >
                          Save
                        </Button>
                        <Button type="button" variant="outline" size="sm" onClick={handleCancelFieldEdit}>
                          Cancel
                        </Button>
                      </div>
                    </div>
                  </div>
                )}

                {/* Fields List */}
                <div className="space-y-2">
                  {(!formData.custom_fields_config || formData.custom_fields_config.length === 0) ? (
                    <div className="p-8 text-center text-muted-foreground border-2 border-dashed rounded-lg">
                      <p>No custom fields configured.</p>
                      <p className="text-sm mt-1">Click "Add Field" to create one.</p>
                    </div>
                  ) : (
                    formData.custom_fields_config
                      .sort((a, b) => a.sort_order - b.sort_order)
                      .map((field, index) => (
                        <div
                          key={field.field_key}
                          className={`flex items-center justify-between p-4 border rounded-lg ${
                            !field.is_active ? 'opacity-50 bg-muted' : 'hover:bg-muted/50'
                          }`}
                        >
                          <div className="flex-1">
                            <div className="font-medium">{field.label}</div>
                            <div className="text-sm text-muted-foreground">
                              {field.field_type}
                              {field.is_required && <span className="ml-2 text-red-600">Required</span>}
                            </div>
                            {/* Show options - check both field.options and field.validation_rules.options */}
                            {(() => {
                              const options = field.options || (field.validation_rules as Record<string, any>)?.options;
                              if (!options || !Array.isArray(options) || options.length === 0) return null;
                              const optionLabels = (options as any[]).map((opt: any) => {
                                if (typeof opt === 'string') return opt;
                                return String(opt);
                              }).filter(Boolean);
                              if (optionLabels.length === 0) return null;
                              return (
                                <div className="text-xs text-muted-foreground mt-1">
                                  Options: {optionLabels.join(' • ')}
                                </div>
                              );
                            })()}
                          </div>

                          {!isLocked('custom_fields_config') && (
                            <div className="flex gap-1">
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={() => handleMoveField(index, 'up')}
                                disabled={index === 0}
                              >
                                <ChevronUp className="w-4 h-4" />
                              </Button>
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={() => handleMoveField(index, 'down')}
                                disabled={index === (formData.custom_fields_config?.length ?? 0) - 1}
                              >
                                <ChevronDown className="w-4 h-4" />
                              </Button>
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={() => toggleFieldActive(index)}
                                title={field.is_active ? 'Disable field' : 'Enable field'}
                              >
                                {field.is_active ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                              </Button>
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={() => handleEditField(index)}
                              >
                                <Pencil className="w-4 h-4" />
                              </Button>
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={() => handleDeleteField(index)}
                                className="text-destructive hover:text-destructive"
                              >
                                <Trash2 className="w-4 h-4" />
                              </Button>
                            </div>
                          )}
                        </div>
                      ))
                  )}
                </div>

                {/* Field Values for active fields */}
                {formData.custom_fields_config && formData.custom_fields_config.filter(f => f.is_active).length > 0 && (
                  <div className="mt-6 pt-6 border-t">
                    <h4 className="text-lg font-semibold mb-4">Preview</h4>
                    <div className="space-y-4">
                      {formData.custom_fields_config
                        .filter((field) => field.is_active)
                        .sort((a, b) => a.sort_order - b.sort_order)
                        .map((field) => (
                          <CustomFieldInputWrapper
                            key={field.field_key}
                            field={field}
                            value={formData.custom_fields_values?.[field.field_key]}
                            onChange={(value) => {
                              updateField('custom_fields_values', {
                                ...formData.custom_fields_values,
                                [field.field_key]: value,
                              });
                            }}
                            disabled={isLocked('custom_fields_values')}
                          />
                        ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Tab 6: Team Assignment */}
          <TabsContent value="team">
            <Card>
              <CardHeader>
                <CardTitle>Team Assignment</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Hiring Manager */}
                  <div className="space-y-2">
                    <Label htmlFor="hiring_manager_id">
                      Hiring Manager
                      {renderLockIcon('hiring_manager_id')}
                    </Label>
                    <Input
                      id="hiring_manager_id"
                      value={formData.hiring_manager_id || ''}
                      onChange={(e) =>
                        updateField('hiring_manager_id', e.target.value || undefined)
                      }
                      placeholder="User ID of hiring manager"
                      disabled={isLocked('hiring_manager_id')}
                    />
                    <p className="text-xs text-muted-foreground">
                      TODO: Replace with user search/select component
                    </p>
                  </div>

                  {/* Recruiter */}
                  <div className="space-y-2">
                    <Label htmlFor="recruiter_id">
                      Recruiter
                      {renderLockIcon('recruiter_id')}
                    </Label>
                    <Input
                      id="recruiter_id"
                      value={formData.recruiter_id || ''}
                      onChange={(e) =>
                        updateField('recruiter_id', e.target.value || undefined)
                      }
                      placeholder="User ID of recruiter"
                      disabled={isLocked('recruiter_id')}
                    />
                    <p className="text-xs text-muted-foreground">
                      TODO: Replace with user search/select component
                    </p>
                  </div>
                </div>

                <Alert>
                  <Info className="h-4 w-4" />
                  <AlertDescription>
                    Stage-level user assignments can be configured after the position is created
                    through the pipeline settings.
                  </AlertDescription>
                </Alert>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Form Actions */}
        <div className="flex items-center justify-between mt-6 pt-6 border-t">
          <Button type="button" variant="outline" onClick={() => navigate(-1)}>
            Cancel
          </Button>

          <Button type="submit" disabled={saving || isLoading}>
            <Save className="w-4 h-4 mr-2" />
            {saving ? 'Saving...' : 'Save'}
          </Button>
        </div>
      </form>
    </div>
  );
}

// Helper to extract option value and label from options (simple strings)
function getOptionValueAndLabel(option: any): { value: string; label: string } {
  const str = typeof option === 'string' ? option : String(option);
  return { value: str, label: str };
}

// Helper component for rendering custom field inputs
function CustomFieldInputWrapper({
  field,
  value,
  onChange,
  disabled,
}: {
  field: CustomFieldDefinition;
  value: unknown;
  onChange: (value: unknown) => void;
  disabled: boolean;
}) {
  const renderInput = () => {
    switch (field.field_type) {
      case 'TEXT':
        return (
          <Input
            type="text"
            value={(value as string) || ''}
            onChange={(e) => onChange(e.target.value)}
            disabled={disabled}
            required={field.is_required}
            placeholder={`Enter ${field.label.toLowerCase()}`}
          />
        );

      case 'NUMBER':
        return (
          <Input
            type="number"
            value={(value as number) || ''}
            onChange={(e) => onChange(e.target.value ? Number(e.target.value) : null)}
            disabled={disabled}
            required={field.is_required}
            placeholder={`Enter ${field.label.toLowerCase()}`}
          />
        );

      case 'DATE':
        return (
          <Input
            type="date"
            value={(value as string) || ''}
            onChange={(e) => onChange(e.target.value)}
            disabled={disabled}
            required={field.is_required}
          />
        );

      case 'BOOLEAN':
        return (
          <div className="flex items-center gap-2">
            <Checkbox
              checked={Boolean(value)}
              onCheckedChange={(checked) => onChange(checked === true)}
              disabled={disabled}
            />
            <span className="text-sm text-gray-700">{field.label}</span>
          </div>
        );

      case 'SELECT':
        return (
          <Select
            value={(value as string) || ''}
            onValueChange={(v) => onChange(v)}
            disabled={disabled}
          >
            <SelectTrigger>
              <SelectValue placeholder={`Select ${field.label.toLowerCase()}`} />
            </SelectTrigger>
            <SelectContent>
              {field.options?.map((option, idx) => {
                const { value: optValue, label: optLabel } = getOptionValueAndLabel(option);
                return (
                  <SelectItem key={optValue || idx} value={optValue}>
                    {optLabel}
                  </SelectItem>
                );
              })}
            </SelectContent>
          </Select>
        );

      case 'MULTISELECT':
        const selectedValues = (value as string[]) || [];
        return (
          <div className="space-y-2">
            {field.options?.map((option, idx) => {
              const { value: optValue, label: optLabel } = getOptionValueAndLabel(option);
              return (
                <div key={optValue || idx} className="flex items-center gap-2">
                  <Checkbox
                    checked={selectedValues.includes(optValue)}
                    onCheckedChange={(checked) => {
                      if (checked) {
                        onChange([...selectedValues, optValue]);
                      } else {
                        onChange(selectedValues.filter((v) => v !== optValue));
                      }
                    }}
                    disabled={disabled}
                  />
                  <span className="text-sm text-gray-700">{optLabel}</span>
                </div>
              );
            })}
          </div>
        );

      case 'URL':
        return (
          <Input
            type="url"
            value={(value as string) || ''}
            onChange={(e) => onChange(e.target.value)}
            disabled={disabled}
            required={field.is_required}
            placeholder="https://example.com"
          />
        );

      default:
        return (
          <Input
            type="text"
            value={(value as string) || ''}
            onChange={(e) => onChange(e.target.value)}
            disabled={disabled}
          />
        );
    }
  };

  // Don't render label for BOOLEAN since it's inline
  if (field.field_type === 'BOOLEAN') {
    return <div>{renderInput()}</div>;
  }

  return (
    <div className="space-y-2">
      <Label>
        {field.label}
        {field.is_required && <span className="text-red-500 ml-1">*</span>}
      </Label>
      {renderInput()}
    </div>
  );
}

export default PositionFormTabs;
