/**
 * ScreeningQuestionsEditor - Reusable component for editing screening template questions
 * Used in both interview template editor and job position killer questions tab
 */
import React, { useState, useEffect } from 'react';
import { Plus, ChevronUp, ChevronDown, Pencil, Trash2, X, MessageSquare, Star } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';
import { companyInterviewTemplateService } from '@/services/companyInterviewTemplateService';
import type { InterviewTemplateQuestion } from '@/services/companyInterviewTemplateService';

interface ScreeningQuestionsEditorProps {
  sectionId: string;
  disabled?: boolean;
  onQuestionsChange?: (questions: InterviewTemplateQuestion[]) => void;
}

export const ScreeningQuestionsEditor: React.FC<ScreeningQuestionsEditorProps> = ({
  sectionId,
  disabled = false,
  onQuestionsChange,
}) => {
  const [questions, setQuestions] = useState<InterviewTemplateQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showQuestionForm, setShowQuestionForm] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState<InterviewTemplateQuestion | null>(null);

  useEffect(() => {
    fetchQuestions();
  }, [sectionId]);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await companyInterviewTemplateService.getQuestionsBySection(sectionId);
      const sortedQuestions = response.sort((a, b) => a.sort_order - b.sort_order);
      setQuestions(sortedQuestions);
      onQuestionsChange?.(sortedQuestions);
    } catch (err: any) {
      setError(err.message || 'Failed to load questions');
    } finally {
      setLoading(false);
    }
  };

  const handleAddQuestion = () => {
    setEditingQuestion(null);
    setShowQuestionForm(true);
  };

  const handleEditQuestion = (question: InterviewTemplateQuestion) => {
    setEditingQuestion(question);
    setShowQuestionForm(true);
  };

  const handleCancelQuestionForm = () => {
    setShowQuestionForm(false);
    setEditingQuestion(null);
  };

  const handleSaveQuestion = async (questionData: any) => {
    try {
      if (editingQuestion) {
        // Update existing question
        await companyInterviewTemplateService.updateQuestion(editingQuestion.id, questionData);
      } else {
        // Create new question with automatic sort_order
        const nextSortOrder = questions.length;
        await companyInterviewTemplateService.createQuestion({
          ...questionData,
          interview_template_section_id: sectionId,
          sort_order: nextSortOrder,
        });
      }

      setShowQuestionForm(false);
      setEditingQuestion(null);
      await fetchQuestions();
    } catch (err: any) {
      setError(err.message || 'Failed to save question');
    }
  };

  const handleDeleteQuestion = async (questionId: string) => {
    if (confirm('Are you sure you want to delete this question?')) {
      try {
        await companyInterviewTemplateService.deleteQuestion(questionId);
        await fetchQuestions();
      } catch (err: any) {
        setError(err.message || 'Failed to delete question');
      }
    }
  };

  const handleMoveQuestion = async (questionId: string, direction: 'up' | 'down') => {
    const currentIndex = questions.findIndex(q => q.id === questionId);
    const newIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;

    if (newIndex < 0 || newIndex >= questions.length) return;

    const updatedQuestions = [...questions];
    [updatedQuestions[currentIndex], updatedQuestions[newIndex]] =
    [updatedQuestions[newIndex], updatedQuestions[currentIndex]];

    // Update sort_order values
    updatedQuestions.forEach((q, index) => {
      q.sort_order = index;
    });

    setQuestions(updatedQuestions);
    onQuestionsChange?.(updatedQuestions);

    // TODO: Persist to backend when API supports it
  };

  const getDataTypeLabel = (dataType: string): string => {
    const labels: Record<string, string> = {
      'int': 'Number',
      'date': 'Date',
      'short_string': 'Short Text',
      'large_string': 'Long Text',
      'scoring': 'Multiple Choice',
      'boolean': 'Yes/No',
    };
    return labels[dataType] || dataType;
  };

  return (
    <div className="space-y-4">
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {loading ? (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h5 className="text-sm font-medium text-muted-foreground">
              {questions.length} question{questions.length !== 1 ? 's' : ''}
            </h5>
            {!disabled && (
              <Button
                type="button"
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  handleAddQuestion();
                }}
                variant="outline"
                size="sm"
              >
                <Plus className="w-4 h-4 mr-1" />
                Add Question
              </Button>
            )}
          </div>

          {questions.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground border-2 border-dashed rounded-lg">
              <MessageSquare className="w-10 h-10 mx-auto mb-3 opacity-50" />
              <p className="font-medium">No questions yet</p>
              <p className="text-sm mt-1">Add screening questions to evaluate candidates</p>
            </div>
          ) : (
            <div className="space-y-2">
              {questions.map((question, index) => (
                <Card key={question.id}>
                  <CardContent className="py-3 px-4">
                    <div className="flex justify-between items-start gap-4">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start gap-2">
                          <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary/10 text-primary text-xs font-medium flex items-center justify-center mt-0.5">
                            {index + 1}
                          </span>
                          <div className="flex-1 min-w-0">
                            <h5 className="font-medium text-sm">{question.name}</h5>
                            {question.description && (
                              <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{question.description}</p>
                            )}
                            <div className="flex items-center gap-2 mt-2">
                              <span className="text-xs px-2 py-0.5 bg-muted rounded">
                                {getDataTypeLabel(question.data_type)}
                              </span>
                              {question.scoring_values && question.scoring_values.length > 0 && (
                                <span className="text-xs px-2 py-0.5 bg-amber-100 text-amber-800 rounded">
                                  {question.scoring_values.length} options
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>

                      {!disabled && (
                        <div className="flex items-center gap-1">
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={(e) => { e.preventDefault(); e.stopPropagation(); handleMoveQuestion(question.id, 'up'); }}
                                disabled={index === 0}
                                className="h-7 w-7 p-0"
                              >
                                <ChevronUp className="w-4 h-4" />
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>Move up</TooltipContent>
                          </Tooltip>

                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={(e) => { e.preventDefault(); e.stopPropagation(); handleMoveQuestion(question.id, 'down'); }}
                                disabled={index >= questions.length - 1}
                                className="h-7 w-7 p-0"
                              >
                                <ChevronDown className="w-4 h-4" />
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>Move down</TooltipContent>
                          </Tooltip>

                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={(e) => { e.preventDefault(); e.stopPropagation(); handleEditQuestion(question); }}
                                className="h-7 w-7 p-0"
                              >
                                <Pencil className="w-4 h-4" />
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>Edit</TooltipContent>
                          </Tooltip>

                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={(e) => { e.preventDefault(); e.stopPropagation(); handleDeleteQuestion(question.id); }}
                                className="h-7 w-7 p-0 text-destructive hover:text-destructive"
                              >
                                <Trash2 className="w-4 h-4" />
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>Delete</TooltipContent>
                          </Tooltip>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Question Form Modal */}
      <Dialog open={showQuestionForm} onOpenChange={(open) => !open && handleCancelQuestionForm()}>
        <ScreeningQuestionFormModal
          question={editingQuestion}
          sectionId={sectionId}
          onSave={handleSaveQuestion}
          onCancel={handleCancelQuestionForm}
        />
      </Dialog>
    </div>
  );
};

// Question Form Modal Component (ABSOLUTE mode only, no DISTANCE)
interface ScreeningQuestionFormModalProps {
  question: InterviewTemplateQuestion | null;
  sectionId: string;
  onSave: (questionData: any) => void;
  onCancel: () => void;
}

const ScreeningQuestionFormModal: React.FC<ScreeningQuestionFormModalProps> = ({
  question,
  sectionId,
  onSave,
  onCancel
}) => {
  const [formData, setFormData] = useState({
    name: question?.name || '',
    description: question?.description || '',
    code: question?.code || `q_${Date.now()}`,
    sort_order: question?.sort_order || 0,
    scope: 'global',
    data_type: question?.data_type || 'short_string',
    allow_ai_followup: question?.allow_ai_followup || false,
    legal_notice: question?.legal_notice || '',
    scoring_values: question?.scoring_values || [],
  });

  const dataTypeOptions = [
    { value: 'short_string', label: 'Short Text' },
    { value: 'large_string', label: 'Long Text' },
    { value: 'int', label: 'Number' },
    { value: 'date', label: 'Date' },
    { value: 'scoring', label: 'Multiple Choice (with scoring)' },
  ];

  const isScoringType = formData.data_type === 'scoring';

  // Convert scoring to star rating (0-5 stars, each worth 2 points)
  const getStarRatingFromScoring = (score: number | null): number => {
    if (score === null || score === undefined) return 0;
    return Math.round(score / 2);
  };

  // Convert star rating (0-5) to score (0-10)
  const getScoringFromStarRating = (stars: number): number => {
    return stars * 2;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave({
      ...formData,
      interview_template_section_id: sectionId
    });
  };

  const handleAddScoringValue = () => {
    setFormData({
      ...formData,
      scoring_values: [...formData.scoring_values, { label: '', scoring: 2 }]
    });
  };

  const handleRemoveScoringValue = (index: number) => {
    const newValues = formData.scoring_values.filter((_: any, i: number) => i !== index);
    setFormData({ ...formData, scoring_values: newValues });
  };

  const handleUpdateScoringLabel = (index: number, label: string) => {
    const newValues = [...formData.scoring_values];
    newValues[index] = { ...newValues[index], label };
    setFormData({ ...formData, scoring_values: newValues });
  };

  const handleStarClick = (valueIndex: number, starIndex: number) => {
    const currentValue = formData.scoring_values[valueIndex];
    const currentRating = getStarRatingFromScoring(currentValue?.scoring);
    const clickedRating = starIndex + 1;
    const newRating = clickedRating === currentRating ? 0 : clickedRating;
    const newScore = getScoringFromStarRating(newRating);

    const newValues = [...formData.scoring_values];
    newValues[valueIndex] = { ...newValues[valueIndex], scoring: newScore };
    setFormData({ ...formData, scoring_values: newValues });
  };

  return (
    <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>{question ? 'Edit Question' : 'Add Question'}</DialogTitle>
        <DialogDescription>
          {question ? 'Modify the screening question details' : 'Create a new screening question'}
        </DialogDescription>
      </DialogHeader>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <Label htmlFor="questionName">Question *</Label>
          <Input
            id="questionName"
            type="text"
            required
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="Enter the question text..."
            className="mt-1"
          />
        </div>

        <div>
          <Label htmlFor="questionDescription">Description</Label>
          <Textarea
            id="questionDescription"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            rows={2}
            placeholder="Additional context for the question (optional)"
            className="mt-1"
          />
        </div>

        <div>
          <Label htmlFor="questionDataType">Answer Type</Label>
          <Select
            value={formData.data_type}
            onValueChange={(value) => setFormData({
              ...formData,
              data_type: value,
              scoring_values: value === 'scoring' ? formData.scoring_values : []
            })}
          >
            <SelectTrigger className="mt-1">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {dataTypeOptions.map(option => (
                <SelectItem key={option.value} value={option.value}>{option.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {isScoringType && (
          <div>
            <Label>Answer Options with Scoring</Label>
            <p className="text-xs text-muted-foreground mb-3">
              Add options and assign a score (0-10) using the star rating. Higher scores indicate better answers.
            </p>
            <div className="space-y-2">
              {formData.scoring_values.map((value: { label: string; scoring: number }, index: number) => {
                const currentRating = getStarRatingFromScoring(value.scoring);

                return (
                  <div key={index} className="flex items-center gap-2 p-3 border rounded-lg bg-muted/20">
                    <div className="flex-1">
                      <Input
                        type="text"
                        value={value.label}
                        onChange={(e) => handleUpdateScoringLabel(index, e.target.value)}
                        placeholder="Option label..."
                      />
                    </div>
                    <div className="flex items-center gap-1">
                      {[0, 1, 2, 3, 4].map((starIndex) => {
                        const isFilled = starIndex < currentRating;
                        return (
                          <button
                            key={starIndex}
                            type="button"
                            onClick={() => handleStarClick(index, starIndex)}
                            className={`transition-colors ${
                              isFilled
                                ? 'text-yellow-400 hover:text-yellow-500'
                                : 'text-gray-300 hover:text-gray-400'
                            }`}
                          >
                            <Star
                              className="w-5 h-5"
                              fill={isFilled ? 'currentColor' : 'none'}
                              strokeWidth={isFilled ? 0 : 1.5}
                            />
                          </button>
                        );
                      })}
                      <span className="text-xs text-muted-foreground ml-2 w-10">
                        ({value.scoring}/10)
                      </span>
                    </div>
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => handleRemoveScoringValue(index)}
                      className="h-8 w-8 p-0"
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                );
              })}
              <Button
                type="button"
                variant="outline"
                onClick={handleAddScoringValue}
                className="w-full"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Option
              </Button>
            </div>
          </div>
        )}

        <div className="flex items-center space-x-2">
          <Checkbox
            id="allow_ai_followup"
            checked={formData.allow_ai_followup}
            onCheckedChange={(checked) => setFormData({ ...formData, allow_ai_followup: checked === true })}
          />
          <label htmlFor="allow_ai_followup" className="text-sm cursor-pointer">
            Allow AI follow-up questions
          </label>
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" onClick={onCancel}>
            Cancel
          </Button>
          <Button type="submit" disabled={!formData.name.trim()}>
            {question ? 'Update' : 'Add Question'}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  );
};

export default ScreeningQuestionsEditor;
