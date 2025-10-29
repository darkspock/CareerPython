import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import type { CompanyCandidate } from '../../types/companyCandidate';

interface CandidateNameRowProps {
  candidate: CompanyCandidate;
  onClick?: () => void;
}

export const CandidateNameRow: React.FC<CandidateNameRowProps> = ({
  candidate,
  onClick
}) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: candidate.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  const handleClick = () => {
    onClick?.();
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="candidate-name-row"
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
