import type {
  Interview,
  InterviewProgress,
  InterviewType,
  QuestionCategory,
  QuestionDifficulty,
  ConversationalQuestion
} from '../types/interview';

// Analytics Data Types
export interface InterviewCompletionAnalytics {
  interviewId: string;
  candidateId: string;
  templateId: string;
  interviewType: InterviewType;
  completionMetrics: {
    totalDuration: number; // seconds
    questionsAnswered: number;
    questionsSkipped: number;
    completionRate: number; // 0-1
    averageQuestionTime: number;
    timeDistribution: {
      category: QuestionCategory;
      totalTime: number;
      questionCount: number;
      averageTime: number;
    }[];
  };
  performanceMetrics: {
    overallScore: number; // 0-10
    categoryScores: Record<QuestionCategory, {
      score: number;
      questionsAnswered: number;
      averageConfidence: number;
      timeEfficiency: number;
    }>;
    difficultyPerformance: Record<QuestionDifficulty, {
      score: number;
      questionsAnswered: number;
      successRate: number;
    }>;
    consistencyScore: number; // variance in performance
    improvementTrend: 'improving' | 'stable' | 'declining';
  };
  qualityMetrics: {
    responseQuality: {
      averageLength: number;
      vocabularyDiversity: number;
      technicalDepth: number;
      clarityScore: number;
    };
    engagementMetrics: {
      responsiveness: number; // how quickly they respond
      elaborationLevel: number; // depth of answers
      questionAsking: number; // how many questions they ask
      overallEngagement: number;
    };
  };
  behavioralInsights: {
    communicationStyle: 'concise' | 'detailed' | 'storytelling' | 'mixed';
    confidencePattern: 'building' | 'stable' | 'declining' | 'variable';
    stressIndicators: {
      timeOutliers: number; // questions taking unusually long
      qualityDips: number; // drops in response quality
      confidenceDrops: number;
      overallStressLevel: 'low' | 'moderate' | 'high';
    };
    strengths: string[];
    growthAreas: string[];
  };
}

export interface CandidatePerformanceInsights {
  candidateId: string;
  profileSummary: {
    totalInterviews: number;
    averageScore: number;
    improvementRate: number;
    strongestCategory: QuestionCategory;
    weakestCategory: QuestionCategory;
    preferredDifficulty: QuestionDifficulty;
  };
  performanceHistory: Array<{
    date: string;
    interviewType: InterviewType;
    score: number;
    duration: number;
    completionRate: number;
    keyInsights: string[];
  }>;
  skillProgression: Record<string, {
    currentLevel: number;
    progressRate: number;
    assessmentCount: number;
    lastAssessment: string;
    trendDirection: 'up' | 'stable' | 'down';
  }>;
  adaptiveRecommendations: {
    focusAreas: string[];
    recommendedResources: Array<{
      type: 'course' | 'practice' | 'reading' | 'mentoring';
      title: string;
      description: string;
      priority: 'critical' | 'high' | 'medium' | 'low';
      estimatedTime: string;
    }>;
    nextInterviewStrategy: {
      recommendedType: InterviewType;
      suggestedDifficulty: QuestionDifficulty;
      focusCategories: QuestionCategory[];
      preparationTime: number;
    };
  };
}

export interface InterviewEffectivenessMetrics {
  templateId: string;
  templateName: string;
  effectivenessScore: number; // 0-10
  usageStatistics: {
    totalUses: number;
    averageCompletionRate: number;
    averageDuration: number;
    candidateSatisfaction: number;
    interviewerSatisfaction: number;
  };
  questionEffectiveness: Array<{
    questionId: string;
    questionText: string;
    category: QuestionCategory;
    difficulty: QuestionDifficulty;
    metrics: {
      averageResponseTime: number;
      averageResponseQuality: number;
      candidateConfidence: number;
      discriminationIndex: number; // how well it differentiates candidates
      difficultyCalibration: number; // actual vs intended difficulty
    };
    improvements: string[];
  }>;
  templateOptimizations: {
    suggestedQuestionOrder: string[];
    recommendedTimeAllocations: Record<string, number>;
    proposedDifficultyAdjustments: Array<{
      questionId: string;
      currentDifficulty: QuestionDifficulty;
      suggestedDifficulty: QuestionDifficulty;
      reasoning: string;
    }>;
  };
}

export interface TemplatePerformanceAnalytics {
  templateId: string;
  performanceMetrics: {
    totalCompletions: number;
    averageScore: number;
    completionRate: number;
    candidateSatisfaction: number;
    timeEfficiency: number;
  };
  questionAnalytics: Array<{
    questionId: string;
    performanceData: {
      averageScore: number;
      responseTime: number;
      skipRate: number;
      difficultyAccuracy: number;
    };
    candidateFeedback: {
      clarity: number;
      relevance: number;
      difficulty: number;
      engagement: number;
    };
  }>;
  categoryDistribution: Record<QuestionCategory, {
    questionCount: number;
    averagePerformance: number;
    timeAllocation: number;
    effectiveness: number;
  }>;
  recommendedImprovements: Array<{
    type: 'question_replacement' | 'order_optimization' | 'difficulty_adjustment' | 'time_reallocation';
    description: string;
    impact: 'high' | 'medium' | 'low';
    implementation: string;
  }>;
}

export interface InterviewImprovementRecommendation {
  id: string;
  type: 'template' | 'process' | 'candidate_specific' | 'system_wide';
  priority: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  reasoning: string;
  expectedImpact: {
    scoreImprovement: number;
    timeReduction: number;
    satisfactionIncrease: number;
    implementationEffort: 'low' | 'medium' | 'high';
  };
  actionSteps: Array<{
    step: string;
    owner: 'interviewer' | 'candidate' | 'system' | 'admin';
    timeframe: string;
    resources?: string[];
  }>;
  metrics: {
    baseline: Record<string, number>;
    targets: Record<string, number>;
    measurement: string;
  };
}

class InterviewAnalyticsService {
  private readonly API_BASE = '/api/interviews/analytics';

  // Interview Completion Analytics
  async generateCompletionAnalytics(interviewId: string): Promise<InterviewCompletionAnalytics> {
    try {
      // In real implementation, this would call the API
      // For now, implementing sophisticated mock analytics

      // Fetch interview data
      const interview = await this.fetchInterviewData(interviewId);
      const responses = await this.fetchInterviewResponses(interviewId);
      const progress = await this.fetchInterviewProgress(interviewId);

      // Calculate completion metrics
      const completionMetrics = this.calculateCompletionMetrics(interview, responses, progress);

      // Calculate performance metrics
      const performanceMetrics = this.calculatePerformanceMetrics(responses);

      // Analyze response quality
      const qualityMetrics = this.analyzeResponseQuality(responses);

      // Generate behavioral insights
      const behavioralInsights = this.generateBehavioralInsights(responses, progress);

      return {
        interviewId,
        candidateId: interview.candidateId,
        templateId: interview.templateId,
        interviewType: interview.type,
        completionMetrics,
        performanceMetrics,
        qualityMetrics,
        behavioralInsights
      };

    } catch (error) {
      console.error('Failed to generate completion analytics:', error);
      throw new Error('Completion analytics generation failed');
    }
  }

  // Candidate Performance Tracking
  async generateCandidateInsights(candidateId: string): Promise<CandidatePerformanceInsights> {
    try {
      // Fetch candidate's interview history
      const interviewHistory = await this.fetchCandidateInterviews(candidateId);

      // Generate profile summary
      const profileSummary = this.calculateProfileSummary(interviewHistory);

      // Analyze performance history
      const performanceHistory = this.analyzePerformanceHistory(interviewHistory);

      // Track skill progression
      const skillProgression = this.trackSkillProgression(interviewHistory);

      // Generate adaptive recommendations
      const adaptiveRecommendations = this.generateAdaptiveRecommendations(
        profileSummary,
        performanceHistory,
        skillProgression
      );

      return {
        candidateId,
        profileSummary,
        performanceHistory,
        skillProgression,
        adaptiveRecommendations
      };

    } catch (error) {
      console.error('Failed to generate candidate insights:', error);
      throw new Error('Candidate insights generation failed');
    }
  }

  // Interview Effectiveness Measurement
  async measureInterviewEffectiveness(templateId: string): Promise<InterviewEffectivenessMetrics> {
    try {
      // Fetch template usage data
      const templateData = await this.fetchTemplateData(templateId);
      const usageHistory = await this.fetchTemplateUsageHistory(templateId);

      // Calculate effectiveness score
      const effectivenessScore = this.calculateEffectivenessScore(usageHistory);

      // Analyze usage statistics
      const usageStatistics = this.analyzeUsageStatistics(usageHistory);

      // Evaluate question effectiveness
      const questionEffectiveness = this.evaluateQuestionEffectiveness(usageHistory);

      // Generate optimization recommendations
      const templateOptimizations = this.generateTemplateOptimizations(
        questionEffectiveness,
        usageStatistics
      );

      return {
        templateId,
        templateName: templateData.name,
        effectivenessScore,
        usageStatistics,
        questionEffectiveness,
        templateOptimizations
      };

    } catch (error) {
      console.error('Failed to measure interview effectiveness:', error);
      throw new Error('Interview effectiveness measurement failed');
    }
  }

  // Template Performance Analytics
  async analyzeTemplatePerformance(templateId: string): Promise<TemplatePerformanceAnalytics> {
    try {
      const usageData = await this.fetchTemplateUsageHistory(templateId);

      // Calculate performance metrics
      const performanceMetrics = this.calculateTemplatePerformanceMetrics(usageData);

      // Analyze individual questions
      const questionAnalytics = this.analyzeTemplateQuestions(usageData);

      // Calculate category distribution
      const categoryDistribution = this.calculateCategoryDistribution(usageData);

      // Generate improvement recommendations
      const recommendedImprovements = this.generateTemplateImprovements(
        performanceMetrics,
        questionAnalytics,
        categoryDistribution
      );

      return {
        templateId,
        performanceMetrics,
        questionAnalytics,
        categoryDistribution,
        recommendedImprovements
      };

    } catch (error) {
      console.error('Failed to analyze template performance:', error);
      throw new Error('Template performance analysis failed');
    }
  }

  // Interview Improvement Recommendations
  async generateImprovementRecommendations(
    context: {
      templateId?: string;
      candidateId?: string;
      interviewId?: string;
      systemWide?: boolean;
    }
  ): Promise<InterviewImprovementRecommendation[]> {
    try {
      const recommendations: InterviewImprovementRecommendation[] = [];

      if (context.templateId) {
        const templateRecommendations = await this.generateTemplateRecommendations(context.templateId);
        recommendations.push(...templateRecommendations);
      }

      if (context.candidateId) {
        const candidateRecommendations = await this.generateCandidateRecommendations(context.candidateId);
        recommendations.push(...candidateRecommendations);
      }

      if (context.interviewId) {
        const interviewRecommendations = await this.generateInterviewSpecificRecommendations(context.interviewId);
        recommendations.push(...interviewRecommendations);
      }

      if (context.systemWide) {
        const systemRecommendations = await this.generateSystemWideRecommendations();
        recommendations.push(...systemRecommendations);
      }

      // Sort by priority and impact
      return recommendations.sort((a, b) => {
        const priorityOrder = { critical: 4, high: 3, medium: 2, low: 1 };
        const aPriority = priorityOrder[a.priority];
        const bPriority = priorityOrder[b.priority];

        if (aPriority !== bPriority) {
          return bPriority - aPriority;
        }

        return b.expectedImpact.scoreImprovement - a.expectedImpact.scoreImprovement;
      });

    } catch (error) {
      console.error('Failed to generate improvement recommendations:', error);
      throw new Error('Improvement recommendations generation failed');
    }
  }

  // Private helper methods for analytics calculations

  private async fetchInterviewData(interviewId: string): Promise<any> {
    // Mock interview data
    return {
      id: interviewId,
      candidateId: 'candidate-123',
      templateId: 'template-456',
      type: InterviewType.TECHNICAL,
      startTime: new Date(Date.now() - 3600000), // 1 hour ago
      endTime: new Date(),
      status: 'completed'
    };
  }

