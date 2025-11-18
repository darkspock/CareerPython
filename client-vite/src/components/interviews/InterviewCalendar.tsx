import React, { useMemo, useCallback } from 'react';
import { Calendar } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { Interview } from '../../services/companyInterviewService';

interface InterviewCalendarProps {
  interviews: Interview[];
  loading: boolean;
  onDateClick: (date: Date) => void;
}

export const InterviewCalendar: React.FC<InterviewCalendarProps> = ({ 
  interviews, 
  loading, 
  onDateClick 
}) => {
  // Memoize interviews by date for performance
  const interviewsByDate = useMemo(() => {
    const map = new Map<string, number>();
    interviews.forEach(interview => {
      if (interview.scheduled_at) {
        const date = new Date(interview.scheduled_at);
        const dateKey = `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
        map.set(dateKey, (map.get(dateKey) || 0) + 1);
      }
    });
    return map;
  }, [interviews]);

  const getInterviewsForDate = useCallback((date: Date): number => {
    const dateKey = `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
    return interviewsByDate.get(dateKey) || 0;
  }, [interviewsByDate]);

  const handleDateClick = useCallback((date: Date) => {
    onDateClick(date);
  }, [onDateClick]);

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-sm font-medium text-gray-600 flex items-center gap-2">
          <Calendar className="w-4 h-4" />
          Calendario
        </CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-7 gap-1 text-xs">
            {['L', 'M', 'X', 'J', 'V', 'S', 'D'].map((day) => (
              <div key={day} className="text-center font-medium text-gray-500 p-1">
                {day}
              </div>
            ))}
            {Array.from({ length: 35 }, (_, i) => {
              const date = new Date();
              date.setDate(1);
              date.setDate(date.getDate() - date.getDay() + 1 + i);
              const isCurrentMonth = date.getMonth() === new Date().getMonth();
              const isToday = date.toDateString() === new Date().toDateString();
              const interviewCount = getInterviewsForDate(date);

              return (
                <div
                  key={i}
                  className={`text-center p-1 cursor-pointer rounded hover:bg-gray-100 ${
                    isCurrentMonth ? 'text-gray-900' : 'text-gray-400'
                  } ${isToday ? 'bg-blue-50 font-bold' : ''}`}
                  onClick={() => handleDateClick(date)}
                  title={`${interviewCount} entrevista(s)`}
                >
                  <div className="text-xs">{date.getDate()}</div>
                  {interviewCount > 0 && (
                    <div className="text-[8px] text-blue-600 font-bold mt-0.5">
                      {interviewCount}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

