/**
 * SkillsChips Component
 * Displays skills as chip/tag elements
 */
import React from 'react';
import { X } from 'lucide-react';

interface SkillsChipsProps {
  skills: string[];
  maxDisplay?: number;
  size?: 'sm' | 'md' | 'lg';
  onRemove?: (skill: string) => void;
  className?: string;
}

export const SkillsChips: React.FC<SkillsChipsProps> = ({
  skills,
  maxDisplay,
  size = 'md',
  onRemove,
  className = ''
}) => {
  if (!skills || skills.length === 0) {
    return null;
  }

  const displaySkills = maxDisplay ? skills.slice(0, maxDisplay) : skills;
  const remainingCount = maxDisplay ? skills.length - maxDisplay : 0;

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base'
  };

  return (
    <div className={`flex flex-wrap gap-2 ${className}`}>
      {displaySkills.map((skill, index) => (
        <span
          key={`${skill}-${index}`}
          className={`inline-flex items-center gap-1 font-medium rounded-full bg-indigo-50 text-indigo-700 ${sizeClasses[size]}`}
        >
          {skill}
          {onRemove && (
            <button
              type="button"
              onClick={() => onRemove(skill)}
              className="ml-0.5 hover:bg-indigo-100 rounded-full p-0.5"
            >
              <X size={12} />
            </button>
          )}
        </span>
      ))}
      {remainingCount > 0 && (
        <span
          className={`inline-flex items-center font-medium rounded-full bg-gray-100 text-gray-600 ${sizeClasses[size]}`}
        >
          +{remainingCount} more
        </span>
      )}
    </div>
  );
};

export default SkillsChips;
