import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, ArrowUp, ArrowDown, Layers, GripVertical } from 'lucide-react';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { arrayMove, SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy, useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import type { DragEndEvent } from '@dnd-kit/core';
import { phaseService } from '../../services/phaseService';
import type { Phase } from '../../types/phase';
import PhaseFormModal from '../../components/phases/PhaseFormModal';

// Sortable Phase Row Component
function SortablePhaseRow({
  phase,
  index,
  onEdit,
  onDelete,
  onMoveUp,
  onMoveDown,
  isFirst,
  isLast
}: {
  phase: Phase;
  index: number;
  onEdit: (phase: Phase) => void;
  onDelete: (phaseId: string) => void;
  onMoveUp: (index: number) => void;
  onMoveDown: (index: number) => void;
  isFirst: boolean;
  isLast: boolean;
}) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: phase.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  const getDefaultViewLabel = (view: string): string => {
    return view === 'KANBAN' ? 'Kanban Board' : 'List View';
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
    >
      <div className="p-6">
        <div className="flex items-start justify-between">
          {/* Drag Handle */}
          <div
            {...attributes}
            {...listeners}
            className="cursor-grab active:cursor-grabbing text-gray-400 hover:text-gray-600 mr-4 mt-1"
          >
            <GripVertical className="w-5 h-5" />
          </div>

          {/* Phase Info */}
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-sm font-medium text-gray-500">
                #{phase.sort_order}
              </span>
              <h3 className="text-lg font-semibold text-gray-900">
                {phase.name}
              </h3>
              <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">
                {getDefaultViewLabel(phase.default_view)}
              </span>
            </div>

            {phase.objective && (
              <p className="text-sm text-gray-600 mt-2">
                {phase.objective}
              </p>
            )}

            <div className="mt-3 text-xs text-gray-500">
              <span>Created: {new Date(phase.created_at).toLocaleDateString()}</span>
              {phase.updated_at !== phase.created_at && (
                <span className="ml-3">
                  Updated: {new Date(phase.updated_at).toLocaleDateString()}
                </span>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2 ml-4">
            {/* Move Up */}
            <button
              onClick={() => onMoveUp(index)}
              disabled={isFirst}
              className="p-2 text-gray-600 hover:text-gray-900 disabled:text-gray-300 disabled:cursor-not-allowed rounded-lg hover:bg-gray-100 transition-colors"
              title="Move up"
            >
              <ArrowUp className="w-5 h-5" />
            </button>

            {/* Move Down */}
            <button
              onClick={() => onMoveDown(index)}
              disabled={isLast}
              className="p-2 text-gray-600 hover:text-gray-900 disabled:text-gray-300 disabled:cursor-not-allowed rounded-lg hover:bg-gray-100 transition-colors"
              title="Move down"
            >
              <ArrowDown className="w-5 h-5" />
            </button>

            {/* Edit */}
            <button
              onClick={() => onEdit(phase)}
              className="p-2 text-blue-600 hover:text-blue-800 rounded-lg hover:bg-blue-50 transition-colors"
              title="Edit phase"
            >
              <Edit className="w-5 h-5" />
            </button>

            {/* Delete */}
            <button
              onClick={() => onDelete(phase.id)}
              className="p-2 text-red-600 hover:text-red-800 rounded-lg hover:bg-red-50 transition-colors"
              title="Delete phase"
            >
              <Trash2 className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function PhasesPage() {
  const [phases, setPhases] = useState<Phase[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedPhase, setSelectedPhase] = useState<Phase | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

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
    loadPhases();
  }, []);

  const loadPhases = async () => {
    try {
      setLoading(true);
      const companyId = getCompanyId();
      if (!companyId) {
        setError('Company ID not found');
        return;
      }

      const data = await phaseService.listPhases(companyId);
      // Sort by sort_order
      const sortedData = data.sort((a, b) => a.sort_order - b.sort_order);
      setPhases(sortedData);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load phases');
      console.error('Error loading phases:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePhase = () => {
    setSelectedPhase(null);
    setModalOpen(true);
  };

  const handleEditPhase = (phase: Phase) => {
    setSelectedPhase(phase);
    setModalOpen(true);
  };

  const handleDeletePhase = async (phaseId: string) => {
    if (!confirm('Are you sure you want to delete this phase? This action cannot be undone.')) {
      return;
    }

    try {
      const companyId = getCompanyId();
      if (!companyId) {
        alert('Company ID not found');
        return;
      }

      await phaseService.deletePhase(companyId, phaseId);
      loadPhases();
    } catch (err: any) {
      alert('Failed to delete phase: ' + err.message);
    }
  };

  const handleMovePhaseUp = async (index: number) => {
    if (index === 0) return; // Already at the top

    const companyId = getCompanyId();
    if (!companyId) return;

    try {
      const currentPhase = phases[index];
      const previousPhase = phases[index - 1];

      // Swap sort orders
      await phaseService.updatePhase(companyId, currentPhase.id, {
        name: currentPhase.name,
        sort_order: previousPhase.sort_order,
        default_view: currentPhase.default_view,
        objective: currentPhase.objective || undefined,
      });

      await phaseService.updatePhase(companyId, previousPhase.id, {
        name: previousPhase.name,
        sort_order: currentPhase.sort_order,
        default_view: previousPhase.default_view,
        objective: previousPhase.objective || undefined,
      });

      loadPhases();
    } catch (err: any) {
      alert('Failed to reorder phases: ' + err.message);
    }
  };

  const handleMovePhaseDown = async (index: number) => {
    if (index === phases.length - 1) return; // Already at the bottom

    const companyId = getCompanyId();
    if (!companyId) return;

    try {
      const currentPhase = phases[index];
      const nextPhase = phases[index + 1];

      // Swap sort orders
      await phaseService.updatePhase(companyId, currentPhase.id, {
        name: currentPhase.name,
        sort_order: nextPhase.sort_order,
        default_view: currentPhase.default_view,
        objective: currentPhase.objective || undefined,
      });

      await phaseService.updatePhase(companyId, nextPhase.id, {
        name: nextPhase.name,
        sort_order: currentPhase.sort_order,
        default_view: nextPhase.default_view,
        objective: nextPhase.objective || undefined,
      });

      loadPhases();
    } catch (err: any) {
      alert('Failed to reorder phases: ' + err.message);
    }
  };

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;

    if (!over || active.id === over.id) {
      return;
    }

    const oldIndex = phases.findIndex((p) => p.id === active.id);
    const newIndex = phases.findIndex((p) => p.id === over.id);

    const newPhases = arrayMove(phases, oldIndex, newIndex);
    setPhases(newPhases);

    // Update sort_order on backend for all affected phases
    try {
      const companyId = getCompanyId();
      if (!companyId) return;

      // Update each phase with new sort_order
      await Promise.all(
        newPhases.map((phase, index) =>
          phaseService.updatePhase(companyId, phase.id, {
            name: phase.name,
            sort_order: index,
            default_view: phase.default_view,
            objective: phase.objective || undefined,
          })
        )
      );

      loadPhases(); // Refresh to get updated data
    } catch (err: any) {
      setError('Failed to reorder phases: ' + err.message);
      loadPhases(); // Revert on error
    }
  };

  const handleModalClose = () => {
    setModalOpen(false);
    setSelectedPhase(null);
  };

  const handleModalSuccess = () => {
    loadPhases();
  };

  const handleInitializeDefaults = async () => {
    if (!confirm('This will create 3 default phases with their workflows:\n\n1. Sourcing (Kanban) - Screening process\n2. Evaluation (Kanban) - Interview process\n3. Offer and Pre-Onboarding (List) - Offer negotiation\n\nContinue?')) {
      return;
    }

    try {
      const companyId = getCompanyId();
      if (!companyId) {
        alert('Company ID not found');
        return;
      }

      setLoading(true);
      await phaseService.initializeDefaultPhases(companyId);
      loadPhases();
    } catch (err: any) {
      alert('Failed to initialize default phases: ' + err.message);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const companyId = getCompanyId();
  if (!companyId) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">Company ID not found. Please log in again.</p>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Phase Management</h1>
          <p className="text-gray-600 mt-1">
            Organize your recruitment process into high-level phases
          </p>
        </div>
        <button
          onClick={handleCreatePhase}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Create Phase
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Phases List */}
      {phases.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <Layers className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No phases yet</h3>
          <p className="text-gray-600 mb-6">
            Get started quickly with our default phases or create your own custom phase
          </p>
          <div className="flex items-center justify-center gap-3">
            <button
              onClick={handleInitializeDefaults}
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Layers className="w-5 h-5" />
              Initialize Default Phases
            </button>
            <button
              onClick={handleCreatePhase}
              className="inline-flex items-center gap-2 px-4 py-2 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Plus className="w-5 h-5" />
              Create Custom Phase
            </button>
          </div>
        </div>
      ) : (
        <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
          <SortableContext items={phases.map((p) => p.id)} strategy={verticalListSortingStrategy}>
            <div className="space-y-4">
              {phases.map((phase, index) => (
                <SortablePhaseRow
                  key={phase.id}
                  phase={phase}
                  index={index}
                  onEdit={handleEditPhase}
                  onDelete={handleDeletePhase}
                  onMoveUp={handleMovePhaseUp}
                  onMoveDown={handleMovePhaseDown}
                  isFirst={index === 0}
                  isLast={index === phases.length - 1}
                />
              ))}
            </div>
          </SortableContext>
        </DndContext>
      )}

      {/* Info Box */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <div className="flex items-start gap-3">
          <Layers className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
          <div>
            <h4 className="font-semibold text-blue-900 mb-1">About Phases</h4>
            <p className="text-blue-800 text-sm mb-2">
              Phases are high-level organizational structures that group related workflows together.
              For example, you might have phases like "Sourcing & Screening", "Interview", and
              "Offer & Onboarding". Each phase can contain one or more workflows, and workflows can
              automatically transition candidates to the next phase when they reach a success stage.
            </p>
            <p className="text-blue-800 text-sm">
              <strong>Tip:</strong> Drag and drop phases using the grip handle to reorder them, or use the arrow buttons for precise positioning.
            </p>
          </div>
        </div>
      </div>

      {/* Form Modal */}
      <PhaseFormModal
        isOpen={modalOpen}
        onClose={handleModalClose}
        onSuccess={handleModalSuccess}
        companyId={companyId}
        phase={selectedPhase}
      />
    </div>
  );
}
