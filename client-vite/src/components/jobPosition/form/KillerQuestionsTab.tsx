/**
 * KillerQuestionsTab Component
 * Tab for managing killer questions in job position form
 * Two modes:
 * 1. Select existing SCREENING template
 * 2. Add questions directly (stored as JSON in job position)
 */
import { useState, useEffect } from 'react';
import { FileQuestion, Plus, Trash2, GripVertical, ChevronUp, ChevronDown, Star, Edit, ExternalLink } from 'lucide-react';
import { useCompanyNavigation } from '../../../hooks/useCompanyNavigation';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
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
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Checkbox } from '@/components/ui/checkbox';
import { companyInterviewTemplateService } from '@/services/companyInterviewTemplateService';
import type { InterviewTemplate } from '@/services/companyInterviewTemplateService';

// Type for a killer question
export interface KillerQuestion {
  id: string;
  name: string;
  description?: string;
  data_type: 'short_string' | 'large_string' | 'int' | 'date' | 'scoring';
  scoring_values?: Array<{ label: string; scoring: number }>;
  is_killer?: boolean;
  sort_order: number;
}

interface KillerQuestionsTabProps {
  // Template mode
  screeningTemplateId?: string | null;
  onTemplateChange: (templateId: string | null) => void;
  // Direct questions mode
  questions: KillerQuestion[];
  onQuestionsChange: (questions: KillerQuestion[]) => void;
  disabled?: boolean;
}

// Generate unique ID
const generateId = () => `q_${crypto.randomUUID().replace(/-/g, '').substring(0, 12)}`;

// Data type options
const DATA_TYPES = [
  { value: 'short_string', label: 'Short Text' },
  { value: 'large_string', label: 'Long Text' },
  { value: 'int', label: 'Number' },
  { value: 'date', label: 'Date' },
  { value: 'scoring', label: 'Options with Scoring' },
];

// Default scoring options
const DEFAULT_SCORING_VALUES = [
  { label: 'Yes', scoring: 10 },
  { label: 'No', scoring: 0 },
];