  private async fetchInterviewResponses(interviewId: string): Promise<any[]> {
    // Mock response data with varying quality and timing
    return [
      {
        questionId: 'q1',
        category: QuestionCategory.TECHNICAL,
        difficulty: QuestionDifficulty.MEDIUM,
        response: 'I would approach this problem by first understanding the requirements and then designing a scalable solution using microservices architecture.',
        responseTime: 180,
        confidence: 0.8,
        quality: 0.75,
        wordCount: 95
      },
      {
        questionId: 'q2',
        category: QuestionCategory.BEHAVIORAL,
        difficulty: QuestionDifficulty.EASY,
        response: 'In my previous role, I led a team of 5 developers through a challenging project that had tight deadlines.',
        responseTime: 120,
        confidence: 0.9,
        quality: 0.85,
        wordCount: 67
      },
      // ... more mock responses
    ];
  }

  private async fetchInterviewProgress(interviewId: string): Promise<any> {
    return {
      questionsTotal: 15,
      questionsAnswered: 12,
      questionsSkipped: 3,
      currentQuestion: null,
      timeSpent: 3600,
      completionPercentage: 0.8
    };
  }

  private calculateCompletionMetrics(interview: any, responses: any[], progress: any): any {
    const totalDuration = (interview.endTime - interview.startTime) / 1000;
    const questionsAnswered = responses.length;
    const questionsSkipped = progress.questionsTotal - questionsAnswered;
    const completionRate = questionsAnswered / progress.questionsTotal;
    const averageQuestionTime = totalDuration / questionsAnswered;

    // Calculate time distribution by category
    const timeDistribution = Object.values(QuestionCategory).map(category => {
      const categoryResponses = responses.filter(r => r.category === category);
      const totalTime = categoryResponses.reduce((sum, r) => sum + r.responseTime, 0);
      const questionCount = categoryResponses.length;

      return {
        category,
        totalTime,
        questionCount,
        averageTime: questionCount > 0 ? totalTime / questionCount : 0
      };
    });

    return {
      totalDuration,
      questionsAnswered,
      questionsSkipped,
      completionRate,
      averageQuestionTime,
      timeDistribution
    };
  }

  private calculatePerformanceMetrics(responses: any[]): any {
    // Calculate overall score
    const overallScore = responses.reduce((sum, r) => sum + r.quality, 0) / responses.length * 10;

    // Calculate category scores
    const categoryScores = Object.values(QuestionCategory).reduce((acc, category) => {
      const categoryResponses = responses.filter(r => r.category === category);
      if (categoryResponses.length > 0) {
        const score = categoryResponses.reduce((sum, r) => sum + r.quality, 0) / categoryResponses.length * 10;
        const averageConfidence = categoryResponses.reduce((sum, r) => sum + r.confidence, 0) / categoryResponses.length;
        const timeEfficiency = this.calculateTimeEfficiency(categoryResponses);

        acc[category] = {
          score,
          questionsAnswered: categoryResponses.length,
          averageConfidence,
          timeEfficiency
        };
      }
      return acc;
    }, {} as Record<QuestionCategory, any>);

    // Calculate difficulty performance
    const difficultyPerformance = Object.values(QuestionDifficulty).reduce((acc, difficulty) => {
      const difficultyResponses = responses.filter(r => r.difficulty === difficulty);
      if (difficultyResponses.length > 0) {
        const score = difficultyResponses.reduce((sum, r) => sum + r.quality, 0) / difficultyResponses.length * 10;
        const successRate = difficultyResponses.filter(r => r.quality > 0.6).length / difficultyResponses.length;

        acc[difficulty] = {
          score,
          questionsAnswered: difficultyResponses.length,
          successRate
        };
      }
      return acc;
    }, {} as Record<QuestionDifficulty, any>);

    // Calculate consistency score
    const scores = responses.map(r => r.quality);
    const mean = scores.reduce((sum, score) => sum + score, 0) / scores.length;
    const variance = scores.reduce((sum, score) => sum + Math.pow(score - mean, 2), 0) / scores.length;
    const consistencyScore = Math.max(0, 1 - Math.sqrt(variance));

    // Determine improvement trend
    const firstHalf = responses.slice(0, Math.ceil(responses.length / 2));
    const secondHalf = responses.slice(Math.floor(responses.length / 2));
    const firstHalfAvg = firstHalf.reduce((sum, r) => sum + r.quality, 0) / firstHalf.length;
    const secondHalfAvg = secondHalf.reduce((sum, r) => sum + r.quality, 0) / secondHalf.length;

    const improvementTrend = secondHalfAvg > firstHalfAvg + 0.1 ? 'improving' :
                            secondHalfAvg < firstHalfAvg - 0.1 ? 'declining' : 'stable';

    return {
      overallScore,
      categoryScores,
      difficultyPerformance,
      consistencyScore,
      improvementTrend
    };
  }

  private analyzeResponseQuality(responses: any[]): any {
    const averageLength = responses.reduce((sum, r) => sum + r.wordCount, 0) / responses.length;

    // Mock quality metrics - in real implementation, these would use NLP
    const vocabularyDiversity = 0.7; // Based on unique words / total words
    const technicalDepth = 0.8; // Based on technical term usage
    const clarityScore = 0.75; // Based on readability metrics

    const responseTimes = responses.map(r => r.responseTime);
    const averageResponseTime = responseTimes.reduce((sum, time) => sum + time, 0) / responseTimes.length;
    const responsiveness = Math.max(0, 1 - (averageResponseTime - 60) / 300); // Normalized

    const elaborationLevel = Math.min(1, averageLength / 100); // Normalized to 100 words
    const questionAsking = 0.2; // Mock - candidates asking clarifying questions
    const overallEngagement = (responsiveness + elaborationLevel + questionAsking) / 3;

    return {
      responseQuality: {
        averageLength,
        vocabularyDiversity,
        technicalDepth,
        clarityScore
      },
      engagementMetrics: {
        responsiveness,
        elaborationLevel,
        questionAsking,
        overallEngagement
      }
    };
  }

  private generateBehavioralInsights(responses: any[], progress: any): any {
    // Analyze communication style based on response patterns
    const averageLength = responses.reduce((sum, r) => sum + r.wordCount, 0) / responses.length;
    const communicationStyle = averageLength > 150 ? 'detailed' :
                              averageLength < 50 ? 'concise' : 'balanced';

    // Analyze confidence pattern
    const confidences = responses.map(r => r.confidence);
    const firstHalf = confidences.slice(0, Math.ceil(confidences.length / 2));
    const secondHalf = confidences.slice(Math.floor(confidences.length / 2));
    const firstAvg = firstHalf.reduce((sum, c) => sum + c, 0) / firstHalf.length;
    const secondAvg = secondHalf.reduce((sum, c) => sum + c, 0) / secondHalf.length;

    const confidencePattern = secondAvg > firstAvg + 0.1 ? 'building' :
                             secondAvg < firstAvg - 0.1 ? 'declining' : 'stable';

    // Analyze stress indicators
    const responseTimes = responses.map(r => r.responseTime);
    const avgTime = responseTimes.reduce((sum, time) => sum + time, 0) / responseTimes.length;
    const timeOutliers = responseTimes.filter(time => time > avgTime * 2).length;

    const qualities = responses.map(r => r.quality);
    const avgQuality = qualities.reduce((sum, q) => sum + q, 0) / qualities.length;
    const qualityDips = qualities.filter(q => q < avgQuality * 0.7).length;

    const confidenceDrops = confidences.filter(c => c < 0.5).length;

    const stressLevel = timeOutliers + qualityDips + confidenceDrops > 3 ? 'high' :
                       timeOutliers + qualityDips + confidenceDrops > 1 ? 'moderate' : 'low';

    // Identify strengths and growth areas
    const categoryPerformance = Object.values(QuestionCategory).map(category => {
      const categoryResponses = responses.filter(r => r.category === category);
      if (categoryResponses.length === 0) return null;

      const avgScore = categoryResponses.reduce((sum, r) => sum + r.quality, 0) / categoryResponses.length;
      return { category, score: avgScore };
    }).filter(Boolean);

    const sortedCategories = categoryPerformance.sort((a, b) => b!.score - a!.score);
    const strengths = sortedCategories.slice(0, 2).map(c => c!.category);
    const growthAreas = sortedCategories.slice(-2).map(c => c!.category);

    return {
      communicationStyle,
      confidencePattern,
      stressIndicators: {
        timeOutliers,
        qualityDips,
        confidenceDrops,
        overallStressLevel: stressLevel
      },
      strengths,
      growthAreas
    };
  }

  private calculateTimeEfficiency(responses: any[]): number {
    // Calculate efficiency as quality per unit time
    const efficiencies = responses.map(r => r.quality / (r.responseTime / 60)); // quality per minute
    const avgEfficiency = efficiencies.reduce((sum, eff) => sum + eff, 0) / efficiencies.length;
    return Math.min(1, avgEfficiency / 0.5); // Normalize assuming max 0.5 quality per minute
  }

  // Additional placeholder methods for comprehensive analytics
  private async fetchCandidateInterviews(candidateId: string): Promise<any[]> {
    // Mock comprehensive interview history for demonstration
    return [
      {
        id: 'int-1',
        date: '2024-01-20T14:30:00Z',
        type: InterviewType.TECHNICAL,
        overallScore: 7.8,
        duration: 3600,
        completionRate: 0.9,
        categoryScores: {
          [QuestionCategory.TECHNICAL]: 8.2,
          [QuestionCategory.BEHAVIORAL]: 7.1,
          [QuestionCategory.SYSTEM_DESIGN]: 7.5
        },
        difficultyPerformance: {
          [QuestionDifficulty.EASY]: { score: 8.5, count: 3 },
          [QuestionDifficulty.MEDIUM]: { score: 7.8, count: 5 },
          [QuestionDifficulty.HARD]: { score: 6.9, count: 2 }
        },
        skillsAssessed: ['JavaScript', 'React', 'Node.js', 'System Design', 'Problem Solving'],
        keyInsights: ['Strong technical fundamentals', 'Good problem-solving approach', 'Could improve system design depth']
      },
      {
        id: 'int-2',
        date: '2024-01-10T09:00:00Z',
        type: InterviewType.BEHAVIORAL,
        overallScore: 8.3,
        duration: 2700,
        completionRate: 1.0,
        categoryScores: {
          [QuestionCategory.BEHAVIORAL]: 8.7,
          [QuestionCategory.SITUATIONAL]: 7.9
        },
        skillsAssessed: ['Leadership', 'Communication', 'Team Collaboration', 'Conflict Resolution'],
        keyInsights: ['Excellent communication skills', 'Strong leadership examples', 'Good cultural fit']
      },
      {
        id: 'int-3',
        date: '2023-12-15T16:00:00Z',
        type: InterviewType.TECHNICAL,
        overallScore: 7.1,
        duration: 4200,
        completionRate: 0.8,
        categoryScores: {
          [QuestionCategory.TECHNICAL]: 7.3,
          [QuestionCategory.SYSTEM_DESIGN]: 6.8
        },
        skillsAssessed: ['JavaScript', 'Algorithms', 'Data Structures', 'System Design'],
        keyInsights: ['Solid coding skills', 'Needs improvement in complex algorithms', 'System design understanding developing']
      }
    ];
  }

