import { useState, useMemo, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ArrowLeft, Edit, Move, ChevronDown, FileText } from 'lucide-react';
import type { CompanyCandidate } from '../../types/companyCandidate';
import type { WorkflowStage } from '../../types/workflow';
import { KanbanDisplay } from '../../types/workflow';
import CandidateReportModal from './CandidateReportModal';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface CandidateHeaderProps {
  candidate: CompanyCandidate;
  candidateId: string;
  availableStages: WorkflowStage[];
  changingStage: boolean;
  onMoveToStage: (stageId: string) => void;
}

export default function CandidateHeader({
  candidate,
  candidateId,
  availableStages,
  changingStage,
  onMoveToStage,
}: CandidateHeaderProps) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [showReportModal, setShowReportModal] = useState(false);

  const stagesToShow = useMemo((): { stages: WorkflowStage[]; nextStageOption: WorkflowStage | null } => {
    if (availableStages.length === 0) return { stages: [], nextStageOption: null };

    const currentStage = candidate.current_stage_id
      ? availableStages.find((s) => s.id === candidate.current_stage_id)
      : null;

    const nextStageOption = currentStage
      ? availableStages
          .filter((s) => s.order > currentStage.order && s.is_active)
          .sort((a, b) => a.order - b.order)[0] || null
      : null;

    const hiddenOrRowStages = availableStages.filter((s) => {
      if (!s.is_active || s.id === candidate.current_stage_id) return false;
      const display = s.kanban_display;
      return display === KanbanDisplay.ROW || display === KanbanDisplay.NONE;
    });

    const stages = [
      ...(nextStageOption ? [nextStageOption] : []),
      ...hiddenOrRowStages.filter((s) => !nextStageOption || s.id !== nextStageOption.id),
    ].sort((a, b) => a.order - b.order);

    return { stages, nextStageOption };
  }, [availableStages, candidate.current_stage_id]);

  const handleEditClick = useCallback(() => {
    navigate(`/company/candidates/${candidateId}/edit`);
  }, [navigate, candidateId]);

  if (stagesToShow.stages.length === 0 && availableStages.length === 0) {
    return null;
  }

  return (
    <div className="mb-6">
      <Button
        variant="ghost"
        onClick={() => navigate('/company/candidates')}
        className="mb-4 text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="w-5 h-5 mr-2" />
        {t('company.candidates.backToCandidates')}
      </Button>

      <div className="flex items-start justify-between">
        <div className="flex items-center gap-4">
          {/* Avatar */}
          <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
            <span className="text-2xl font-bold text-primary">
              {candidate.candidate_name?.charAt(0).toUpperCase() || 'C'}
            </span>
          </div>

          {/* Name & Email */}
          <div>
            <h1 className="text-2xl font-bold text-foreground">
              {candidate.candidate_name || 'N/A'}
            </h1>
            <p className="text-muted-foreground">{candidate.candidate_email || 'N/A'}</p>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <Button
            variant="default"
            onClick={() => setShowReportModal(true)}
            className="bg-green-600 hover:bg-green-700"
            title={t('company.candidates.generateReport', 'Generate AI Report')}
          >
            <FileText className="w-4 h-4 mr-2" />
            {t('company.candidates.report.button', 'Report')}
          </Button>

          <Button
            variant="default"
            onClick={handleEditClick}
            title={t('company.candidates.editCandidateDetails')}
          >
            <Edit className="w-4 h-4 mr-2" />
            {t('company.candidates.edit')}
          </Button>

          {/* Move to Stage Dropdown */}
          {stagesToShow.stages.length > 0 && (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="default"
                  disabled={changingStage}
                  className="bg-purple-600 hover:bg-purple-700"
                >
                  <Move className="w-4 h-4 mr-2" />
                  {t('company.workflowBoard.moveToStage')}
                  <ChevronDown className="w-4 h-4 ml-2" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="min-w-[200px]">
                {stagesToShow.stages.map((stage) => (
                  <DropdownMenuItem
                    key={stage.id}
                    onClick={() => onMoveToStage(stage.id)}
                    disabled={changingStage}
                    className="cursor-pointer"
                  >
                    <span
                      className="text-sm mr-2"
                      dangerouslySetInnerHTML={{ __html: stage.style?.icon || '' }}
                    />
                    <span>
                      {stage.name}
                      {stagesToShow.nextStageOption && stage.id === stagesToShow.nextStageOption.id && (
                        <span className="ml-2 text-primary text-xs">
                          ({t('company.workflowBoard.nextStage')})
                        </span>
                      )}
                    </span>
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
      </div>

      {/* Report Modal */}
      <CandidateReportModal
        isOpen={showReportModal}
        onClose={() => setShowReportModal(false)}
        companyCandidateId={candidateId}
        candidateName={candidate.candidate_name || 'Candidate'}
      />
    </div>
  );
}

