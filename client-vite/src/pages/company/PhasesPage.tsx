import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, ArrowUp, ArrowDown, Layers, GripVertical, Archive, CheckCircle } from 'lucide-react';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { arrayMove, SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy, useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import type { DragEndEvent } from '@dnd-kit/core';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { phaseService } from '../../services/phaseService';
import type { Phase } from '../../types/phase';
import { PhaseStatus } from '../../types/phase';
import PhaseFormModal from '../../components/phases/PhaseFormModal';

// Sortable Phase Row Component
function SortablePhaseRow({
  phase,
  index,
  onEdit,
  onDelete,
  onArchive,
  onActivate,
  onMoveUp,
  onMoveDown,
  isFirst,
  isLast
}: {
  phase: Phase;
  index: number;
  onEdit: (phase: Phase) => void;
  onDelete: (phaseId: string) => void;
  onArchive: (phaseId: string) => void;
  onActivate: (phaseId: string) => void;
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

  const getWorkflowTypeLabel = (type: string): string => {
    switch (type) {
      case 'CA':
        return 'Candidate Application';
      case 'PO':
        return 'Job Position Opening';
      case 'CO':
        return 'Candidate Onboarding';
      default:
        return type;
    }
  };

  return (
    <Card
      ref={setNodeRef}
      style={style}
      className="hover:shadow-md transition-shadow"
    >
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          {/* Drag Handle */}
          <div
            {...attributes}
            {...listeners}
            className="cursor-grab active:cursor-grabbing text-muted-foreground hover:text-foreground mr-4 mt-1"
          >
            <GripVertical className="w-5 h-5" />
          </div>

          {/* Phase Info */}
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-sm font-medium text-muted-foreground">
                #{phase.sort_order}
              </span>
              <h3 className="text-lg font-semibold text-gray-900">
                {phase.name}
              </h3>
              {/* Workflow Type Badge */}
              <Badge variant="secondary" className="bg-purple-100 text-purple-800">
                {getWorkflowTypeLabel(phase.workflow_type)}
              </Badge>
              <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                {getDefaultViewLabel(phase.default_view)}
              </Badge>
              {/* Status Badge */}
              <Badge
                variant={
                  phase.status === PhaseStatus.ACTIVE
                    ? 'default'
                    : phase.status === PhaseStatus.DRAFT
                    ? 'secondary'
                    : 'destructive'
                }
                className={
                  phase.status === PhaseStatus.ACTIVE
                    ? 'bg-green-100 text-green-800'
                    : phase.status === PhaseStatus.DRAFT
                    ? 'bg-gray-100 text-gray-700'
                    : 'bg-red-100 text-red-700'
                }
              >
                {phase.status}
              </Badge>
            </div>

            {phase.objective && (
              <p className="text-sm text-muted-foreground mt-2">
                {phase.objective}
              </p>
            )}

            <div className="mt-3 text-xs text-muted-foreground">
              <span>Created: {new Date(phase.created_at).toLocaleDateString()}</span>
              {phase.updated_at !== phase.created_at && (
                <span className="ml-3">
                  Updated: {new Date(phase.updated_at).toLocaleDateString()}
                </span>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-1 ml-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onMoveUp(index)}
              disabled={isFirst}
              title="Move up"
            >
              <ArrowUp className="w-4 h-4" />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={() => onMoveDown(index)}
              disabled={isLast}
              title="Move down"
            >
              <ArrowDown className="w-4 h-4" />
            </Button>

            {phase.status !== PhaseStatus.ACTIVE && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onActivate(phase.id)}
                className="text-green-600 hover:text-green-800 hover:bg-green-50"
                title="Activate phase"
              >
                <CheckCircle className="w-4 h-4" />
              </Button>
            )}

            {phase.status === PhaseStatus.ACTIVE && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onArchive(phase.id)}
                className="text-orange-600 hover:text-orange-800 hover:bg-orange-50"
                title="Archive phase"
              >
                <Archive className="w-4 h-4" />
              </Button>
            )}

            <Button
              variant="ghost"
              size="icon"
              onClick={() => onEdit(phase)}
              className="text-blue-600 hover:text-blue-800 hover:bg-blue-50"
              title="Edit phase"
            >
              <Edit className="w-4 h-4" />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={() => onDelete(phase.id)}
              className="text-red-600 hover:text-red-800 hover:bg-red-50"
              title="Delete phase"
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

// Workflow Types
const WORKFLOW_TYPES = {
  CA: { value: 'CA', label: 'Candidate Application' },
  PO: { value: 'PO', label: 'Job Position Opening' },
  CO: { value: 'CO', label: 'Candidate Onboarding' },
} as const;

type WorkflowTypeFilter = 'CA' | 'PO' | 'CO';

export default function PhasesPage() {
  const [phases, setPhases] = useState<Phase[]>([]);
  const [filteredPhases, setFilteredPhases] = useState<Phase[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedPhase, setSelectedPhase] = useState<Phase | null>(null);
  const [activeTypeFilter, setActiveTypeFilter] = useState<WorkflowTypeFilter>('CA');

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

  useEffect(() => {
    setFilteredPhases(phases.filter(phase => phase.workflow_type === activeTypeFilter));
  }, [phases, activeTypeFilter]);

  const loadPhases = async () => {
    try {
      setLoading(true);
      const companyId = getCompanyId();
      if (!companyId) {
        setError('Company ID not found');
        return;
      }

      const data = await phaseService.listPhases(companyId);
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

  const handleArchivePhase = async (phaseId: string) => {
    if (!confirm('Are you sure you want to archive this phase? Archived phases are hidden but not deleted.')) {
      return;
    }

    try {
      const companyId = getCompanyId();
      if (!companyId) {
        alert('Company ID not found');
        return;
      }

      await phaseService.archivePhase(companyId, phaseId);
      loadPhases();
    } catch (err: any) {
      alert('Failed to archive phase: ' + err.message);
    }
  };

  const handleActivatePhase = async (phaseId: string) => {
    try {
      const companyId = getCompanyId();
      if (!companyId) {
        alert('Company ID not found');
        return;
      }

      await phaseService.activatePhase(companyId, phaseId);
      loadPhases();
    } catch (err: any) {
      alert('Failed to activate phase: ' + err.message);
    }
  };

  const handleMovePhaseUp = async (index: number) => {
    if (index === 0) return;

    const companyId = getCompanyId();
    if (!companyId) return;

    try {
      const currentPhase = phases[index];
      const previousPhase = phases[index - 1];

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
    if (index === phases.length - 1) return;

    const companyId = getCompanyId();
    if (!companyId) return;

    try {
      const currentPhase = phases[index];
      const nextPhase = phases[index + 1];

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

    try {
      const companyId = getCompanyId();
      if (!companyId) return;

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

      loadPhases();
    } catch (err: any) {
      setError('Failed to reorder phases: ' + err.message);
      loadPhases();
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
    if (!confirm('This will ARCHIVE all existing phases and create 3 new default phases:\n\n1. Sourcing (Kanban) - Screening process\n2. Evaluation (Kanban) - Interview process\n3. Offer and Pre-Onboarding (List) - Offer negotiation\n\nYour existing phases will be archived but not deleted.\n\nContinue?')) {
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
      <Alert variant="destructive">
        <AlertDescription>Company ID not found. Please log in again.</AlertDescription>
      </Alert>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Phase Management v2</h1>
          <p className="text-muted-foreground mt-1">
            Organize your recruitment process into high-level phases
          </p>
        </div>
        <Button onClick={handleCreatePhase}>
          <Plus className="w-4 h-4 mr-2" />
          Create Phase
        </Button>
      </div>

      {/* Error Message */}
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Workflow Type Filter Tabs */}
      <div className="mb-6">
        <Tabs value={activeTypeFilter} onValueChange={(value) => setActiveTypeFilter(value as WorkflowTypeFilter)}>
          <TabsList>
            {Object.values(WORKFLOW_TYPES).map((type) => (
              <TabsTrigger key={type.value} value={type.value}>
                {type.label}
              </TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
      </div>

      {/* Phases List */}
      {phases.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <Layers className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No phases yet</h3>
            <p className="text-muted-foreground mb-6">
              Get started quickly with our default phases or create your own custom phase
            </p>
            <div className="flex items-center justify-center gap-3">
              <Button onClick={handleInitializeDefaults}>
                <Layers className="w-4 h-4 mr-2" />
                Initialize Default Phases
              </Button>
              <Button variant="outline" onClick={handleCreatePhase}>
                <Plus className="w-4 h-4 mr-2" />
                Create Custom Phase
              </Button>
            </div>
          </CardContent>
        </Card>
      ) : filteredPhases.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <Layers className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No phases found</h3>
            <p className="text-muted-foreground mb-6">
              No phases match the selected filter. Try selecting a different workflow type.
            </p>
          </CardContent>
        </Card>
      ) : (
        <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
          <SortableContext items={filteredPhases.map((p) => p.id)} strategy={verticalListSortingStrategy}>
            <div className="space-y-4">
              {filteredPhases.map((phase, index) => (
                <SortablePhaseRow
                  key={phase.id}
                  phase={phase}
                  index={index}
                  onEdit={handleEditPhase}
                  onDelete={handleDeletePhase}
                  onArchive={handleArchivePhase}
                  onActivate={handleActivatePhase}
                  onMoveUp={handleMovePhaseUp}
                  onMoveDown={handleMovePhaseDown}
                  isFirst={index === 0}
                  isLast={index === filteredPhases.length - 1}
                />
              ))}
            </div>
          </SortableContext>
        </DndContext>
      )}

      {/* Info Box */}
      <Alert className="mt-8 border-blue-200 bg-blue-50">
        <Layers className="w-5 h-5 text-blue-600" />
        <AlertDescription className="text-blue-800">
          <h4 className="font-semibold text-blue-900 mb-1">About Phases</h4>
          <p className="text-sm mb-2">
            Phases are high-level organizational structures that group related workflows together.
            For example, you might have phases like "Sourcing & Screening", "Interview", and
            "Offer & Onboarding". Each phase can contain one or more workflows, and workflows can
            automatically transition candidates to the next phase when they reach a success stage.
          </p>
          <p className="text-sm">
            <strong>Tip:</strong> Drag and drop phases using the grip handle to reorder them, or use the arrow buttons for precise positioning.
          </p>
        </AlertDescription>
      </Alert>

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