  private calculateProfileSummary(interviews: any[]): any {
    if (interviews.length === 0) {
      return {
        totalInterviews: 0,
        averageScore: 0,
        improvementRate: 0,
        strongestCategory: QuestionCategory.TECHNICAL,
        weakestCategory: QuestionCategory.BEHAVIORAL,
        preferredDifficulty: QuestionDifficulty.MEDIUM
      };
    }

    const totalInterviews = interviews.length;
    const averageScore = interviews.reduce((sum, interview) => sum + interview.overallScore, 0) / totalInterviews;

    // Calculate improvement rate by comparing first half to second half
    const firstHalf = interviews.slice(0, Math.ceil(interviews.length / 2));
    const secondHalf = interviews.slice(Math.floor(interviews.length / 2));

    const firstHalfAvg = firstHalf.reduce((sum, int) => sum + int.overallScore, 0) / firstHalf.length;
    const secondHalfAvg = secondHalf.reduce((sum, int) => sum + int.overallScore, 0) / secondHalf.length;
    const improvementRate = (secondHalfAvg - firstHalfAvg) / firstHalfAvg;

    // Find strongest and weakest categories
    const categoryTotals = interviews.reduce((acc, interview) => {
      Object.entries(interview.categoryScores || {}).forEach(([category, score]) => {
        if (!acc[category]) acc[category] = { total: 0, count: 0 };
        acc[category].total += score as number;
        acc[category].count += 1;
      });
      return acc;
    }, {} as Record<string, { total: number; count: number }>);

    const categoryAverages = Object.entries(categoryTotals).map(([category, data]) => ({
      category: category as QuestionCategory,
      average: data.total / data.count
    }));

    const sortedCategories = categoryAverages.sort((a, b) => b.average - a.average);
    const strongestCategory = sortedCategories[0]?.category || QuestionCategory.TECHNICAL;
    const weakestCategory = sortedCategories[sortedCategories.length - 1]?.category || QuestionCategory.BEHAVIORAL;

    // Analyze preferred difficulty (where they perform best)
    const difficultyPerformance = interviews.reduce((acc, interview) => {
      Object.entries(interview.difficultyPerformance || {}).forEach(([difficulty, data]) => {
        if (!acc[difficulty]) acc[difficulty] = { totalScore: 0, totalCount: 0 };
        acc[difficulty].totalScore += (data as any).score * (data as any).count;
        acc[difficulty].totalCount += (data as any).count;
      });
      return acc;
    }, {} as Record<string, { totalScore: number; totalCount: number }>);

    const difficultyAverages = Object.entries(difficultyPerformance).map(([difficulty, data]) => ({
      difficulty: difficulty as QuestionDifficulty,
      average: data.totalScore / data.totalCount
    }));

    const preferredDifficulty = difficultyAverages.sort((a, b) => b.average - a.average)[0]?.difficulty || QuestionDifficulty.MEDIUM;

    return {
      totalInterviews,
      averageScore,
      improvementRate,
      strongestCategory,
      weakestCategory,
      preferredDifficulty
    };
  }

  private analyzePerformanceHistory(interviews: any[]): any[] {
    return interviews.map(interview => ({
      date: interview.date,
      interviewType: interview.type,
      score: interview.overallScore,
      duration: interview.duration,
      completionRate: interview.completionRate,
      keyInsights: interview.keyInsights
    }));
  }

  private trackSkillProgression(interviews: any[]): Record<string, any> {
    const skillData: Record<string, { scores: number[]; dates: string[] }> = {};

    // Collect skill assessments from all interviews
    interviews.forEach(interview => {
      if (interview.skillsAssessed) {
        interview.skillsAssessed.forEach((skill: string) => {
          if (!skillData[skill]) {
            skillData[skill] = { scores: [], dates: [] };
          }
          // Use category score as proxy for skill score
          const categoryScore = interview.categoryScores?.[QuestionCategory.TECHNICAL] || interview.overallScore;
          skillData[skill].scores.push(categoryScore);
          skillData[skill].dates.push(interview.date);
        });
      }
    });

    // Calculate progression for each skill
    const skillProgression: Record<string, any> = {};
    Object.entries(skillData).forEach(([skill, data]) => {
      if (data.scores.length > 0) {
        const currentLevel = data.scores[data.scores.length - 1];
        const firstLevel = data.scores[0];
        const progressRate = data.scores.length > 1 ? (currentLevel - firstLevel) / firstLevel : 0;

        let trendDirection: 'up' | 'stable' | 'down' = 'stable';
        if (progressRate > 0.1) trendDirection = 'up';
        else if (progressRate < -0.1) trendDirection = 'down';

        skillProgression[skill] = {
          currentLevel,
          progressRate,
          assessmentCount: data.scores.length,
          lastAssessment: data.dates[data.dates.length - 1],
          trendDirection
        };
      }
    });

    return skillProgression;
  }

  private generateAdaptiveRecommendations(profile: any, history: any[], skills: any): any {
    const focusAreas: string[] = [];
    const recommendedResources: any[] = [];

    // Identify focus areas based on weakest category and declining skills
    if (profile.weakestCategory) {
      focusAreas.push(`Improve ${profile.weakestCategory.replace('_', ' ')} skills`);
    }

    // Add declining skills to focus areas
    Object.entries(skills).forEach(([skill, data]) => {
      if ((data as any).trendDirection === 'down') {
        focusAreas.push(`Strengthen ${skill} capabilities`);
      }
    });

    // Generate resources based on focus areas
    if (focusAreas.some(area => area.includes('TECHNICAL'))) {
      recommendedResources.push({
        type: 'course',
        title: 'Advanced Algorithm Design',
        description: 'Comprehensive course covering complex algorithms and data structures',
        priority: 'high',
        estimatedTime: '4-6 weeks'
      });
    }

    if (focusAreas.some(area => area.includes('SYSTEM_DESIGN'))) {
      recommendedResources.push({
        type: 'practice',
        title: 'System Design Interview Practice',
        description: 'Practice with real-world system design problems',
        priority: 'critical',
        estimatedTime: '2-3 weeks'
      });
    }

    if (focusAreas.some(area => area.includes('BEHAVIORAL'))) {
      recommendedResources.push({
        type: 'mentoring',
        title: 'Leadership Skills Mentoring',
        description: 'One-on-one mentoring for leadership and communication skills',
        priority: 'medium',
        estimatedTime: '8-10 weeks'
      });
    }

    // Determine next interview strategy
    let recommendedType = InterviewType.TECHNICAL;
    let suggestedDifficulty = profile.preferredDifficulty;
    const focusCategories: QuestionCategory[] = [];

    // If behavioral is weak, recommend behavioral interview
    if (profile.weakestCategory === QuestionCategory.BEHAVIORAL) {
      recommendedType = InterviewType.BEHAVIORAL;
      focusCategories.push(QuestionCategory.BEHAVIORAL, QuestionCategory.SITUATIONAL);
    } else if (profile.weakestCategory === QuestionCategory.SYSTEM_DESIGN) {
      recommendedType = InterviewType.SYSTEM_DESIGN;
      focusCategories.push(QuestionCategory.SYSTEM_DESIGN, QuestionCategory.TECHNICAL);
    } else {
      focusCategories.push(QuestionCategory.TECHNICAL);
    }

    // Adjust difficulty based on recent performance
    if (profile.improvementRate > 0.1) {
      // Performing well, can handle higher difficulty
      if (suggestedDifficulty === QuestionDifficulty.EASY) suggestedDifficulty = QuestionDifficulty.MEDIUM;
      else if (suggestedDifficulty === QuestionDifficulty.MEDIUM) suggestedDifficulty = QuestionDifficulty.HARD;
    } else if (profile.improvementRate < -0.1) {
      // Struggling, reduce difficulty
      if (suggestedDifficulty === QuestionDifficulty.HARD) suggestedDifficulty = QuestionDifficulty.MEDIUM;
      else if (suggestedDifficulty === QuestionDifficulty.MEDIUM) suggestedDifficulty = QuestionDifficulty.EASY;
    }

    return {
      focusAreas,
      recommendedResources,
      nextInterviewStrategy: {
        recommendedType,
        suggestedDifficulty,
        focusCategories,
        preparationTime: Math.max(60, focusAreas.length * 30) // More focus areas = more prep time
      }
    };
  }

  private async fetchTemplateData(templateId: string): Promise<any> {
    // Mock comprehensive template data for demonstration
    return {
      id: templateId,
      name: 'Senior Full-Stack Developer Technical Interview',
      description: 'Comprehensive technical interview for senior-level candidates',
      version: '2.1',
      createdDate: '2024-01-15T10:00:00Z',
      lastModified: '2024-11-20T14:30:00Z',
      category: InterviewType.TECHNICAL,
      estimatedDuration: 3600, // 60 minutes
      questionCount: 12,
      difficultyDistribution: {
        [QuestionDifficulty.EASY]: 3,
        [QuestionDifficulty.MEDIUM]: 6,
        [QuestionDifficulty.HARD]: 3
      },
      categoryDistribution: {
        [QuestionCategory.TECHNICAL]: 8,
        [QuestionCategory.BEHAVIORAL]: 2,
        [QuestionCategory.SYSTEM_DESIGN]: 2
      },
      targetAudience: 'Senior developers with 5+ years experience',
      objectives: [
        'Assess technical problem-solving abilities',
        'Evaluate system design thinking',
        'Gauge communication and collaboration skills',
        'Determine cultural fit and leadership potential'
      ]
    };
  }

  private async fetchTemplateUsageHistory(templateId: string): Promise<any[]> {
    // Mock comprehensive usage history with detailed analytics data
    return [
      {
        id: 'usage-1',
        interviewId: 'int-001',
        candidateId: 'cand-001',
        interviewDate: '2024-11-15T14:00:00Z',
        completionStatus: 'completed',
        completionRate: 0.92,
        totalDuration: 3420, // 57 minutes
        candidateSatisfaction: 4.2,
        interviewerSatisfaction: 4.5,
        overallScore: 7.8,
        questionResponses: [
          {
            questionId: 'q-tech-001',
            responseTime: 240,
            quality: 0.85,
            confidence: 0.8,
            completed: true,
            difficulty: QuestionDifficulty.MEDIUM,
            category: QuestionCategory.TECHNICAL
          },
          {
            questionId: 'q-tech-002',
            responseTime: 420,
            quality: 0.72,
            confidence: 0.65,
            completed: true,
            difficulty: QuestionDifficulty.HARD,
            category: QuestionCategory.TECHNICAL
          },
          {
            questionId: 'q-sys-001',
            responseTime: 600,
            quality: 0.88,
            confidence: 0.9,
            completed: true,
            difficulty: QuestionDifficulty.HARD,
            category: QuestionCategory.SYSTEM_DESIGN
          },
          {
            questionId: 'q-beh-001',
            responseTime: 180,
            quality: 0.91,
            confidence: 0.95,
            completed: true,
            difficulty: QuestionDifficulty.EASY,
            category: QuestionCategory.BEHAVIORAL
          }
        ],
        feedbackSummary: {
          strengths: ['Strong system design thinking', 'Good communication skills'],
          improvements: ['Could improve algorithm optimization', 'More concrete examples needed'],
          recommendation: 'Strong candidate - recommend for next round'
        }
      },
      {
        id: 'usage-2',
        interviewId: 'int-002',
        candidateId: 'cand-002',
        interviewDate: '2024-11-10T10:00:00Z',
        completionStatus: 'completed',
        completionRate: 0.83,
        totalDuration: 3900, // 65 minutes
        candidateSatisfaction: 3.8,
        interviewerSatisfaction: 3.9,
        overallScore: 6.5,
        questionResponses: [
          {
            questionId: 'q-tech-001',
            responseTime: 320,
            quality: 0.65,
            confidence: 0.6,
            completed: true,
            difficulty: QuestionDifficulty.MEDIUM,
            category: QuestionCategory.TECHNICAL
          },
          {
            questionId: 'q-tech-002',
            responseTime: 780,
            quality: 0.45,
            confidence: 0.3,
            completed: false,
            difficulty: QuestionDifficulty.HARD,
            category: QuestionCategory.TECHNICAL
          },
          {
            questionId: 'q-sys-001',
            responseTime: 540,
            quality: 0.75,
            confidence: 0.7,
            completed: true,
            difficulty: QuestionDifficulty.HARD,
            category: QuestionCategory.SYSTEM_DESIGN
          }
        ]
      },
      // Additional mock usage data for comprehensive analysis
      {
        id: 'usage-3',
        interviewId: 'int-003',
        candidateId: 'cand-003',
        interviewDate: '2024-11-05T16:00:00Z',
        completionStatus: 'completed',
        completionRate: 1.0,
        totalDuration: 3300,
        candidateSatisfaction: 4.7,
        interviewerSatisfaction: 4.8,
        overallScore: 8.9,
        questionResponses: [
          {
            questionId: 'q-tech-001',
            responseTime: 180,
            quality: 0.95,
            confidence: 0.95,
            completed: true,
            difficulty: QuestionDifficulty.MEDIUM,
            category: QuestionCategory.TECHNICAL
          },
          {
            questionId: 'q-tech-002',
            responseTime: 300,
            quality: 0.92,
            confidence: 0.88,
            completed: true,
            difficulty: QuestionDifficulty.HARD,
            category: QuestionCategory.TECHNICAL
          }
        ]
      }
    ];
  }

