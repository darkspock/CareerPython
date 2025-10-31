import React from 'react';
import { useTranslation } from 'react-i18next';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { useDroppable } from '@dnd-kit/core';
import type { WorkflowStage } from '../../types/workflow';
import type { CompanyCandidate } from '../../types/companyCandidate';
import { CandidateNameRow } from './CandidateNameRow';

interface RowStageSectionProps {
  stage: WorkflowStage;
  candidates: CompanyCandidate[];
  onCandidateClick?: (candidate: CompanyCandidate) => void;
}

export const RowStageSection: React.FC<RowStageSectionProps> = ({
  stage,
  candidates,
  onCandidateClick
}) => {
  const { t } = useTranslation();
  const { setNodeRef, isOver } = useDroppable({
    id: stage.id,
  });

  return (
    <div className="row-stage-section">
      <div 
        className="stage-header"
        style={{ 
          backgroundColor: stage.style.background_color,
          color: stage.style.color 
        }}
      >
        <div className="flex items-center gap-2">
          <span 
            className="text-lg"
            dangerouslySetInnerHTML={{ __html: stage.style.icon }}
          />
          <h3 className="stage-name">{stage.name}</h3>
        </div>
        <span 
          className="candidate-count"
          style={{ 
            backgroundColor: stage.style.color + '20', // 20% opacity
            color: stage.style.color 
          }}
        >
          ({candidates.length})
        </span>
      </div>
      
      <div 
        ref={setNodeRef}
        className={`candidates-row ${isOver ? 'drop-zone-active' : ''}`}
      >
        {candidates.length === 0 ? (
          <div className="empty-state">
            <span className="text-gray-500 text-sm">{t('company.workflowBoard.noCandidatesInStage')}</span>
          </div>
        ) : (
          <SortableContext items={candidates.map(c => c.id)} strategy={verticalListSortingStrategy}>
            {candidates.map((candidate) => (
              <CandidateNameRow
                key={candidate.id}
                candidate={candidate}
                onClick={() => onCandidateClick?.(candidate)}
              />
            ))}
          </SortableContext>
        )}
      </div>
    </div>
  );
};
