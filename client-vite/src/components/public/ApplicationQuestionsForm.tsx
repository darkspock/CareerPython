/**
 * Application Questions Form
 * Component for displaying and answering application questions
 */

import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { HelpCircle, AlertCircle } from 'lucide-react';
import {
  publicQuestionService,
  type PublicApplicationQuestion,
} from '../../services/publicQuestionService';

interface ApplicationQuestionsFormProps {
  positionId: string;
  onAnswersChange?: (answers: Record<string, unknown>, isValid: boolean) => void;
  readOnly?: boolean;
  initialAnswers?: Record<string, unknown>;
}

export function ApplicationQuestionsForm({
  positionId,
  onAnswersChange,
  readOnly = false,
  initialAnswers = {},
}: ApplicationQuestionsFormProps) {
  const { t } = useTranslation();
  const [questions, setQuestions] = useState<PublicApplicationQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<string, unknown>>(initialAnswers);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (positionId) {
      loadQuestions();
    }
  }, [positionId]);

  useEffect(() => {
    if (onAnswersChange) {
      const isValid = validateAnswers();
      onAnswersChange(answers, isValid);
    }
  }, [answers]);

  const loadQuestions = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await publicQuestionService.getQuestionsForPosition(positionId);
      setQuestions(data.sort((a, b) => a.sort_order - b.sort_order));
    } catch (err: any) {
      setError(err.message || t('publicQuestions.loadError'));
    } finally {
      setLoading(false);
    }
  };

  const validateAnswers = (): boolean => {
    for (const question of questions) {
      if (question.is_required) {
        const answer = answers[question.field_key];
        if (answer === undefined || answer === null || answer === '') {
          return false;
        }
        if (Array.isArray(answer) && answer.length === 0) {
          return false;
        }
      }
    }
    return true;
  };

  const handleAnswerChange = (fieldKey: string, value: unknown) => {
    setAnswers((prev) => ({
      ...prev,
      [fieldKey]: value,
    }));
  };

  const renderInput = (question: PublicApplicationQuestion) => {
    const value = answers[question.field_key];

    switch (question.field_type) {
      case 'TEXT':
        return (
          <input
            type="text"
            value={(value as string) || ''}
            onChange={(e) => handleAnswerChange(question.field_key, e.target.value)}
            disabled={readOnly}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
            placeholder={t('publicQuestions.enterAnswer')}
          />
        );

      case 'TEXTAREA':
        return (
          <textarea
            value={(value as string) || ''}
            onChange={(e) => handleAnswerChange(question.field_key, e.target.value)}
            disabled={readOnly}
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
            placeholder={t('publicQuestions.enterAnswer')}
          />
        );

      case 'NUMBER':
        return (
          <input
            type="number"
            value={(value as number) ?? ''}
            onChange={(e) => handleAnswerChange(question.field_key, e.target.value ? Number(e.target.value) : '')}
            disabled={readOnly}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
            placeholder={t('publicQuestions.enterNumber')}
          />
        );

      case 'DATE':
        return (
          <input
            type="date"
            value={(value as string) || ''}
            onChange={(e) => handleAnswerChange(question.field_key, e.target.value)}
            disabled={readOnly}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
          />
        );

      case 'SELECT':
        return (
          <select
            value={(value as string) || ''}
            onChange={(e) => handleAnswerChange(question.field_key, e.target.value)}
            disabled={readOnly}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
          >
            <option value="">{t('publicQuestions.selectOption')}</option>
            {question.options?.map((option, index) => (
              <option key={index} value={option}>
                {option}
              </option>
            ))}
          </select>
        );

      case 'MULTISELECT':
        const selectedValues = (value as string[]) || [];
        return (
          <div className="space-y-2">
            {question.options?.map((option, index) => (
              <label key={index} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedValues.includes(option)}
                  onChange={(e) => {
                    const newValues = e.target.checked
                      ? [...selectedValues, option]
                      : selectedValues.filter((v) => v !== option);
                    handleAnswerChange(question.field_key, newValues);
                  }}
                  disabled={readOnly}
                  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <span className="text-gray-700">{option}</span>
              </label>
            ))}
          </div>
        );

      case 'BOOLEAN':
        return (
          <div className="flex gap-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name={`question_${question.id}`}
                checked={value === true}
                onChange={() => handleAnswerChange(question.field_key, true)}
                disabled={readOnly}
                className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              />
              <span className="text-gray-700">{t('common.yes')}</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name={`question_${question.id}`}
                checked={value === false}
                onChange={() => handleAnswerChange(question.field_key, false)}
                disabled={readOnly}
                className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              />
              <span className="text-gray-700">{t('common.no')}</span>
            </label>
          </div>
        );

      default:
        return (
          <input
            type="text"
            value={(value as string) || ''}
            onChange={(e) => handleAnswerChange(question.field_key, e.target.value)}
            disabled={readOnly}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
          />
        );
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
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

  if (questions.length === 0) {
    return null; // No questions to show
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 mb-4">
        <HelpCircle className="w-5 h-5 text-purple-600" />
        <h3 className="text-lg font-semibold text-gray-900">{t('publicQuestions.title')}</h3>
      </div>

      <div className="space-y-4">
        {questions.map((question) => (
          <div key={question.id} className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {question.label}
              {question.is_required && <span className="text-red-500 ml-1">*</span>}
            </label>
            {question.description && (
              <p className="text-sm text-gray-500">{question.description}</p>
            )}
            {renderInput(question)}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ApplicationQuestionsForm;