  private calculateEffectivenessScore(usageHistory: any[]): number {
    if (usageHistory.length === 0) return 0;

    let totalScore = 0;
    let validEntries = 0;

    // Weighted effectiveness calculation
    const weights = {
      completionRate: 0.25,        // How often interviews are completed
      candidateSatisfaction: 0.25, // Candidate experience quality
      interviewerSatisfaction: 0.25, // Interviewer experience quality
      discriminationPower: 0.25    // How well it differentiates candidates
    };

    usageHistory.forEach(usage => {
      if (usage.completionStatus === 'completed') {
        let effectivenessScore = 0;

        // Completion rate contribution
        effectivenessScore += usage.completionRate * weights.completionRate * 10;

        // Satisfaction contributions
        effectivenessScore += (usage.candidateSatisfaction / 5) * weights.candidateSatisfaction * 10;
        effectivenessScore += (usage.interviewerSatisfaction / 5) * weights.interviewerSatisfaction * 10;

        // Discrimination power (how well it spreads candidate scores)
        const normalizedScore = usage.overallScore / 10;
        const discriminationValue = Math.abs(normalizedScore - 0.5) * 2; // Distance from median
        effectivenessScore += discriminationValue * weights.discriminationPower * 10;

        totalScore += effectivenessScore;
        validEntries++;
      }
    });

    return validEntries > 0 ? totalScore / validEntries : 0;
  }

  private analyzeUsageStatistics(usageHistory: any[]): any {
    if (usageHistory.length === 0) {
      return {
        totalUses: 0,
        averageCompletionRate: 0,
        averageDuration: 0,
        candidateSatisfaction: 0,
        interviewerSatisfaction: 0
      };
    }

    const completedInterviews = usageHistory.filter(usage =>
      usage.completionStatus === 'completed'
    );

    // Calculate basic statistics
    const totalUses = usageHistory.length;
    const averageCompletionRate = completedInterviews.length > 0
      ? completedInterviews.reduce((sum, usage) => sum + usage.completionRate, 0) / completedInterviews.length
      : 0;

    const averageDuration = completedInterviews.length > 0
      ? completedInterviews.reduce((sum, usage) => sum + usage.totalDuration, 0) / completedInterviews.length
      : 0;

    const candidateSatisfaction = completedInterviews.length > 0
      ? completedInterviews.reduce((sum, usage) => sum + (usage.candidateSatisfaction || 0), 0) / completedInterviews.length
      : 0;

    const interviewerSatisfaction = completedInterviews.length > 0
      ? completedInterviews.reduce((sum, usage) => sum + (usage.interviewerSatisfaction || 0), 0) / completedInterviews.length
      : 0;

    return {
      totalUses,
      averageCompletionRate,
      averageDuration,
      candidateSatisfaction,
      interviewerSatisfaction,
      successRate: completedInterviews.length / totalUses,
      averageScore: completedInterviews.length > 0
        ? completedInterviews.reduce((sum, usage) => sum + usage.overallScore, 0) / completedInterviews.length
        : 0,
      completionTrend: this.calculateCompletionTrend(usageHistory),
      satisfactionTrend: this.calculateSatisfactionTrend(completedInterviews)
    };
  }

  private calculateCompletionTrend(usageHistory: any[]): string {
    if (usageHistory.length < 4) return 'insufficient_data';

    const sortedUsage = usageHistory.sort((a, b) =>
      new Date(a.interviewDate).getTime() - new Date(b.interviewDate).getTime()
    );

    const firstHalf = sortedUsage.slice(0, Math.ceil(sortedUsage.length / 2));
    const secondHalf = sortedUsage.slice(Math.floor(sortedUsage.length / 2));

    const firstHalfRate = firstHalf.reduce((sum, usage) => sum + usage.completionRate, 0) / firstHalf.length;
    const secondHalfRate = secondHalf.reduce((sum, usage) => sum + usage.completionRate, 0) / secondHalf.length;

    const improvement = secondHalfRate - firstHalfRate;
    if (improvement > 0.05) return 'improving';
    if (improvement < -0.05) return 'declining';
    return 'stable';
  }

  private calculateSatisfactionTrend(completedInterviews: any[]): string {
    if (completedInterviews.length < 4) return 'insufficient_data';

    const sortedInterviews = completedInterviews.sort((a, b) =>
      new Date(a.interviewDate).getTime() - new Date(b.interviewDate).getTime()
    );

    const firstHalf = sortedInterviews.slice(0, Math.ceil(sortedInterviews.length / 2));
    const secondHalf = sortedInterviews.slice(Math.floor(sortedInterviews.length / 2));

    const firstHalfSatisfaction = firstHalf.reduce((sum, interview) =>
      sum + ((interview.candidateSatisfaction + interview.interviewerSatisfaction) / 2), 0
    ) / firstHalf.length;

    const secondHalfSatisfaction = secondHalf.reduce((sum, interview) =>
      sum + ((interview.candidateSatisfaction + interview.interviewerSatisfaction) / 2), 0
    ) / secondHalf.length;

    const improvement = secondHalfSatisfaction - firstHalfSatisfaction;
    if (improvement > 0.2) return 'improving';
    if (improvement < -0.2) return 'declining';
    return 'stable';
  }

  private evaluateQuestionEffectiveness(usageHistory: any[]): any[] {
    if (usageHistory.length === 0) return [];

    // Aggregate question performance data
    const questionStats: Record<string, {
      responses: any[];
      totalResponseTime: number;
      totalQuality: number;
      totalConfidence: number;
      completionCount: number;
      skipCount: number;
    }> = {};

    usageHistory.forEach(usage => {
      usage.questionResponses?.forEach((response: any) => {
        if (!questionStats[response.questionId]) {
          questionStats[response.questionId] = {
            responses: [],
            totalResponseTime: 0,
            totalQuality: 0,
            totalConfidence: 0,
            completionCount: 0,
            skipCount: 0
          };
        }

        const stats = questionStats[response.questionId];
        stats.responses.push(response);
        stats.totalResponseTime += response.responseTime;
        stats.totalQuality += response.quality;
        stats.totalConfidence += response.confidence;

        if (response.completed) {
          stats.completionCount++;
        } else {
          stats.skipCount++;
        }
      });
    });

    // Mock question database for detailed question information
    const questionDatabase: Record<string, {
      text: string;
      category: QuestionCategory;
      difficulty: QuestionDifficulty;
      expectedDuration: number;
    }> = {
      'q-tech-001': {
        text: 'Implement a function to find the longest palindromic substring in a given string.',
        category: QuestionCategory.TECHNICAL,
        difficulty: QuestionDifficulty.MEDIUM,
        expectedDuration: 300
      },
      'q-tech-002': {
        text: 'Design and implement a rate limiter for an API with different limits per user tier.',
        category: QuestionCategory.TECHNICAL,
        difficulty: QuestionDifficulty.HARD,
        expectedDuration: 450
      },
      'q-sys-001': {
        text: 'Design a system to handle real-time messaging for 10 million concurrent users.',
        category: QuestionCategory.SYSTEM_DESIGN,
        difficulty: QuestionDifficulty.HARD,
        expectedDuration: 600
      },
      'q-beh-001': {
        text: 'Tell me about a time when you had to work with a difficult team member.',
        category: QuestionCategory.BEHAVIORAL,
        difficulty: QuestionDifficulty.EASY,
        expectedDuration: 180
      }
    };

    return Object.entries(questionStats).map(([questionId, stats]) => {
      const questionInfo = questionDatabase[questionId] || {
        text: `Question ${questionId}`,
        category: QuestionCategory.TECHNICAL,
        difficulty: QuestionDifficulty.MEDIUM,
        expectedDuration: 300
      };

      const totalResponses = stats.responses.length;
      const averageResponseTime = stats.totalResponseTime / totalResponses;
      const averageResponseQuality = stats.totalQuality / totalResponses;
      const candidateConfidence = stats.totalConfidence / totalResponses;
      const completionRate = stats.completionCount / totalResponses;

      // Calculate discrimination index (how well question differentiates candidates)
      const qualityScores = stats.responses.map(r => r.quality);
      const sortedCandidates = [...qualityScores].sort((a, b) => b - a);
      const topThird = sortedCandidates.slice(0, Math.ceil(sortedCandidates.length / 3));
      const bottomThird = sortedCandidates.slice(-Math.ceil(sortedCandidates.length / 3));

      const topAvg = topThird.reduce((sum, score) => sum + score, 0) / topThird.length;
      const bottomAvg = bottomThird.reduce((sum, score) => sum + score, 0) / bottomThird.length;
      const discriminationIndex = topAvg - bottomAvg;

      // Calculate difficulty calibration (actual vs intended difficulty)
      const actualDifficulty = 1 - averageResponseQuality; // Inverse of quality
      const intendedDifficulty = this.getDifficultyScore(questionInfo.difficulty) / 3; // Normalized
      const difficultyCalibration = 1 - Math.abs(actualDifficulty - intendedDifficulty);

      // Generate improvement suggestions
      const improvements: string[] = [];

      if (averageResponseTime > questionInfo.expectedDuration * 1.3) {
        improvements.push('Consider simplifying question or providing more context');
      }
      if (candidateConfidence < 0.5) {
        improvements.push('Question may be confusing - consider clearer wording');
      }
      if (discriminationIndex < 0.2) {
        improvements.push('Question has low discrimination power - may need refinement');
      }
      if (completionRate < 0.8) {
        improvements.push('High skip rate - question may be too difficult or unclear');
      }
      if (difficultyCalibration < 0.7) {
        improvements.push('Actual difficulty does not match intended level');
      }

      return {
        questionId,
        questionText: questionInfo.text,
        category: questionInfo.category,
        difficulty: questionInfo.difficulty,
        metrics: {
          averageResponseTime,
          averageResponseQuality,
          candidateConfidence,
          discriminationIndex,
          difficultyCalibration,
          completionRate,
          totalUses: totalResponses
        },
        improvements: improvements.length > 0 ? improvements : ['Question performs well - no major improvements needed'],
        effectivenessScore: this.calculateQuestionEffectivenessScore({
          averageResponseQuality,
          discriminationIndex,
          difficultyCalibration,
          completionRate,
          candidateConfidence
        })
      };
    }).sort((a, b) => b.effectivenessScore - a.effectivenessScore);
  }

  private calculateQuestionEffectivenessScore(metrics: {
    averageResponseQuality: number;
    discriminationIndex: number;
    difficultyCalibration: number;
    completionRate: number;
    candidateConfidence: number;
  }): number {
    const weights = {
      quality: 0.2,
      discrimination: 0.3,
      calibration: 0.2,
      completion: 0.15,
      confidence: 0.15
    };

    return (
      metrics.averageResponseQuality * weights.quality +
      metrics.discriminationIndex * weights.discrimination +
      metrics.difficultyCalibration * weights.calibration +
      metrics.completionRate * weights.completion +
      metrics.candidateConfidence * weights.confidence
    ) * 10; // Scale to 0-10
  }

