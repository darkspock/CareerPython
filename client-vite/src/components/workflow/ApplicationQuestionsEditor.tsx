/**
 * Application Questions Editor
 * Component for managing screening questions at workflow level
 */

import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Plus,
  Trash2,
  GripVertical,
  Edit2,
  Save,
  X,
  ChevronDown,
  ChevronUp,
  HelpCircle,
  ToggleLeft,
  ToggleRight,
} from 'lucide-react';
import { toast } from 'react-toastify';
import {
  applicationQuestionService,
  type ApplicationQuestion,
  type ApplicationQuestionFieldType,
  type CreateApplicationQuestionRequest,
} from '../../services/applicationQuestionService';

interface ApplicationQuestionsEditorProps {
  workflowId: string;
  onQuestionsChange?: (questions: ApplicationQuestion[]) => void;
}

const FIELD_TYPES: { value: ApplicationQuestionFieldType; label: string; icon: string }[] = [
  { value: 'TEXT', label: 'Text (short)', icon: 'Aa' },
  { value: 'TEXTAREA', label: 'Text (long)', icon: 'Tt' },
  { value: 'NUMBER', label: 'Number', icon: '#' },
  { value: 'DATE', label: 'Date', icon: 'D' },
  { value: 'SELECT', label: 'Single select', icon: 'O' },
  { value: 'MULTISELECT', label: 'Multi select', icon: 'M' },
  { value: 'BOOLEAN', label: 'Yes/No', icon: 'Y' },
];

