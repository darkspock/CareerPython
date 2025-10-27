import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, Plus, X } from 'lucide-react';
import { PositionService } from '../../services/positionService';
import type { Position, UpdatePositionRequest } from '../../types/position';
import { WorkflowSelector, StageAssignmentEditor, PhaseWorkflowSelector } from '../../components/workflow';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import type { WorkflowStage } from '../../types/workflow';
import { api } from '../../lib/api';

export default function EditPositionPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<UpdatePositionRequest>({
    workflow_id: null,
    phase_workflows: {},  // Phase 12.8: phase_id -> workflow_id mapping
    title: '',
    description: '',
    location: '',
    department: '',
    employment_type: 'full_time',
    experience_level: 'mid',
    salary_min: undefined,
    salary_max: undefined,
    salary_currency: 'USD',
    requirements: [],
    benefits: [],
    skills: [],
    is_remote: false,
    application_deadline: '',
    application_url: '',
    application_email: '',
    working_hours: '',
    travel_required: 0,
    visa_sponsorship: false,
    contact_person: '',
    reports_to: '',
    number_of_openings: 1,
    job_category: 'other',
  });

  const [companyId, setCompanyId] = useState<string>('');

  const [requirementInput, setRequirementInput] = useState('');
  const [benefitInput, setBenefitInput] = useState('');
  const [skillInput, setSkillInput] = useState('');

  // Stage assignment states
  const [workflowStages, setWorkflowStages] = useState<WorkflowStage[]>([]);
  const [companyUsers, setCompanyUsers] = useState<Array<{ id: string; name: string; email: string }>>([]);
  const [loadingStages, setLoadingStages] = useState(false);
  const [loadingUsers, setLoadingUsers] = useState(false);

  useEffect(() => {
    if (id) {
      loadPosition();
    }
  }, [id]);

  const loadPosition = async () => {
    if (!id) return;

    try {
      setLoading(true);
      const position = await PositionService.getPositionById(id);

      // Convert Position to form data
      setFormData({
        workflow_id: position.workflow_id,
        phase_workflows: position.phase_workflows || {},  // Phase 12.8
        title: position.title,
        description: position.description,
        location: position.location,
        department: position.department,
        employment_type: position.employment_type || position.contract_type as any,
        experience_level: position.experience_level || position.position_level as any,
        salary_min: position.salary_range?.min_amount,
        salary_max: position.salary_range?.max_amount,
        salary_currency: position.salary_range?.currency || 'USD',
        requirements: Array.isArray(position.requirements) ? position.requirements : [],
        benefits: position.benefits || [],
        skills: position.skills || [],
        is_remote: position.is_remote || position.work_location_type === 'remote',
        application_deadline: position.application_deadline,
        application_url: position.application_url,
        application_email: position.application_email,
        working_hours: position.working_hours,
        travel_required: typeof position.travel_required === 'boolean' ? 0 : position.travel_required,
        visa_sponsorship: position.visa_sponsorship,
        contact_person: position.contact_person,
        reports_to: position.reports_to,
        number_of_openings: position.number_of_openings,
        job_category: position.job_category,
      });

      setCompanyId(position.company_id);

      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load position');
      console.error('Error loading position:', err);
    } finally {
      setLoading(false);
    }
  };

  // Load workflow stages when workflow_id changes
  useEffect(() => {
    const loadWorkflowStages = async () => {
      if (!formData.workflow_id) {
        setWorkflowStages([]);
        return;
      }

      setLoadingStages(true);
      try {
        const stages = await companyWorkflowService.listStagesByWorkflow(formData.workflow_id);
        setWorkflowStages(stages);
      } catch (err) {
        console.error('Error loading workflow stages:', err);
        setWorkflowStages([]);
      } finally {
        setLoadingStages(false);
      }
    };

    loadWorkflowStages();
  }, [formData.workflow_id]);

  // Load company users when component mounts
  useEffect(() => {
    const loadCompanyUsers = async () => {
      if (!companyId) return;

      setLoadingUsers(true);
      try {
        const response = await api.authenticatedRequest(`/company/${companyId}/users?active_only=true`);

        // Map to the format expected by StageAssignmentEditor
        const users = response.map((user: any) => ({
          id: user.user_id,
          name: user.name || user.email,
          email: user.email
        }));

        setCompanyUsers(users);
      } catch (err) {
        console.error('Error loading company users:', err);
        setCompanyUsers([]);
      } finally {
        setLoadingUsers(false);
      }
    };

    loadCompanyUsers();
  }, [companyId]);

  const handleAddItem = (
    inputValue: string,
    setInput: (value: string) => void,
    arrayKey: 'requirements' | 'benefits' | 'skills'
  ) => {
    if (inputValue.trim()) {
      setFormData({
        ...formData,
        [arrayKey]: [...(formData[arrayKey] || []), inputValue.trim()],
      });
      setInput('');
    }
  };

  const handleRemoveItem = (
    index: number,
    arrayKey: 'requirements' | 'benefits' | 'skills'
  ) => {
    setFormData({
      ...formData,
      [arrayKey]: (formData[arrayKey] || []).filter((_, i) => i !== index),
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!id) {
      setError('Position ID not found');
      return;
    }

    if (!formData.title) {
      setError('Title is required');
      return;
    }

    try {
      setSaving(true);
      await PositionService.updatePosition(id, formData);
      navigate(`/company/positions/${id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to update position');
      console.error('Error updating position:', err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate(`/company/positions/${id}`)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Position
        </button>
        <h1 className="text-2xl font-bold text-gray-900">Edit Position</h1>
        <p className="text-gray-600 mt-1">Update job opening details</p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Form - Reusing the same structure as CreatePositionPage */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Basic Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Job Title <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Department</label>
              <input
                type="text"
                value={formData.department}
                onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
              <input
                type="text"
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Employment Type</label>
              <select
                value={formData.employment_type}
                onChange={(e) => setFormData({ ...formData, employment_type: e.target.value as any })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="full_time">Full Time</option>
                <option value="part_time">Part Time</option>
                <option value="contract">Contract</option>
                <option value="internship">Internship</option>
                <option value="freelance">Freelance</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Experience Level</label>
              <select
                value={formData.experience_level}
                onChange={(e) => setFormData({ ...formData, experience_level: e.target.value as any })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="entry">Entry Level</option>
                <option value="mid">Mid Level</option>
                <option value="senior">Senior</option>
                <option value="executive">Executive</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Number of Openings</label>
              <input
                type="number"
                min="1"
                value={formData.number_of_openings}
                onChange={(e) => setFormData({ ...formData, number_of_openings: parseInt(e.target.value) || 1 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="is_remote"
                checked={formData.is_remote}
                onChange={(e) => setFormData({ ...formData, is_remote: e.target.checked })}
                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <label htmlFor="is_remote" className="text-sm font-medium text-gray-700">
                Remote Position
              </label>
            </div>

            {/* Phase 12.8: Phase-Workflow Configuration */}
            <div className="md:col-span-2">
              <PhaseWorkflowSelector
                companyId={companyId}
                phaseWorkflows={formData.phase_workflows || {}}
                onChange={(phaseWorkflows) => setFormData({ ...formData, phase_workflows: phaseWorkflows })}
                label="Recruitment Workflow Configuration"
              />
              <p className="mt-1 text-sm text-gray-500">
                Configure which workflow to use for each recruitment phase. The system will automatically
                guide candidates through the configured phases.
              </p>
            </div>

            {/* Stage Assignments Editor */}
            {formData.workflow_id && !loadingStages && workflowStages.length > 0 && id && (
              <div className="md:col-span-2">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <StageAssignmentEditor
                    positionId={id}
                    stages={workflowStages}
                    companyUsers={companyUsers}
                    disabled={saving || loadingUsers}
                  />
                  <p className="mt-3 text-sm text-gray-500">
                    Assign team members to each workflow stage. They will be responsible for processing candidates at that stage.
                  </p>
                </div>
              </div>
            )}

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows={5}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Salary Information */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Salary Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Minimum Salary</label>
              <input
                type="number"
                value={formData.salary_min || ''}
                onChange={(e) => setFormData({ ...formData, salary_min: e.target.value ? parseInt(e.target.value) : undefined })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Maximum Salary</label>
              <input
                type="number"
                value={formData.salary_max || ''}
                onChange={(e) => setFormData({ ...formData, salary_max: e.target.value ? parseInt(e.target.value) : undefined })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Currency</label>
              <select
                value={formData.salary_currency}
                onChange={(e) => setFormData({ ...formData, salary_currency: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="USD">USD</option>
                <option value="EUR">EUR</option>
                <option value="GBP">GBP</option>
                <option value="CAD">CAD</option>
              </select>
            </div>
          </div>
        </div>

        {/* Requirements, Skills, Benefits - Same as CreatePositionPage */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Requirements</h2>
          <div className="flex gap-2 mb-3">
            <input
              type="text"
              value={requirementInput}
              onChange={(e) => setRequirementInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleAddItem(requirementInput, setRequirementInput, 'requirements');
                }
              }}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Add a requirement"
            />
            <button
              type="button"
              onClick={() => handleAddItem(requirementInput, setRequirementInput, 'requirements')}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <Plus className="w-5 h-5" />
            </button>
          </div>
          {formData.requirements && formData.requirements.length > 0 && (
            <ul className="space-y-2">
              {formData.requirements.map((req, idx) => (
                <li key={idx} className="flex items-center justify-between bg-gray-50 px-3 py-2 rounded">
                  <span className="text-sm text-gray-700">{req}</span>
                  <button
                    type="button"
                    onClick={() => handleRemoveItem(idx, 'requirements')}
                    className="text-red-600 hover:text-red-800"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Required Skills</h2>
          <div className="flex gap-2 mb-3">
            <input
              type="text"
              value={skillInput}
              onChange={(e) => setSkillInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleAddItem(skillInput, setSkillInput, 'skills');
                }
              }}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Add a skill"
            />
            <button
              type="button"
              onClick={() => handleAddItem(skillInput, setSkillInput, 'skills')}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <Plus className="w-5 h-5" />
            </button>
          </div>
          {formData.skills && formData.skills.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {formData.skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="inline-flex items-center gap-2 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                >
                  {skill}
                  <button
                    type="button"
                    onClick={() => handleRemoveItem(idx, 'skills')}
                    className="hover:text-blue-900"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Benefits</h2>
          <div className="flex gap-2 mb-3">
            <input
              type="text"
              value={benefitInput}
              onChange={(e) => setBenefitInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleAddItem(benefitInput, setBenefitInput, 'benefits');
                }
              }}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Add a benefit"
            />
            <button
              type="button"
              onClick={() => handleAddItem(benefitInput, setBenefitInput, 'benefits')}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <Plus className="w-5 h-5" />
            </button>
          </div>
          {formData.benefits && formData.benefits.length > 0 && (
            <ul className="space-y-2">
              {formData.benefits.map((benefit, idx) => (
                <li key={idx} className="flex items-center justify-between bg-gray-50 px-3 py-2 rounded">
                  <span className="text-sm text-gray-700">{benefit}</span>
                  <button
                    type="button"
                    onClick={() => handleRemoveItem(idx, 'benefits')}
                    className="text-red-600 hover:text-red-800"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={() => navigate(`/company/positions/${id}`)}
            className="px-6 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Save className="w-5 h-5" />
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </form>
    </div>
  );
}