  private generateTemplateOptimizations(questionEffectiveness: any[], usageStats: any): any {
    // Analyze current question order effectiveness
    const currentOrder = questionEffectiveness.map(q => q.questionId);

    // Suggest optimal question order based on:
    // 1. Warm-up with easier questions
    // 2. Build confidence before difficult questions
    // 3. End with engaging questions to maintain satisfaction

    const easyQuestions = questionEffectiveness.filter(q =>
      q.difficulty === QuestionDifficulty.EASY
    );
    const mediumQuestions = questionEffectiveness.filter(q =>
      q.difficulty === QuestionDifficulty.MEDIUM
    );
    const hardQuestions = questionEffectiveness.filter(q =>
      q.difficulty === QuestionDifficulty.HARD
    );

    // Sort each group by effectiveness score
    easyQuestions.sort((a, b) => b.effectivenessScore - a.effectivenessScore);
    mediumQuestions.sort((a, b) => b.effectivenessScore - a.effectivenessScore);
    hardQuestions.sort((a, b) => b.effectivenessScore - a.effectivenessScore);

    // Optimal ordering strategy: Easy -> Medium -> Hard -> High-confidence finisher
    const suggestedQuestionOrder: string[] = [];

    // Start with 1-2 easy questions for warm-up
    suggestedQuestionOrder.push(...easyQuestions.slice(0, 2).map(q => q.questionId));

    // Add medium questions in effectiveness order
    suggestedQuestionOrder.push(...mediumQuestions.map(q => q.questionId));

    // Add hard questions, but save most effective hard question for middle
    if (hardQuestions.length > 0) {
      const sortedHard = [...hardQuestions];
      const bestHard = sortedHard.shift();
      suggestedQuestionOrder.push(...sortedHard.map(q => q.questionId));
      if (bestHard) {
        suggestedQuestionOrder.splice(Math.floor(suggestedQuestionOrder.length / 2), 0, bestHard.questionId);
      }
    }

    // End with remaining easy questions for positive finish
    suggestedQuestionOrder.push(...easyQuestions.slice(2).map(q => q.questionId));

    // Calculate recommended time allocations based on historical data
    const recommendedTimeAllocations: Record<string, number> = {};
    questionEffectiveness.forEach(question => {
      const baseTime = question.metrics.averageResponseTime;
      const adjustmentFactor = question.effectivenessScore / 10; // Higher effectiveness = more time
      recommendedTimeAllocations[question.questionId] = Math.round(baseTime * (0.8 + 0.4 * adjustmentFactor));
    });

    // Propose difficulty adjustments for poorly calibrated questions
    const proposedDifficultyAdjustments = questionEffectiveness
      .filter(q => q.metrics.difficultyCalibration < 0.7)
      .map(question => {
        const actualDifficulty = 1 - question.metrics.averageResponseQuality;
        let suggestedDifficulty = question.difficulty;
        let reasoning = '';

        if (actualDifficulty > 0.8 && question.difficulty !== QuestionDifficulty.HARD) {
          suggestedDifficulty = this.increaseDifficulty(question.difficulty);
          reasoning = 'Question is performing harder than intended difficulty level';
        } else if (actualDifficulty < 0.3 && question.difficulty !== QuestionDifficulty.EASY) {
          suggestedDifficulty = this.decreaseDifficulty(question.difficulty);
          reasoning = 'Question is performing easier than intended difficulty level';
        }

        return {
          questionId: question.questionId,
          currentDifficulty: question.difficulty,
          suggestedDifficulty,
          reasoning,
          confidenceScore: question.metrics.difficultyCalibration,
          supportingData: {
            averageQuality: question.metrics.averageResponseQuality,
            completionRate: question.metrics.completionRate,
            discriminationPower: question.metrics.discriminationIndex
          }
        };
      });

    return {
      suggestedQuestionOrder,
      recommendedTimeAllocations,
      proposedDifficultyAdjustments,
      overallRecommendations: this.generateOverallTemplateRecommendations(usageStats, questionEffectiveness),
      estimatedImprovements: {
        completionRateIncrease: this.estimateCompletionImprovement(questionEffectiveness),
        satisfactionIncrease: this.estimateSatisfactionImprovement(usageStats, questionEffectiveness),
        discriminationImprovement: this.estimateDiscriminationImprovement(questionEffectiveness)
      }
    };
  }

  private generateOverallTemplateRecommendations(usageStats: any, questionEffectiveness: any[]): string[] {
    const recommendations: string[] = [];

    // Completion rate recommendations
    if (usageStats.averageCompletionRate < 0.8) {
      recommendations.push('Consider reducing total question count or extending time limits to improve completion rates');
    }

    // Satisfaction recommendations
    if (usageStats.candidateSatisfaction < 4.0) {
      recommendations.push('Add more engaging questions or improve question clarity to boost candidate satisfaction');
    }

    if (usageStats.interviewerSatisfaction < 4.0) {
      recommendations.push('Provide better interviewer guidelines or add structured evaluation criteria');
    }

    // Question effectiveness recommendations
    const lowEffectivenessQuestions = questionEffectiveness.filter(q => q.effectivenessScore < 6);
    if (lowEffectivenessQuestions.length > 0) {
      recommendations.push(`Replace or revise ${lowEffectivenessQuestions.length} low-performing questions`);
    }

    // Duration recommendations
    if (usageStats.averageDuration > 4200) { // > 70 minutes
      recommendations.push('Consider reducing question complexity or count to fit within time constraints');
    } else if (usageStats.averageDuration < 2700) { // < 45 minutes
      recommendations.push('Add more comprehensive questions to better assess candidate capabilities');
    }

    // Discrimination recommendations
    const lowDiscriminationQuestions = questionEffectiveness.filter(q => q.metrics.discriminationIndex < 0.3);
    if (lowDiscriminationQuestions.length > questionEffectiveness.length * 0.3) {
      recommendations.push('Improve question variety to better differentiate between candidate skill levels');
    }

    return recommendations.length > 0
      ? recommendations
      : ['Template is performing well - continue monitoring and minor refinements'];
  }

  private estimateCompletionImprovement(questionEffectiveness: any[]): number {
    const lowCompletionQuestions = questionEffectiveness.filter(q => q.metrics.completionRate < 0.8);
    const improvementPotential = lowCompletionQuestions.length / questionEffectiveness.length;
    return Math.round(improvementPotential * 15); // Estimated percentage improvement
  }

  private estimateSatisfactionImprovement(usageStats: any, questionEffectiveness: any[]): number {
    const currentSatisfaction = (usageStats.candidateSatisfaction + usageStats.interviewerSatisfaction) / 2;
    const maxSatisfaction = 5.0;
    const improvementRoom = maxSatisfaction - currentSatisfaction;

    const lowQualityQuestions = questionEffectiveness.filter(q => q.effectivenessScore < 7);
    const improvementFactor = lowQualityQuestions.length / questionEffectiveness.length;

    return Math.round((improvementRoom * improvementFactor * 0.6) * 100) / 100; // Realistic improvement estimate
  }

  private estimateDiscriminationImprovement(questionEffectiveness: any[]): number {
    const currentAvgDiscrimination = questionEffectiveness.reduce((sum, q) =>
      sum + q.metrics.discriminationIndex, 0) / questionEffectiveness.length;

    const maxDiscrimination = 1.0;
    const improvementPotential = maxDiscrimination - currentAvgDiscrimination;

    return Math.round(improvementPotential * 30); // Estimated percentage improvement
  }

  private calculateTemplatePerformanceMetrics(usageData: any[]): any {
    if (usageData.length === 0) {
      return {
        totalCompletions: 0,
        averageScore: 0,
        completionRate: 0,
        candidateSatisfaction: 0,
        timeEfficiency: 0
      };
    }

    const completedInterviews = usageData.filter(usage => usage.completionStatus === 'completed');
    const totalCompletions = completedInterviews.length;

    // Calculate average performance score
    const averageScore = totalCompletions > 0
      ? completedInterviews.reduce((sum, interview) => sum + interview.overallScore, 0) / totalCompletions
      : 0;

    // Calculate completion rate (percentage of started interviews that were completed)
    const completionRate = usageData.length > 0 ? totalCompletions / usageData.length : 0;

    // Calculate candidate satisfaction
    const candidateSatisfaction = completedInterviews.length > 0
      ? completedInterviews.reduce((sum, interview) => sum + (interview.candidateSatisfaction || 0), 0) / completedInterviews.length
      : 0;

    // Calculate time efficiency (actual vs expected duration)
    const expectedDuration = 3600; // 60 minutes baseline
    const averageActualDuration = completedInterviews.length > 0
      ? completedInterviews.reduce((sum, interview) => sum + interview.totalDuration, 0) / completedInterviews.length
      : expectedDuration;

    const timeEfficiency = expectedDuration / Math.max(averageActualDuration, expectedDuration);

    // Additional metrics for comprehensive analysis
    const interviewerSatisfaction = completedInterviews.length > 0
      ? completedInterviews.reduce((sum, interview) => sum + (interview.interviewerSatisfaction || 0), 0) / completedInterviews.length
      : 0;

    const scoreDistribution = this.calculateScoreDistribution(completedInterviews);
    const temporalTrends = this.calculateTemporalTrends(usageData);

    return {
      totalCompletions,
      averageScore,
      completionRate,
      candidateSatisfaction,
      interviewerSatisfaction,
      timeEfficiency,
      averageDuration: averageActualDuration,
      scoreDistribution,
      temporalTrends,
      usageFrequency: this.calculateUsageFrequency(usageData),
      successRate: completedInterviews.filter(interview => interview.overallScore >= 7).length / Math.max(totalCompletions, 1)
    };
  }

  private calculateScoreDistribution(completedInterviews: any[]): any {
    const scoreRanges = {
      excellent: { min: 9, max: 10, count: 0 },
      good: { min: 7, max: 8.99, count: 0 },
      average: { min: 5, max: 6.99, count: 0 },
      poor: { min: 0, max: 4.99, count: 0 }
    };

    completedInterviews.forEach(interview => {
      const score = interview.overallScore;
      if (score >= scoreRanges.excellent.min) scoreRanges.excellent.count++;
      else if (score >= scoreRanges.good.min) scoreRanges.good.count++;
      else if (score >= scoreRanges.average.min) scoreRanges.average.count++;
      else scoreRanges.poor.count++;
    });

    const total = completedInterviews.length;
    return {
      excellent: { count: scoreRanges.excellent.count, percentage: (scoreRanges.excellent.count / Math.max(total, 1)) * 100 },
      good: { count: scoreRanges.good.count, percentage: (scoreRanges.good.count / Math.max(total, 1)) * 100 },
      average: { count: scoreRanges.average.count, percentage: (scoreRanges.average.count / Math.max(total, 1)) * 100 },
      poor: { count: scoreRanges.poor.count, percentage: (scoreRanges.poor.count / Math.max(total, 1)) * 100 }
    };
  }

  private calculateTemporalTrends(usageData: any[]): any {
    if (usageData.length < 3) {
      return {
        scoresTrend: 'insufficient_data',
        completionTrend: 'insufficient_data',
        satisfactionTrend: 'insufficient_data',
        usageTrend: 'insufficient_data'
      };
    }

    const sortedData = usageData.sort((a, b) =>
      new Date(a.interviewDate).getTime() - new Date(b.interviewDate).getTime()
    );

    const firstThird = sortedData.slice(0, Math.ceil(sortedData.length / 3));
    const lastThird = sortedData.slice(-Math.ceil(sortedData.length / 3));

    // Calculate trend changes
    const firstThirdAvgScore = firstThird
      .filter(d => d.completionStatus === 'completed')
      .reduce((sum, d) => sum + d.overallScore, 0) / Math.max(firstThird.filter(d => d.completionStatus === 'completed').length, 1);

    const lastThirdAvgScore = lastThird
      .filter(d => d.completionStatus === 'completed')
      .reduce((sum, d) => sum + d.overallScore, 0) / Math.max(lastThird.filter(d => d.completionStatus === 'completed').length, 1);

    const firstThirdCompletion = firstThird.filter(d => d.completionStatus === 'completed').length / firstThird.length;
    const lastThirdCompletion = lastThird.filter(d => d.completionStatus === 'completed').length / lastThird.length;

    const firstThirdSatisfaction = firstThird
      .filter(d => d.completionStatus === 'completed')
      .reduce((sum, d) => sum + (d.candidateSatisfaction || 0), 0) / Math.max(firstThird.filter(d => d.completionStatus === 'completed').length, 1);

    const lastThirdSatisfaction = lastThird
      .filter(d => d.completionStatus === 'completed')
      .reduce((sum, d) => sum + (d.candidateSatisfaction || 0), 0) / Math.max(lastThird.filter(d => d.completionStatus === 'completed').length, 1);

    return {
      scoresTrend: this.getTrendDirection(firstThirdAvgScore, lastThirdAvgScore, 0.3),
      completionTrend: this.getTrendDirection(firstThirdCompletion, lastThirdCompletion, 0.05),
      satisfactionTrend: this.getTrendDirection(firstThirdSatisfaction, lastThirdSatisfaction, 0.2),
      usageTrend: this.calculateUsageTrend(sortedData),
      periodComparison: {
        early: { avgScore: firstThirdAvgScore, completion: firstThirdCompletion, satisfaction: firstThirdSatisfaction },
        recent: { avgScore: lastThirdAvgScore, completion: lastThirdCompletion, satisfaction: lastThirdSatisfaction }
      }
    };
  }

