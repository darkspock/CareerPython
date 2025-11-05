import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Save, Plus, X, ArrowUp, ArrowDown, Settings } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { PositionService } from '../../services/positionService';
import { StageStyleEditor } from '../../components/workflow/StageStyleEditor';
import type { UpdateStageStyleRequest } from '../../types/stageStyle';

interface StageFormData {
  id: string;
  name: string;
  description?: string;
  icon: string;
  background_color: string;
  text_color: string;
  role?: string | null;
  status_mapping: string;
  kanban_display: string;
  field_visibility: Record<string, boolean>;
  field_validation: Record<string, any>;
  field_candidate_visibility: Record<string, boolean>;
}

export default function EditJobPositionWorkflowPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { workflowId } = useParams<{ workflowId: string }>();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [workflowName, setWorkflowName] = useState('');
  const [defaultView, setDefaultView] = useState('kanban');
  const [stages, setStages] = useState<StageFormData[]>([]);
  const [styleEditorOpen, setStyleEditorOpen] = useState(false);
  const [editingStageIndex, setEditingStageIndex] = useState<number | null>(null);

  useEffect(() => {
    if (workflowId) {
      loadWorkflow();
    }
  }, [workflowId]);

  const loadWorkflow = async () => {
    if (!workflowId) return;

    try {
      setLoading(true);
      const workflow = await PositionService.getWorkflow(workflowId);

      setWorkflowName(workflow.name);
      setDefaultView(workflow.default_view);

      const formattedStages: StageFormData[] = workflow.stages.map((stage) => ({
        id: stage.id,
        name: stage.name,
        description: stage.name, // TODO: Get from backend once description field is added
        icon: stage.icon,
        background_color: stage.background_color,
        text_color: stage.text_color,
        role: stage.role || null,
        status_mapping: stage.status_mapping,
        kanban_display: stage.kanban_display,
        field_visibility: stage.field_visibility || {},
        field_validation: stage.field_validation || {},
        field_candidate_visibility: stage.field_candidate_visibility || {},
      }));

      setStages(formattedStages);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load workflow');
      console.error('Error loading workflow:', err);
    } finally {
      setLoading(false);
    }
  };

  const generateStageId = () => {
    return `stage-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  };

  const handleAddStage = () => {
    setStages([
      ...stages,
      {
        id: generateStageId(),
        name: '',
        description: '',
        icon: '📋',
        background_color: '#E5E7EB',
        text_color: '#374151',
        status_mapping: 'draft',
        kanban_display: 'vertical',
        field_visibility: {},
        field_validation: {},
        field_candidate_visibility: {},
      },
    ]);
  };

  const handleRemoveStage = (index: number) => {
    setStages(stages.filter((_, i) => i !== index));
  };

  const handleStageChange = (index: number, field: keyof StageFormData, value: any) => {
    const newStages = [...stages];
    newStages[index] = { ...newStages[index], [field]: value };
    setStages(newStages);
  };

  const handleMoveStageUp = (index: number) => {
    if (index === 0) return;
    const newStages = [...stages];
    [newStages[index - 1], newStages[index]] = [newStages[index], newStages[index - 1]];
    setStages(newStages);
  };

  const handleMoveStageDown = (index: number) => {
    if (index === stages.length - 1) return;
    const newStages = [...stages];
    [newStages[index], newStages[index + 1]] = [newStages[index + 1], newStages[index]];
    setStages(newStages);
  };

  const handleEditStageStyle = (stageIndex: number) => {
    setEditingStageIndex(stageIndex);
    setStyleEditorOpen(true);
  };

  const handleSaveStageStyle = (style: UpdateStageStyleRequest) => {
    if (editingStageIndex === null) return;

    const newStages = [...stages];
    newStages[editingStageIndex] = {
      ...newStages[editingStageIndex],
      icon: style.icon || newStages[editingStageIndex].icon,
      background_color: style.background_color || newStages[editingStageIndex].background_color,
      text_color: style.color || newStages[editingStageIndex].text_color,
    };
    setStages(newStages);

    setStyleEditorOpen(false);
    setEditingStageIndex(null);
  };

  const handleCancelStageStyle = () => {
    setStyleEditorOpen(false);
    setEditingStageIndex(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!workflowId) {
      setError('Workflow ID not found');
      return;
    }

    if (!workflowName.trim()) {
      setError('Workflow name is required');
      return;
    }

    if (stages.length === 0) {
      setError('At least one stage is required');
      return;
    }

    // Validate stages
    for (const stage of stages) {
      if (!stage.name.trim()) {
        setError(`Stage ${stages.indexOf(stage) + 1} name is required`);
        return;
      }
    }

    try {
      setSaving(true);
      await PositionService.updateWorkflow(workflowId, {
        name: workflowName,
        default_view: defaultView,
        stages: stages.map(stage => ({
          id: stage.id,
          name: stage.name,
          icon: stage.icon,
          background_color: stage.background_color,
          text_color: stage.text_color,
          role: stage.role,
          status_mapping: stage.status_mapping,
          kanban_display: stage.kanban_display,
          field_visibility: stage.field_visibility,
          field_validation: stage.field_validation,
          field_candidate_visibility: stage.field_candidate_visibility,
        })),
      });

      navigate('/company/settings/job-position-workflows');
    } catch (err: any) {
      setError(err.message || 'Failed to update workflow');
      console.error('Error updating workflow:', err);
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
          onClick={() => navigate('/company/settings/job-position-workflows')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Volver a Workflows
        </button>
        <h1 className="text-2xl font-bold text-gray-900">Editar Workflow de Posiciones</h1>
        <p className="text-gray-600 mt-1">Actualiza la configuración del workflow</p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Información Básica</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nombre del Workflow <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                required
                value={workflowName}
                onChange={(e) => setWorkflowName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Vista por Defecto</label>
              <select
                value={defaultView}
                onChange={(e) => setDefaultView(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="kanban">Kanban</option>
                <option value="list">Lista</option>
              </select>
            </div>
          </div>
        </div>

        {/* Stages */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Etapas</h2>
            <button
              type="button"
              onClick={handleAddStage}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-4 h-4" />
              Agregar Etapa
            </button>
          </div>

          {stages.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No hay etapas aún. Haz clic en "Agregar Etapa" para crear una.
            </div>
          ) : (
            <div className="space-y-4">
              {stages.map((stage, index) => (
                <div key={stage.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{stage.icon}</span>
                      <h3 className="font-semibold text-gray-900">Etapa {index + 1}</h3>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        onClick={() => handleMoveStageUp(index)}
                        disabled={index === 0}
                        className="p-1 text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
                        title="Mover arriba"
                      >
                        <ArrowUp className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => handleMoveStageDown(index)}
                        disabled={index === stages.length - 1}
                        className="p-1 text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
                        title="Mover abajo"
                      >
                        <ArrowDown className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => handleEditStageStyle(index)}
                        className="p-1 text-blue-600 hover:text-blue-800"
                        title="Editar estilo de etapa"
                      >
                        <Settings className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => handleRemoveStage(index)}
                        className="p-1 text-red-600 hover:text-red-900"
                        title="Eliminar etapa"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Nombre de la Etapa *</label>
                      <input
                        type="text"
                        required
                        value={stage.name}
                        onChange={(e) => handleStageChange(index, 'name', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="Ej: Borrador, Publicada, etc."
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Estilo</label>
                      <button
                        type="button"
                        onClick={() => handleEditStageStyle(index)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2 justify-center"
                      >
                        <Settings className="w-4 h-4" />
                        Editar Icono y Colores
                      </button>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Mapeo de Estado *</label>
                      <select
                        value={stage.status_mapping}
                        onChange={(e) => handleStageChange(index, 'status_mapping', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        required
                      >
                        <option value="draft">Borrador</option>
                        <option value="active">Activa</option>
                        <option value="paused">Pausada</option>
                        <option value="closed">Cerrada</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Visualización en Kanban</label>
                      <select
                        value={stage.kanban_display}
                        onChange={(e) => handleStageChange(index, 'kanban_display', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="vertical">Vertical (Columna)</option>
                        <option value="horizontal_bottom">Horizontal (Fila)</option>
                        <option value="hidden">Oculto</option>
                      </select>
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">Descripción</label>
                      <textarea
                        value={stage.description || ''}
                        onChange={(e) => handleStageChange(index, 'description', e.target.value)}
                        rows={3}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="Describe esta etapa..."
                      />
                    </div>
                  </div>

                  {/* Preview */}
                  <div className="mt-4 p-3 rounded" style={{ backgroundColor: stage.background_color, color: stage.text_color }}>
                    <div className="flex items-center gap-2">
                      <span className="text-lg" dangerouslySetInnerHTML={{ __html: stage.icon }} />
                      <span className="font-semibold">{stage.name}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Custom Fields Configuration - Link to dedicated page */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <Settings className="w-5 h-5 text-blue-600 flex-shrink-0" />
            <div>
              <p className="text-sm text-blue-900">
                {t('company.workflows.customFieldsLinkText')}{' '}
                <button
                  type="button"
                  onClick={() => navigate(`/company/settings/job-position-workflows/${workflowId}/configure`)}
                  className="font-semibold text-blue-600 hover:text-blue-800 underline"
                >
                  {t('company.workflows.customFieldsLinkButton')}
                </button>
              </p>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={() => navigate('/company/settings/job-position-workflows')}
            className="px-6 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={saving}
            className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Save className="w-5 h-5" />
            {saving ? 'Guardando...' : 'Guardar Cambios'}
          </button>
        </div>
      </form>

      {/* Stage Style Editor Modal */}
      {styleEditorOpen && editingStageIndex !== null && (
        <StageStyleEditor
          stageStyle={{
            icon: stages[editingStageIndex].icon,
            color: stages[editingStageIndex].text_color,
            background_color: stages[editingStageIndex].background_color,
          }}
          onSave={handleSaveStageStyle}
          onCancel={handleCancelStageStyle}
          isOpen={styleEditorOpen}
        />
      )}
    </div>
  );
}

