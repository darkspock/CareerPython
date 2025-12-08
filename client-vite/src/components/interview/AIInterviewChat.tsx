/**
 * AI Interview Chat Component
 * Conversational interface for AI-powered interviews
 * Phase: AI Interview Integration
 */

import { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Loader2, Pause, Play, CheckCircle, AlertCircle } from 'lucide-react';
import { ApiClient } from '../../lib/api';

export interface ChatMessage {
  id: string;
  role: 'assistant' | 'user';
  content: string;
  timestamp: Date;
  questionId?: string;
  isFollowUp?: boolean;
  section?: string;
}

export interface AIInterviewChatProps {
  interviewId: string;
  interviewTitle: string;
  sections: Array<{
    id: string;
    name: string;
    questions: Array<{
      id: string;
      name: string;
      description?: string;
    }>;
  }>;
  onAnswerSubmit: (questionId: string, answer: string) => Promise<void>;
  onComplete: () => void;
  existingAnswers?: Record<string, string>;
  allowAIFollowup?: boolean;
}

interface InterviewState {
  currentSectionIndex: number;
  currentQuestionIndex: number;
  isComplete: boolean;
  isPaused: boolean;
  waitingForResponse: boolean;
}

export function AIInterviewChat({
  interviewId: _interviewId,
  interviewTitle,
  sections,
  onAnswerSubmit,
  onComplete,
  existingAnswers = {},
  allowAIFollowup = true
}: AIInterviewChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [state, setState] = useState<InterviewState>({
    currentSectionIndex: 0,
    currentQuestionIndex: 0,
    isComplete: false,
    isPaused: false,
    waitingForResponse: false
  });
  const [error, setError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize chat with welcome message and first question
  useEffect(() => {
    if (messages.length === 0 && sections.length > 0) {
      initializeChat();
    }
  }, [sections]);

  const initializeChat = async () => {
    const welcomeMessage: ChatMessage = {
      id: `msg_welcome_${Date.now()}`,
      role: 'assistant',
      content: `Welcome to the "${interviewTitle}" interview. I'll guide you through a series of questions across ${sections.length} section${sections.length > 1 ? 's' : ''}. Take your time to provide thoughtful responses.\n\nLet's begin with the first section: **${sections[0].name}**`,
      timestamp: new Date()
    };

    setMessages([welcomeMessage]);

    // Add first question after a brief delay
    setTimeout(() => {
      askCurrentQuestion();
    }, 1500);
  };

  const getCurrentQuestion = () => {
    const section = sections[state.currentSectionIndex];
    if (!section) return null;
    return section.questions[state.currentQuestionIndex] || null;
  };

  const askCurrentQuestion = () => {
    const question = getCurrentQuestion();
    if (!question) return;

    const section = sections[state.currentSectionIndex];

    setIsTyping(true);

    setTimeout(() => {
      const questionMessage: ChatMessage = {
        id: `msg_q_${question.id}_${Date.now()}`,
        role: 'assistant',
        content: question.description
          ? `**${question.name}**\n\n${question.description}`
          : question.name,
        timestamp: new Date(),
        questionId: question.id,
        section: section.name
      };

      setMessages(prev => [...prev, questionMessage]);
      setIsTyping(false);
      setState(prev => ({ ...prev, waitingForResponse: true }));

      // Check if there's an existing answer
      if (existingAnswers[question.id]) {
        setInputValue(existingAnswers[question.id]);
      }
    }, 800 + Math.random() * 400);
  };

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();

    if (!inputValue.trim() || state.isPaused || !state.waitingForResponse) return;

    const question = getCurrentQuestion();
    if (!question) return;

    const userMessage: ChatMessage = {
      id: `msg_user_${Date.now()}`,
      role: 'user',
      content: inputValue.trim(),
      timestamp: new Date(),
      questionId: question.id
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setState(prev => ({ ...prev, waitingForResponse: false }));
    setError(null);

    try {
      // Save the answer
      await onAnswerSubmit(question.id, userMessage.content);

      // Simulate AI processing and potential follow-up
      if (allowAIFollowup && Math.random() > 0.6) {
        await handleFollowUpQuestion(userMessage.content, question);
      } else {
        await moveToNextQuestion();
      }
    } catch (err) {
      setError('Failed to save answer. Please try again.');
      setState(prev => ({ ...prev, waitingForResponse: true }));
    }
  };

  const handleFollowUpQuestion = async (userResponse: string, originalQuestion: any) => {
    setIsTyping(true);

    try {
      // Build conversation history from recent messages for context
      const recentMessages = messages.slice(-6).map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      // Call the AI follow-up endpoint
      const response = await ApiClient.post<{
        follow_up_question: string;
        success: boolean;
        error_message?: string;
      }>('/api/candidate/interviews/ai/follow-up', {
        question: originalQuestion.name,
        candidate_response: userResponse,
        position_context: interviewTitle,
        conversation_history: recentMessages
      });

      const followUpContent = response.follow_up_question || generateMockFollowUp(userResponse, originalQuestion.name);

      const followUpMessage: ChatMessage = {
        id: `msg_followup_${Date.now()}`,
        role: 'assistant',
        content: followUpContent,
        timestamp: new Date(),
        questionId: originalQuestion.id,
        isFollowUp: true
      };

      setMessages(prev => [...prev, followUpMessage]);
      setIsTyping(false);
      setState(prev => ({ ...prev, waitingForResponse: true }));

    } catch (err) {
      console.error('Error generating AI follow-up:', err);

      // Fallback to mock follow-up on error
      const fallbackFollowUp = generateMockFollowUp(userResponse, originalQuestion.name);

      const followUpMessage: ChatMessage = {
        id: `msg_followup_${Date.now()}`,
        role: 'assistant',
        content: fallbackFollowUp,
        timestamp: new Date(),
        questionId: originalQuestion.id,
        isFollowUp: true
      };

      setMessages(prev => [...prev, followUpMessage]);
      setIsTyping(false);
      setState(prev => ({ ...prev, waitingForResponse: true }));
    }
  };

  const generateMockFollowUp = (_response: string, _questionText: string): string => {
    // Fallback follow-up questions used when API fails
    const followUps = [
      `That's interesting! Could you elaborate more on that point? Specifically, what was the outcome of that approach?`,
      `Thank you for sharing. Can you give me a specific example of when you applied this in practice?`,
      `I'd like to understand better. What challenges did you face, and how did you overcome them?`,
      `Great insight! How would you handle a similar situation differently if given another chance?`,
      `That's helpful context. What did you learn from that experience that you still apply today?`
    ];

    return followUps[Math.floor(Math.random() * followUps.length)];
  };

  const moveToNextQuestion = async () => {
    setIsTyping(true);

    await new Promise(resolve => setTimeout(resolve, 600));

    const currentSection = sections[state.currentSectionIndex];
    const isLastQuestionInSection = state.currentQuestionIndex >= currentSection.questions.length - 1;
    const isLastSection = state.currentSectionIndex >= sections.length - 1;

    if (isLastQuestionInSection && isLastSection) {
      // Interview complete
      const completeMessage: ChatMessage = {
        id: `msg_complete_${Date.now()}`,
        role: 'assistant',
        content: `Excellent! You've completed all the questions in this interview. Thank you for your thoughtful responses.\n\nYour answers have been saved. You can close this page or review your responses.`,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, completeMessage]);
      setIsTyping(false);
      setState(prev => ({ ...prev, isComplete: true }));
      onComplete();
    } else if (isLastQuestionInSection) {
      // Move to next section
      const nextSection = sections[state.currentSectionIndex + 1];

      const transitionMessage: ChatMessage = {
        id: `msg_transition_${Date.now()}`,
        role: 'assistant',
        content: `Great work on completing the "${currentSection.name}" section!\n\nLet's move on to the next section: **${nextSection.name}**`,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, transitionMessage]);
      setIsTyping(false);

      setState(prev => ({
        ...prev,
        currentSectionIndex: prev.currentSectionIndex + 1,
        currentQuestionIndex: 0
      }));

      setTimeout(() => {
        askCurrentQuestion();
      }, 1500);
    } else {
      // Move to next question in current section
      setIsTyping(false);

      setState(prev => ({
        ...prev,
        currentQuestionIndex: prev.currentQuestionIndex + 1
      }));

      setTimeout(() => {
        askCurrentQuestion();
      }, 500);
    }
  };

  const handleSkipFollowUp = async () => {
    await moveToNextQuestion();
  };

  const togglePause = () => {
    setState(prev => ({ ...prev, isPaused: !prev.isPaused }));
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  // Calculate progress
  const totalQuestions = sections.reduce((acc, s) => acc + s.questions.length, 0);
  const answeredQuestions = sections.slice(0, state.currentSectionIndex).reduce((acc, s) => acc + s.questions.length, 0) + state.currentQuestionIndex;
  const progressPercentage = totalQuestions > 0 ? Math.round((answeredQuestions / totalQuestions) * 100) : 0;

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">{interviewTitle}</h2>
            <p className="text-sm text-gray-500 mt-1">
              AI-Assisted Interview • Section {state.currentSectionIndex + 1} of {sections.length}
            </p>
          </div>
          <div className="flex items-center gap-4">
            {/* Progress */}
            <div className="text-right">
              <p className="text-sm font-medium text-gray-700">{progressPercentage}% Complete</p>
              <div className="w-32 h-2 bg-gray-200 rounded-full mt-1">
                <div
                  className="h-full bg-blue-600 rounded-full transition-all duration-300"
                  style={{ width: `${progressPercentage}%` }}
                />
              </div>
            </div>
            {/* Pause/Resume */}
            {!state.isComplete && (
              <button
                onClick={togglePause}
                className={`p-2 rounded-lg ${
                  state.isPaused
                    ? 'bg-green-100 text-green-700 hover:bg-green-200'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
                title={state.isPaused ? 'Resume Interview' : 'Pause Interview'}
              >
                {state.isPaused ? <Play className="w-5 h-5" /> : <Pause className="w-5 h-5" />}
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Paused Banner */}
      {state.isPaused && (
        <div className="bg-yellow-50 border-b border-yellow-200 px-6 py-3">
          <div className="flex items-center gap-2 text-yellow-800">
            <Pause className="w-4 h-4" />
            <span className="text-sm font-medium">Interview Paused</span>
            <span className="text-sm">- Click the play button to resume</span>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`flex gap-3 max-w-[80%] ${
                message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
              }`}
            >
              {/* Avatar */}
              <div
                className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                {message.role === 'user' ? (
                  <User className="w-4 h-4" />
                ) : (
                  <Bot className="w-4 h-4" />
                )}
              </div>

              {/* Message Content */}
              <div
                className={`rounded-2xl px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : message.isFollowUp
                    ? 'bg-purple-50 border border-purple-200 text-gray-800'
                    : 'bg-white border border-gray-200 text-gray-800'
                }`}
              >
                {message.isFollowUp && (
                  <div className="flex items-center gap-1 text-xs text-purple-600 mb-2">
                    <Bot className="w-3 h-3" />
                    <span>Follow-up Question</span>
                  </div>
                )}
                <div className="whitespace-pre-wrap text-sm leading-relaxed">
                  {message.content.split('**').map((part, i) =>
                    i % 2 === 1 ? <strong key={i}>{part}</strong> : part
                  )}
                </div>
                <p className={`text-xs mt-2 ${
                  message.role === 'user' ? 'text-blue-200' : 'text-gray-400'
                }`}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            </div>
          </div>
        ))}

        {/* Typing Indicator */}
        {isTyping && (
          <div className="flex justify-start">
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                <Bot className="w-4 h-4 text-gray-600" />
              </div>
              <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="flex justify-center">
            <div className="bg-red-50 border border-red-200 rounded-lg px-4 py-2 flex items-center gap-2 text-red-700">
              <AlertCircle className="w-4 h-4" />
              <span className="text-sm">{error}</span>
            </div>
          </div>
        )}

        {/* Complete Message */}
        {state.isComplete && (
          <div className="flex justify-center">
            <div className="bg-green-50 border border-green-200 rounded-lg px-6 py-4 flex items-center gap-3">
              <CheckCircle className="w-6 h-6 text-green-600" />
              <div>
                <p className="font-medium text-green-800">Interview Complete!</p>
                <p className="text-sm text-green-600">All your answers have been saved.</p>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      {!state.isComplete && (
        <div className="border-t border-gray-200 bg-white px-6 py-4">
          {/* Skip follow-up button */}
          {messages.length > 0 && messages[messages.length - 1]?.isFollowUp && state.waitingForResponse && (
            <div className="mb-3 flex justify-end">
              <button
                onClick={handleSkipFollowUp}
                className="text-sm text-gray-500 hover:text-gray-700 underline"
              >
                Skip follow-up and continue
              </button>
            </div>
          )}

          <form onSubmit={handleSubmit} className="flex gap-3">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={
                state.isPaused
                  ? "Interview paused..."
                  : state.waitingForResponse
                  ? "Type your response..."
                  : "Waiting for next question..."
              }
              disabled={state.isPaused || !state.waitingForResponse || isTyping}
              className="flex-1 resize-none rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              rows={2}
            />
            <button
              type="submit"
              disabled={!inputValue.trim() || state.isPaused || !state.waitingForResponse || isTyping}
              className="self-end px-4 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              {isTyping ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </form>
          <p className="text-xs text-gray-400 mt-2 text-center">
            Press Enter to send, Shift+Enter for new line
          </p>
        </div>
      )}
    </div>
  );
}