  private getTrendDirection(early: number, recent: number, threshold: number): string {
    const change = recent - early;
    if (change > threshold) return 'improving';
    if (change < -threshold) return 'declining';
    return 'stable';
  }

  private calculateUsageTrend(sortedData: any[]): string {
    // Group by month and calculate usage frequency change
    const monthlyUsage: Record<string, number> = {};

    sortedData.forEach(usage => {
      const date = new Date(usage.interviewDate);
      const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
      monthlyUsage[monthKey] = (monthlyUsage[monthKey] || 0) + 1;
    });

    const months = Object.keys(monthlyUsage).sort();
    if (months.length < 3) return 'insufficient_data';

    const firstHalfMonths = months.slice(0, Math.ceil(months.length / 2));
    const secondHalfMonths = months.slice(Math.floor(months.length / 2));

    const firstHalfAvg = firstHalfMonths.reduce((sum, month) => sum + monthlyUsage[month], 0) / firstHalfMonths.length;
    const secondHalfAvg = secondHalfMonths.reduce((sum, month) => sum + monthlyUsage[month], 0) / secondHalfMonths.length;

    return this.getTrendDirection(firstHalfAvg, secondHalfAvg, 1);
  }

  private calculateUsageFrequency(usageData: any[]): any {
    const now = new Date();
    const timeRanges = {
      lastWeek: usageData.filter(usage =>
        (now.getTime() - new Date(usage.interviewDate).getTime()) <= (7 * 24 * 60 * 60 * 1000)
      ).length,
      lastMonth: usageData.filter(usage =>
        (now.getTime() - new Date(usage.interviewDate).getTime()) <= (30 * 24 * 60 * 60 * 1000)
      ).length,
      lastQuarter: usageData.filter(usage =>
        (now.getTime() - new Date(usage.interviewDate).getTime()) <= (90 * 24 * 60 * 60 * 1000)
      ).length
    };

    return {
      ...timeRanges,
      dailyAverage: timeRanges.lastMonth / 30,
      weeklyAverage: timeRanges.lastQuarter / 13,
      monthlyAverage: timeRanges.lastQuarter / 3
    };
  }

  private analyzeTemplateQuestions(usageData: any[]): any[] {
    if (usageData.length === 0) return [];

    // Aggregate performance data for each question across all usage instances
    const questionAnalytics: Record<string, {
      performances: any[];
      totalResponseTime: number;
      totalQuality: number;
      completions: number;
      skips: number;
    }> = {};

    usageData.forEach(usage => {
      usage.questionResponses?.forEach((response: any) => {
        if (!questionAnalytics[response.questionId]) {
          questionAnalytics[response.questionId] = {
            performances: [],
            totalResponseTime: 0,
            totalQuality: 0,
            completions: 0,
            skips: 0
          };
        }

        const analytics = questionAnalytics[response.questionId];
        analytics.performances.push(response);
        analytics.totalResponseTime += response.responseTime;
        analytics.totalQuality += response.quality;

        if (response.completed) {
          analytics.completions++;
        } else {
          analytics.skips++;
        }
      });
    });

    return Object.entries(questionAnalytics).map(([questionId, analytics]) => {
      const totalAttempts = analytics.performances.length;
      const averageScore = analytics.totalQuality / totalAttempts;
      const responseTime = analytics.totalResponseTime / totalAttempts;
      const skipRate = analytics.skips / totalAttempts;
      const difficultyAccuracy = this.calculateDifficultyAccuracy(analytics.performances);

      // Calculate candidate feedback metrics
      const candidateFeedback = this.analyzeCandidateFeedback(analytics.performances);

      return {
        questionId,
        performanceData: {
          averageScore,
          responseTime,
          skipRate,
          difficultyAccuracy,
          totalAttempts,
          completionRate: analytics.completions / totalAttempts
        },
        candidateFeedback,
        improvementSuggestions: this.generateQuestionImprovements(averageScore, responseTime, skipRate, difficultyAccuracy),
        effectivenessRating: this.calculateQuestionEffectivenessRating(averageScore, skipRate, difficultyAccuracy, candidateFeedback)
      };
    }).sort((a, b) => b.effectivenessRating - a.effectivenessRating);
  }

  private calculateDifficultyAccuracy(performances: any[]): number {
    // Compare intended difficulty with actual performance
    if (performances.length === 0) return 0;

    const difficultyScore = performances.reduce((sum, perf) => {
      const intendedDifficulty = this.getDifficultyScore(perf.difficulty) / 3; // Normalize to 0-1
      const actualDifficulty = 1 - perf.quality; // Inverse quality as difficulty
      const accuracy = 1 - Math.abs(intendedDifficulty - actualDifficulty);
      return sum + accuracy;
    }, 0);

    return difficultyScore / performances.length;
  }

  private analyzeCandidateFeedback(performances: any[]): any {
    // Mock candidate feedback analysis - in real implementation would come from surveys
    const avgQuality = performances.reduce((sum, p) => sum + p.quality, 0) / performances.length;
    const avgConfidence = performances.reduce((sum, p) => sum + p.confidence, 0) / performances.length;

    return {
      clarity: Math.min(5, avgConfidence * 5), // Convert confidence to 1-5 scale
      relevance: Math.min(5, avgQuality * 5), // Quality as relevance proxy
      difficulty: Math.min(5, (1 - avgQuality + 1) * 2.5), // Inverse quality as difficulty perception
      engagement: Math.min(5, (avgQuality + avgConfidence) * 2.5) // Combined as engagement proxy
    };
  }

  private generateQuestionImprovements(averageScore: number, responseTime: number, skipRate: number, difficultyAccuracy: number): string[] {
    const improvements: string[] = [];

    if (averageScore < 0.6) {
      improvements.push('Consider providing more context or examples to improve understanding');
    }
    if (responseTime > 600) { // > 10 minutes
      improvements.push('Question may be too complex - consider breaking into smaller parts');
    }
    if (skipRate > 0.2) {
      improvements.push('High skip rate indicates question may be unclear or too difficult');
    }
    if (difficultyAccuracy < 0.7) {
      improvements.push('Actual difficulty does not match intended level - consider recalibration');
    }
    if (averageScore > 0.9 && responseTime < 120) { // Too easy
      improvements.push('Question may be too easy - consider increasing complexity');
    }

    return improvements.length > 0 ? improvements : ['Question is performing well'];
  }

  private calculateQuestionEffectivenessRating(averageScore: number, skipRate: number, difficultyAccuracy: number, candidateFeedback: any): number {
    const weights = {
      score: 0.3,
      completion: 0.25,
      difficulty: 0.25,
      feedback: 0.2
    };

    const scoreComponent = averageScore * weights.score;
    const completionComponent = (1 - skipRate) * weights.completion;
    const difficultyComponent = difficultyAccuracy * weights.difficulty;
    const feedbackComponent = (candidateFeedback.clarity + candidateFeedback.engagement) / 10 * weights.feedback;

    return (scoreComponent + completionComponent + difficultyComponent + feedbackComponent) * 10;
  }

  private calculateCategoryDistribution(usageData: any[]): any {
    if (usageData.length === 0) return {};

    const categoryStats: Record<QuestionCategory, {
      questionCount: number;
      totalPerformance: number;
      totalTime: number;
      attempts: number;
    }> = {} as any;

    // Initialize categories
    Object.values(QuestionCategory).forEach(category => {
      categoryStats[category] = {
        questionCount: 0,
        totalPerformance: 0,
        totalTime: 0,
        attempts: 0
      };
    });

    // Track unique questions per category
    const questionsPerCategory: Record<QuestionCategory, Set<string>> = {} as any;
    Object.values(QuestionCategory).forEach(category => {
      questionsPerCategory[category] = new Set();
    });

    usageData.forEach(usage => {
      usage.questionResponses?.forEach((response: any) => {
        const category = response.category;
        if (category && categoryStats[category]) {
          categoryStats[category].totalPerformance += response.quality;
          categoryStats[category].totalTime += response.responseTime;
          categoryStats[category].attempts++;
          questionsPerCategory[category].add(response.questionId);
        }
      });
    });

    // Calculate final metrics for each category
    const distribution: Record<QuestionCategory, {
      questionCount: number;
      averagePerformance: number;
      timeAllocation: number;
      effectiveness: number;
      totalAttempts: number;
      averageTimePerQuestion: number;
    }> = {} as any;

    Object.values(QuestionCategory).forEach(category => {
      const stats = categoryStats[category];
      const questionCount = questionsPerCategory[category].size;

      distribution[category] = {
        questionCount,
        averagePerformance: stats.attempts > 0 ? stats.totalPerformance / stats.attempts : 0,
        timeAllocation: stats.totalTime,
        effectiveness: this.calculateCategoryEffectiveness(stats, questionCount),
        totalAttempts: stats.attempts,
        averageTimePerQuestion: stats.attempts > 0 ? stats.totalTime / stats.attempts : 0
      };
    });

    return distribution;
  }

  private calculateCategoryEffectiveness(stats: any, questionCount: number): number {
    if (stats.attempts === 0 || questionCount === 0) return 0;

    const averagePerformance = stats.totalPerformance / stats.attempts;
    const questionUtilization = Math.min(1, stats.attempts / (questionCount * 3)); // Expect ~3 attempts per question
    const timeEfficiency = Math.min(1, 300 / (stats.totalTime / stats.attempts)); // Expect ~5 minutes per question

    return (averagePerformance * 0.5 + questionUtilization * 0.3 + timeEfficiency * 0.2) * 10;
  }

  private generateTemplateImprovements(metrics: any, questions: any[], distribution: any): any[] {
    const improvements: any[] = [];

    // Overall template improvements
    if (metrics.completionRate < 0.8) {
      improvements.push({
        type: 'time_reallocation',
        description: 'Reduce overall interview time to improve completion rates',
        impact: 'high',
        implementation: 'Remove 1-2 lowest performing questions or reduce time allocation per question'
      });
    }

    if (metrics.candidateSatisfaction < 4.0) {
      improvements.push({
        type: 'question_replacement',
        description: 'Replace low-satisfaction questions with more engaging alternatives',
        impact: 'medium',
        implementation: 'Identify questions with low candidate feedback scores and create more interactive alternatives'
      });
    }

    // Question-specific improvements
    const lowPerformingQuestions = questions.filter(q => q.effectivenessRating < 6);
    if (lowPerformingQuestions.length > 0) {
      improvements.push({
        type: 'question_replacement',
        description: `Replace ${lowPerformingQuestions.length} underperforming questions`,
        impact: 'high',
        implementation: `Review and replace questions: ${lowPerformingQuestions.map(q => q.questionId).join(', ')}`
      });
    }

    // Category balance improvements
    const categoryEntries = Object.entries(distribution);
    const lowEffectivenessCategories = categoryEntries.filter(([, data]: any) => data.effectiveness < 6);

    if (lowEffectivenessCategories.length > 0) {
      improvements.push({
        type: 'order_optimization',
        description: 'Rebalance question categories for better coverage',
        impact: 'medium',
        implementation: `Adjust question distribution for categories: ${lowEffectivenessCategories.map(([cat]) => cat).join(', ')}`
      });
    }

    // Time allocation improvements
    const timeImbalances = categoryEntries.filter(([, data]: any) =>
      data.averageTimePerQuestion > 600 || data.averageTimePerQuestion < 120
    );

    if (timeImbalances.length > 0) {
      improvements.push({
        type: 'time_reallocation',
        description: 'Optimize time allocation across question categories',
        impact: 'medium',
        implementation: 'Rebalance time limits based on historical performance data'
      });
    }

    // Difficulty distribution improvements
    const difficultyIssues = questions.filter(q => q.performanceData.difficultyAccuracy < 0.7);
    if (difficultyIssues.length > 0) {
      improvements.push({
        type: 'difficulty_adjustment',
        description: 'Recalibrate question difficulty levels',
        impact: 'medium',
        implementation: `Adjust difficulty for ${difficultyIssues.length} questions with poor calibration`
      });
    }

    return improvements.length > 0 ? improvements : [{
      type: 'maintenance',
      description: 'Template is performing well - continue regular monitoring',
      impact: 'low',
      implementation: 'Monitor metrics quarterly and make minor adjustments as needed'
    }];
  }