export function KillerQuestionsTab({
  screeningTemplateId,
  onTemplateChange,
  questions,
  onQuestionsChange,
  disabled = false,
}: KillerQuestionsTabProps) {
  const [availableTemplates, setAvailableTemplates] = useState<InterviewTemplate[]>([]);
  const [loadingTemplates, setLoadingTemplates] = useState(true);
  const [editingQuestion, setEditingQuestion] = useState<KillerQuestion | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const { getPath } = useCompanyNavigation();

  // Determine mode: template (if templateId set) or direct (if questions exist or no template)
  const isTemplateMode = !!screeningTemplateId;
  const hasDirectQuestions = questions.length > 0;

  // Load available screening templates
  useEffect(() => {
    const loadTemplates = async () => {
      try {
        setLoadingTemplates(true);
        const templates = await companyInterviewTemplateService.listScreeningTemplates();
        setAvailableTemplates(templates);
      } catch (err) {
        console.error('Failed to load screening templates:', err);
      } finally {
        setLoadingTemplates(false);
      }
    };
    loadTemplates();
  }, []);

  // Sort questions by sort_order
  const sortedQuestions = [...questions].sort((a, b) => a.sort_order - b.sort_order);

  const handleTemplateSelect = (templateId: string) => {
    if (templateId === 'none') {
      onTemplateChange(null);
    } else {
      onTemplateChange(templateId);
      // Clear direct questions when selecting a template
      if (questions.length > 0) {
        onQuestionsChange([]);
      }
    }
  };

  const handleAddQuestion = () => {
    // Clear template when adding direct questions
    if (screeningTemplateId) {
      onTemplateChange(null);
    }

    const newQuestion: KillerQuestion = {
      id: generateId(),
      name: '',
      description: '',
      data_type: 'short_string',
      is_killer: false,
      sort_order: questions.length,
    };
    setEditingQuestion(newQuestion);
    setIsDialogOpen(true);
  };

  const handleEditQuestion = (question: KillerQuestion) => {
    setEditingQuestion({ ...question });
    setIsDialogOpen(true);
  };

  const handleSaveQuestion = () => {
    if (!editingQuestion || !editingQuestion.name.trim()) return;

    const existingIndex = questions.findIndex(q => q.id === editingQuestion.id);

    if (existingIndex >= 0) {
      // Update existing
      const updated = [...questions];
      updated[existingIndex] = editingQuestion;
      onQuestionsChange(updated);
    } else {
      // Add new
      onQuestionsChange([...questions, editingQuestion]);
    }

    setIsDialogOpen(false);
    setEditingQuestion(null);
  };

  const handleDeleteQuestion = (questionId: string) => {
    if (!confirm('Are you sure you want to delete this question?')) return;
    onQuestionsChange(questions.filter(q => q.id !== questionId));
  };

  const handleMoveUp = (index: number) => {
    if (index === 0) return;
    const updated = [...sortedQuestions];
    [updated[index - 1], updated[index]] = [updated[index], updated[index - 1]];
    updated.forEach((q, i) => q.sort_order = i);
    onQuestionsChange(updated);
  };

  const handleMoveDown = (index: number) => {
    if (index === sortedQuestions.length - 1) return;
    const updated = [...sortedQuestions];
    [updated[index], updated[index + 1]] = [updated[index + 1], updated[index]];
    updated.forEach((q, i) => q.sort_order = i);
    onQuestionsChange(updated);
  };

  const hasTemplates = availableTemplates.length > 0;
  const selectedTemplate = availableTemplates.find(t => t.id === screeningTemplateId);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileQuestion className="w-5 h-5" />
          Killer Questions
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Template Selector - only show if templates exist and no direct questions */}
        {hasTemplates && !hasDirectQuestions && (
          <div className="space-y-2">
            <Label>Use existing template</Label>
            <Select
              value={screeningTemplateId || 'none'}
              onValueChange={handleTemplateSelect}
              disabled={disabled || loadingTemplates}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select a screening template..." />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="none">No template (add questions below)</SelectItem>
                {availableTemplates.map((template) => (
                  <SelectItem key={template.id} value={template.id}>
                    {template.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}

        {/* Template Selected - Show info and link */}
        {isTemplateMode && selectedTemplate && (
          <div className="p-4 border rounded-lg bg-muted/50">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">{selectedTemplate.name}</p>
                {selectedTemplate.intro && (
                  <p className="text-sm text-muted-foreground mt-1">{selectedTemplate.intro}</p>
                )}
              </div>
              <div className="flex items-center gap-2">
                <a
                  href={getPath(`interview-templates/${selectedTemplate.id}`)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 text-sm text-primary hover:underline"
                >
                  Edit template
                  <ExternalLink className="w-3 h-3" />
                </a>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => onTemplateChange(null)}
                  disabled={disabled}
                >
                  Remove
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Direct Questions Mode */}
        {!isTemplateMode && (
          <>
            {/* Questions List */}
            {sortedQuestions.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground border-2 border-dashed rounded-lg">
                <FileQuestion className="w-10 h-10 mx-auto mb-3 opacity-50" />
                <p className="font-medium">No screening questions yet</p>
                <p className="text-sm mt-1">Add questions to screen candidates before they apply</p>
              </div>
            ) : (
              <div className="space-y-2">
                {sortedQuestions.map((question, index) => (
                  <div
                    key={question.id}
                    className="flex items-center gap-2 p-3 border rounded-lg bg-card hover:bg-accent/50"
                  >
                    <GripVertical className="w-4 h-4 text-muted-foreground cursor-move" />

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-medium truncate">{question.name}</span>
                        {question.is_killer && (
                          <span className="text-xs bg-destructive/10 text-destructive px-2 py-0.5 rounded">
                            Killer
                          </span>
                        )}
                      </div>
                      <div className="text-xs text-muted-foreground mt-0.5">
                        {DATA_TYPES.find(t => t.value === question.data_type)?.label || question.data_type}
                        {question.data_type === 'scoring' && question.scoring_values && (
                          <span className="ml-2">
                            ({question.scoring_values.length} options)
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex items-center gap-1">
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        onClick={() => handleMoveUp(index)}
                        disabled={disabled || index === 0}
                        className="h-8 w-8"
                      >
                        <ChevronUp className="w-4 h-4" />
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        onClick={() => handleMoveDown(index)}
                        disabled={disabled || index === sortedQuestions.length - 1}
                        className="h-8 w-8"
                      >
                        <ChevronDown className="w-4 h-4" />
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        onClick={() => handleEditQuestion(question)}
                        disabled={disabled}
                        className="h-8 w-8"
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        onClick={() => handleDeleteQuestion(question.id)}
                        disabled={disabled}
                        className="h-8 w-8 text-destructive hover:text-destructive"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Add Question Button */}
            <Button
              type="button"
              variant="outline"
              onClick={handleAddQuestion}
              disabled={disabled}
              className="w-full"
            >
              <Plus className="w-4 h-4 mr-2" />
              Add Question
            </Button>
          </>
        )}

        {/* Edit Dialog */}
        <QuestionFormDialog
          question={editingQuestion}
          open={isDialogOpen}
          onClose={() => {
            setIsDialogOpen(false);
            setEditingQuestion(null);
          }}
          onSave={handleSaveQuestion}
          onChange={setEditingQuestion}
          disabled={disabled}
        />
      </CardContent>
    </Card>
  );
}

// Question Form Dialog Component
interface QuestionFormDialogProps {
  question: KillerQuestion | null;
  open: boolean;
  onClose: () => void;
  onSave: () => void;
  onChange: (question: KillerQuestion) => void;
  disabled?: boolean;
}

function QuestionFormDialog({
  question,
  open,
  onClose,
  onSave,
  onChange,
  disabled = false,
}: QuestionFormDialogProps) {
  if (!question) return null;

  const updateField = <K extends keyof KillerQuestion>(field: K, value: KillerQuestion[K]) => {
    onChange({ ...question, [field]: value });
  };

  const handleDataTypeChange = (newType: string) => {
    const updated: KillerQuestion = {
      ...question,
      data_type: newType as KillerQuestion['data_type'],
    };

    // Add default scoring values if switching to scoring type
    if (newType === 'scoring' && !updated.scoring_values) {
      updated.scoring_values = [...DEFAULT_SCORING_VALUES];
    }

    onChange(updated);
  };

  const handleScoringOptionChange = (index: number, field: 'label' | 'scoring', value: string | number) => {
    if (!question.scoring_values) return;
    const updated = [...question.scoring_values];
    updated[index] = { ...updated[index], [field]: value };
    onChange({ ...question, scoring_values: updated });
  };

  const handleAddScoringOption = () => {
    const current = question.scoring_values || [];
    onChange({
      ...question,
      scoring_values: [...current, { label: '', scoring: 0 }],
    });
  };

  const handleRemoveScoringOption = (index: number) => {
    if (!question.scoring_values) return;
    onChange({
      ...question,
      scoring_values: question.scoring_values.filter((_, i) => i !== index),
    });
  };

  // Star rating helpers
  const getStarRating = (scoring: number) => Math.round(scoring / 2);
  const setStarRating = (index: number, stars: number) => {
    handleScoringOptionChange(index, 'scoring', stars * 2);
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>
            {question.name ? 'Edit Question' : 'Add Question'}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4 py-4">
          {/* Question Text */}
          <div className="space-y-2">
            <Label>Question *</Label>
            <Input
              value={question.name}
              onChange={(e) => updateField('name', e.target.value)}
              placeholder="Enter your question..."
              disabled={disabled}
            />
          </div>

          {/* Description */}
          <div className="space-y-2">
            <Label>Description (optional)</Label>
            <Textarea
              value={question.description || ''}
              onChange={(e) => updateField('description', e.target.value)}
              placeholder="Additional context or instructions..."
              rows={2}
              disabled={disabled}
            />
          </div>

          {/* Data Type */}
          <div className="space-y-2">
            <Label>Answer Type</Label>
            <Select
              value={question.data_type}
              onValueChange={handleDataTypeChange}
              disabled={disabled}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {DATA_TYPES.map((type) => (
                  <SelectItem key={type.value} value={type.value}>
                    {type.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Scoring Options (only for scoring type) */}
          {question.data_type === 'scoring' && (
            <div className="space-y-3">
              <Label>Answer Options with Scoring</Label>
              <div className="space-y-2">
                {(question.scoring_values || []).map((option, index) => (
                  <div key={index} className="flex items-center gap-2">
                    <Input
                      value={option.label}
                      onChange={(e) => handleScoringOptionChange(index, 'label', e.target.value)}
                      placeholder="Option label..."
                      className="flex-1"
                      disabled={disabled}
                    />
                    {/* Star Rating */}
                    <div className="flex items-center gap-0.5">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button
                          key={star}
                          type="button"
                          onClick={() => setStarRating(index, star)}
                          disabled={disabled}
                          className="p-0.5"
                        >
                          <Star
                            className={`w-4 h-4 ${
                              star <= getStarRating(option.scoring)
                                ? 'fill-yellow-400 text-yellow-400'
                                : 'text-gray-300'
                            }`}
                          />
                        </button>
                      ))}
                      <span className="text-xs text-muted-foreground ml-1 w-6">
                        {option.scoring}
                      </span>
                    </div>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      onClick={() => handleRemoveScoringOption(index)}
                      disabled={disabled || (question.scoring_values?.length || 0) <= 2}
                      className="h-8 w-8 text-destructive"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                ))}
              </div>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={handleAddScoringOption}
                disabled={disabled}
              >
                <Plus className="w-4 h-4 mr-1" />
                Add Option
              </Button>
            </div>
          )}

          {/* Is Killer Question */}
          <div className="flex items-center gap-3 pt-2">
            <Checkbox
              id="is_killer"
              checked={question.is_killer || false}
              onCheckedChange={(checked: boolean) => updateField('is_killer', checked)}
              disabled={disabled}
            />
            <div>
              <Label htmlFor="is_killer">Killer Question</Label>
              <p className="text-xs text-muted-foreground">
                Auto-reject candidates with low scores on this question
              </p>
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button
            type="button"
            onClick={onSave}
            disabled={disabled || !question.name.trim()}
          >
            Save Question
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
