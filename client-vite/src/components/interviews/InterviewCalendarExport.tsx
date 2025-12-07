/**
 * Interview Calendar Export Component
 * Provides options to add interviews to external calendars
 */

import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Calendar, Download, ExternalLink, Copy, Check } from 'lucide-react';
import { ApiClient } from '../../lib/api';

interface CalendarLinks {
  google_calendar_url: string;
  outlook_url: string;
  ics_download_url: string;
  interview_id: string;
  scheduled_at: string | null;
}

interface InterviewCalendarExportProps {
  interviewId: string;
  scheduledAt?: string | Date | null;
  variant?: 'button' | 'dropdown' | 'inline';
  className?: string;
}

export function InterviewCalendarExport({
  interviewId,
  scheduledAt,
  variant = 'dropdown',
  className = ''
}: InterviewCalendarExportProps) {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [calendarLinks, setCalendarLinks] = useState<CalendarLinks | null>(null);
  const [copied, setCopied] = useState(false);

  // Don't render if not scheduled
  if (!scheduledAt) {
    return null;
  }

  const fetchCalendarLinks = async () => {
    if (calendarLinks) return calendarLinks;

    setLoading(true);
    try {
      const links = await ApiClient.get<CalendarLinks>(
        `/api/company/interviews/${interviewId}/calendar-links`
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

  const handleOpenDropdown = async () => {
    setIsOpen(!isOpen);
    if (!isOpen && !calendarLinks) {
      await fetchCalendarLinks();
    }
  };

  const handleDownloadIcs = async () => {
    const links = calendarLinks || await fetchCalendarLinks();
    if (links) {
      window.location.href = links.ics_download_url;
    }
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

  const handleCopyLink = async () => {
    const links = calendarLinks || await fetchCalendarLinks();
    if (links) {
      const fullUrl = `${window.location.origin}${links.ics_download_url}`;
      await navigator.clipboard.writeText(fullUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (variant === 'button') {
    return (
      <button
        onClick={handleDownloadIcs}
        disabled={loading}
        className={`inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 ${className}`}
      >
        <Calendar className="w-4 h-4" />
        {t('calendar.download')}
      </button>
    );
  }

  if (variant === 'inline') {
    return (
      <div className={`flex items-center gap-2 ${className}`}>
        <button
          onClick={handleOpenGoogleCalendar}
          disabled={loading}
          className="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded"
          title={t('calendar.addToGoogle')}
        >
          <ExternalLink className="w-3 h-3" />
          Google
        </button>
        <button
          onClick={handleOpenOutlook}
          disabled={loading}
          className="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded"
          title={t('calendar.addToOutlook')}
        >
          <ExternalLink className="w-3 h-3" />
          Outlook
        </button>
        <button
          onClick={handleDownloadIcs}
          disabled={loading}
          className="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium text-gray-600 hover:text-gray-700 hover:bg-gray-50 rounded"
          title={t('calendar.download')}
        >
          <Download className="w-3 h-3" />
          .ics
        </button>
      </div>
    );
  }

  // Default: dropdown variant
  return (
    <div className={`relative ${className}`}>
      <button
        onClick={handleOpenDropdown}
        disabled={loading}
        className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
      >
        <Calendar className="w-4 h-4" />
        {t('calendar.addToCalendar', 'Add to Calendar')}
        {loading && (
          <span className="w-4 h-4 border-2 border-gray-300 border-t-gray-600 rounded-full animate-spin" />
        )}
      </button>

      {isOpen && calendarLinks && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />

          {/* Dropdown Menu */}
          <div className="absolute right-0 z-20 mt-2 w-56 bg-white border border-gray-200 rounded-lg shadow-lg">
            <div className="py-1">
              <button
                onClick={handleOpenGoogleCalendar}
                className="flex items-center gap-3 w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
              >
                <ExternalLink className="w-4 h-4 text-gray-400" />
                {t('calendar.addToGoogle', 'Add to Google Calendar')}
              </button>

              <button
                onClick={handleOpenOutlook}
                className="flex items-center gap-3 w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
              >
                <ExternalLink className="w-4 h-4 text-gray-400" />
                {t('calendar.addToOutlook', 'Add to Outlook')}
              </button>

              <hr className="my-1 border-gray-200" />

              <button
                onClick={handleDownloadIcs}
                className="flex items-center gap-3 w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
              >
                <Download className="w-4 h-4 text-gray-400" />
                {t('calendar.download', 'Download .ics')}
              </button>

              <button
                onClick={handleCopyLink}
                className="flex items-center gap-3 w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
              >
                {copied ? (
                  <>
                    <Check className="w-4 h-4 text-green-500" />
                    {t('calendar.linkCopied', 'Link copied!')}
                  </>
                ) : (
                  <>
                    <Copy className="w-4 h-4 text-gray-400" />
                    {t('calendar.copyLink', 'Copy Calendar Link')}
                  </>
                )}
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default InterviewCalendarExport;