  private async generateTemplateRecommendations(templateId: string): Promise<InterviewImprovementRecommendation[]> {
    try {
      // Fetch template effectiveness data
      const effectivenessMetrics = await this.measureInterviewEffectiveness(templateId);
      const performanceAnalytics = await this.analyzeTemplatePerformance(templateId);

      const recommendations: InterviewImprovementRecommendation[] = [];

      // Template effectiveness recommendations
      if (effectivenessMetrics.effectivenessScore < 7) {
        recommendations.push({
          id: `template_effectiveness_${templateId}_${Date.now()}`,
          type: 'template',
          priority: 'high',
          title: 'Improve Template Overall Effectiveness',
          description: `Template "${effectivenessMetrics.templateName}" has a low effectiveness score of ${effectivenessMetrics.effectivenessScore.toFixed(1)}/10`,
          reasoning: 'Low effectiveness scores indicate poor candidate experience, low completion rates, or inadequate discrimination between skill levels',
          expectedImpact: {
            scoreImprovement: 1.5,
            timeReduction: 10,
            satisfactionIncrease: 0.8,
            implementationEffort: 'medium'
          },
          actionSteps: [
            {
              step: 'Review and replace the 3 lowest-performing questions',
              owner: 'admin',
              timeframe: '2 weeks',
              resources: ['Question database', 'Performance analytics']
            },
            {
              step: 'Optimize question order based on analytics recommendations',
              owner: 'admin',
              timeframe: '1 week'
            },
            {
              step: 'Test revised template with pilot group',
              owner: 'interviewer',
              timeframe: '3 weeks',
              resources: ['Test candidates', 'Feedback forms']
            }
          ],
          metrics: {
            baseline: { effectivenessScore: effectivenessMetrics.effectivenessScore },
            targets: { effectivenessScore: Math.min(10, effectivenessMetrics.effectivenessScore + 2) },
            measurement: 'Template effectiveness score over 30-day period'
          }
        });
      }

      // Question-specific recommendations
      const lowPerformingQuestions = effectivenessMetrics.questionEffectiveness.filter(q =>
        q.metrics.averageResponseQuality < 0.6 || q.metrics.completionRate < 0.8
      );

      if (lowPerformingQuestions.length > 0) {
        recommendations.push({
          id: `question_replacement_${templateId}_${Date.now()}`,
          type: 'template',
          priority: 'medium',
          title: 'Replace Underperforming Questions',
          description: `${lowPerformingQuestions.length} questions are underperforming and negatively impacting candidate experience`,
          reasoning: 'Questions with low response quality or high skip rates indicate unclear instructions, inappropriate difficulty, or poor relevance',
          expectedImpact: {
            scoreImprovement: 0.8,
            timeReduction: 5,
            satisfactionIncrease: 0.5,
            implementationEffort: 'low'
          },
          actionSteps: [
            {
              step: `Review questions: ${lowPerformingQuestions.map(q => q.questionId).slice(0, 3).join(', ')}`,
              owner: 'admin',
              timeframe: '1 week'
            },
            {
              step: 'Create alternative questions with clearer instructions',
              owner: 'admin',
              timeframe: '2 weeks',
              resources: ['Question writing guidelines', 'Best practices document']
            },
            {
              step: 'A/B test new questions against current versions',
              owner: 'interviewer',
              timeframe: '4 weeks'
            }
          ],
          metrics: {
            baseline: {
              averageQuestionQuality: lowPerformingQuestions.reduce((sum, q) => sum + q.metrics.averageResponseQuality, 0) / lowPerformingQuestions.length,
              averageCompletionRate: lowPerformingQuestions.reduce((sum, q) => sum + q.metrics.completionRate, 0) / lowPerformingQuestions.length
            },
            targets: {
              averageQuestionQuality: 0.75,
              averageCompletionRate: 0.85
            },
            measurement: 'Question performance metrics over 4-week A/B test period'
          }
        });
      }

      // Time allocation recommendations
      if (effectivenessMetrics.usageStatistics.averageDuration > 4500) { // > 75 minutes
        recommendations.push({
          id: `time_optimization_${templateId}_${Date.now()}`,
          type: 'template',
          priority: 'medium',
          title: 'Optimize Interview Duration',
          description: 'Template is taking longer than expected, potentially causing fatigue and reduced performance',
          reasoning: 'Extended interview duration (>75 minutes) correlates with decreased candidate performance and satisfaction in latter portions',
          expectedImpact: {
            scoreImprovement: 0.5,
            timeReduction: 15,
            satisfactionIncrease: 0.6,
            implementationEffort: 'low'
          },
          actionSteps: [
            {
              step: 'Reduce time allocation for questions exceeding target duration by >30%',
              owner: 'admin',
              timeframe: '3 days'
            },
            {
              step: 'Consider removing 1-2 least effective questions',
              owner: 'admin',
              timeframe: '1 week'
            },
            {
              step: 'Update interviewer guidelines with time management tips',
              owner: 'admin',
              timeframe: '1 week',
              resources: ['Interviewer training materials']
            }
          ],
          metrics: {
            baseline: { averageDuration: effectivenessMetrics.usageStatistics.averageDuration },
            targets: { averageDuration: 4200 }, // 70 minutes
            measurement: 'Average interview duration over 2-week implementation period'
          }
        });
      }

      return recommendations;

    } catch (error) {
      console.error('Failed to generate template recommendations:', error);
      return [];
    }
  }

  private async generateCandidateRecommendations(candidateId: string): Promise<InterviewImprovementRecommendation[]> {
    try {
      const candidateInsights = await this.generateCandidateInsights(candidateId);
      const recommendations: InterviewImprovementRecommendation[] = [];

      // Performance improvement recommendations
      if (candidateInsights.profileSummary.averageScore < 6.5) {
        recommendations.push({
          id: `candidate_performance_${candidateId}_${Date.now()}`,
          type: 'candidate_specific',
          priority: 'high',
          title: 'Comprehensive Skill Development Plan',
          description: `Candidate's average score of ${candidateInsights.profileSummary.averageScore.toFixed(1)} indicates need for targeted improvement`,
          reasoning: 'Below-average performance across multiple interviews suggests systematic skill gaps that can be addressed through focused development',
          expectedImpact: {
            scoreImprovement: 2.0,
            timeReduction: 0,
            satisfactionIncrease: 0.3,
            implementationEffort: 'high'
          },
          actionSteps: [
            {
              step: `Focus on improving ${candidateInsights.profileSummary.weakestCategory} skills through targeted practice`,
              owner: 'candidate',
              timeframe: '4-6 weeks',
              resources: candidateInsights.adaptiveRecommendations.recommendedResources.map(r => r.title)
            },
            {
              step: 'Complete practice interviews in weak areas before next assessment',
              owner: 'candidate',
              timeframe: '3 weeks',
              resources: ['Mock interview platform', 'Practice question database']
            },
            {
              step: 'Schedule follow-up assessment to measure improvement',
              owner: 'interviewer',
              timeframe: '6 weeks'
            }
          ],
          metrics: {
            baseline: {
              averageScore: candidateInsights.profileSummary.averageScore,
              weakestCategoryScore: this.getWeakestCategoryScore(candidateInsights)
            },
            targets: {
              averageScore: Math.min(10, candidateInsights.profileSummary.averageScore + 1.5),
              weakestCategoryScore: this.getTargetImprovement(candidateInsights)
            },
            measurement: 'Performance scores in next interview within 6 weeks'
          }
        });
      }

      // Skill-specific recommendations based on progression analysis
      const decliningSkills = Object.entries(candidateInsights.skillProgression)
        .filter(([, progression]) => progression.trendDirection === 'down')
        .slice(0, 3); // Focus on top 3 declining skills

      if (decliningSkills.length > 0) {
        recommendations.push({
          id: `skill_recovery_${candidateId}_${Date.now()}`,
          type: 'candidate_specific',
          priority: 'medium',
          title: 'Address Declining Skills',
          description: `${decliningSkills.length} skills showing negative progression trends`,
          reasoning: 'Declining skill performance may indicate knowledge gaps, lack of practice, or need for updated approaches in these areas',
          expectedImpact: {
            scoreImprovement: 1.0,
            timeReduction: 0,
            satisfactionIncrease: 0.4,
            implementationEffort: 'medium'
          },
          actionSteps: decliningSkills.map(([skill, progression]) => ({
            step: `Create refresher plan for ${skill} (current level: ${progression.currentLevel.toFixed(1)})`,
            owner: 'candidate',
            timeframe: '2-3 weeks',
            resources: ['Skill-specific learning resources', 'Practice exercises']
          })),
          metrics: {
            baseline: Object.fromEntries(decliningSkills.map(([skill, prog]) => [skill, prog.currentLevel])),
            targets: Object.fromEntries(decliningSkills.map(([skill, prog]) => [skill, Math.min(10, prog.currentLevel + 1)])),
            measurement: 'Skill assessment scores in targeted areas over next 4 weeks'
          }
        });
      }

      // Next interview strategy recommendation
      const nextStrategy = candidateInsights.adaptiveRecommendations.nextInterviewStrategy;
      recommendations.push({
        id: `interview_strategy_${candidateId}_${Date.now()}`,
        type: 'candidate_specific',
        priority: 'low',
        title: 'Optimized Next Interview Strategy',
        description: `Prepare for ${nextStrategy.recommendedType} interview focusing on ${nextStrategy.focusCategories.join(', ')}`,
        reasoning: 'Personalized interview strategy based on performance history and improvement patterns',
        expectedImpact: {
          scoreImprovement: 0.7,
          timeReduction: 5,
          satisfactionIncrease: 0.5,
          implementationEffort: 'low'
        },
        actionSteps: [
          {
            step: `Prepare for ${nextStrategy.recommendedType} interview format`,
            owner: 'candidate',
            timeframe: `${nextStrategy.preparationTime} minutes`,
            resources: ['Interview format guidelines', 'Sample questions']
          },
          {
            step: `Practice ${nextStrategy.focusCategories.join(' and ')} questions`,
            owner: 'candidate',
            timeframe: '1 week',
            resources: ['Category-specific practice sets']
          },
          {
            step: `Set difficulty level to ${nextStrategy.suggestedDifficulty}`,
            owner: 'interviewer',
            timeframe: 'Before interview'
          }
        ],
        metrics: {
          baseline: { currentAverageScore: candidateInsights.profileSummary.averageScore },
          targets: { nextInterviewScore: Math.min(10, candidateInsights.profileSummary.averageScore + 0.5) },
          measurement: 'Performance in next scheduled interview'
        }
      });

      return recommendations;

    } catch (error) {
      console.error('Failed to generate candidate recommendations:', error);
      return [];
    }
  }

