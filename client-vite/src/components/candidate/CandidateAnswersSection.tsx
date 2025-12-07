/**
 * Candidate Answers Section
 * Displays application question answers for a candidate
 */

import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { HelpCircle, AlertCircle, CheckCircle, XCircle } from 'lucide-react';
import { ApiClient } from '../../lib/api';

interface ApplicationAnswer {
  id: string;
  application_id: string;
  question_id: string;
  field_key: string;
  answer_value: string;
  question_label?: string;
  question_type?: string;
  is_required?: boolean;
  created_at: string;
}

interface CandidateAnswersSectionProps {
  applicationId: string;
}

export function CandidateAnswersSection({ applicationId }: CandidateAnswersSectionProps) {
  const { t } = useTranslation();
  const [answers, setAnswers] = useState<ApplicationAnswer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (applicationId) {
      loadAnswers();
    }
  }, [applicationId]);

  const loadAnswers = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await ApiClient.get<ApplicationAnswer[]>(
        `/api/applications/${applicationId}/answers`
      );
      setAnswers(data);
    } catch (err: any) {
      if (err.message.includes('404') || err.message.includes('Not Found')) {
        // No answers yet - not an error
        setAnswers([]);
      } else {
        setError(err.message || t('candidateAnswers.loadError'));
      }
    } finally {
      setLoading(false);
    }
  };

  const formatAnswerValue = (answer: ApplicationAnswer): string => {
    const value = answer.answer_value;

    // Try to parse as JSON for array values (multiselect)
    try {
      const parsed = JSON.parse(value);
      if (Array.isArray(parsed)) {
        return parsed.join(', ');
      }
      // Handle boolean
      if (typeof parsed === 'boolean') {
        return parsed ? t('common.yes') : t('common.no');
      }
      return String(parsed);
    } catch {
      // Not JSON, return as-is
      // Handle boolean strings
      if (value === 'true') return t('common.yes');
      if (value === 'false') return t('common.no');
      return value;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-2">
        <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
        <p className="text-sm text-red-800">{error}</p>
      </div>
    );
  }

  if (answers.length === 0) {
    return (
      <div className="text-center py-8 bg-gray-50 rounded-lg border border-dashed border-gray-300">
        <HelpCircle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <p className="text-gray-600">{t('candidateAnswers.noAnswers')}</p>
        <p className="text-sm text-gray-500 mt-1">{t('candidateAnswers.noAnswersHint')}</p>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center gap-2 mb-4">
        <HelpCircle className="w-5 h-5 text-purple-600" />
        <h3 className="text-lg font-semibold text-gray-900">{t('candidateAnswers.title')}</h3>
      </div>

      <div className="space-y-4">
        {answers.map((answer) => (
          <div
            key={answer.id}
            className="p-4 bg-white border border-gray-200 rounded-lg"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-medium text-gray-900">
                    {answer.question_label || answer.field_key}
                  </span>
                  {answer.is_required && (
                    <span className="px-2 py-0.5 text-xs bg-red-100 text-red-700 rounded">
                      {t('candidateAnswers.required')}
                    </span>
                  )}
                </div>
                <p className="text-gray-700 mt-2">
                  {formatAnswerValue(answer) || (
                    <span className="text-gray-400 italic">{t('candidateAnswers.notAnswered')}</span>
                  )}
                </p>
              </div>
              <div className="flex-shrink-0">
                {answer.answer_value ? (
                  <CheckCircle className="w-5 h-5 text-green-600" />
                ) : (
                  <XCircle className="w-5 h-5 text-gray-400" />
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 text-sm text-gray-500 text-right">
        {t('candidateAnswers.count', { count: answers.length })}
      </div>
    </div>
  );
}

export default CandidateAnswersSection;
