/**
 * Position Questions Editor
 * Component for enabling/disabling application questions at position level
 */

import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  HelpCircle,
  ToggleLeft,
  ToggleRight,
  AlertCircle,
  Check,
} from 'lucide-react';
import { toast } from 'react-toastify';
import {
  applicationQuestionService,
  type ApplicationQuestion,
} from '../../services/applicationQuestionService';
import {
  positionQuestionConfigService,
  type PositionQuestionConfig,
} from '../../services/positionQuestionConfigService';

interface PositionQuestionsEditorProps {
  positionId: string;
  workflowId: string;
}

interface QuestionWithConfig {
  question: ApplicationQuestion;
  config: PositionQuestionConfig | null;
  isEnabled: boolean;
  isRequired: boolean;
}

export function PositionQuestionsEditor({
  positionId,
  workflowId,
}: PositionQuestionsEditorProps) {
  const { t } = useTranslation();
  const [questions, setQuestions] = useState<QuestionWithConfig[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState<string | null>(null);

  useEffect(() => {
    if (workflowId && positionId) {
      loadData();
    }
  }, [workflowId, positionId]);

  const loadData = async () => {
    try {
      setLoading(true);

      // Load workflow questions and position configs in parallel
      const [workflowQuestions, positionConfigs] = await Promise.all([
        applicationQuestionService.listQuestions(workflowId, true), // active only
        positionQuestionConfigService.listConfigs(positionId),
      ]);

      // Build config map for quick lookup
      const configMap = new Map<string, PositionQuestionConfig>();
      positionConfigs.forEach((config) => configMap.set(config.question_id, config));

      // Combine questions with their configs
      const combined: QuestionWithConfig[] = workflowQuestions
        .sort((a, b) => a.sort_order - b.sort_order)
        .map((question) => {
          const config = configMap.get(question.id) || null;
          return {
            question,
            config,
            // If no config exists, question is enabled by default
            isEnabled: config ? config.enabled : true,
            // Use override if exists, otherwise use question's default
            isRequired: config?.is_required_override !== undefined
              ? config.is_required_override
              : question.is_required,
          };
        });

      setQuestions(combined);
    } catch (error: any) {
      toast.error(error.message || t('positionQuestions.loadError'));
    } finally {
      setLoading(false);
    }
  };

  const handleToggleEnabled = async (questionId: string, currentlyEnabled: boolean) => {
    setSaving(questionId);
    try {
      await positionQuestionConfigService.configureQuestion(positionId, {
        question_id: questionId,
        enabled: !currentlyEnabled,
      });

      // Update local state
      setQuestions((prev) =>
        prev.map((q) =>
          q.question.id === questionId
            ? { ...q, isEnabled: !currentlyEnabled, config: { ...q.config, enabled: !currentlyEnabled } as PositionQuestionConfig }
            : q
        )
      );

      toast.success(
        !currentlyEnabled
          ? t('positionQuestions.questionEnabled')
          : t('positionQuestions.questionDisabled')
      );
    } catch (error: any) {
      toast.error(error.message || t('positionQuestions.updateError'));
    } finally {
      setSaving(null);
    }
  };

  const handleToggleRequired = async (questionId: string, currentlyRequired: boolean) => {
    setSaving(questionId);
    try {
      await positionQuestionConfigService.configureQuestion(positionId, {
        question_id: questionId,
        enabled: true, // Keep enabled
        is_required_override: !currentlyRequired,
      });

      // Update local state
      setQuestions((prev) =>
        prev.map((q) =>
          q.question.id === questionId
            ? { ...q, isRequired: !currentlyRequired }
            : q
        )
      );

      toast.success(t('positionQuestions.updateSuccess'));
    } catch (error: any) {
      toast.error(error.message || t('positionQuestions.updateError'));
    } finally {
      setSaving(null);
    }
  };

  const getFieldTypeLabel = (type: string): string => {
    const labels: Record<string, string> = {
      TEXT: t('positionQuestions.fieldTypes.text'),
      TEXTAREA: t('positionQuestions.fieldTypes.textarea'),
      NUMBER: t('positionQuestions.fieldTypes.number'),
      DATE: t('positionQuestions.fieldTypes.date'),
      SELECT: t('positionQuestions.fieldTypes.select'),
      MULTISELECT: t('positionQuestions.fieldTypes.multiselect'),
      BOOLEAN: t('positionQuestions.fieldTypes.boolean'),
    };
    return labels[type] || type;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="text-center py-8 bg-gray-50 rounded-lg border border-dashed border-gray-300">
        <HelpCircle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <p className="text-gray-600">{t('positionQuestions.noQuestions')}</p>
        <p className="text-sm text-gray-500 mt-1">{t('positionQuestions.noQuestionsHint')}</p>
      </div>
    );
  }

  const enabledCount = questions.filter((q) => q.isEnabled).length;

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-purple-600" />
            {t('positionQuestions.title')}
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            {t('positionQuestions.description')}
          </p>
        </div>
        <div className="text-sm text-gray-500">
          {enabledCount} / {questions.length} {t('positionQuestions.questionsEnabled')}
        </div>
      </div>

      {/* Info Box */}
      <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg flex items-start gap-2">
        <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <p className="text-sm text-blue-800">
          {t('positionQuestions.infoBox')}
        </p>
      </div>

      {/* Questions List */}
      <div className="space-y-2">
        {questions.map(({ question, isEnabled, isRequired }) => (
          <div
            key={question.id}
            className={`flex items-center justify-between p-4 border rounded-lg transition-all ${
              isEnabled
                ? 'bg-white border-gray-200'
                : 'bg-gray-50 border-gray-200 opacity-60'
            }`}
          >
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className={`font-medium ${isEnabled ? 'text-gray-900' : 'text-gray-500'}`}>
                  {question.label}
                </span>
                {isEnabled && isRequired && (
                  <span className="px-2 py-0.5 text-xs bg-red-100 text-red-700 rounded">
                    {t('positionQuestions.required')}
                  </span>
                )}
                <span className="px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded">
                  {getFieldTypeLabel(question.field_type)}
                </span>
              </div>
              {question.description && (
                <p className="text-sm text-gray-500 mt-1 truncate">{question.description}</p>
              )}
            </div>

            <div className="flex items-center gap-4 ml-4">
              {/* Required toggle (only when enabled) */}
              {isEnabled && (
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isRequired}
                    onChange={() => handleToggleRequired(question.id, isRequired)}
                    disabled={saving === question.id}
                    className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-600">{t('positionQuestions.requiredLabel')}</span>
                </label>
              )}

              {/* Enable/Disable toggle */}
              <button
                onClick={() => handleToggleEnabled(question.id, isEnabled)}
                disabled={saving === question.id}
                className={`p-2 rounded-lg transition-colors ${
                  isEnabled
                    ? 'text-green-600 hover:bg-green-50'
                    : 'text-gray-400 hover:bg-gray-100'
                }`}
                title={isEnabled ? t('positionQuestions.disable') : t('positionQuestions.enable')}
              >
                {saving === question.id ? (
                  <div className="w-5 h-5 animate-spin rounded-full border-2 border-purple-600 border-t-transparent" />
                ) : isEnabled ? (
                  <ToggleRight className="w-6 h-6" />
                ) : (
                  <ToggleLeft className="w-6 h-6" />
                )}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Summary */}
      {enabledCount > 0 && (
        <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2">
          <Check className="w-5 h-5 text-green-600" />
          <p className="text-sm text-green-800">
            {t('positionQuestions.summary', { count: enabledCount })}
          </p>
        </div>
      )}
    </div>
  );
}

export default PositionQuestionsEditor;