  private async generateInterviewSpecificRecommendations(interviewId: string): Promise<InterviewImprovementRecommendation[]> {
    try {
      const completionAnalytics = await this.generateCompletionAnalytics(interviewId);
      const recommendations: InterviewImprovementRecommendation[] = [];

      // Behavioral insights recommendations
      const insights = completionAnalytics.behavioralInsights;

      if (insights.stressIndicators.overallStressLevel === 'high') {
        recommendations.push({
          id: `stress_mitigation_${interviewId}_${Date.now()}`,
          type: 'process',
          priority: 'high',
          title: 'Implement Stress Reduction Measures',
          description: 'High stress indicators detected during interview affecting candidate performance',
          reasoning: 'High stress levels (time outliers, quality dips, confidence drops) suggest interview environment or format may be too pressured',
          expectedImpact: {
            scoreImprovement: 1.2,
            timeReduction: 0,
            satisfactionIncrease: 1.0,
            implementationEffort: 'medium'
          },
          actionSteps: [
            {
              step: 'Add 2-minute breaks between difficult question sections',
              owner: 'interviewer',
              timeframe: 'Next interview',
              resources: ['Updated interview script']
            },
            {
              step: 'Provide encouragement after challenging questions',
              owner: 'interviewer',
              timeframe: 'Immediate',
              resources: ['Interviewer guidelines for candidate support']
            },
            {
              step: 'Review question ordering to reduce stress buildup',
              owner: 'admin',
              timeframe: '1 week'
            }
          ],
          metrics: {
            baseline: {
              stressLevel: insights.stressIndicators.overallStressLevel,
              timeOutliers: insights.stressIndicators.timeOutliers,
              qualityDips: insights.stressIndicators.qualityDips
            },
            targets: {
              stressLevel: 'moderate',
              timeOutliers: Math.max(0, insights.stressIndicators.timeOutliers - 2),
              qualityDips: Math.max(0, insights.stressIndicators.qualityDips - 1)
            },
            measurement: 'Stress indicators in subsequent interviews with same template'
          }
        });
      }

      // Performance pattern recommendations
      if (completionAnalytics.performanceMetrics.improvementTrend === 'declining') {
        recommendations.push({
          id: `performance_pattern_${interviewId}_${Date.now()}`,
          type: 'process',
          priority: 'medium',
          title: 'Address Performance Decline Pattern',
          description: 'Performance declined during interview, suggesting fatigue or increasing difficulty',
          reasoning: 'Declining performance pattern may indicate poor question sequencing, candidate fatigue, or inappropriate difficulty progression',
          expectedImpact: {
            scoreImprovement: 0.8,
            timeReduction: 5,
            satisfactionIncrease: 0.6,
            implementationEffort: 'low'
          },
          actionSteps: [
            {
              step: 'Reorder questions to alternate difficulty levels',
              owner: 'admin',
              timeframe: '3 days'
            },
            {
              step: 'Add motivational checkpoints every 15 minutes',
              owner: 'interviewer',
              timeframe: 'Next interview',
              resources: ['Checkpoint script examples']
            },
            {
              step: 'Monitor energy levels and adjust pacing accordingly',
              owner: 'interviewer',
              timeframe: 'Ongoing'
            }
          ],
          metrics: {
            baseline: { improvementTrend: 'declining', consistencyScore: completionAnalytics.performanceMetrics.consistencyScore },
            targets: { improvementTrend: 'stable', consistencyScore: Math.min(1, completionAnalytics.performanceMetrics.consistencyScore + 0.2) },
            measurement: 'Performance trend analysis in next 5 interviews using this template'
          }
        });
      }

      // Quality metrics recommendations
      if (completionAnalytics.qualityMetrics.engagementMetrics.overallEngagement < 0.6) {
        recommendations.push({
          id: `engagement_improvement_${interviewId}_${Date.now()}`,
          type: 'process',
          priority: 'medium',
          title: 'Improve Candidate Engagement',
          description: 'Low engagement metrics suggest candidate may not be fully invested in the interview process',
          reasoning: 'Poor engagement affects response quality and provides incomplete assessment of candidate capabilities',
          expectedImpact: {
            scoreImprovement: 0.6,
            timeReduction: 0,
            satisfactionIncrease: 0.8,
            implementationEffort: 'low'
          },
          actionSteps: [
            {
              step: 'Include more interactive questions requiring detailed explanations',
              owner: 'admin',
              timeframe: '1 week'
            },
            {
              step: 'Ask follow-up questions to encourage elaboration',
              owner: 'interviewer',
              timeframe: 'Next interview',
              resources: ['Follow-up question templates']
            },
            {
              step: 'Provide real-time feedback on interesting responses',
              owner: 'interviewer',
              timeframe: 'Immediate'
            }
          ],
          metrics: {
            baseline: {
              overallEngagement: completionAnalytics.qualityMetrics.engagementMetrics.overallEngagement,
              elaborationLevel: completionAnalytics.qualityMetrics.engagementMetrics.elaborationLevel
            },
            targets: {
              overallEngagement: 0.75,
              elaborationLevel: Math.min(1, completionAnalytics.qualityMetrics.engagementMetrics.elaborationLevel + 0.2)
            },
            measurement: 'Engagement metrics in next interview with same candidate type'
          }
        });
      }

      return recommendations;

    } catch (error) {
      console.error('Failed to generate interview-specific recommendations:', error);
      return [];
    }
  }

  private async generateSystemWideRecommendations(): Promise<InterviewImprovementRecommendation[]> {
    try {
      // Generate system-wide recommendations based on overall platform analytics
      const recommendations: InterviewImprovementRecommendation[] = [];

      // Mock system-wide analytics - in real implementation, this would aggregate data across all templates and interviews
      const systemMetrics = await this.getSystemWideMetrics();

      // Template standardization recommendation
      if (systemMetrics.templateVariability > 0.3) {
        recommendations.push({
          id: `template_standardization_${Date.now()}`,
          type: 'system_wide',
          priority: 'high',
          title: 'Standardize Interview Templates',
          description: 'High variability in template performance indicates need for standardization',
          reasoning: 'Inconsistent template quality creates unfair candidate experiences and unreliable assessment outcomes',
          expectedImpact: {
            scoreImprovement: 0.8,
            timeReduction: 10,
            satisfactionIncrease: 0.7,
            implementationEffort: 'high'
          },
          actionSteps: [
            {
              step: 'Audit all interview templates for quality and consistency',
              owner: 'admin',
              timeframe: '4 weeks',
              resources: ['Template audit checklist', 'Quality standards document']
            },
            {
              step: 'Create standardized template creation guidelines',
              owner: 'admin',
              timeframe: '2 weeks',
              resources: ['Best practices research', 'Template examples']
            },
            {
              step: 'Implement template review process for new creations',
              owner: 'admin',
              timeframe: '1 week',
              resources: ['Review workflow system']
            },
            {
              step: 'Train template creators on new standards',
              owner: 'admin',
              timeframe: '3 weeks',
              resources: ['Training materials', 'Workshop sessions']
            }
          ],
          metrics: {
            baseline: { templateVariability: systemMetrics.templateVariability },
            targets: { templateVariability: 0.15 },
            measurement: 'Template performance variability coefficient over 3-month period'
          }
        });
      }

      // Interviewer training recommendation
      if (systemMetrics.interviewerConsistency < 0.7) {
        recommendations.push({
          id: `interviewer_training_${Date.now()}`,
          type: 'system_wide',
          priority: 'high',
          title: 'Comprehensive Interviewer Training Program',
          description: 'Low consistency across interviewers indicates need for standardized training',
          reasoning: 'Interviewer variability creates inconsistent candidate experiences and assessment reliability issues',
          expectedImpact: {
            scoreImprovement: 1.0,
            timeReduction: 5,
            satisfactionIncrease: 0.9,
            implementationEffort: 'high'
          },
          actionSteps: [
            {
              step: 'Develop comprehensive interviewer training curriculum',
              owner: 'admin',
              timeframe: '6 weeks',
              resources: ['Training development team', 'Best practices research']
            },
            {
              step: 'Implement mandatory certification program for all interviewers',
              owner: 'admin',
              timeframe: '8 weeks',
              resources: ['Certification platform', 'Assessment tools']
            },
            {
              step: 'Establish ongoing coaching and feedback system',
              owner: 'admin',
              timeframe: '4 weeks',
              resources: ['Coaching framework', 'Performance tracking system']
            },
            {
              step: 'Create interviewer performance dashboards',
              owner: 'system',
              timeframe: '3 weeks',
              resources: ['Analytics platform', 'Dashboard development']
            }
          ],
          metrics: {
            baseline: { interviewerConsistency: systemMetrics.interviewerConsistency },
            targets: { interviewerConsistency: 0.85 },
            measurement: 'Inter-interviewer reliability coefficient over 6-month period'
          }
        });
      }

      // Technology platform improvements
      if (systemMetrics.platformReliability < 0.95) {
        recommendations.push({
          id: `platform_reliability_${Date.now()}`,
          type: 'system_wide',
          priority: 'critical',
          title: 'Improve Platform Reliability',
          description: 'Platform reliability issues are affecting interview completion rates',
          reasoning: 'Technical failures during interviews create negative candidate experiences and invalid assessment results',
          expectedImpact: {
            scoreImprovement: 0.5,
            timeReduction: 15,
            satisfactionIncrease: 1.2,
            implementationEffort: 'high'
          },
          actionSteps: [
            {
              step: 'Implement comprehensive error monitoring and alerting',
              owner: 'system',
              timeframe: '2 weeks',
              resources: ['Monitoring tools', 'Alert system setup']
            },
            {
              step: 'Add automatic backup and recovery mechanisms',
              owner: 'system',
              timeframe: '4 weeks',
              resources: ['Backup infrastructure', 'Recovery procedures']
            },
            {
              step: 'Create redundant systems for critical interview functions',
              owner: 'system',
              timeframe: '6 weeks',
              resources: ['Infrastructure team', 'Redundancy architecture']
            },
            {
              step: 'Establish 24/7 technical support during interview hours',
              owner: 'admin',
              timeframe: '2 weeks',
              resources: ['Support team', 'Escalation procedures']
            }
          ],
          metrics: {
            baseline: { platformReliability: systemMetrics.platformReliability },
            targets: { platformReliability: 0.99 },
            measurement: 'Platform uptime and error rate over 3-month period'
          }
        });
      }

      // Analytics and reporting enhancement
      recommendations.push({
        id: `analytics_enhancement_${Date.now()}`,
        type: 'system_wide',
        priority: 'medium',
        title: 'Enhance Analytics and Reporting Capabilities',
        description: 'Expand analytics to provide deeper insights into interview effectiveness',
        reasoning: 'Better analytics enable data-driven improvements to interview processes and candidate experiences',
        expectedImpact: {
          scoreImprovement: 0.4,
          timeReduction: 8,
          satisfactionIncrease: 0.3,
          implementationEffort: 'medium'
        },
        actionSteps: [
          {
            step: 'Implement real-time analytics dashboard for interview administrators',
            owner: 'system',
            timeframe: '4 weeks',
            resources: ['Dashboard development', 'Real-time data pipeline']
          },
          {
            step: 'Add predictive analytics for candidate success probability',
            owner: 'system',
            timeframe: '8 weeks',
            resources: ['Machine learning team', 'Historical data analysis']
          },
          {
            step: 'Create automated reporting for continuous improvement tracking',
            owner: 'system',
            timeframe: '3 weeks',
            resources: ['Reporting framework', 'Automation tools']
          }
        ],
        metrics: {
          baseline: { analyticsUtilization: systemMetrics.analyticsUtilization },
          targets: { analyticsUtilization: 0.8 },
          measurement: 'Analytics feature usage and improvement implementation rate over 6 months'
        }
      });

      return recommendations;

    } catch (error) {
      console.error('Failed to generate system-wide recommendations:', error);
      return [];
    }
  }

  private async getSystemWideMetrics(): Promise<any> {
    // Mock system-wide metrics - in real implementation, would aggregate across all data
    return {
      templateVariability: 0.35, // High variability in template performance
      interviewerConsistency: 0.65, // Low consistency across interviewers
      platformReliability: 0.92, // Below target reliability
      analyticsUtilization: 0.45, // Low usage of analytics features
      overallSatisfaction: 4.1,
      systemUptime: 0.989,
      errorRate: 0.03
    };
  }

  private getWeakestCategoryScore(candidateInsights: any): number {
    // Find the score for the weakest category
    const weakestCategory = candidateInsights.profileSummary.weakestCategory;
    // Mock category score extraction - in real implementation would come from detailed analytics
    return Math.max(0, candidateInsights.profileSummary.averageScore - 1.5);
  }

  private getTargetImprovement(candidateInsights: any): number {
    const weakestScore = this.getWeakestCategoryScore(candidateInsights);
    return Math.min(10, weakestScore + 2);
  }
}

export const interviewAnalyticsService = new InterviewAnalyticsService();