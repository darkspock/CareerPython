import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Plus, Workflow, Users, Layers, Briefcase } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import { phaseService } from '../../services/phaseService';
import { PositionService } from '../../services/positionService';
import type { CompanyWorkflow } from '../../types/workflow';
import type { Phase } from '../../types/phase';

export default function WorkflowSelectionPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const [positionTitle, setPositionTitle] = useState<string>('');
  const [publicationWorkflows, setPublicationWorkflows] = useState<CompanyWorkflow[]>([]);
  const [phases, setPhases] = useState<Phase[]>([]);
  const [caWorkflowsByPhase, setCaWorkflowsByPhase] = useState<Record<string, CompanyWorkflow[]>>({});
  const [selectedPublicationWorkflow, setSelectedPublicationWorkflow] = useState<string>('');
  const [selectedPhaseWorkflows, setSelectedPhaseWorkflows] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
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
    loadData();
  }, []);

  const loadData = async () => {
    const companyId = getCompanyId();
    if (!companyId) {
      setError('Company ID not found');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);

      // Load publication workflows, phases, and CA workflows in parallel
      const [poWorkflows, phasesData, caWorkflows] = await Promise.all([
        companyWorkflowService.listWorkflowsByCompany(companyId, 'PO'),
        phaseService.listPhases(companyId),
        companyWorkflowService.listWorkflowsByCompany(companyId, 'CA'),
      ]);

      // Filter only non-archived workflows
      const availablePO = poWorkflows.filter((w: CompanyWorkflow) => w.status !== 'ARCHIVED');
      const availableCA = caWorkflows.filter((w: CompanyWorkflow) => w.status !== 'ARCHIVED');

      // Filter active phases of type CA (Candidate Application)
      const activePhases = phasesData.filter((p: Phase) => p.status === 'ACTIVE' && p.workflow_type === 'CA');

      setPublicationWorkflows(availablePO);
      setPhases(activePhases);

      // Group CA workflows by phase
      const workflowsByPhase: Record<string, CompanyWorkflow[]> = {};
      for (const phase of activePhases) {
        // Get workflows for this phase
        const phaseWorkflows = availableCA.filter((w: CompanyWorkflow) => w.phase_id === phase.id);
        workflowsByPhase[phase.id] = phaseWorkflows;
      }
      setCaWorkflowsByPhase(workflowsByPhase);

      // Auto-select publication workflow if only one
      if (availablePO.length === 1) {
        setSelectedPublicationWorkflow(availablePO[0].id);
      }

      // Auto-select CA workflows if only one per phase
      const autoSelectedPhaseWorkflows: Record<string, string> = {};
      for (const phase of activePhases) {
        const phaseWorkflows = workflowsByPhase[phase.id] || [];
        if (phaseWorkflows.length === 1) {
          autoSelectedPhaseWorkflows[phase.id] = phaseWorkflows[0].id;
        }
      }
      setSelectedPhaseWorkflows(autoSelectedPhaseWorkflows);
    } catch (err: any) {
      console.error('Error loading data:', err);
      setError(err.message || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handlePhaseWorkflowChange = (phaseId: string, workflowId: string) => {
    setSelectedPhaseWorkflows((prev) => ({
      ...prev,
      [phaseId]: workflowId,
    }));
  };

  const handleCreate = async () => {
    const companyId = getCompanyId();
    if (!companyId) {
      setError('Company ID not found');
      return;
    }

    setCreating(true);
    setError(null);

    try {
      // Create the position - response is JobPositionActionResponse with position_id
      const response = await PositionService.createPosition({
        company_id: companyId,
        title: positionTitle.trim(),
        job_position_workflow_id: selectedPublicationWorkflow,
        phase_workflows: selectedPhaseWorkflows,
        visibility: 'hidden',
      });

      // The response contains position_id from JobPositionActionResponse
      const positionId = (response as any).position_id || response.id;
      if (!positionId) {
        throw new Error('No position ID returned');
      }

      // Navigate to edit page
      navigate(`/company/positions/${positionId}/edit`);
    } catch (err: any) {
      console.error('Error creating position:', err);
      setError(err.message || 'Failed to create position');
      setCreating(false);
    }
  };

  // Check if all required selections are made
  const allPhasesHaveWorkflows = phases.every(
    (phase) => {
      const phaseWorkflows = caWorkflowsByPhase[phase.id] || [];
      // If phase has no workflows available, it's not required
      if (phaseWorkflows.length === 0) return true;
      // Otherwise, must have a selection
      return selectedPhaseWorkflows[phase.id];
    }
  );
  const canCreate = positionTitle.trim() && selectedPublicationWorkflow && allPhasesHaveWorkflows;

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // Check if any workflows are missing
  const missingPublicationWorkflows = publicationWorkflows.length === 0;
  const missingPhases = phases.length === 0;

  if (missingPublicationWorkflows || missingPhases) {
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
            {t('position.create.missingWorkflows')}
          </h2>
          <p className="text-yellow-700 mb-4">
            {t('position.create.missingWorkflowsDescription')}
          </p>
          <ul className="space-y-2 mb-6">
            {missingPublicationWorkflows && (
              <li className="flex items-center gap-2 text-yellow-700">
                <Workflow className="w-5 h-5" />
                <span>{t('position.create.noPublicationWorkflows')}</span>
                <a
                  href="/company/settings/publication-workflows"
                  className="text-blue-600 hover:underline ml-2"
                >
                  {t('position.create.createOne')}
                </a>
              </li>
            )}
            {missingPhases && (
              <li className="flex items-center gap-2 text-yellow-700">
                <Layers className="w-5 h-5" />
                <span>{t('position.create.noPhases')}</span>
                <a
                  href="/company/settings/phases"
                  className="text-blue-600 hover:underline ml-2"
                >
                  {t('position.create.createOne')}
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
        {t('position.create.title')}
      </h1>
      <p className="text-gray-600 mb-8">
        {t('position.create.description')}
      </p>

      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          {error}
        </div>
      )}

      <div className="space-y-8">
        {/* Position Title */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <Briefcase className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">
                {t('position.create.positionTitle')}
              </h2>
              <p className="text-sm text-gray-500">
                {t('position.create.positionTitleDescription')}
              </p>
            </div>
          </div>

          <input
            type="text"
            value={positionTitle}
            onChange={(e) => setPositionTitle(e.target.value)}
            placeholder={t('position.create.positionTitlePlaceholder')}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
          />
        </div>

        {/* Publication Workflow Selection */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
              <Workflow className="w-5 h-5 text-indigo-600" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">
                {t('position.create.publicationWorkflow')}
              </h2>
              <p className="text-sm text-gray-500">
                {t('position.create.publicationWorkflowDescription')}
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
                      {workflow.stages?.length || 0} {t('position.create.stages')}
                    </div>
                  </div>
                </label>
              ))}
            </div>
          )}
        </div>

        {/* Phase Workflows Selection */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Users className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">
                {t('position.create.hiringPipeline')}
              </h2>
              <p className="text-sm text-gray-500">
                {t('position.create.hiringPipelineDescription')}
              </p>
            </div>
          </div>

          <div className="space-y-6">
            {phases.map((phase) => {
              const phaseWorkflows = caWorkflowsByPhase[phase.id] || [];
              const selectedWorkflowId = selectedPhaseWorkflows[phase.id] || '';

              if (phaseWorkflows.length === 0) {
                return (
                  <div key={phase.id} className="border-l-4 border-gray-200 pl-4">
                    <div className="font-medium text-gray-700">{phase.name}</div>
                    <div className="text-sm text-gray-400 mt-1">
                      {t('position.create.noWorkflowsForPhase')}
                    </div>
                  </div>
                );
              }

              return (
                <div key={phase.id} className="border-l-4 border-blue-400 pl-4">
                  <div className="font-medium text-gray-900 mb-2">{phase.name}</div>

                  {phaseWorkflows.length === 1 ? (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                      <div className="font-medium text-blue-900">{phaseWorkflows[0].name}</div>
                      {phaseWorkflows[0].description && (
                        <div className="text-sm text-blue-700 mt-1">{phaseWorkflows[0].description}</div>
                      )}
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {phaseWorkflows.map((workflow) => (
                        <label
                          key={workflow.id}
                          className={`flex items-start gap-3 p-3 border rounded-lg cursor-pointer transition-colors ${
                            selectedWorkflowId === workflow.id
                              ? 'border-blue-500 bg-blue-50'
                              : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
                          }`}
                        >
                          <input
                            type="radio"
                            name={`phase-${phase.id}`}
                            value={workflow.id}
                            checked={selectedWorkflowId === workflow.id}
                            onChange={(e) => handlePhaseWorkflowChange(phase.id, e.target.value)}
                            className="mt-1"
                          />
                          <div>
                            <div className="font-medium text-gray-900">{workflow.name}</div>
                            {workflow.description && (
                              <div className="text-sm text-gray-500 mt-1">{workflow.description}</div>
                            )}
                            <div className="text-xs text-gray-400 mt-1">
                              {workflow.stages?.length || 0} {t('position.create.stages')}
                            </div>
                          </div>
                        </label>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Info box */}
      <div className="mt-6 bg-gray-50 border border-gray-200 rounded-lg p-4 text-sm text-gray-600">
        <strong>{t('position.create.note')}:</strong>{' '}
        {t('position.create.cannotChangeAfterCreation')}
      </div>

      {/* Create button */}
      <div className="mt-8 flex justify-end">
        <button
          onClick={handleCreate}
          disabled={!canCreate || creating}
          className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors ${
            canCreate && !creating
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          }`}
        >
          {creating ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              {t('position.create.creating')}
            </>
          ) : (
            <>
              <Plus className="w-5 h-5" />
              {t('position.create.createButton')}
            </>
          )}
        </button>
      </div>
    </div>
  );
}
