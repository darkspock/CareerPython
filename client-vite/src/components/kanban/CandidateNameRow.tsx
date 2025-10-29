import React from 'react';
import type { CompanyCandidate } from '../../types/companyCandidate';

interface CandidateNameRowProps {
  candidate: CompanyCandidate;
  onClick?: () => void;
}

export const CandidateNameRow: React.FC<CandidateNameRowProps> = ({
  candidate,
  onClick
}) => {
  const handleDragStart = (e: React.DragEvent) => {
    e.dataTransfer.setData('text/plain', candidate.id);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleClick = () => {
    onClick?.();
  };

  return (
    <div
      className="candidate-name-row"
      draggable
      onDragStart={handleDragStart}
      onClick={handleClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleClick();
        }
      }}
    >
      <span className="candidate-name">
        {candidate.candidate_name || 'Unnamed Candidate'}
      </span>
    </div>
  );
};
