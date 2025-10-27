/**
 * PhaseBadge Component
 * Phase 12: Display recruitment phase indicator with color coding
 */

import { useEffect, useState } from 'react';
import { Tag } from 'lucide-react';
import { phaseService } from '../../services/phaseService';
import type { Phase } from '../../types/phase';

interface PhaseBadgeProps {
  phaseId?: string;
  companyId: string;
  size?: 'sm' | 'md' | 'lg';
  showIcon?: boolean;
}

// Color palette for phases based on sort_order
const PHASE_COLORS = [
  'bg-blue-100 text-blue-800 border-blue-200',      // Phase 0: Sourcing
  'bg-purple-100 text-purple-800 border-purple-200', // Phase 1: Evaluation
  'bg-amber-100 text-amber-800 border-amber-200',    // Phase 2: Offer
  'bg-green-100 text-green-800 border-green-200',    // Phase 3: Talent Pool
  'bg-indigo-100 text-indigo-800 border-indigo-200', // Phase 4+
  'bg-pink-100 text-pink-800 border-pink-200',
  'bg-cyan-100 text-cyan-800 border-cyan-200',
];

export function PhaseBadge({
  phaseId,
  companyId,
  size = 'md',
  showIcon = true
}: PhaseBadgeProps) {
  const [phase, setPhase] = useState<Phase | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!phaseId || !companyId) {
      setLoading(false);
      return;
    }

    const fetchPhase = async () => {
      try {
        setLoading(true);
        const fetchedPhase = await phaseService.getPhase(companyId, phaseId);
        setPhase(fetchedPhase);
      } catch (error) {
        console.error('Error fetching phase:', error);
        setPhase(null);
      } finally {
        setLoading(false);
      }
    };

    fetchPhase();
  }, [phaseId, companyId]);

  if (loading) {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-400 animate-pulse">
        Loading...
      </span>
    );
  }

  if (!phase) {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-500">
        {showIcon && <Tag className="w-3 h-3" />}
        No Phase
      </span>
    );
  }

  // Get color based on sort_order
  const colorClass = PHASE_COLORS[phase.sort_order % PHASE_COLORS.length];

  // Size classes
  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base'
  };

  const iconSizes = {
    sm: 'w-3 h-3',
    md: 'w-3.5 h-3.5',
    lg: 'w-4 h-4'
  };

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full border font-medium ${colorClass} ${sizeClasses[size]}`}
      title={phase.objective || phase.name}
    >
      {showIcon && <Tag className={iconSizes[size]} />}
      {phase.name}
    </span>
  );
}
