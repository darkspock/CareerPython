import { useState, useMemo, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ArrowLeft, Edit, Move, ChevronDown, FileText } from 'lucide-react';
import type { CompanyCandidate } from '../../types/companyCandidate';
import type { WorkflowStage } from '../../types/workflow';
import { KanbanDisplay } from '../../types/workflow';
import CandidateReportModal from './CandidateReportModal';

interface CandidateHeaderProps {
  candidate: CompanyCandidate;
  candidateId: string;
  availableStages: WorkflowStage[];
  changingStage: boolean;
  showMoveToStageDropdown: boolean;
  onToggleMoveToStageDropdown: () => void;
  onMoveToStage: (stageId: string) => void;
  moveToStageDropdownRef: React.RefObject<HTMLDivElement | null>;
}

export default function CandidateHeader({
  candidate,
  candidateId,
  availableStages,
  changingStage,
  showMoveToStageDropdown,
  onToggleMoveToStageDropdown,
  onMoveToStage,
  moveToStageDropdownRef,
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
      <button
        onClick={() => navigate('/company/candidates')}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
      >
        <ArrowLeft className="w-5 h-5" />
        {t('company.candidates.backToCandidates')}
      </button>

      <div className="flex items-start justify-between">
        <div className="flex items-center gap-4">
          {/* Avatar */}
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
            <span className="text-2xl font-bold text-blue-600">
              {candidate.candidate_name?.charAt(0).toUpperCase() || 'C'}
            </span>
          </div>

          {/* Name & Email */}
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {candidate.candidate_name || 'N/A'}
            </h1>
            <p className="text-gray-600">{candidate.candidate_email || 'N/A'}</p>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowReportModal(true)}
            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            title={t('company.candidates.generateReport', 'Generate AI Report')}
          >
            <FileText className="w-4 h-4" />
            {t('company.candidates.report.button', 'Report')}
          </button>

          <button
            onClick={handleEditClick}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            title={t('company.candidates.editCandidateDetails')}
          >
            <Edit className="w-4 h-4" />
            {t('company.candidates.edit')}
          </button>

          {/* Move to Stage Dropdown */}
          {stagesToShow.stages.length > 0 && (
            <div ref={moveToStageDropdownRef} className="relative">
              <button
                onClick={onToggleMoveToStageDropdown}
                disabled={changingStage}
                className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                title={t('company.workflowBoard.moveToStage')}
              >
                <Move className="w-4 h-4" />
                {t('company.workflowBoard.moveToStage')}
                <ChevronDown className="w-4 h-4" />
              </button>

              {showMoveToStageDropdown && (
                <div className="absolute top-full right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-10 min-w-[200px]">
                  <div className="py-1">
                    {stagesToShow.stages.map((stage) => (
                      <button
                        key={stage.id}
                        onClick={() => onMoveToStage(stage.id)}
                        disabled={changingStage}
                        className="flex items-center gap-2 px-3 py-2 text-sm hover:bg-gray-50 w-full text-left disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <span
                          className="text-sm"
                          dangerouslySetInnerHTML={{ __html: stage.style?.icon || '' }}
                        />
                        <span className="text-gray-700">
                          {stage.name}
                          {stagesToShow.nextStageOption && stage.id === stagesToShow.nextStageOption.id && (
                            <span className="ml-2 text-blue-600 text-xs">
                              ({t('company.workflowBoard.nextStage')})
                            </span>
                          )}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
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