export function ApplicationQuestionsEditor({
  workflowId,
  onQuestionsChange,
}: ApplicationQuestionsEditorProps) {
  const { t } = useTranslation();
  const [questions, setQuestions] = useState<ApplicationQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  // Form state
  const [formData, setFormData] = useState<CreateApplicationQuestionRequest>({
    field_key: '',
    label: '',
    description: '',
    field_type: 'TEXT',
    options: [],
    is_required: false,
    sort_order: 0,
  });
  const [optionsText, setOptionsText] = useState('');

  useEffect(() => {
    loadQuestions();
  }, [workflowId]);

  const loadQuestions = async () => {
    try {
      setLoading(true);
      const data = await applicationQuestionService.listQuestions(workflowId);
      const sorted = data.sort((a, b) => a.sort_order - b.sort_order);
      setQuestions(sorted);
      onQuestionsChange?.(sorted);
    } catch (error: any) {
      toast.error(error.message || t('applicationQuestions.loadError'));
    } finally {
      setLoading(false);
    }
  };

  const generateFieldKey = (label: string): string => {
    return label
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '_')
      .replace(/^_|_$/g, '')
      .substring(0, 50);
  };

  const handleLabelChange = (label: string) => {
    setFormData((prev) => ({
      ...prev,
      label,
      field_key: prev.field_key || generateFieldKey(label),
    }));
  };

  const handleAddQuestion = async () => {
    if (!formData.label.trim()) {
      toast.error(t('applicationQuestions.labelRequired'));
      return;
    }

    try {
      const newQuestion: CreateApplicationQuestionRequest = {
        ...formData,
        field_key: formData.field_key || generateFieldKey(formData.label),
        options:
          formData.field_type === 'SELECT' || formData.field_type === 'MULTISELECT'
            ? optionsText.split('\n').filter((o) => o.trim())
            : undefined,
        sort_order: questions.length,
      };

      await applicationQuestionService.createQuestion(workflowId, newQuestion);
      toast.success(t('applicationQuestions.createSuccess'));
      resetForm();
      loadQuestions();
    } catch (error: any) {
      toast.error(error.message || t('applicationQuestions.createError'));
    }
  };

  const handleUpdateQuestion = async (questionId: string) => {
    try {
      const updateData = {
        label: formData.label,
        description: formData.description,
        field_type: formData.field_type,
        options:
          formData.field_type === 'SELECT' || formData.field_type === 'MULTISELECT'
            ? optionsText.split('\n').filter((o) => o.trim())
            : undefined,
        is_required: formData.is_required,
      };

      await applicationQuestionService.updateQuestion(workflowId, questionId, updateData);
      toast.success(t('applicationQuestions.updateSuccess'));
      setEditingId(null);
      loadQuestions();
    } catch (error: any) {
      toast.error(error.message || t('applicationQuestions.updateError'));
    }
  };

  const handleDeleteQuestion = async (questionId: string) => {
    if (!confirm(t('applicationQuestions.confirmDelete'))) return;

    try {
      await applicationQuestionService.deleteQuestion(workflowId, questionId);
      toast.success(t('applicationQuestions.deleteSuccess'));
      loadQuestions();
    } catch (error: any) {
      toast.error(error.message || t('applicationQuestions.deleteError'));
    }
  };

  const handleToggleActive = async (question: ApplicationQuestion) => {
    try {
      await applicationQuestionService.updateQuestion(workflowId, question.id, {
        is_active: !question.is_active,
      });
      loadQuestions();
    } catch (error: any) {
      toast.error(error.message || t('applicationQuestions.updateError'));
    }
  };

  const handleMoveUp = async (index: number) => {
    if (index === 0) return;
    const newQuestions = [...questions];
    [newQuestions[index - 1], newQuestions[index]] = [newQuestions[index], newQuestions[index - 1]];

    // Update sort orders
    const updates = newQuestions.map((q, i) => ({ question_id: q.id, sort_order: i }));
    try {
      await applicationQuestionService.reorderQuestions(workflowId, updates);
      loadQuestions();
    } catch (error: any) {
      toast.error(error.message || t('applicationQuestions.reorderError'));
    }
  };

  const handleMoveDown = async (index: number) => {
    if (index === questions.length - 1) return;
    const newQuestions = [...questions];
    [newQuestions[index], newQuestions[index + 1]] = [newQuestions[index + 1], newQuestions[index]];

    // Update sort orders
    const updates = newQuestions.map((q, i) => ({ question_id: q.id, sort_order: i }));
    try {
      await applicationQuestionService.reorderQuestions(workflowId, updates);
      loadQuestions();
    } catch (error: any) {
      toast.error(error.message || t('applicationQuestions.reorderError'));
    }
  };

  const startEditing = (question: ApplicationQuestion) => {
    setEditingId(question.id);
    setFormData({
      field_key: question.field_key,
      label: question.label,
      description: question.description || '',
      field_type: question.field_type,
      options: question.options || [],
      is_required: question.is_required,
      sort_order: question.sort_order,
    });
    setOptionsText(question.options?.join('\n') || '');
  };

  const resetForm = () => {
    setShowAddForm(false);
    setEditingId(null);
    setFormData({
      field_key: '',
      label: '',
      description: '',
      field_type: 'TEXT',
      options: [],
      is_required: false,
      sort_order: 0,
    });
    setOptionsText('');
  };

  const getFieldTypeLabel = (type: ApplicationQuestionFieldType): string => {
    const found = FIELD_TYPES.find((ft) => ft.value === type);
    return found?.label || type;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-purple-600" />
            {t('applicationQuestions.title')}
          </h3>
          <p className="text-sm text-gray-600 mt-1">{t('applicationQuestions.description')}</p>
        </div>
        {!showAddForm && (
          <button
            onClick={() => setShowAddForm(true)}
            className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            {t('applicationQuestions.addQuestion')}
          </button>
        )}
      </div>

      {/* Add Form */}
      {showAddForm && (
        <div className="mb-6 p-4 bg-purple-50 border border-purple-200 rounded-lg">
          <h4 className="font-medium text-purple-900 mb-4">{t('applicationQuestions.newQuestion')}</h4>
          <QuestionForm
            formData={formData}
            optionsText={optionsText}
            onLabelChange={handleLabelChange}
            onFormDataChange={setFormData}
            onOptionsTextChange={setOptionsText}
            onSave={handleAddQuestion}
            onCancel={resetForm}
            isNew
          />
        </div>
      )}

      {/* Questions List */}
      {questions.length === 0 && !showAddForm ? (
        <div className="text-center py-8 bg-gray-50 rounded-lg border border-dashed border-gray-300">
          <HelpCircle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
          <p className="text-gray-600 mb-4">{t('applicationQuestions.noQuestions')}</p>
          <button
            onClick={() => setShowAddForm(true)}
            className="inline-flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            {t('applicationQuestions.addFirstQuestion')}
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          {questions.map((question, index) => (
            <div
              key={question.id}
              className={`border rounded-lg transition-all ${
                question.is_active
                  ? 'bg-white border-gray-200'
                  : 'bg-gray-50 border-gray-200 opacity-60'
              }`}
            >
              {/* Question Header */}
              <div className="flex items-center gap-3 p-4">
                <div className="flex flex-col gap-1">
                  <button
                    onClick={() => handleMoveUp(index)}
                    disabled={index === 0}
                    className="p-1 text-gray-400 hover:text-gray-600 disabled:opacity-30"
                  >
                    <ChevronUp className="w-4 h-4" />
                  </button>
                  <GripVertical className="w-4 h-4 text-gray-400" />
                  <button
                    onClick={() => handleMoveDown(index)}
                    disabled={index === questions.length - 1}
                    className="p-1 text-gray-400 hover:text-gray-600 disabled:opacity-30"
                  >
                    <ChevronDown className="w-4 h-4" />
                  </button>
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-gray-900 truncate">{question.label}</span>
                    {question.is_required && (
                      <span className="px-2 py-0.5 text-xs bg-red-100 text-red-700 rounded">
                        {t('applicationQuestions.required')}
                      </span>
                    )}
                    <span className="px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded">
                      {getFieldTypeLabel(question.field_type)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-500 truncate">
                    {question.description || t('applicationQuestions.noDescription')}
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleToggleActive(question)}
                    className={`p-2 rounded-lg transition-colors ${
                      question.is_active
                        ? 'text-green-600 hover:bg-green-50'
                        : 'text-gray-400 hover:bg-gray-100'
                    }`}
                    title={question.is_active ? t('applicationQuestions.deactivate') : t('applicationQuestions.activate')}
                  >
                    {question.is_active ? (
                      <ToggleRight className="w-5 h-5" />
                    ) : (
                      <ToggleLeft className="w-5 h-5" />
                    )}
                  </button>
                  <button
                    onClick={() =>
                      expandedId === question.id
                        ? setExpandedId(null)
                        : setExpandedId(question.id)
                    }
                    className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
                  >
                    {expandedId === question.id ? (
                      <ChevronUp className="w-5 h-5" />
                    ) : (
                      <ChevronDown className="w-5 h-5" />
                    )}
                  </button>
                  <button
                    onClick={() => startEditing(question)}
                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg"
                    title={t('common.edit')}
                  >
                    <Edit2 className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDeleteQuestion(question.id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                    title={t('common.delete')}
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Expanded Details / Edit Form */}
              {(expandedId === question.id || editingId === question.id) && (
                <div className="border-t border-gray-200 p-4 bg-gray-50">
                  {editingId === question.id ? (
                    <QuestionForm
                      formData={formData}
                      optionsText={optionsText}
                      onLabelChange={(label) => setFormData((prev) => ({ ...prev, label }))}
                      onFormDataChange={setFormData}
                      onOptionsTextChange={setOptionsText}
                      onSave={() => handleUpdateQuestion(question.id)}
                      onCancel={resetForm}
                      isNew={false}
                    />
                  ) : (
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500">{t('applicationQuestions.fieldKey')}:</span>
                        <span className="ml-2 font-mono text-gray-700">{question.field_key}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">{t('applicationQuestions.fieldType')}:</span>
                        <span className="ml-2">{getFieldTypeLabel(question.field_type)}</span>
                      </div>
                      {question.options && question.options.length > 0 && (
                        <div className="col-span-2">
                          <span className="text-gray-500">{t('applicationQuestions.options')}:</span>
                          <div className="mt-1 flex flex-wrap gap-1">
                            {question.options.map((opt, i) => (
                              <span
                                key={i}
                                className="px-2 py-1 bg-white border border-gray-200 rounded text-gray-700"
                              >
                                {opt}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Question Form Component
interface QuestionFormProps {
  formData: CreateApplicationQuestionRequest;
  optionsText: string;
  onLabelChange: (label: string) => void;
  onFormDataChange: (data: CreateApplicationQuestionRequest) => void;
  onOptionsTextChange: (text: string) => void;
  onSave: () => void;
  onCancel: () => void;
  isNew: boolean;
}

function QuestionForm({
  formData,
  optionsText,
  onLabelChange,
  onFormDataChange,
  onOptionsTextChange,
  onSave,
  onCancel,
  isNew,
}: QuestionFormProps) {
  const { t } = useTranslation();
  const showOptions = formData.field_type === 'SELECT' || formData.field_type === 'MULTISELECT';

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {t('applicationQuestions.label')} *
          </label>
          <input
            type="text"
            value={formData.label}
            onChange={(e) => onLabelChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
            placeholder={t('applicationQuestions.labelPlaceholder')}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {t('applicationQuestions.fieldType')}
          </label>
          <select
            value={formData.field_type}
            onChange={(e) =>
              onFormDataChange({
                ...formData,
                field_type: e.target.value as ApplicationQuestionFieldType,
              })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
          >
            {FIELD_TYPES.map((ft) => (
              <option key={ft.value} value={ft.value}>
                {ft.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {t('applicationQuestions.descriptionLabel')}
        </label>
        <textarea
          value={formData.description}
          onChange={(e) => onFormDataChange({ ...formData, description: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
          rows={2}
          placeholder={t('applicationQuestions.descriptionPlaceholder')}
        />
      </div>

      {isNew && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {t('applicationQuestions.fieldKey')}
          </label>
          <input
            type="text"
            value={formData.field_key}
            onChange={(e) =>
              onFormDataChange({
                ...formData,
                field_key: e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, '_'),
              })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 font-mono"
            placeholder="auto_generated_from_label"
          />
          <p className="text-xs text-gray-500 mt-1">{t('applicationQuestions.fieldKeyHelp')}</p>
        </div>
      )}

      {showOptions && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {t('applicationQuestions.options')} *
          </label>
          <textarea
            value={optionsText}
            onChange={(e) => onOptionsTextChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 font-mono"
            rows={4}
            placeholder={t('applicationQuestions.optionsPlaceholder')}
          />
          <p className="text-xs text-gray-500 mt-1">{t('applicationQuestions.optionsHelp')}</p>
        </div>
      )}

      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          id="is_required"
          checked={formData.is_required}
          onChange={(e) => onFormDataChange({ ...formData, is_required: e.target.checked })}
          className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
        />
        <label htmlFor="is_required" className="text-sm text-gray-700">
          {t('applicationQuestions.isRequired')}
        </label>
      </div>

      <div className="flex items-center gap-2 pt-2">
        <button
          onClick={onSave}
          className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          <Save className="w-4 h-4" />
          {isNew ? t('applicationQuestions.create') : t('applicationQuestions.save')}
        </button>
        <button
          onClick={onCancel}
          className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
        >
          <X className="w-4 h-4" />
          {t('common.cancel')}
        </button>
      </div>
    </div>
  );
}

export default ApplicationQuestionsEditor;
