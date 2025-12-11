import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Workflow, Users } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import type { CompanyWorkflow } from '../../types/workflow';

interface WorkflowSelectionPageProps {
  onSelect?: (publicationWorkflowId: string, hiringPipelineId: string) => void;
}

export default function WorkflowSelectionPage({ onSelect }: WorkflowSelectionPageProps) {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const [publicationWorkflows, setPublicationWorkflows] = useState<CompanyWorkflow[]>([]);
  const [hiringPipelines, setHiringPipelines] = useState<CompanyWorkflow[]>([]);
  const [selectedPublicationWorkflow, setSelectedPublicationWorkflow] = useState<string>('');
  const [selectedHiringPipeline, setSelectedHiringPipeline] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const getCompanyId = () => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_id;
    } catch {
      return null;
    }
  };

  useEffect(() => {
    loadWorkflows();
  }, []);

  const loadWorkflows = async () => {
    const companyId = getCompanyId();
    if (!companyId) {
      setError('Company ID not found');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);

      // Load both workflow types in parallel
      const [poWorkflows, caWorkflows] = await Promise.all([
        companyWorkflowService.listWorkflowsByCompany(companyId, 'PO'),
        companyWorkflowService.listWorkflowsByCompany(companyId, 'CA'),
      ]);

      // Filter only published workflows
      const publishedPO = poWorkflows.filter((w: CompanyWorkflow) => w.status === 'published');
      const publishedCA = caWorkflows.filter((w: CompanyWorkflow) => w.status === 'published');

      setPublicationWorkflows(publishedPO);
      setHiringPipelines(publishedCA);

      // Auto-select if only one option
      if (publishedPO.length === 1) {
        setSelectedPublicationWorkflow(publishedPO[0].id);
      }
      if (publishedCA.length === 1) {
        setSelectedHiringPipeline(publishedCA[0].id);
      }

      // If both have only one option, navigate directly
      if (publishedPO.length === 1 && publishedCA.length === 1) {
        handleContinue(publishedPO[0].id, publishedCA[0].id);
      }
    } catch (err: any) {
      console.error('Error loading workflows:', err);
      setError(err.message || 'Failed to load workflows');
    } finally {
      setLoading(false);
    }
  };

  const handleContinue = (poId?: string, caId?: string) => {
    const publicationId = poId || selectedPublicationWorkflow;
    const hiringId = caId || selectedHiringPipeline;

    if (onSelect) {
      onSelect(publicationId, hiringId);
    } else {
      // Navigate to create position page with selected workflows
      const params = new URLSearchParams();
      if (publicationId) params.set('publication_workflow_id', publicationId);
      if (hiringId) params.set('hiring_pipeline_id', hiringId);
      navigate(`/company/positions/create?${params.toString()}`);
    }
  };

  const canContinue = selectedPublicationWorkflow && selectedHiringPipeline;

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          {error}
        </div>
      </div>
    );
  }

  // Check if any workflows are missing
  const missingPublicationWorkflows = publicationWorkflows.length === 0;
  const missingHiringPipelines = hiringPipelines.length === 0;

  if (missingPublicationWorkflows || missingHiringPipelines) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <button
          onClick={() => navigate('/company/positions')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-5 h-5" />
          {t('common.back')}
        </button>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-yellow-800 mb-4">
            {t('position.workflowSelection.missingWorkflows')}
          </h2>
          <p className="text-yellow-700 mb-4">
            {t('position.workflowSelection.missingWorkflowsDescription')}
          </p>
          <ul className="space-y-2 mb-6">
            {missingPublicationWorkflows && (
              <li className="flex items-center gap-2 text-yellow-700">
                <Workflow className="w-5 h-5" />
                <span>{t('position.workflowSelection.noPublicationWorkflows')}</span>
                <a
                  href="/company/settings/publication-workflows"
                  className="text-blue-600 hover:underline ml-2"
                >
                  {t('position.workflowSelection.createOne')}
                </a>
              </li>
            )}
            {missingHiringPipelines && (
              <li className="flex items-center gap-2 text-yellow-700">
                <Users className="w-5 h-5" />
                <span>{t('position.workflowSelection.noHiringPipelines')}</span>
                <a
                  href="/company/settings/hiring-pipelines"
                  className="text-blue-600 hover:underline ml-2"
                >
                  {t('position.workflowSelection.createOne')}
                </a>
              </li>
            )}
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      <button
        onClick={() => navigate('/company/positions')}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
      >
        <ArrowLeft className="w-5 h-5" />
        {t('common.back')}
      </button>

      <h1 className="text-2xl font-bold text-gray-900 mb-2">
        {t('position.workflowSelection.title')}
      </h1>
      <p className="text-gray-600 mb-8">
        {t('position.workflowSelection.description')}
      </p>

      <div className="space-y-8">
        {/* Publication Workflow Selection */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
              <Workflow className="w-5 h-5 text-indigo-600" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">
                {t('position.workflowSelection.publicationWorkflow')}
              </h2>
              <p className="text-sm text-gray-500">
                {t('position.workflowSelection.publicationWorkflowDescription')}
              </p>
            </div>
          </div>

          {publicationWorkflows.length === 1 ? (
            <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
              <div className="font-medium text-indigo-900">{publicationWorkflows[0].name}</div>
              {publicationWorkflows[0].description && (
                <div className="text-sm text-indigo-700 mt-1">{publicationWorkflows[0].description}</div>
              )}
            </div>
          ) : (
            <div className="space-y-3">
              {publicationWorkflows.map((workflow) => (
                <label
                  key={workflow.id}
                  className={`flex items-start gap-3 p-4 border rounded-lg cursor-pointer transition-colors ${
                    selectedPublicationWorkflow === workflow.id
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-gray-200 hover:border-indigo-300 hover:bg-gray-50'
                  }`}
                >
                  <input
                    type="radio"
                    name="publicationWorkflow"
                    value={workflow.id}
                    checked={selectedPublicationWorkflow === workflow.id}
                    onChange={(e) => setSelectedPublicationWorkflow(e.target.value)}
                    className="mt-1"
                  />
                  <div>
                    <div className="font-medium text-gray-900">{workflow.name}</div>
                    {workflow.description && (
                      <div className="text-sm text-gray-500 mt-1">{workflow.description}</div>
                    )}
                    <div className="text-xs text-gray-400 mt-1">
                      {workflow.stages?.length || 0} {t('position.workflowSelection.stages')}
                    </div>
                  </div>
                </label>
              ))}
            </div>
          )}
        </div>

        {/* Hiring Pipeline Selection */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Users className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">
                {t('position.workflowSelection.hiringPipeline')}
              </h2>
              <p className="text-sm text-gray-500">
                {t('position.workflowSelection.hiringPipelineDescription')}
              </p>
            </div>
          </div>

          {hiringPipelines.length === 1 ? (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="font-medium text-blue-900">{hiringPipelines[0].name}</div>
              {hiringPipelines[0].description && (
                <div className="text-sm text-blue-700 mt-1">{hiringPipelines[0].description}</div>
              )}
            </div>
          ) : (
            <div className="space-y-3">
              {hiringPipelines.map((workflow) => (
                <label
                  key={workflow.id}
                  className={`flex items-start gap-3 p-4 border rounded-lg cursor-pointer transition-colors ${
                    selectedHiringPipeline === workflow.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
                  }`}
                >
                  <input
                    type="radio"
                    name="hiringPipeline"
                    value={workflow.id}
                    checked={selectedHiringPipeline === workflow.id}
                    onChange={(e) => setSelectedHiringPipeline(e.target.value)}
                    className="mt-1"
                  />
                  <div>
                    <div className="font-medium text-gray-900">{workflow.name}</div>
                    {workflow.description && (
                      <div className="text-sm text-gray-500 mt-1">{workflow.description}</div>
                    )}
                    <div className="text-xs text-gray-400 mt-1">
                      {workflow.stages?.length || 0} {t('position.workflowSelection.stages')}
                    </div>
                  </div>
                </label>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Info box */}
      <div className="mt-6 bg-gray-50 border border-gray-200 rounded-lg p-4 text-sm text-gray-600">
        <strong>{t('position.workflowSelection.note')}:</strong>{' '}
        {t('position.workflowSelection.cannotChangeAfterCreation')}
      </div>

      {/* Continue button */}
      <div className="mt-8 flex justify-end">
        <button
          onClick={() => handleContinue()}
          disabled={!canContinue}
          className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors ${
            canContinue
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          }`}
        >
          {t('position.workflowSelection.continue')}
          <ArrowRight className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
