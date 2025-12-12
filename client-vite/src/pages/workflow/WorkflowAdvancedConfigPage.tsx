import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Save } from 'lucide-react';
import { toast } from 'react-toastify';
import { useTranslation } from 'react-i18next';
import { companyWorkflowService } from '../../services/companyWorkflowService.ts';
import type { CompanyWorkflow, WorkflowStage } from '../../types/workflow.ts';
import type { CustomField, FieldConfiguration } from '../../types/customization.ts';
import { EntityCustomFieldEditor, FieldVisibilityMatrix } from '../../components/customization';

export default function WorkflowAdvancedConfigPage() {
  console.log('WorkflowAdvancedConfigPage component rendered');
  
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { workflowId } = useParams<{ workflowId: string }>();
  
  console.log('workflowId from params:', workflowId);
  
  const [workflow, setWorkflow] = useState<CompanyWorkflow | null>(null);
  const [stages, setStages] = useState<WorkflowStage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

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
    // eslint-disable-next-line react-hooks/exhaustive-deps
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
    // Note: Individual components (EntityCustomFieldEditor, FieldVisibilityMatrix)
    // save automatically when changes are made. This function reloads data to ensure sync.
    try {
      setSaving(true);
      
      // Reload workflow and stages to ensure we have the latest data
      if (workflowId) {
        await loadWorkflow();
      }
      
      // Show success message
      toast.success(t('company.workflows.advancedConfigSaveSuccess'), {
        position: 'top-right',
        autoClose: 3000
      });
    } catch (err: any) {
      toast.error(t('company.workflows.advancedConfigSaveError', { error: err.message || t('company.workflows.advancedConfigUnknownError') }), {
        position: 'top-right',
        autoClose: 5000
      });
    } finally {
      setSaving(false);
    }
  };

  const handleBack = () => {
    navigate('/company/settings/hiring-pipelines');
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
          <h2 className="text-lg font-semibold text-red-800 mb-2">{t('company.workflows.advancedConfigError')}</h2>
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={handleBack}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            {t('company.workflows.advancedConfigGoBack')}
          </button>
        </div>
      </div>
    );
  }

  if (!workflow) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
          <h2 className="text-lg font-semibold text-yellow-800 mb-2">{t('company.workflows.advancedConfigWorkflowNotFound')}</h2>
          <p className="text-yellow-600 mb-4">{t('company.workflows.advancedConfigWorkflowNotFoundDescription')}</p>
          <button
            onClick={handleBack}
            className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors"
          >
            {t('company.workflows.advancedConfigGoBack')}
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
            title={t('company.workflows.advancedConfigGoBackTooltip')}
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {t('company.workflows.advancedConfigTitle')}
            </h1>
            <p className="text-gray-600">
              {workflow.name} - {t('company.workflows.advancedConfigSubtitle')}
            </p>
          </div>
        </div>
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Save className="w-4 h-4" />
          {saving ? t('company.workflows.advancedConfigSaving') : t('company.workflows.advancedConfigSaveChanges')}
        </button>
      </div>

      {/* Content */}
      <div className="space-y-6">
        {/* Custom Fields */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <EntityCustomFieldEditor
            entityType="Workflow"
            entityId={workflowId!}
            onFieldsChange={setCustomFields}
          />
        </div>

        {/* Field Visibility Matrix */}
        {customFields.length > 0 && stages.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <FieldVisibilityMatrix
              entityType="Workflow"
              entityId={workflowId!}
              contextType="Workflow"
              contexts={stages.map(s => ({ id: s.id, name: s.name }))}
              fields={customFields}
              onConfigurationsChange={setFieldConfigurations}
            />
          </div>
        )}

        {/* Info Message */}
        {customFields.length === 0 && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
            <h3 className="text-lg font-semibold text-blue-800 mb-2">
              {t('company.workflows.advancedConfigNoCustomFields')}
            </h3>
            <p className="text-blue-600 mb-4">
              {t('company.workflows.advancedConfigNoCustomFieldsDescription')}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
