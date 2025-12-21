/**
 * Candidate Answers Section
 * Displays application question answers for a candidate
 */

import { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { HelpCircle, CheckCircle, XCircle } from 'lucide-react';
import { ApiClient } from '../../lib/api';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import EmptyState from '@/components/common/EmptyState';

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

  const loadAnswers = useCallback(async () => {
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
  }, [applicationId, t]);

  useEffect(() => {
    if (applicationId) {
      loadAnswers();
    }
  }, [applicationId, loadAnswers]);

  const formatAnswerValue = useCallback((answer: ApplicationAnswer): string => {
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
  }, [t]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <LoadingSpinner size="lg" color="blue" />
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  if (answers.length === 0) {
    return (
      <EmptyState
        icon={HelpCircle}
        title={t('candidateAnswers.noAnswers')}
        description={t('candidateAnswers.noAnswersHint')}
        size="md"
      />
    );
  }

  return (
    <div>
      <div className="flex items-center gap-2 mb-4">
        <HelpCircle className="w-5 h-5 text-primary" />
        <h3 className="text-lg font-semibold text-foreground">{t('candidateAnswers.title')}</h3>
      </div>

      <div className="space-y-4">
        {answers.map((answer) => (
          <Card key={answer.id}>
            <CardContent className="pt-4">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium text-foreground">
                      {answer.question_label || answer.field_key}
                    </span>
                    {answer.is_required && (
                      <Badge variant="destructive" className="text-xs">
                        {t('candidateAnswers.required')}
                      </Badge>
                    )}
                  </div>
                  <p className="text-muted-foreground mt-2">
                    {formatAnswerValue(answer) || (
                      <span className="italic">{t('candidateAnswers.notAnswered')}</span>
                    )}
                  </p>
                </div>
                <div className="flex-shrink-0">
                  {answer.answer_value ? (
                    <CheckCircle className="w-5 h-5 text-green-600" />
                  ) : (
                    <XCircle className="w-5 h-5 text-muted-foreground" />
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="mt-4 text-sm text-muted-foreground text-right">
        {t('candidateAnswers.count', { count: answers.length })}
      </div>
    </div>
  );
}

export default CandidateAnswersSection;
