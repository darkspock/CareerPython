/**
 * Public Interview Answer Page
 * Full-page interface for candidates and interviewers to answer interview questions
 * Accessible via secure token link
 */

import { useState, useEffect } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { Save, CheckCircle, AlertCircle, Loader2, Star } from 'lucide-react';
import { publicInterviewService, type InterviewQuestionsResponse, type InterviewSection, type InterviewQuestion } from '../../services/publicInterviewService';
import { toast } from 'react-toastify';

export default function InterviewAnswerPage() {
  const { interviewId } = useParams<{ interviewId: string }>();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  const [data, setData] = useState<InterviewQuestionsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState<Record<string, boolean>>({});
  const [saved, setSaved] = useState<Record<string, boolean>>({});

  useEffect(() => {
    if (interviewId && token) {
      loadInterviewQuestions();
    } else {
      setError('Interview ID or token is missing');
      setLoading(false);
    }
  }, [interviewId, token]);

  useEffect(() => {
    // Initialize answers from existing_answers
    if (data?.existing_answers) {
      const initialAnswers: Record<string, string> = {};
      Object.entries(data.existing_answers).forEach(([questionId, answerText]) => {
        if (answerText) {
          initialAnswers[questionId] = answerText;
        }
      });
      setAnswers(initialAnswers);
    }
  }, [data]);

  const loadInterviewQuestions = async () => {
    if (!interviewId || !token) return;

    try {
      setLoading(true);
      setError(null);
      const response = await publicInterviewService.getInterviewQuestions(interviewId, token);
      setData(response);
    } catch (err: any) {
      setError(err.message || 'Failed to load interview questions');
      console.error('Error loading interview questions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId: string, answerText: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: answerText }));
    setSaved(prev => ({ ...prev, [questionId]: false }));
  };

  const handleSaveAnswer = async (question: InterviewQuestion) => {
    if (!interviewId || !token) return;

    const answerText = answers[question.id] || '';
    setSaving(prev => ({ ...prev, [question.id]: true }));

    try {
      await publicInterviewService.submitAnswer(interviewId, token, {
        question_id: question.id,
        answer_text: answerText,
        question_text: question.name
      });

      setSaved(prev => ({ ...prev, [question.id]: true }));
      toast.success('Answer saved successfully');
      
      // Clear saved status after 3 seconds
      setTimeout(() => {
        setSaved(prev => {
          const newSaved = { ...prev };
          delete newSaved[question.id];
          return newSaved;
        });
      }, 3000);
    } catch (err: any) {
      toast.error(err.message || 'Failed to save answer');
      console.error('Error saving answer:', err);
    } finally {
      setSaving(prev => {
        const newSaving = { ...prev };
        delete newSaving[question.id];
        return newSaving;
      });
    }
  };

  const renderQuestion = (question: InterviewQuestion, section: InterviewSection) => {
    const answerText = answers[question.id] || '';
    const isSaving = saving[question.id] || false;
    const isSaved = saved[question.id] || false;
    
    // Check if this is a scoring question and determine the mode
    const scoringMode = data?.template?.scoring_mode?.toUpperCase();
    const isScoringQuestion = question.data_type?.toLowerCase() === 'scoring';
    const isDistanceMode = isScoringQuestion && scoringMode === 'DISTANCE';
    const isAbsoluteMode = isScoringQuestion && scoringMode === 'ABSOLUTE';
    
    // Distance mode options: Cerca (10), Medio (6), Lejos (3), Muy Lejos (1)
    const distanceOptions = [
      { label: 'Cerca', value: '10' },
      { label: 'Medio', value: '6' },
      { label: 'Lejos', value: '3' },
      { label: 'Muy Lejos', value: '1' }
    ];
    
    // Convert answer text to star rating (0-5 stars, each worth 2 points) for ABSOLUTE mode
    const getStarRatingFromAnswer = (text: string): number => {
      const num = parseInt(text, 10);
      if (isNaN(num)) return 0;
      // Convert score (0-10) to stars (0-5), where each star = 2 points
      return Math.round(num / 2);
    };
    
    // Convert star rating (0-5) to score (0-10) for ABSOLUTE mode
    const getAnswerFromStarRating = (stars: number): string => {
      return (stars * 2).toString();
    };
    
    const currentStarRating = isAbsoluteMode ? getStarRatingFromAnswer(answerText) : 0;

    const handleStarClick = (starIndex: number) => {
      if (!isAbsoluteMode) return;
      // starIndex is 0-based (0-4), but we want 1-5 stars
      const clickedRating = starIndex + 1;
      // If clicking the same star that's already selected, deselect (set to 0)
      const newRating = clickedRating === currentStarRating ? 0 : clickedRating;
      const newAnswer = getAnswerFromStarRating(newRating);
      handleAnswerChange(question.id, newAnswer);
    };
    
    const handleDistanceChange = (value: string) => {
      handleAnswerChange(question.id, value);
    };

    return (
      <div key={question.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-4">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {question.name}
            </h3>
            {question.description && (
              <p className="text-sm text-gray-600 mb-3">{question.description}</p>
            )}
          </div>
          {isSaved && (
            <div className="flex items-center text-green-600 ml-4">
              <CheckCircle className="w-5 h-5 mr-1" />
              <span className="text-sm font-medium">Saved</span>
            </div>
          )}
        </div>

        <div className="mb-4">
          {isDistanceMode ? (
            // DISTANCE mode: Show dropdown with distance options
            <div className="flex flex-col items-start">
              <select
                value={answerText || ''}
                onChange={(e) => handleDistanceChange(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 min-w-[200px]"
              >
                <option value="">Select a distance...</option>
                {distanceOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label} ({option.value} puntos)
                  </option>
                ))}
              </select>
              {answerText && (
                <p className="text-sm text-gray-600 mt-2">
                  Selected: {distanceOptions.find(opt => opt.value === answerText)?.label || answerText} puntos
                </p>
              )}
            </div>
          ) : isAbsoluteMode ? (
            // ABSOLUTE mode: Show 5 stars (each worth 2 points)
            <div className="flex flex-col items-start">
              <div className="flex items-center gap-2 mb-2">
                {[0, 1, 2, 3, 4].map((starIndex) => {
                  const isFilled = starIndex < currentStarRating;
                  return (
                    <button
                      key={starIndex}
                      type="button"
                      onClick={() => handleStarClick(starIndex)}
                      className={`transition-colors ${
                        isFilled
                          ? 'text-yellow-400 hover:text-yellow-500'
                          : 'text-gray-300 hover:text-gray-400'
                      }`}
                      aria-label={`Rate ${starIndex + 1} out of 5 stars`}
                    >
                      <Star
                        className="w-8 h-8"
                        fill={isFilled ? 'currentColor' : 'none'}
                        strokeWidth={isFilled ? 0 : 1.5}
                      />
                    </button>
                  );
                })}
              </div>
              <p className="text-sm text-gray-600">
                {currentStarRating > 0 ? `Score: ${currentStarRating * 2}/10` : 'Select a rating (each star = 2 points)'}
              </p>
            </div>
          ) : (
            // Regular question: Show textarea
            <textarea
              value={answerText}
              onChange={(e) => handleAnswerChange(question.id, e.target.value)}
              placeholder="Type your answer here..."
              className="w-full min-h-[120px] px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-y"
              rows={5}
            />
          )}
        </div>

        {question.legal_notice && (
          <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
            <p className="text-xs text-yellow-800">{question.legal_notice}</p>
          </div>
        )}

        <div className="flex justify-end">
          <button
            onClick={() => handleSaveAnswer(question)}
            disabled={isSaving}
            className={`flex items-center px-4 py-2 rounded-md font-medium transition-colors ${
              isSaving
                ? 'bg-gray-400 text-white cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {isSaving ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Saving...
              </>
            ) : (
              <>
                <Save className="w-4 h-4 mr-2" />
                Save Answer
              </>
            )}
          </button>
        </div>
      </div>
    );
  };

  const renderSection = (section: InterviewSection) => {
    if (section.questions.length === 0) {
      return null;
    }

    return (
      <div key={section.id} className="mb-8">
        <div className="mb-4">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">{section.name}</h2>
          {section.intro && (
            <p className="text-gray-600 mb-4">{section.intro}</p>
          )}
          {section.goal && (
            <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mb-4">
              <p className="text-sm text-blue-800">
                <strong>Goal:</strong> {section.goal}
              </p>
            </div>
          )}
        </div>

        <div>
          {section.questions
            .sort((a, b) => a.sort_order - b.sort_order)
            .map(question => renderQuestion(question, section))}
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading interview questions...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center mb-4">
            <AlertCircle className="w-8 h-8 text-red-600 mr-3" />
            <h2 className="text-xl font-bold text-gray-900">Error</h2>
          </div>
          <p className="text-gray-600 mb-4">{error}</p>
          <p className="text-sm text-gray-500">
            Please check that you have the correct link and that it hasn't expired.
          </p>
        </div>
      </div>
    );
  }

  if (!data) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {data.interview_title || 'Interview Questions'}
          </h1>
          {data.interview_description && (
            <p className="text-gray-600">{data.interview_description}</p>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {data.template && (
          <>
            {data.template.intro && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
                <h2 className="text-xl font-semibold text-gray-900 mb-2">Introduction</h2>
                <p className="text-gray-700 whitespace-pre-wrap">{data.template.intro}</p>
              </div>
            )}

            {data.template.sections
              .sort((a, b) => a.sort_order - b.sort_order)
              .map(section => renderSection(section))}
          </>
        )}

        {(!data.template || data.template.sections.length === 0) && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
            <p className="text-gray-600">No questions available for this interview.</p>
          </div>
        )}
      </div>
    </div>
  );
}

