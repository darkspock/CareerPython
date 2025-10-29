import React from 'react';
import type { WorkflowStage } from '../../types/workflow';
import type { CompanyCandidate } from '../../types/companyCandidate';
import { CandidateNameRow } from './CandidateNameRow';

interface RowStageSectionProps {
  stage: WorkflowStage;
  candidates: CompanyCandidate[];
  onCandidateClick?: (candidate: CompanyCandidate) => void;
  onDrop?: (candidateId: string, stageId: string) => void;
}

export const RowStageSection: React.FC<RowStageSectionProps> = ({
  stage,
  candidates,
  onCandidateClick,
  onDrop
}) => {
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const candidateId = e.dataTransfer.getData('text/plain');
    if (candidateId && onDrop) {
      onDrop(candidateId, stage.id);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  return (
    <div className="row-stage-section">
      <div className="stage-header">
        <h3 className="stage-name">{stage.name}</h3>
        <span className="candidate-count">({candidates.length})</span>
      </div>
      
      <div 
        className="candidates-row"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        {candidates.length === 0 ? (
          <div className="empty-state">
            <span className="text-gray-500 text-sm">No candidates in this stage</span>
          </div>
        ) : (
          candidates.map((candidate) => (
            <CandidateNameRow
              key={candidate.id}
              candidate={candidate}
              onClick={() => onCandidateClick?.(candidate)}
            />
          ))
        )}
      </div>
    </div>
  );
};
