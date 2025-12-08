/**
 * Interview Calendar Button Component (for Candidates)
 * Simple button to add interview to calendar
 */

import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Calendar, Download, ChevronDown } from 'lucide-react';
import { ApiClient } from '../../lib/api';

interface CalendarLinks {
  google_calendar_url: string;
  outlook_url: string;
  ics_download_url: string;
  interview_id: string;
  scheduled_at: string | null;
}

interface InterviewCalendarButtonProps {
  interviewId: string;
  token: string;
  scheduledAt?: string | Date | null;
  className?: string;
}

export function InterviewCalendarButton({
  interviewId,
  token,
  scheduledAt,
  className = ''
}: InterviewCalendarButtonProps) {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [calendarLinks, setCalendarLinks] = useState<CalendarLinks | null>(null);

  // Don't render if not scheduled
  if (!scheduledAt) {
    return null;
  }

  const fetchCalendarLinks = async () => {
    if (calendarLinks) return calendarLinks;

    setLoading(true);
    try {
      const links = await ApiClient.get<CalendarLinks>(
        `/api/candidate/interviews/${interviewId}/calendar-links?token=${token}`
      );
      setCalendarLinks(links);
      return links;
    } catch (error) {
      console.error('Failed to fetch calendar links:', error);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async () => {
    if (!isOpen && !calendarLinks) {
      await fetchCalendarLinks();
    }
    setIsOpen(!isOpen);
  };

  const handleOpenGoogleCalendar = async () => {
    const links = calendarLinks || await fetchCalendarLinks();
    if (links) {
      window.open(links.google_calendar_url, '_blank');
    }
    setIsOpen(false);
  };

  const handleOpenOutlook = async () => {
    const links = calendarLinks || await fetchCalendarLinks();
    if (links) {
      window.open(links.outlook_url, '_blank');
    }
    setIsOpen(false);
  };

  const handleDownloadIcs = async () => {
    const links = calendarLinks || await fetchCalendarLinks();
    if (links) {
      window.location.href = links.ics_download_url;
    }
    setIsOpen(false);
  };

  return (
    <div className={`relative ${className}`}>
      <button
        onClick={handleToggle}
        disabled={loading}
        className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
      >
        <Calendar className="w-4 h-4" />
        {t('calendar.addToCalendar', 'Add to Calendar')}
        <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        {loading && (
          <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
        )}
      </button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />

          {/* Dropdown Menu */}
          <div className="absolute left-0 z-20 mt-2 w-52 bg-white border border-gray-200 rounded-lg shadow-lg">
            <div className="py-1">
              <button
                onClick={handleOpenGoogleCalendar}
                className="flex items-center gap-3 w-full px-4 py-3 text-sm text-gray-700 hover:bg-gray-50"
              >
                <div className="w-5 h-5 flex items-center justify-center">
                  <svg viewBox="0 0 24 24" className="w-5 h-5">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                  </svg>
                </div>
                Google Calendar
              </button>

              <button
                onClick={handleOpenOutlook}
                className="flex items-center gap-3 w-full px-4 py-3 text-sm text-gray-700 hover:bg-gray-50"
              >
                <div className="w-5 h-5 flex items-center justify-center">
                  <svg viewBox="0 0 24 24" className="w-5 h-5">
                    <path fill="#0078D4" d="M24 7.387v10.478c0 .23-.08.424-.238.576-.153.153-.35.234-.584.234h-9.644V6.577h9.644c.235 0 .431.078.584.234.159.152.238.35.238.576zM13.534 18.675V5.325L0 8.073v7.854l13.534 2.748z"/>
                    <path fill="#0078D4" d="M7.877 10.143c-.597 0-1.07.155-1.421.464-.35.31-.526.728-.526 1.256 0 .518.169.932.507 1.241.337.31.793.464 1.368.464.585 0 1.063-.151 1.433-.452.37-.302.556-.71.556-1.225 0-.537-.176-.962-.528-1.275-.352-.315-.816-.473-1.389-.473z"/>
                  </svg>
                </div>
                Outlook
              </button>

              <hr className="my-1 border-gray-200" />

              <button
                onClick={handleDownloadIcs}
                className="flex items-center gap-3 w-full px-4 py-3 text-sm text-gray-700 hover:bg-gray-50"
              >
                <Download className="w-5 h-5 text-gray-400" />
                {t('calendar.download', 'Download .ics file')}
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default InterviewCalendarButton;
