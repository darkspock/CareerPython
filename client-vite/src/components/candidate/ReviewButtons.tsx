/**
 * Review Buttons Component
 * 
 * Displays buttons for rating a candidate with scores:
 * - 0: Ban (prohibited)
 * - 3: Thumbs down (not recommended)
 * - 6: Thumbs up (recommended)
 * - 10: Favorite (highly recommended)
 */

import React from 'react';
import { Ban, ThumbsDown, ThumbsUp, Heart } from 'lucide-react';
import type { ReviewScore } from '../../types/candidateReview';

interface ReviewButtonsProps {
  onScoreSelect: (score: ReviewScore) => void;
  currentScore?: ReviewScore | null;
  disabled?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

const scoreConfig: Record<ReviewScore, { icon: React.ReactNode; label: string; color: string; bgColor: string }> = {
  0: {
    icon: <Ban className="w-5 h-5" />,
    label: 'Prohibido',
    color: 'text-red-600',
    bgColor: 'bg-red-50 hover:bg-red-100',
  },
  3: {
    icon: <ThumbsDown className="w-5 h-5" />,
    label: 'No recomendado',
    color: 'text-orange-600',
    bgColor: 'bg-orange-50 hover:bg-orange-100',
  },
  6: {
    icon: <ThumbsUp className="w-5 h-5" />,
    label: 'Recomendado',
    color: 'text-blue-600',
    bgColor: 'bg-blue-50 hover:bg-blue-100',
  },
  10: {
    icon: <Heart className="w-5 h-5" />,
    label: 'Favorito',
    color: 'text-pink-600',
    bgColor: 'bg-pink-50 hover:bg-pink-100',
  },
};

export default function ReviewButtons({
  onScoreSelect,
  currentScore,
  disabled = false,
  size = 'md',
}: ReviewButtonsProps) {
  const sizeClasses = {
    sm: 'p-2',
    md: 'p-3',
    lg: 'p-4',
  };

  const handleScoreClick = (score: ReviewScore) => {
    if (disabled) return;
    onScoreSelect(score);
  };

  return (
    <div className="flex items-center gap-2">
      {(Object.keys(scoreConfig) as ReviewScore[]).map((score) => {
        const config = scoreConfig[score];
        const isSelected = currentScore === score;

        return (
          <button
            key={score}
            type="button"
            onClick={() => handleScoreClick(score)}
            disabled={disabled}
            className={`
              ${sizeClasses[size]}
              rounded-lg
              border-2
              transition-all
              flex items-center gap-2
              ${isSelected 
                ? `${config.bgColor} ${config.color} border-current` 
                : 'bg-white border-gray-200 text-gray-600 hover:border-gray-300'
              }
              ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            `}
            title={config.label}
          >
            {config.icon}
            {size !== 'sm' && (
              <span className="text-sm font-medium">{score}</span>
            )}
          </button>
        );
      })}
    </div>
  );
}

