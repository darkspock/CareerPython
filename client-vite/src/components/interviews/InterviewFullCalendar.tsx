import React, { useMemo, useState, useCallback } from 'react';
import { ChevronLeft, ChevronRight, Clock, User, Briefcase } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import type { Interview, InterviewType } from '../../services/companyInterviewService';

type ViewMode = 'week' | 'month';

interface InterviewFullCalendarProps {
  interviews: Interview[];
  loading: boolean;
  onInterviewClick: (interviewId: string) => void;
  onDateClick?: (date: Date) => void;
}

// Color mapping for interview types
const interviewTypeColors: Record<InterviewType, { bg: string; text: string; border: string }> = {
  TECHNICAL: { bg: 'bg-blue-100', text: 'text-blue-800', border: 'border-blue-300' },
  BEHAVIORAL: { bg: 'bg-purple-100', text: 'text-purple-800', border: 'border-purple-300' },
  CULTURAL_FIT: { bg: 'bg-green-100', text: 'text-green-800', border: 'border-green-300' },
  KNOWLEDGE_CHECK: { bg: 'bg-yellow-100', text: 'text-yellow-800', border: 'border-yellow-300' },
  EXPERIENCE_CHECK: { bg: 'bg-orange-100', text: 'text-orange-800', border: 'border-orange-300' },
  CUSTOM: { bg: 'bg-gray-100', text: 'text-gray-800', border: 'border-gray-300' },
};

const interviewTypeLabels: Record<InterviewType, string> = {
  TECHNICAL: 'Tecnica',
  BEHAVIORAL: 'Conductual',
  CULTURAL_FIT: 'Ajuste Cultural',
  KNOWLEDGE_CHECK: 'Conocimientos',
  EXPERIENCE_CHECK: 'Experiencia',
  CUSTOM: 'Personalizada',
};

const getInterviewColor = (type: InterviewType) => {
  return interviewTypeColors[type] || interviewTypeColors.CUSTOM;
};

const formatTime = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
};


