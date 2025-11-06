import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Save } from 'lucide-react';
import { companyWorkflowService } from '../../services/companyWorkflowService.ts';
import type { CompanyWorkflow, CustomField, FieldConfiguration, WorkflowStage } from '../../types/workflow.ts';
import { CustomFieldEditor, FieldVisibilityMatrix } from '../../components/workflow';
import { ValidationRuleEditor } from '../../components/workflow/ValidationRuleEditor.tsx';

export default function WorkflowAdvancedConfigPage() {
  console.log('WorkflowAdvancedConfigPage component rendered');
  
  const navigate = useNavigate();
  const { workflowId } = useParams<{ workflowId: string }>();
  
  console.log('workflowId from params:', workflowId);
  
  const [workflow, setWorkflow] = useState<CompanyWorkflow | null>(null);
  const [stages, setStages] = useState<WorkflowStage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saving, _setSaving] = useState(false);

  // Custom fields state
  const [customFields, setCustomFields] = useState<CustomField[]>([]);
  const [_fieldConfigurations, setFieldConfigurations] = useState<FieldConfiguration[]>([]);

  useEffect(() => {
    console.log('useEffect triggered, workflowId:', workflowId);
    if (workflowId) {
      console.log('Calling loadWorkflow...');
      loadWorkflow();
    } else {
      console.log('No workflowId, not loading workflow');
    }
  }, [workflowId]);

  const loadWorkflow = async () => {
    if (!workflowId) {
      console.log('No workflowId provided');
      return;
    }

    console.log('Loading workflow with ID:', workflowId);
    
    try {
      setLoading(true);
      console.log('Calling companyWorkflowService.getWorkflow...');
      const data = await companyWorkflowService.getWorkflow(workflowId);
      console.log('Workflow data received:', data);
      setWorkflow(data);
      
      // Load stages separately
      console.log('Loading stages...');
      const stagesData = await companyWorkflowService.listStagesByWorkflow(workflowId);
      console.log('Stages data received:', stagesData);
      setStages(stagesData);
      
      setError(null);
    } catch (err: any) {
      console.error('Error loading workflow:', err);
      setError(err.message || 'Failed to load workflow');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    // This page is read-only for now, but we can add save functionality later
    // if needed for any advanced configurations
    console.log('Save functionality not implemented yet');
  };

  const handleBack = () => {
    navigate('/company/settings/workflows');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <h2 className="text-lg font-semibold text-red-800 mb-2">Error</h2>
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={handleBack}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  if (!workflow) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
          <h2 className="text-lg font-semibold text-yellow-800 mb-2">Workflow Not Found</h2>
          <p className="text-yellow-600 mb-4">The requested workflow could not be found.</p>
          <button
            onClick={handleBack}
            className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <button
            onClick={handleBack}
            className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
            title="Go back to workflows"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Advanced Configuration
            </h1>
            <p className="text-gray-600">
              {workflow.name} - Custom Fields & Validations
            </p>
          </div>
        </div>
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Save className="w-4 h-4" />
          {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      {/* Content */}
      <div className="space-y-6">
        {/* Custom Fields */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <CustomFieldEditor
            workflowId={workflowId!}
            onFieldsChange={setCustomFields}
          />
        </div>

        {/* Field Visibility Matrix */}
        {customFields.length > 0 && stages.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <FieldVisibilityMatrix
              workflowId={workflowId!}
              stages={stages}
              fields={customFields}
              onConfigurationsChange={setFieldConfigurations}
            />
          </div>
        )}

        {/* Validation Rules */}
        {customFields.length > 0 && stages.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <ValidationRuleEditor
              workflowId={workflowId!}
              stages={stages}
              customFields={customFields}
            />
          </div>
        )}

        {/* Info Message */}
        {customFields.length === 0 && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
            <h3 className="text-lg font-semibold text-blue-800 mb-2">
              No Custom Fields Yet
            </h3>
            <p className="text-blue-600 mb-4">
              Add custom fields to your workflow to configure their visibility and validation rules.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
