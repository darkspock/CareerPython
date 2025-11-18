import React, { useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { InterviewStatsResponse } from '../../services/companyInterviewService';

interface InterviewStatsProps {
  stats: InterviewStatsResponse | null;
  onFilterClick: (filterType: string) => void;
}

export const InterviewStats: React.FC<InterviewStatsProps> = ({ stats, onFilterClick }) => {
  const handleFilterClick = useCallback((filterType: string) => {
    onFilterClick(filterType);
  }, [onFilterClick]);

  if (!stats) return null;

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
      <Card
        className="cursor-pointer hover:shadow-md transition-shadow"
        onClick={() => handleFilterClick('pending_to_plan')}
      >
        <CardHeader className="pb-2">
          <CardTitle className="text-xs font-medium text-gray-600">
            Pendientes de Planificar
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-orange-600">
            {stats.pending_to_plan || 0}
          </div>
        </CardContent>
      </Card>
      
      <Card
        className="cursor-pointer hover:shadow-md transition-shadow"
        onClick={() => handleFilterClick('planned')}
      >
        <CardHeader className="pb-2">
          <CardTitle className="text-xs font-medium text-gray-600">
            Planificadas
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-blue-600">
            {stats.planned || 0}
          </div>
        </CardContent>
      </Card>
      
      <Card
        className="cursor-pointer hover:shadow-md transition-shadow"
        onClick={() => handleFilterClick('in_progress')}
      >
        <CardHeader className="pb-2">
          <CardTitle className="text-xs font-medium text-gray-600">
            En Proceso
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-green-600">
            {stats.in_progress_interviews || 0}
          </div>
        </CardContent>
      </Card>
      
      <Card
        className="cursor-pointer hover:shadow-md transition-shadow"
        onClick={() => handleFilterClick('recently_finished')}
      >
        <CardHeader className="pb-2">
          <CardTitle className="text-xs font-medium text-gray-600">
            Finalizadas Recientes
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-purple-600">
            {stats.recently_finished || 0}
          </div>
        </CardContent>
      </Card>
      
      <Card
        className="cursor-pointer hover:shadow-md transition-shadow"
        onClick={() => handleFilterClick('overdue')}
      >
        <CardHeader className="pb-2">
          <CardTitle className="text-xs font-medium text-gray-600">
            Pasadas Fecha Límite
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-red-600">
            {stats.overdue || 0}
          </div>
        </CardContent>
      </Card>
      
      <Card
        className="cursor-pointer hover:shadow-md transition-shadow"
        onClick={() => handleFilterClick('pending_feedback')}
      >
        <CardHeader className="pb-2">
          <CardTitle className="text-xs font-medium text-gray-600">
            Pendiente Feedback
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-yellow-600">
            {stats.pending_feedback || 0}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