export const InterviewFullCalendar: React.FC<InterviewFullCalendarProps> = ({
  interviews,
  loading,
  onInterviewClick,
  onDateClick,
}) => {
  const [viewMode, setViewMode] = useState<ViewMode>('week');
  const [currentDate, setCurrentDate] = useState(new Date());

  // Get the start and end of the current view period
  const viewRange = useMemo(() => {
    const start = new Date(currentDate);
    const end = new Date(currentDate);

    if (viewMode === 'week') {
      // Start from Monday
      const day = start.getDay();
      const diff = start.getDate() - day + (day === 0 ? -6 : 1);
      start.setDate(diff);
      start.setHours(0, 0, 0, 0);

      end.setDate(start.getDate() + 6);
      end.setHours(23, 59, 59, 999);
    } else {
      // Month view
      start.setDate(1);
      start.setHours(0, 0, 0, 0);

      end.setMonth(end.getMonth() + 1);
      end.setDate(0);
      end.setHours(23, 59, 59, 999);
    }

    return { start, end };
  }, [currentDate, viewMode]);

  // Group interviews by date
  const interviewsByDate = useMemo(() => {
    const map = new Map<string, Interview[]>();

    interviews.forEach(interview => {
      if (interview.scheduled_at) {
        const date = new Date(interview.scheduled_at);
        const dateKey = date.toISOString().split('T')[0];

        if (!map.has(dateKey)) {
          map.set(dateKey, []);
        }
        map.get(dateKey)!.push(interview);
      }
    });

    // Sort interviews by time within each day
    map.forEach((dayInterviews) => {
      dayInterviews.sort((a, b) => {
        const timeA = new Date(a.scheduled_at!).getTime();
        const timeB = new Date(b.scheduled_at!).getTime();
        return timeA - timeB;
      });
    });

    return map;
  }, [interviews]);

  // Generate days for the current view
  const days = useMemo(() => {
    const result: Date[] = [];
    const current = new Date(viewRange.start);

    if (viewMode === 'week') {
      for (let i = 0; i < 7; i++) {
        result.push(new Date(current));
        current.setDate(current.getDate() + 1);
      }
    } else {
      // Month view - include days from prev/next month to fill grid
      const firstDay = new Date(viewRange.start);
      const startDay = firstDay.getDay();
      const daysFromPrevMonth = startDay === 0 ? 6 : startDay - 1;

      current.setDate(current.getDate() - daysFromPrevMonth);

      // Generate 6 weeks (42 days) to ensure full calendar
      for (let i = 0; i < 42; i++) {
        result.push(new Date(current));
        current.setDate(current.getDate() + 1);
      }
    }

    return result;
  }, [viewRange, viewMode]);

  const handlePrevious = useCallback(() => {
    const newDate = new Date(currentDate);
    if (viewMode === 'week') {
      newDate.setDate(newDate.getDate() - 7);
    } else {
      newDate.setMonth(newDate.getMonth() - 1);
    }
    setCurrentDate(newDate);
  }, [currentDate, viewMode]);

  const handleNext = useCallback(() => {
    const newDate = new Date(currentDate);
    if (viewMode === 'week') {
      newDate.setDate(newDate.getDate() + 7);
    } else {
      newDate.setMonth(newDate.getMonth() + 1);
    }
    setCurrentDate(newDate);
  }, [currentDate, viewMode]);

  const handleToday = useCallback(() => {
    setCurrentDate(new Date());
  }, []);

  const getHeaderTitle = () => {
    if (viewMode === 'week') {
      const startStr = viewRange.start.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' });
      const endStr = viewRange.end.toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' });
      return `${startStr} - ${endStr}`;
    }
    return currentDate.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });
  };

  const isToday = (date: Date) => {
    const today = new Date();
    return date.toDateString() === today.toDateString();
  };

  const isCurrentMonth = (date: Date) => {
    return date.getMonth() === currentDate.getMonth();
  };

  const renderInterviewCard = (interview: Interview) => {
    const colors = getInterviewColor(interview.interview_type);

    return (
      <Tooltip key={interview.id}>
        <TooltipTrigger asChild>
          <div
            onClick={() => onInterviewClick(interview.id)}
            className={`
              ${colors.bg} ${colors.border} border rounded px-2 py-1 mb-1 cursor-pointer
              hover:opacity-80 transition-opacity text-xs truncate
            `}
          >
            <div className="flex items-center gap-1">
              <Clock className="w-3 h-3 flex-shrink-0" />
              <span className="font-medium">{formatTime(interview.scheduled_at!)}</span>
            </div>
            <div className="truncate font-medium mt-0.5">
              {interview.candidate_name || 'Sin nombre'}
            </div>
          </div>
        </TooltipTrigger>
        <TooltipContent side="right" className="max-w-xs">
          <div className="space-y-2">
            <div className="font-semibold">{interview.title || interview.interview_template_name || 'Entrevista'}</div>
            <div className="flex items-center gap-2 text-sm">
              <User className="w-4 h-4" />
              {interview.candidate_name || 'Sin nombre'}
            </div>
            <div className="flex items-center gap-2 text-sm">
              <Clock className="w-4 h-4" />
              {formatTime(interview.scheduled_at!)}
            </div>
            {interview.job_position_title && (
              <div className="flex items-center gap-2 text-sm">
                <Briefcase className="w-4 h-4" />
                {interview.job_position_title}
              </div>
            )}
            <Badge className={`${colors.bg} ${colors.text} text-xs`}>
              {interviewTypeLabels[interview.interview_type]}
            </Badge>
          </div>
        </TooltipContent>
      </Tooltip>
    );
  };

  if (loading) {
    return (
      <Card>
        <CardContent className="pt-12 pb-12">
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600">Cargando calendario...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">{getHeaderTitle()}</CardTitle>
          <div className="flex items-center gap-2">
            {/* View Mode Toggle */}
            <div className="flex rounded-lg border overflow-hidden">
              <button
                onClick={() => setViewMode('week')}
                className={`px-3 py-1.5 text-sm font-medium transition-colors ${
                  viewMode === 'week'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-600 hover:bg-gray-100'
                }`}
              >
                Semana
              </button>
              <button
                onClick={() => setViewMode('month')}
                className={`px-3 py-1.5 text-sm font-medium transition-colors ${
                  viewMode === 'month'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-600 hover:bg-gray-100'
                }`}
              >
                Mes
              </button>
            </div>

            {/* Navigation */}
            <Button variant="outline" size="sm" onClick={handleToday}>
              Hoy
            </Button>
            <Button variant="outline" size="icon" onClick={handlePrevious}>
              <ChevronLeft className="w-4 h-4" />
            </Button>
            <Button variant="outline" size="icon" onClick={handleNext}>
              <ChevronRight className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap gap-2 mt-4">
          {Object.entries(interviewTypeLabels).map(([type, label]) => {
            const colors = interviewTypeColors[type as InterviewType];
            return (
              <div key={type} className="flex items-center gap-1">
                <div className={`w-3 h-3 rounded ${colors.bg} ${colors.border} border`} />
                <span className="text-xs text-gray-600">{label}</span>
              </div>
            );
          })}
        </div>
      </CardHeader>

      <CardContent>
        {viewMode === 'week' ? (
          // Week View
          <div className="grid grid-cols-7 gap-2">
            {/* Day Headers */}
            {days.map((day, index) => (
              <div
                key={index}
                className={`text-center p-2 font-medium ${
                  isToday(day) ? 'bg-blue-50 rounded-t-lg' : ''
                }`}
              >
                <div className="text-xs text-gray-500 uppercase">
                  {day.toLocaleDateString('es-ES', { weekday: 'short' })}
                </div>
                <div className={`text-lg ${isToday(day) ? 'text-blue-600 font-bold' : ''}`}>
                  {day.getDate()}
                </div>
              </div>
            ))}

            {/* Day Content */}
            {days.map((day, index) => {
              const dateKey = day.toISOString().split('T')[0];
              const dayInterviews = interviewsByDate.get(dateKey) || [];

              return (
                <div
                  key={`content-${index}`}
                  className={`min-h-[200px] border rounded-lg p-2 ${
                    isToday(day) ? 'bg-blue-50 border-blue-200' : 'bg-gray-50'
                  }`}
                  onClick={() => onDateClick?.(day)}
                >
                  {dayInterviews.length === 0 ? (
                    <div className="text-xs text-gray-400 text-center mt-4">
                      Sin entrevistas
                    </div>
                  ) : (
                    <div className="space-y-1">
                      {dayInterviews.slice(0, 5).map(renderInterviewCard)}
                      {dayInterviews.length > 5 && (
                        <div className="text-xs text-gray-500 text-center">
                          +{dayInterviews.length - 5} mas
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        ) : (
          // Month View
          <div className="grid grid-cols-7 gap-1">
            {/* Day Headers */}
            {['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom'].map((day) => (
              <div key={day} className="text-center p-2 font-medium text-xs text-gray-500 uppercase">
                {day}
              </div>
            ))}

            {/* Day Cells */}
            {days.map((day, index) => {
              const dateKey = day.toISOString().split('T')[0];
              const dayInterviews = interviewsByDate.get(dateKey) || [];
              const isCurrentMonthDay = isCurrentMonth(day);

              return (
                <div
                  key={index}
                  className={`min-h-[100px] border rounded p-1 cursor-pointer hover:bg-gray-100 transition-colors ${
                    isToday(day)
                      ? 'bg-blue-50 border-blue-300'
                      : isCurrentMonthDay
                      ? 'bg-white'
                      : 'bg-gray-50'
                  }`}
                  onClick={() => onDateClick?.(day)}
                >
                  <div
                    className={`text-xs font-medium mb-1 ${
                      isToday(day)
                        ? 'text-blue-600'
                        : isCurrentMonthDay
                        ? 'text-gray-900'
                        : 'text-gray-400'
                    }`}
                  >
                    {day.getDate()}
                  </div>
                  <div className="space-y-0.5">
                    {dayInterviews.slice(0, 3).map((interview) => {
                      const colors = getInterviewColor(interview.interview_type);
                      return (
                        <Tooltip key={interview.id}>
                          <TooltipTrigger asChild>
                            <div
                              onClick={(e) => {
                                e.stopPropagation();
                                onInterviewClick(interview.id);
                              }}
                              className={`${colors.bg} rounded px-1 py-0.5 text-[10px] truncate cursor-pointer hover:opacity-80`}
                            >
                              {formatTime(interview.scheduled_at!)} {interview.candidate_name?.split(' ')[0] || ''}
                            </div>
                          </TooltipTrigger>
                          <TooltipContent>
                            <div>
                              <div className="font-semibold">{interview.candidate_name}</div>
                              <div className="text-sm">{interview.title || interview.interview_template_name}</div>
                              <div className="text-sm">{formatTime(interview.scheduled_at!)}</div>
                            </div>
                          </TooltipContent>
                        </Tooltip>
                      );
                    })}
                    {dayInterviews.length > 3 && (
                      <div className="text-[10px] text-gray-500 text-center">
                        +{dayInterviews.length - 3}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
};
