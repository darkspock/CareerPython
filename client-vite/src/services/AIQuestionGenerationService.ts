import { api } from '../lib/api';
import {
  QuestionType,
  QuestionCategory,
  QuestionDifficulty,
  ConversationalQuestion,
  InterviewType
} from '../types/interview';

export interface ResumeContent {
  workExperience: Array<{
    id: string;
    company: string;
    position: string;
    description: string;
    technologies: string[];
    achievements: string[];
    startDate: string;
    endDate?: string;
    industry: string;
  }>;
  education: Array<{
    id: string;
    institution: string;
    degree: string;
    field: string;
    gpa?: number;
    graduationDate: string;
    relevantCourses: string[];
  }>;
  projects: Array<{
    id: string;
    name: string;
    description: string;
    technologies: string[];
    outcomes: string[];
    duration: string;
    teamSize?: number;
  }>;
  skills: {
    technical: string[];
    soft: string[];
    languages: string[];
    certifications: string[];
  };
  personalInfo: {
    yearsExperience: number;
    seniorityLevel: 'junior' | 'mid' | 'senior' | 'lead' | 'executive';
    industries: string[];
    preferredRoles: string[];
  };
}

export interface JobDescription {
  title: string;
  company: string;
  description: string;
  requirements: {
    required: string[];
    preferred: string[];
    experience: string;
    education: string;
  };
  responsibilities: string[];
  technologies: string[];
  industry: string;
  level: 'junior' | 'mid' | 'senior' | 'lead' | 'executive';
  location: string;
  benefits: string[];
}

export interface QuestionGenerationContext {
  resumeContent?: ResumeContent;
  jobDescription?: JobDescription;
  interviewType: InterviewType;
  previousQuestions: ConversationalQuestion[];
  previousResponses: Array<{
    questionId: string;
    response: string;
    quality: number;
    completeness: number;
    confidence: number;
  }>;
  targetDifficulty?: QuestionDifficulty;
  focusAreas?: QuestionCategory[];
  personalityProfile?: {
    communicationStyle: 'direct' | 'detailed' | 'storytelling';
    confidenceLevel: number;
    technicalDepth: number;
    leadershipOriented: boolean;
  };
}

export interface GeneratedQuestion extends ConversationalQuestion {
  generationMetadata: {
    source: 'resume_experience' | 'resume_project' | 'resume_skill' | 'job_requirement' | 'contextual_followup' | 'template_based';
    confidence: number;
    relevanceScore: number;
    difficultyJustification: string;
    adaptationReason?: string;
    sourceReferences: string[];
    alternatives: Array<{
      question: string;
      focus: string;
      difficulty: QuestionDifficulty;
    }>;
  };
}

export interface QuestionGenerationRequest {
  context: QuestionGenerationContext;
  count: number;
  diversityFactor: number; // 0-1, higher = more diverse questions
  includeFollowUps: boolean;
  maxDifficulty?: QuestionDifficulty;
  excludeCategories?: QuestionCategory[];
}

export interface QuestionGenerationResponse {
  questions: GeneratedQuestion[];
  metadata: {
    totalGenerated: number;
    diversityScore: number;
    averageRelevance: number;
    coverageAnalysis: {
      categories: Record<QuestionCategory, number>;
      difficulties: Record<QuestionDifficulty, number>;
      sources: Record<string, number>;
    };
    recommendations: string[];
  };
}

class AIQuestionGenerationService {
  private readonly API_BASE = '/api/interviews/ai/questions';

  // Resume-based question generation
  async generateFromResume(
    resumeContent: ResumeContent,
    options: {
      interviewType: InterviewType;
      count?: number;
      focusAreas?: QuestionCategory[];
      targetDifficulty?: QuestionDifficulty;
    }
  ): Promise<GeneratedQuestion[]> {
    try {
      // In real implementation, this would call the AI service
      // For now, implementing sophisticated mock logic

      const questions: GeneratedQuestion[] = [];
      const { interviewType, count = 10, focusAreas, targetDifficulty } = options;

      // Generate questions from work experience
      if (resumeContent.workExperience.length > 0) {
        const experienceQuestions = this.generateExperienceQuestions(
          resumeContent.workExperience,
          interviewType,
          Math.ceil(count * 0.4)
        );
        questions.push(...experienceQuestions);
      }

      // Generate questions from projects
      if (resumeContent.projects.length > 0) {
        const projectQuestions = this.generateProjectQuestions(
          resumeContent.projects,
          interviewType,
          Math.ceil(count * 0.3)
        );
        questions.push(...projectQuestions);
      }

      // Generate questions from skills
      const skillQuestions = this.generateSkillQuestions(
        resumeContent.skills,
        interviewType,
        Math.ceil(count * 0.3)
      );
      questions.push(...skillQuestions);

      // Filter and adjust based on options
      let filteredQuestions = questions;

      if (focusAreas && focusAreas.length > 0) {
        filteredQuestions = questions.filter(q =>
          focusAreas.includes(q.category)
        );
      }

      if (targetDifficulty) {
        filteredQuestions = this.adjustQuestionDifficulty(filteredQuestions, targetDifficulty);
      }

      // Select the best questions based on relevance and diversity
      return this.selectBestQuestions(filteredQuestions, count);

    } catch (error) {
      console.error('Failed to generate questions from resume:', error);
      throw new Error('Question generation failed');
    }
  }

  // Job-specific question generation
  async generateFromJobDescription(
    jobDescription: JobDescription,
    resumeContent?: ResumeContent,
    options: {
      count?: number;
      emphasizeGaps?: boolean;
      includeCompanySpecific?: boolean;
    } = {}
  ): Promise<GeneratedQuestion[]> {
    try {
      const { count = 8, emphasizeGaps = true, includeCompanySpecific = true } = options;
      const questions: GeneratedQuestion[] = [];

      // Generate questions based on job requirements
      const requirementQuestions = this.generateRequirementQuestions(
        jobDescription.requirements,
        count * 0.5
      );
      questions.push(...requirementQuestions);

      // Generate questions based on responsibilities
      const responsibilityQuestions = this.generateResponsibilityQuestions(
        jobDescription.responsibilities,
        count * 0.3
      );
      questions.push(...responsibilityQuestions);

      // If resume is provided, generate gap analysis questions
      if (resumeContent && emphasizeGaps) {
        const gapQuestions = this.generateSkillGapQuestions(
          resumeContent,
          jobDescription,
          count * 0.2
        );
        questions.push(...gapQuestions);
      }

      return this.selectBestQuestions(questions, count);

    } catch (error) {
      console.error('Failed to generate job-specific questions:', error);
      throw new Error('Job-specific question generation failed');
    }
  }

  // Advanced contextual question chaining for natural conversation flow
  async generateContextualQuestionChain(
    context: QuestionGenerationContext,
    conversationHistory: Array<{
      questionId: string;
      questionText: string;
      response: string;
      quality: number;
      completeness: number;
      category: QuestionCategory;
    }>,
    options: {
      count?: number;
      followTopic?: boolean;
      exploreDepth?: boolean;
      bridgeToNewArea?: boolean;
    } = {}
  ): Promise<GeneratedQuestion[]> {
    try {
      const { count = 3, followTopic = true, exploreDepth = true, bridgeToNewArea = false } = options;
      const questions: GeneratedQuestion[] = [];

      if (conversationHistory.length === 0) {
        return [];
      }

      const lastInteraction = conversationHistory[conversationHistory.length - 1];

      // Analyze conversation patterns and themes
      const conversationAnalysis = this.analyzeConversationFlow(conversationHistory);

      // Generate topic continuation questions
      if (followTopic && conversationAnalysis.currentTopic) {
        const topicQuestions = await this.generateTopicContinuationQuestions(
          lastInteraction,
          conversationAnalysis,
          Math.ceil(count * 0.4)
        );
        questions.push(...topicQuestions);
      }

      // Generate depth exploration questions
      if (exploreDepth) {
        const depthQuestions = await this.generateDepthExplorationQuestions(
          lastInteraction,
          conversationAnalysis,
          Math.ceil(count * 0.4)
        );
        questions.push(...depthQuestions);
      }

      // Generate bridge questions to new areas
      if (bridgeToNewArea || questions.length < count) {
        const bridgeQuestions = await this.generateBridgeQuestions(
          lastInteraction,
          conversationAnalysis,
          context,
          count - questions.length
        );
        questions.push(...bridgeQuestions);
      }

      return this.selectBestQuestions(questions, count);

    } catch (error) {
      console.error('Contextual question chain generation failed:', error);
      throw new Error('Contextual question chain generation failed');
    }
  }

  // Contextual follow-up question generation
  async generateFollowUpQuestions(
    context: QuestionGenerationContext,
    lastResponse: {
      questionId: string;
      response: string;
      quality: number;
      completeness: number;
    },
    options: {
      count?: number;
      deepenUnderstanding?: boolean;
      exploreChallenges?: boolean;
    } = {}
  ): Promise<GeneratedQuestion[]> {
    try {
      const { count = 3, deepenUnderstanding = true, exploreChallenges = true } = options;
      const questions: GeneratedQuestion[] = [];

      const lastQuestion = context.previousQuestions.find(q => q.question_id === lastResponse.questionId);
      if (!lastQuestion) {
        throw new Error('Previous question not found');
      }

      // Analyze the response to determine follow-up directions
      const responseAnalysis = this.analyzeResponse(lastResponse.response, lastQuestion);

      // Generate deepening questions if response quality is good
      if (deepenUnderstanding && lastResponse.quality > 0.7) {
        const deepeningQuestions = this.generateDeepeningQuestions(
          lastQuestion,
          responseAnalysis,
          Math.ceil(count * 0.6)
        );
        questions.push(...deepeningQuestions);
      }

      // Generate challenge/clarification questions if response needs more detail
      if (exploreChallenges && lastResponse.completeness < 0.8) {
        const challengeQuestions = this.generateChallengeQuestions(
          lastQuestion,
          responseAnalysis,
          Math.ceil(count * 0.4)
        );
        questions.push(...challengeQuestions);
      }

      // Generate alternative angle questions
      const alternativeQuestions = this.generateAlternativeAngleQuestions(
        lastQuestion,
        responseAnalysis,
        Math.max(1, count - questions.length)
      );
      questions.push(...alternativeQuestions);

      return questions.slice(0, count);

    } catch (error) {
      console.error('Failed to generate follow-up questions:', error);
      throw new Error('Follow-up question generation failed');
    }
  }

  // Enhanced dynamic difficulty adjustment with performance patterns
  async generateAdaptiveDifficultyQuestions(
    context: QuestionGenerationContext,
    performanceHistory: Array<{
      questionId: string;
      category: QuestionCategory;
      difficulty: QuestionDifficulty;
      score: number;
      timeSpent: number;
      confidence: number;
      completeness: number;
    }>,
    options: {
      count?: number;
      targetCategory?: QuestionCategory;
      adaptationStrategy?: 'progressive' | 'targeted' | 'balanced';
    } = {}
  ): Promise<GeneratedQuestion[]> {
    try {
      const { count = 5, targetCategory, adaptationStrategy = 'balanced' } = options;

      // Analyze performance patterns
      const performanceAnalysis = this.analyzePerformancePatterns(performanceHistory);

      // Generate base questions
      let baseQuestions: GeneratedQuestion[] = [];
      if (context.resumeContent) {
        baseQuestions = await this.generateFromResume(context.resumeContent, {
          interviewType: context.interviewType,
          count: count * 2, // Generate more to have selection options
          focusAreas: targetCategory ? [targetCategory] : undefined
        });
      }

      // Apply adaptive difficulty adjustment
      const adaptedQuestions = this.applyAdaptiveDifficulty(
        baseQuestions,
        performanceAnalysis,
        adaptationStrategy
      );

      return this.selectBestQuestions(adaptedQuestions, count);

    } catch (error) {
      console.error('Adaptive difficulty generation failed:', error);
      throw new Error('Adaptive difficulty generation failed');
    }
  }

  private analyzePerformancePatterns(performanceHistory: Array<{
    questionId: string;
    category: QuestionCategory;
    difficulty: QuestionDifficulty;
    score: number;
    timeSpent: number;
    confidence: number;
    completeness: number;
  }>): any {
    if (performanceHistory.length === 0) {
      return {
        overallTrend: 'neutral',
        categoryStrengths: {},
        difficultyComfort: {},
        timeEfficiency: 0.5,
        confidencePattern: 'stable',
        recommendedDifficulty: QuestionDifficulty.MEDIUM
      };
    }

    // Analyze performance by category
    const categoryPerformance = performanceHistory.reduce((acc, item) => {
      if (!acc[item.category]) {
        acc[item.category] = { scores: [], times: [], confidences: [] };
      }
      acc[item.category].scores.push(item.score);
      acc[item.category].times.push(item.timeSpent);
      acc[item.category].confidences.push(item.confidence);
      return acc;
    }, {} as Record<QuestionCategory, { scores: number[]; times: number[]; confidences: number[] }>);

    const categoryStrengths = Object.entries(categoryPerformance).reduce((acc, [category, data]) => {
      const avgScore = data.scores.reduce((sum, score) => sum + score, 0) / data.scores.length;
      const avgConfidence = data.confidences.reduce((sum, conf) => sum + conf, 0) / data.confidences.length;
      acc[category as QuestionCategory] = {
        strength: (avgScore + avgConfidence) / 2,
        consistency: this.calculateConsistency(data.scores),
        efficiency: this.calculateTimeEfficiency(data.times, data.scores)
      };
      return acc;
    }, {} as Record<QuestionCategory, any>);

    // Analyze performance by difficulty
    const difficultyPerformance = performanceHistory.reduce((acc, item) => {
      if (!acc[item.difficulty]) {
        acc[item.difficulty] = { scores: [], confidences: [] };
      }
      acc[item.difficulty].scores.push(item.score);
      acc[item.difficulty].confidences.push(item.confidence);
      return acc;
    }, {} as Record<QuestionDifficulty, { scores: number[]; confidences: number[] }>);

    const difficultyComfort = Object.entries(difficultyPerformance).reduce((acc, [difficulty, data]) => {
      const avgScore = data.scores.reduce((sum, score) => sum + score, 0) / data.scores.length;
      const avgConfidence = data.confidences.reduce((sum, conf) => sum + conf, 0) / data.confidences.length;
      acc[difficulty as QuestionDifficulty] = {
        comfort: (avgScore + avgConfidence) / 2,
        consistency: this.calculateConsistency(data.scores)
      };
      return acc;
    }, {} as Record<QuestionDifficulty, any>);

    // Determine overall trend
    const recentScores = performanceHistory.slice(-3).map(item => item.score);
    const earlyScores = performanceHistory.slice(0, 3).map(item => item.score);
    const recentAvg = recentScores.reduce((sum, score) => sum + score, 0) / recentScores.length;
    const earlyAvg = earlyScores.reduce((sum, score) => sum + score, 0) / earlyScores.length;

    const overallTrend = recentAvg > earlyAvg + 0.1 ? 'improving' :
                        recentAvg < earlyAvg - 0.1 ? 'declining' : 'stable';

    // Calculate recommended difficulty
    const overallPerformance = performanceHistory.reduce((sum, item) => sum + item.score, 0) / performanceHistory.length;
    const overallConfidence = performanceHistory.reduce((sum, item) => sum + item.confidence, 0) / performanceHistory.length;

    let recommendedDifficulty = QuestionDifficulty.MEDIUM;
    if (overallPerformance > 0.8 && overallConfidence > 0.7) {
      recommendedDifficulty = QuestionDifficulty.HARD;
    } else if (overallPerformance < 0.6 || overallConfidence < 0.4) {
      recommendedDifficulty = QuestionDifficulty.EASY;
    }

    return {
      overallTrend,
      categoryStrengths,
      difficultyComfort,
      timeEfficiency: this.calculateOverallTimeEfficiency(performanceHistory),
      confidencePattern: this.analyzeConfidencePattern(performanceHistory),
      recommendedDifficulty,
      performanceScore: overallPerformance,
      confidenceScore: overallConfidence
    };
  }

  private applyAdaptiveDifficulty(
    questions: GeneratedQuestion[],
    performanceAnalysis: any,
    strategy: 'progressive' | 'targeted' | 'balanced'
  ): GeneratedQuestion[] {
    return questions.map((question, index) => {
      let targetDifficulty = performanceAnalysis.recommendedDifficulty;

      switch (strategy) {
        case 'progressive':
          // Gradually increase difficulty if performing well
          if (performanceAnalysis.overallTrend === 'improving' && performanceAnalysis.performanceScore > 0.7) {
            targetDifficulty = this.increaseDifficulty(performanceAnalysis.recommendedDifficulty);
          }
          break;

        case 'targeted':
          // Focus on weak areas with appropriate difficulty
          const categoryStrength = performanceAnalysis.categoryStrengths[question.category];
          if (categoryStrength && categoryStrength.strength < 0.6) {
            targetDifficulty = this.decreaseDifficulty(performanceAnalysis.recommendedDifficulty);
          } else if (categoryStrength && categoryStrength.strength > 0.8) {
            targetDifficulty = this.increaseDifficulty(performanceAnalysis.recommendedDifficulty);
          }
          break;

        case 'balanced':
          // Mix of difficulties to maintain engagement
          const difficultyVariations = [
            performanceAnalysis.recommendedDifficulty,
            this.increaseDifficulty(performanceAnalysis.recommendedDifficulty),
            this.decreaseDifficulty(performanceAnalysis.recommendedDifficulty)
          ];
          targetDifficulty = difficultyVariations[index % difficultyVariations.length];
          break;
      }

      // Apply difficulty adjustment
      if (targetDifficulty !== question.difficulty) {
        return {
          ...question,
          difficulty: targetDifficulty,
          question_text: this.adjustQuestionComplexity(
            question.question_text,
            question.difficulty,
            targetDifficulty
          ),
          generationMetadata: {
            ...question.generationMetadata,
            adaptationReason: `Difficulty adjusted using ${strategy} strategy based on performance analysis`,
            confidence: question.generationMetadata.confidence * 0.9 // Slightly reduce confidence for adapted questions
          }
        };
      }

      return question;
    });
  }

  private calculateConsistency(scores: number[]): number {
    if (scores.length < 2) return 1;
    const mean = scores.reduce((sum, score) => sum + score, 0) / scores.length;
    const variance = scores.reduce((sum, score) => sum + Math.pow(score - mean, 2), 0) / scores.length;
    const standardDeviation = Math.sqrt(variance);
    return Math.max(0, 1 - standardDeviation); // Higher consistency = lower standard deviation
  }

  private calculateTimeEfficiency(times: number[], scores: number[]): number {
    if (times.length !== scores.length || times.length === 0) return 0.5;

    // Calculate efficiency as score per unit time (normalized)
    const efficiencies = times.map((time, index) => scores[index] / (time / 60)); // score per minute
    const avgEfficiency = efficiencies.reduce((sum, eff) => sum + eff, 0) / efficiencies.length;

    // Normalize to 0-1 scale (assuming max efficiency of 0.5 score per minute)
    return Math.min(1, avgEfficiency / 0.5);
  }

  private calculateOverallTimeEfficiency(performanceHistory: any[]): number {
    const times = performanceHistory.map(item => item.timeSpent);
    const scores = performanceHistory.map(item => item.score);
    return this.calculateTimeEfficiency(times, scores);
  }

  private analyzeConfidencePattern(performanceHistory: any[]): string {
    const confidences = performanceHistory.map(item => item.confidence);
    if (confidences.length < 3) return 'insufficient_data';

    const recent = confidences.slice(-3);
    const early = confidences.slice(0, 3);

    const recentAvg = recent.reduce((sum, conf) => sum + conf, 0) / recent.length;
    const earlyAvg = early.reduce((sum, conf) => sum + conf, 0) / early.length;

    if (recentAvg > earlyAvg + 0.1) return 'building';
    if (recentAvg < earlyAvg - 0.1) return 'declining';

    const consistency = this.calculateConsistency(confidences);
    return consistency > 0.7 ? 'stable' : 'variable';
  }

  // Dynamic difficulty adjustment
  adjustQuestionDifficulty(
    questions: GeneratedQuestion[],
    targetDifficulty: QuestionDifficulty,
    candidatePerformance?: {
      averageScore: number;
      responseQuality: number;
      confidenceLevel: number;
    }
  ): GeneratedQuestion[] {
    return questions.map(question => {
      let adjustedDifficulty = targetDifficulty;

      // Adjust based on candidate performance if provided
      if (candidatePerformance) {
        if (candidatePerformance.averageScore > 0.8 && candidatePerformance.confidenceLevel > 0.7) {
          // Increase difficulty for high performers
          adjustedDifficulty = this.increaseDifficulty(targetDifficulty);
        } else if (candidatePerformance.averageScore < 0.6 || candidatePerformance.confidenceLevel < 0.4) {
          // Decrease difficulty for struggling candidates
          adjustedDifficulty = this.decreaseDifficulty(targetDifficulty);
        }
      }

      // Update question with adjusted difficulty
      const adjustedQuestion: GeneratedQuestion = {
        ...question,
        difficulty: adjustedDifficulty,
        generationMetadata: {
          ...question.generationMetadata,
          adaptationReason: candidatePerformance
            ? `Difficulty adjusted based on candidate performance (avg: ${candidatePerformance.averageScore}, confidence: ${candidatePerformance.confidenceLevel})`
            : 'Difficulty adjusted to target level'
        }
      };

      // Adjust question complexity based on difficulty
      if (adjustedDifficulty !== question.difficulty) {
        adjustedQuestion.question_text = this.adjustQuestionComplexity(
          question.question_text,
          question.difficulty,
          adjustedDifficulty
        );
      }

      return adjustedQuestion;
    });
  }

  // Personalized question generation for different interview types
  async generatePersonalizedQuestions(
    context: QuestionGenerationContext,
    interviewPersonalization: {
      interviewType: InterviewType;
      companyInfo?: {
        name: string;
        industry: string;
        size: 'startup' | 'scale-up' | 'enterprise';
        culture: string[];
        techStack?: string[];
        challenges?: string[];
      };
      roleSpecifics?: {
        level: 'junior' | 'mid' | 'senior' | 'lead' | 'executive';
        teamSize?: number;
        responsibilities: string[];
        keySkills: string[];
        niceToHave?: string[];
      };
      interviewFormat?: {
        duration: number; // minutes
        interviewerCount: number;
        isRemote: boolean;
        includesPairProgramming?: boolean;
        includesWhiteboarding?: boolean;
        includesPresentation?: boolean;
      };
      candidatePreferences?: {
        strengths: string[];
        improvementAreas: string[];
        careerGoals?: string[];
        communicationStyle?: 'direct' | 'detailed' | 'storytelling';
      };
    },
    options: {
      count?: number;
      focusBalance?: {
        technical: number;
        behavioral: number;
        situational: number;
        systemDesign: number;
      };
    } = {}
  ): Promise<GeneratedQuestion[]> {
    try {
      const { count = 10 } = options;
      const questions: GeneratedQuestion[] = [];

      // Generate company-specific questions
      if (interviewPersonalization.companyInfo) {
        const companyQuestions = await this.generateCompanySpecificQuestions(
          context,
          interviewPersonalization.companyInfo,
          Math.ceil(count * 0.3)
        );
        questions.push(...companyQuestions);
      }

      // Generate role-specific questions
      if (interviewPersonalization.roleSpecifics) {
        const roleQuestions = await this.generateRoleSpecificQuestions(
          context,
          interviewPersonalization.roleSpecifics,
          Math.ceil(count * 0.4)
        );
        questions.push(...roleQuestions);
      }

      // Generate format-adapted questions
      if (interviewPersonalization.interviewFormat) {
        const formatQuestions = await this.generateFormatAdaptedQuestions(
          context,
          interviewPersonalization.interviewFormat,
          Math.ceil(count * 0.2)
        );
        questions.push(...formatQuestions);
      }

      // Generate personalized based on candidate preferences
      if (interviewPersonalization.candidatePreferences) {
        const personalizedQuestions = await this.generateCandidateAdaptedQuestions(
          context,
          interviewPersonalization.candidatePreferences,
          Math.ceil(count * 0.1)
        );
        questions.push(...personalizedQuestions);
      }

      // Apply focus balance if specified
      if (options.focusBalance) {
        return this.applyFocusBalance(questions, options.focusBalance, count);
      }

      return this.selectBestQuestions(questions, count);

    } catch (error) {
      console.error('Personalized question generation failed:', error);
      throw new Error('Personalized question generation failed');
    }
  }

  private async generateCompanySpecificQuestions(
    context: QuestionGenerationContext,
    companyInfo: any,
    count: number
  ): Promise<GeneratedQuestion[]> {
    const questions: GeneratedQuestion[] = [];

    const companyTemplates = {
      startup: [
        `${companyInfo.name} is a growing startup. How do you handle the fast-paced, ambiguous environment typical of startups?`,
        `In a startup like ${companyInfo.name}, you might wear multiple hats. Describe a time when you took on responsibilities outside your core expertise.`,
        `What attracts you to working at a startup like ${companyInfo.name}, and what concerns do you have?`,
        `How would you prioritize features when resources are limited, as is common in startups like ${companyInfo.name}?`
      ],
      'scale-up': [
        `${companyInfo.name} is scaling rapidly. How do you maintain code quality and system stability during rapid growth?`,
        `How would you help ${companyInfo.name} build processes and infrastructure that can scale with the company?`,
        `What's your experience with the challenges that come with scaling from startup to mid-size company?`,
        `How do you balance technical debt with feature development in a growing company like ${companyInfo.name}?`
      ],
      enterprise: [
        `${companyInfo.name} is a large enterprise. How do you navigate complex organizational structures and processes?`,
        `How would you drive technical decisions in a large organization like ${companyInfo.name} with many stakeholders?`,
        `What's your approach to working with legacy systems, which are common in enterprises like ${companyInfo.name}?`,
        `How do you ensure innovation while maintaining stability in enterprise environments?`
      ]
    };

    const industryTemplates: Record<string, string[]> = {
      fintech: [
        'How do you approach security and compliance requirements in financial technology?',
        'What experience do you have with financial regulations and their impact on software development?',
        'How would you handle the unique challenges of processing financial transactions at scale?'
      ],
      healthcare: [
        'How do you ensure data privacy and HIPAA compliance in healthcare applications?',
        'What considerations are important when building software that impacts patient care?',
        'How do you balance user experience with regulatory requirements in healthcare?'
      ],
      ecommerce: [
        'How would you design systems to handle traffic spikes during peak shopping periods?',
        'What strategies do you use to optimize conversion rates and user experience?',
        'How do you approach inventory management and supply chain integration?'
      ]
    };

    // Generate company size-specific questions
    const sizeTemplates = companyTemplates[companyInfo.size] || companyTemplates.startup;
    for (let i = 0; i < Math.min(count / 2, sizeTemplates.length); i++) {
      const questionText = sizeTemplates[i];

      const question: GeneratedQuestion = {
        question_id: `gen_company_${companyInfo.size}_${Date.now()}_${i}`,
        question_text: questionText,
        question_type: QuestionType.TEXT,
        category: QuestionCategory.BEHAVIORAL,
        difficulty: QuestionDifficulty.MEDIUM,
        expected_duration: 180,
        context: `Company-specific question for ${companyInfo.name} (${companyInfo.size})`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'job_requirement',
          confidence: 0.85,
          relevanceScore: 0.9,
          difficultyJustification: `Tailored for ${companyInfo.size} company environment`,
          sourceReferences: [companyInfo.name, companyInfo.size],
          alternatives: []
        }
      };

      questions.push(question);
    }

    // Generate industry-specific questions
    const industryQuestions = industryTemplates[companyInfo.industry.toLowerCase()];
    if (industryQuestions) {
      for (let i = 0; i < Math.min(count / 2, industryQuestions.length); i++) {
        const questionText = industryQuestions[i];

        const question: GeneratedQuestion = {
          question_id: `gen_industry_${companyInfo.industry}_${Date.now()}_${i}`,
          question_text: questionText,
          question_type: QuestionType.TEXT,
          category: QuestionCategory.SITUATIONAL,
          difficulty: QuestionDifficulty.MEDIUM,
          expected_duration: 160,
          context: `Industry-specific question for ${companyInfo.industry} sector`,
          follow_up_questions: [],
          multimedia_assets: [],
          generationMetadata: {
            source: 'job_requirement',
            confidence: 0.8,
            relevanceScore: 0.85,
            difficultyJustification: `Tailored for ${companyInfo.industry} industry context`,
            sourceReferences: [companyInfo.industry],
            alternatives: []
          }
        };

        questions.push(question);
      }
    }

    return questions.slice(0, count);
  }

  private async generateRoleSpecificQuestions(
    context: QuestionGenerationContext,
    roleSpecifics: any,
    count: number
  ): Promise<GeneratedQuestion[]> {
    const questions: GeneratedQuestion[] = [];

    const levelTemplates = {
      junior: [
        'How do you approach learning new technologies and staying current with industry trends?',
        'Describe a challenging problem you solved early in your career. What did you learn?',
        'How do you seek feedback and handle constructive criticism?',
        'What resources do you use to improve your technical skills?'
      ],
      mid: [
        'How do you balance technical work with mentoring junior team members?',
        'Describe a time when you had to make a technical decision with limited information.',
        'How do you contribute to technical discussions and code reviews?',
        'What\'s your approach to technical debt and when to address it?'
      ],
      senior: [
        'How do you influence technical direction and architectural decisions?',
        'Describe your approach to mentoring and developing other engineers.',
        'How do you handle disagreements about technical approaches with other senior engineers?',
        'What\'s your strategy for balancing technical excellence with business needs?'
      ],
      lead: [
        'How do you set technical vision and strategy for your team?',
        'Describe your approach to hiring and building high-performing engineering teams.',
        'How do you measure and improve team productivity and code quality?',
        'What\'s your philosophy on technical leadership vs. people management?'
      ]
    };

    const templates = levelTemplates[roleSpecifics.level] || levelTemplates.mid;

    for (let i = 0; i < Math.min(count, templates.length); i++) {
      const questionText = templates[i];

      const question: GeneratedQuestion = {
        question_id: `gen_role_${roleSpecifics.level}_${Date.now()}_${i}`,
        question_text: questionText,
        question_type: QuestionType.TEXT,
        category: roleSpecifics.level === 'junior' ? QuestionCategory.BEHAVIORAL : QuestionCategory.SITUATIONAL,
        difficulty: this.getDifficultyForLevel(roleSpecifics.level),
        expected_duration: this.getDurationForLevel(roleSpecifics.level),
        context: `Role-specific question for ${roleSpecifics.level} level position`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'job_requirement',
          confidence: 0.9,
          relevanceScore: 0.92,
          difficultyJustification: `Tailored for ${roleSpecifics.level} level expectations`,
          sourceReferences: [roleSpecifics.level],
          alternatives: []
        }
      };

      questions.push(question);
    }

    return questions;
  }

  private async generateFormatAdaptedQuestions(
    context: QuestionGenerationContext,
    format: any,
    count: number
  ): Promise<GeneratedQuestion[]> {
    const questions: GeneratedQuestion[] = [];

    // Adapt questions based on interview format
    if (format.includesPairProgramming) {
      questions.push({
        question_id: `gen_format_pair_${Date.now()}`,
        question_text: 'Let\'s work together on implementing a solution to this problem. I\'ll be your pair programming partner.',
        question_type: QuestionType.CODE,
        category: QuestionCategory.TECHNICAL,
        difficulty: QuestionDifficulty.MEDIUM,
        expected_duration: Math.min(format.duration * 0.4, 30 * 60), // 40% of interview or 30 min max
        context: 'Pair programming exercise',
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'template_based',
          confidence: 0.95,
          relevanceScore: 1.0,
          difficultyJustification: 'Interactive pair programming session',
          sourceReferences: ['pair_programming'],
          alternatives: []
        }
      });
    }

    if (format.includesWhiteboarding) {
      questions.push({
        question_id: `gen_format_whiteboard_${Date.now()}`,
        question_text: 'Please design and diagram the architecture for a system that handles [specific requirements]. Walk me through your thought process.',
        question_type: QuestionType.TEXT,
        category: QuestionCategory.SYSTEM_DESIGN,
        difficulty: QuestionDifficulty.HARD,
        expected_duration: Math.min(format.duration * 0.3, 25 * 60), // 30% of interview or 25 min max
        context: 'Whiteboarding system design exercise',
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'template_based',
          confidence: 0.9,
          relevanceScore: 0.95,
          difficultyJustification: 'Whiteboard system design challenge',
          sourceReferences: ['whiteboarding'],
          alternatives: []
        }
      });
    }

    if (format.includesPresentation) {
      questions.push({
        question_id: `gen_format_presentation_${Date.now()}`,
        question_text: 'Please present a technical concept or project you\'ve worked on to the team. You have 5-10 minutes.',
        question_type: QuestionType.TEXT,
        category: QuestionCategory.BEHAVIORAL,
        difficulty: QuestionDifficulty.MEDIUM,
        expected_duration: 10 * 60, // 10 minutes
        context: 'Technical presentation exercise',
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'template_based',
          confidence: 0.85,
          relevanceScore: 0.9,
          difficultyJustification: 'Communication and presentation skills assessment',
          sourceReferences: ['presentation'],
          alternatives: []
        }
      });
    }

    // Adjust question duration based on total interview time
    if (format.duration < 60) {
      // Short interview - focus on core questions
      questions.forEach(q => {
        q.expected_duration = Math.min(q.expected_duration, 10 * 60); // Max 10 minutes per question
        q.context += ' (shortened for brief interview format)';
      });
    }

    return questions.slice(0, count);
  }

  private async generateCandidateAdaptedQuestions(
    context: QuestionGenerationContext,
    preferences: any,
    count: number
  ): Promise<GeneratedQuestion[]> {
    const questions: GeneratedQuestion[] = [];

    // Adapt questions based on communication style
    if (preferences.communicationStyle === 'storytelling') {
      questions.push({
        question_id: `gen_candidate_storytelling_${Date.now()}`,
        question_text: 'Tell me the story of your most challenging project. What was the journey like from start to finish?',
        question_type: QuestionType.TEXT,
        category: QuestionCategory.BEHAVIORAL,
        difficulty: QuestionDifficulty.MEDIUM,
        expected_duration: 240, // Longer for storytelling style
        context: 'Adapted for storytelling communication preference',
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'contextual_followup',
          confidence: 0.8,
          relevanceScore: 0.85,
          difficultyJustification: 'Adapted for storytelling communication style',
          sourceReferences: ['storytelling'],
          alternatives: []
        }
      });
    }

    // Focus on strengths while still exploring growth areas
    if (preferences.strengths && preferences.strengths.length > 0) {
      const strength = preferences.strengths[0];
      questions.push({
        question_id: `gen_candidate_strength_${Date.now()}`,
        question_text: `I see that ${strength} is one of your key strengths. Can you walk me through how you've applied this strength to solve a complex problem?`,
        question_type: QuestionType.TEXT,
        category: QuestionCategory.BEHAVIORAL,
        difficulty: QuestionDifficulty.MEDIUM,
        expected_duration: 180,
        context: `Question focused on candidate strength: ${strength}`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'contextual_followup',
          confidence: 0.85,
          relevanceScore: 0.9,
          difficultyJustification: 'Focused on candidate strength area',
          sourceReferences: [strength],
          alternatives: []
        }
      });
    }

    return questions.slice(0, count);
  }

  private applyFocusBalance(
    questions: GeneratedQuestion[],
    focusBalance: any,
    targetCount: number
  ): GeneratedQuestion[] {
    const categorizedQuestions = {
      [QuestionCategory.TECHNICAL]: questions.filter(q => q.category === QuestionCategory.TECHNICAL),
      [QuestionCategory.BEHAVIORAL]: questions.filter(q => q.category === QuestionCategory.BEHAVIORAL),
      [QuestionCategory.SITUATIONAL]: questions.filter(q => q.category === QuestionCategory.SITUATIONAL),
      [QuestionCategory.SYSTEM_DESIGN]: questions.filter(q => q.category === QuestionCategory.SYSTEM_DESIGN)
    };

    const selectedQuestions: GeneratedQuestion[] = [];
    const totalWeight = Object.values(focusBalance).reduce((sum, weight) => sum + weight, 0);

    Object.entries(focusBalance).forEach(([category, weight]) => {
      const categoryQuestions = categorizedQuestions[category as QuestionCategory] || [];
      const targetCount = Math.round((weight / totalWeight) * targetCount);
      const selected = this.selectBestQuestions(categoryQuestions, targetCount);
      selectedQuestions.push(...selected);
    });

    return selectedQuestions.slice(0, targetCount);
  }

  private getDifficultyForLevel(level: string): QuestionDifficulty {
    switch (level) {
      case 'junior': return QuestionDifficulty.EASY;
      case 'mid': return QuestionDifficulty.MEDIUM;
      case 'senior': return QuestionDifficulty.HARD;
      case 'lead': return QuestionDifficulty.HARD;
      default: return QuestionDifficulty.MEDIUM;
    }
  }

  private getDurationForLevel(level: string): number {
    switch (level) {
      case 'junior': return 120; // 2 minutes
      case 'mid': return 150; // 2.5 minutes
      case 'senior': return 180; // 3 minutes
      case 'lead': return 240; // 4 minutes
      default: return 150;
    }
  }

  // Comprehensive question generation with advanced AI
  async generateAdvancedQuestions(request: QuestionGenerationRequest): Promise<QuestionGenerationResponse> {
    try {
      const { context, count, diversityFactor, includeFollowUps } = request;
      let questions: GeneratedQuestion[] = [];

      // Generate base questions from different sources
      if (context.resumeContent) {
        const resumeQuestions = await this.generateFromResume(context.resumeContent, {
          interviewType: context.interviewType,
          count: Math.ceil(count * 0.6),
          focusAreas: context.focusAreas,
          targetDifficulty: context.targetDifficulty
        });
        questions.push(...resumeQuestions);
      }

      if (context.jobDescription) {
        const jobQuestions = await this.generateFromJobDescription(
          context.jobDescription,
          context.resumeContent,
          { count: Math.ceil(count * 0.4) }
        );
        questions.push(...jobQuestions);
      }

      // Generate contextual follow-ups if requested and previous responses exist
      if (includeFollowUps && context.previousResponses.length > 0) {
        for (const response of context.previousResponses.slice(-2)) { // Last 2 responses
          const followUps = await this.generateFollowUpQuestions(context, response);
          questions.push(...followUps);
        }
      }

      // Apply diversity and selection algorithms
      const selectedQuestions = this.optimizeQuestionSelection(questions, count, diversityFactor);

      // Calculate metadata
      const metadata = this.calculateGenerationMetadata(selectedQuestions, questions.length);

      return {
        questions: selectedQuestions,
        metadata
      };

    } catch (error) {
      console.error('Advanced question generation failed:', error);
      throw new Error('Advanced question generation failed');
    }
  }

  // Advanced conversation analysis methods

  private analyzeConversationFlow(conversationHistory: Array<{
    questionId: string;
    questionText: string;
    response: string;
    quality: number;
    completeness: number;
    category: QuestionCategory;
  }>): any {
    const recentHistory = conversationHistory.slice(-3); // Focus on last 3 interactions

    // Identify current topic and themes
    const allConcepts = recentHistory.flatMap(interaction =>
      this.extractConcepts(interaction.response)
    );
    const conceptFrequency = allConcepts.reduce((acc, concept) => {
      acc[concept] = (acc[concept] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const dominantConcepts = Object.entries(conceptFrequency)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3)
      .map(([concept]) => concept);

    // Analyze response quality trends
    const qualityTrend = recentHistory.map(h => h.quality);
    const avgQuality = qualityTrend.reduce((sum, q) => sum + q, 0) / qualityTrend.length;

    // Identify areas of strength and weakness
    const categoryPerformance = recentHistory.reduce((acc, interaction) => {
      if (!acc[interaction.category]) {
        acc[interaction.category] = { total: 0, sum: 0 };
      }
      acc[interaction.category].total++;
      acc[interaction.category].sum += interaction.quality;
      return acc;
    }, {} as Record<QuestionCategory, { total: number; sum: number }>);

    const strongAreas = Object.entries(categoryPerformance)
      .filter(([, perf]) => perf.sum / perf.total > 0.7)
      .map(([category]) => category);

    const weakAreas = Object.entries(categoryPerformance)
      .filter(([, perf]) => perf.sum / perf.total < 0.6)
      .map(([category]) => category);

    return {
      currentTopic: dominantConcepts[0],
      themes: dominantConcepts,
      avgQuality,
      qualityTrend,
      strongAreas,
      weakAreas,
      conversationDepth: recentHistory.length,
      lastCategory: recentHistory[recentHistory.length - 1]?.category
    };
  }

  private async generateTopicContinuationQuestions(
    lastInteraction: any,
    conversationAnalysis: any,
    count: number
  ): Promise<GeneratedQuestion[]> {
    const questions: GeneratedQuestion[] = [];
    const currentTopic = conversationAnalysis.currentTopic;

    const continuationTemplates = [
      `You mentioned ${currentTopic}. Can you walk me through the specific steps you took?`,
      `Building on your ${currentTopic} experience, what would you do differently next time?`,
      `How did your approach to ${currentTopic} evolve over time?`,
      `What was the biggest challenge you faced with ${currentTopic}?`,
      `Can you share a specific example where ${currentTopic} made a significant impact?`
    ];

    for (let i = 0; i < Math.min(count, continuationTemplates.length); i++) {
      const template = continuationTemplates[i];
      const questionText = template.replace(/\${currentTopic}/g, currentTopic);

      const question: GeneratedQuestion = {
        question_id: `gen_continuation_${Date.now()}_${i}`,
        question_text: questionText,
        question_type: QuestionType.TEXT,
        category: lastInteraction.category,
        difficulty: QuestionDifficulty.MEDIUM,
        expected_duration: 150,
        context: `Topic continuation from: ${currentTopic}`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'contextual_followup',
          confidence: 0.8,
          relevanceScore: 0.9,
          difficultyJustification: 'Topic continuation to maintain conversation flow',
          sourceReferences: [lastInteraction.questionId, currentTopic],
          alternatives: []
        }
      };

      questions.push(question);
    }

    return questions;
  }

  private async generateDepthExplorationQuestions(
    lastInteraction: any,
    conversationAnalysis: any,
    count: number
  ): Promise<GeneratedQuestion[]> {
    const questions: GeneratedQuestion[] = [];

    const depthTemplates = [
      'What were the underlying factors that influenced your decision-making process?',
      'How did you measure the success of your approach?',
      'What alternative solutions did you consider, and why did you choose this one?',
      'How did you handle any unexpected obstacles or setbacks?',
      'What lessons from this experience have you applied to other situations?',
      'How did stakeholders react to your approach, and how did you manage their expectations?'
    ];

    for (let i = 0; i < Math.min(count, depthTemplates.length); i++) {
      const template = depthTemplates[i];

      const question: GeneratedQuestion = {
        question_id: `gen_depth_${Date.now()}_${i}`,
        question_text: template,
        question_type: QuestionType.TEXT,
        category: lastInteraction.category,
        difficulty: this.increaseDifficulty(QuestionDifficulty.MEDIUM),
        expected_duration: 180,
        context: `Depth exploration following: ${lastInteraction.questionText}`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'contextual_followup',
          confidence: 0.85,
          relevanceScore: 0.88,
          difficultyJustification: 'Deep exploration to understand reasoning and impact',
          sourceReferences: [lastInteraction.questionId],
          alternatives: []
        }
      };

      questions.push(question);
    }

    return questions;
  }

  private async generateBridgeQuestions(
    lastInteraction: any,
    conversationAnalysis: any,
    context: QuestionGenerationContext,
    count: number
  ): Promise<GeneratedQuestion[]> {
    const questions: GeneratedQuestion[] = [];

    // Identify unexplored areas based on conversation analysis
    const allCategories = [
      QuestionCategory.TECHNICAL,
      QuestionCategory.BEHAVIORAL,
      QuestionCategory.SITUATIONAL,
      QuestionCategory.SYSTEM_DESIGN
    ];

    const unexploredCategories = allCategories.filter(category =>
      !conversationAnalysis.strongAreas.includes(category)
    );

    const bridgeTemplates = [
      'That\'s interesting. Now, shifting gears a bit, how would you approach {new_area}?',
      'Building on what you\'ve shared, let\'s explore {new_area}. Can you tell me about a time when {scenario}?',
      'Your experience shows strong {current_strength}. How do you apply similar thinking to {new_area}?',
      'I\'d like to understand your perspective on {new_area}. How do you typically {action}?'
    ];

    for (let i = 0; i < Math.min(count, bridgeTemplates.length); i++) {
      if (unexploredCategories.length === 0) break;

      const targetCategory = unexploredCategories[i % unexploredCategories.length];
      const template = bridgeTemplates[i % bridgeTemplates.length];

      let questionText = template
        .replace('{current_strength}', conversationAnalysis.strongAreas[0] || 'technical skills')
        .replace('{new_area}', this.getCategoryDescription(targetCategory));

      // Add specific scenarios based on target category
      if (template.includes('{scenario}')) {
        const scenario = this.getCategoryScenario(targetCategory);
        questionText = questionText.replace('{scenario}', scenario);
      }

      if (template.includes('{action}')) {
        const action = this.getCategoryAction(targetCategory);
        questionText = questionText.replace('{action}', action);
      }

      const question: GeneratedQuestion = {
        question_id: `gen_bridge_${Date.now()}_${i}`,
        question_text: questionText,
        question_type: QuestionType.TEXT,
        category: targetCategory,
        difficulty: QuestionDifficulty.MEDIUM,
        expected_duration: 160,
        context: `Bridge question transitioning to: ${targetCategory}`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'contextual_followup',
          confidence: 0.75,
          relevanceScore: 0.8,
          difficultyJustification: 'Bridge question to explore new competency areas',
          sourceReferences: [lastInteraction.questionId],
          alternatives: []
        }
      };

      questions.push(question);
    }

    return questions;
  }

  private getCategoryDescription(category: QuestionCategory): string {
    switch (category) {
      case QuestionCategory.TECHNICAL:
        return 'technical problem-solving';
      case QuestionCategory.BEHAVIORAL:
        return 'team collaboration and leadership';
      case QuestionCategory.SITUATIONAL:
        return 'handling challenging situations';
      case QuestionCategory.SYSTEM_DESIGN:
        return 'system architecture and design';
      default:
        return 'problem-solving';
    }
  }

  private getCategoryScenario(category: QuestionCategory): string {
    switch (category) {
      case QuestionCategory.TECHNICAL:
        return 'you had to solve a complex technical problem with limited resources';
      case QuestionCategory.BEHAVIORAL:
        return 'you had to lead a team through a difficult period';
      case QuestionCategory.SITUATIONAL:
        return 'you faced an ethical dilemma in the workplace';
      case QuestionCategory.SYSTEM_DESIGN:
        return 'you had to design a system to handle massive scale';
      default:
        return 'you encountered an unexpected challenge';
    }
  }

  private getCategoryAction(category: QuestionCategory): string {
    switch (category) {
      case QuestionCategory.TECHNICAL:
        return 'approach debugging complex issues';
      case QuestionCategory.BEHAVIORAL:
        return 'motivate and guide team members';
      case QuestionCategory.SITUATIONAL:
        return 'handle conflicts and difficult decisions';
      case QuestionCategory.SYSTEM_DESIGN:
        return 'design scalable and maintainable systems';
      default:
        return 'solve challenging problems';
    }
  }

  // Private helper methods for question generation logic

  private generateExperienceQuestions(
    experiences: ResumeContent['workExperience'],
    interviewType: InterviewType,
    count: number
  ): GeneratedQuestion[] {
    const questions: GeneratedQuestion[] = [];
    const sortedExperiences = experiences.sort((a, b) =>
      new Date(b.startDate).getTime() - new Date(a.startDate).getTime()
    );

    const questionTemplates = {
      technical: [
        "Can you walk me through the technical architecture of {project/system} you worked on at {company}?",
        "What were the biggest technical challenges you faced while working with {technology} at {company}?",
        "How did you implement {specific_technology/feature} in your role at {company}?",
        "Describe a complex problem you solved using {technology} during your time at {company}."
      ],
      behavioral: [
        "Tell me about a time when you had to {responsibility/challenge} at {company}. How did you approach it?",
        "Describe a situation where you had to collaborate with {team/stakeholder} at {company}. What was the outcome?",
        "Can you give me an example of how you handled {challenge/conflict} in your role at {company}?",
        "What was your biggest achievement during your {duration} at {company}?"
      ],
      situational: [
        "If you had to {hypothetical_scenario} similar to your experience at {company}, how would you approach it?",
        "Given your experience with {technology/process} at {company}, how would you handle {new_scenario}?"
      ]
    };

    for (let i = 0; i < Math.min(count, sortedExperiences.length * 2); i++) {
      const experience = sortedExperiences[i % sortedExperiences.length];
      const templateCategory = this.selectQuestionCategory(interviewType);
      const templates = questionTemplates[templateCategory] || questionTemplates.behavioral;
      const template = templates[Math.floor(Math.random() * templates.length)];

      const question = this.populateQuestionTemplate(template, experience, templateCategory);
      questions.push(question);
    }

    return questions.slice(0, count);
  }

  private generateProjectQuestions(
    projects: ResumeContent['projects'],
    interviewType: InterviewType,
    count: number
  ): GeneratedQuestion[] {
    const questions: GeneratedQuestion[] = [];
    const projectsByComplexity = projects.sort((a, b) => b.technologies.length - a.technologies.length);

    const questionTemplates = [
      "Can you describe the {project_name} project you worked on? What was your specific role and contribution?",
      "What were the main technical challenges you encountered in {project_name} and how did you overcome them?",
      "How did you ensure the quality and maintainability of the code in {project_name}?",
      "What would you do differently if you were to start {project_name} again?",
      "How did you collaborate with your team during {project_name}? What was the team dynamic?",
      "What technologies did you choose for {project_name} and why? Were there any trade-offs?",
      "Can you walk me through the architecture decisions you made for {project_name}?",
      "What was the most valuable lesson you learned from working on {project_name}?"
    ];

    for (let i = 0; i < Math.min(count, projects.length * 2); i++) {
      const project = projectsByComplexity[i % projectsByComplexity.length];
      const template = questionTemplates[i % questionTemplates.length];

      const questionText = template.replace('{project_name}', project.name);

      const question: GeneratedQuestion = {
        question_id: `gen_proj_${project.id}_${Date.now()}_${i}`,
        question_text: questionText,
        question_type: QuestionType.TEXT,
        category: project.technologies.length > 3 ? QuestionCategory.TECHNICAL : QuestionCategory.BEHAVIORAL,
        difficulty: this.calculateProjectDifficulty(project),
        expected_duration: 180,
        context: `Generated from project: ${project.name}`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'resume_project',
          confidence: 0.85,
          relevanceScore: 0.9,
          difficultyJustification: `Based on project complexity (${project.technologies.length} technologies, ${project.teamSize || 'unknown'} team size)`,
          sourceReferences: [project.id],
          alternatives: this.generateAlternativeQuestions(questionText, project)
        }
      };

      questions.push(question);
    }

    return questions.slice(0, count);
  }

  private generateSkillQuestions(
    skills: ResumeContent['skills'],
    interviewType: InterviewType,
    count: number
  ): GeneratedQuestion[] {
    const questions: GeneratedQuestion[] = [];
    const allSkills = [...skills.technical, ...skills.soft];

    const skillQuestionTemplates = {
      technical: [
        "How would you rate your proficiency in {skill} and can you provide an example of how you've used it?",
        "What's the most complex project you've worked on using {skill}?",
        "How do you stay updated with the latest developments in {skill}?",
        "Can you explain a challenging problem you solved using {skill}?",
        "How would you teach someone new to {skill} the fundamentals?"
      ],
      soft: [
        "Can you give me an example of how you've demonstrated {skill} in a professional setting?",
        "Describe a situation where your {skill} skills made a significant difference.",
        "How have you developed your {skill} abilities over time?",
        "Tell me about a time when {skill} was crucial to a project's success."
      ]
    };

    // Prioritize technical skills for technical interviews
    const prioritizedSkills = interviewType === InterviewType.TECHNICAL
      ? [...skills.technical, ...skills.soft.slice(0, 3)]
      : [...skills.soft, ...skills.technical.slice(0, 3)];

    for (let i = 0; i < Math.min(count, prioritizedSkills.length); i++) {
      const skill = prioritizedSkills[i];
      const isTechnical = skills.technical.includes(skill);
      const templates = skillQuestionTemplates[isTechnical ? 'technical' : 'soft'];
      const template = templates[Math.floor(Math.random() * templates.length)];

      const questionText = template.replace('{skill}', skill);

      const question: GeneratedQuestion = {
        question_id: `gen_skill_${skill.replace(/\s+/g, '_').toLowerCase()}_${Date.now()}_${i}`,
        question_text: questionText,
        question_type: QuestionType.TEXT,
        category: isTechnical ? QuestionCategory.TECHNICAL : QuestionCategory.BEHAVIORAL,
        difficulty: this.calculateSkillDifficulty(skill, isTechnical),
        expected_duration: 120,
        context: `Generated from ${isTechnical ? 'technical' : 'soft'} skill: ${skill}`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'resume_skill',
          confidence: 0.8,
          relevanceScore: 0.85,
          difficultyJustification: `Based on skill complexity and type (${isTechnical ? 'technical' : 'soft'} skill)`,
          sourceReferences: [skill],
          alternatives: []
        }
      };

      questions.push(question);
    }

    return questions;
  }

  private generateRequirementQuestions(
    requirements: JobDescription['requirements'],
    count: number
  ): GeneratedQuestion[] {
    const questions: GeneratedQuestion[] = [];
    const allRequirements = [...requirements.required, ...requirements.preferred];

    const requirementTemplates = [
      "This role requires {requirement}. Can you describe your experience with this?",
      "How would you approach {requirement} in this position?",
      "The job description mentions {requirement}. Can you give me a specific example of your work in this area?",
      "What's your experience level with {requirement} and how have you applied it in previous roles?",
      "This position involves {requirement}. What methodologies or approaches do you typically use?"
    ];

    for (let i = 0; i < Math.min(count, allRequirements.length); i++) {
      const requirement = allRequirements[i];
      const template = requirementTemplates[i % requirementTemplates.length];
      const questionText = template.replace('{requirement}', requirement);

      const isRequired = requirements.required.includes(requirement);

      const question: GeneratedQuestion = {
        question_id: `gen_req_${requirement.replace(/\s+/g, '_').toLowerCase()}_${Date.now()}_${i}`,
        question_text: questionText,
        question_type: QuestionType.TEXT,
        category: this.categorizeRequirement(requirement),
        difficulty: isRequired ? QuestionDifficulty.MEDIUM : QuestionDifficulty.EASY,
        expected_duration: 150,
        context: `Generated from job ${isRequired ? 'required' : 'preferred'} requirement: ${requirement}`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'job_requirement',
          confidence: 0.9,
          relevanceScore: isRequired ? 0.95 : 0.8,
          difficultyJustification: `${isRequired ? 'Required' : 'Preferred'} job requirement`,
          sourceReferences: [requirement],
          alternatives: []
        }
      };

      questions.push(question);
    }

    return questions;
  }

  private generateResponsibilityQuestions(
    responsibilities: string[],
    count: number
  ): GeneratedQuestion[] {
    const questions: GeneratedQuestion[] = [];

    const responsibilityTemplates = [
      "This role involves {responsibility}. How would you approach this responsibility?",
      "Can you describe a time when you had to {responsibility} in a previous role?",
      "What strategies would you use to effectively {responsibility}?",
      "How do you prioritize when you need to {responsibility} along with other tasks?"
    ];

    for (let i = 0; i < Math.min(count, responsibilities.length); i++) {
      const responsibility = responsibilities[i];
      const template = responsibilityTemplates[i % responsibilityTemplates.length];
      const questionText = template.replace('{responsibility}', responsibility.toLowerCase());

      const question: GeneratedQuestion = {
        question_id: `gen_resp_${i}_${Date.now()}`,
        question_text: questionText,
        question_type: QuestionType.TEXT,
        category: QuestionCategory.BEHAVIORAL,
        difficulty: QuestionDifficulty.MEDIUM,
        expected_duration: 180,
        context: `Generated from job responsibility: ${responsibility}`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'job_requirement',
          confidence: 0.85,
          relevanceScore: 0.9,
          difficultyJustification: 'Based on job responsibility complexity',
          sourceReferences: [responsibility],
          alternatives: []
        }
      };

      questions.push(question);
    }

    return questions;
  }

  private generateSkillGapQuestions(
    resumeContent: ResumeContent,
    jobDescription: JobDescription,
    count: number
  ): GeneratedQuestion[] {
    const questions: GeneratedQuestion[] = [];

    // Identify skill gaps
    const resumeSkills = [...resumeContent.skills.technical, ...resumeContent.skills.soft];
    const jobRequirements = [...jobDescription.requirements.required, ...jobDescription.requirements.preferred];
    const jobTechnologies = jobDescription.technologies;

    const skillGaps = [...jobRequirements, ...jobTechnologies].filter(requirement =>
      !resumeSkills.some(skill =>
        skill.toLowerCase().includes(requirement.toLowerCase()) ||
        requirement.toLowerCase().includes(skill.toLowerCase())
      )
    );

    const gapQuestionTemplates = [
      "I notice this role requires {skill}, which isn't explicitly mentioned in your resume. How would you approach learning this?",
      "This position involves {skill}. While you may not have direct experience, how would you apply your existing skills to this area?",
      "The job requires {skill}. Can you describe any related experience or how you'd quickly get up to speed?",
      "How would you handle the learning curve for {skill} which is important for this role?"
    ];

    for (let i = 0; i < Math.min(count, skillGaps.length); i++) {
      const gap = skillGaps[i];
      const template = gapQuestionTemplates[i % gapQuestionTemplates.length];
      const questionText = template.replace('{skill}', gap);

      const question: GeneratedQuestion = {
        question_id: `gen_gap_${gap.replace(/\s+/g, '_').toLowerCase()}_${Date.now()}_${i}`,
        question_text: questionText,
        question_type: QuestionType.TEXT,
        category: QuestionCategory.SITUATIONAL,
        difficulty: QuestionDifficulty.MEDIUM,
        expected_duration: 120,
        context: `Generated from identified skill gap: ${gap}`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'job_requirement',
          confidence: 0.75,
          relevanceScore: 0.8,
          difficultyJustification: 'Addressing skill gap between resume and job requirements',
          sourceReferences: [gap],
          alternatives: []
        }
      };

      questions.push(question);
    }

    return questions;
  }

  private analyzeResponse(response: string, question: ConversationalQuestion): any {
    // Mock response analysis - in real implementation, this would use NLP
    return {
      mentionedConcepts: this.extractConcepts(response),
      sentiment: 'positive',
      confidence: 0.8,
      completeness: response.length > 100 ? 0.8 : 0.5,
      technicalDepth: question.category === QuestionCategory.TECHNICAL ? 0.7 : 0.3,
      areas: this.identifyResponseAreas(response)
    };
  }

  private generateDeepeningQuestions(
    originalQuestion: ConversationalQuestion,
    responseAnalysis: any,
    count: number
  ): GeneratedQuestion[] {
    const deepeningTemplates = [
      "You mentioned {concept}. Can you elaborate on how that specifically impacted the outcome?",
      "That's interesting about {concept}. What challenges did you face with that approach?",
      "Can you walk me through the decision-making process behind {concept}?",
      "How did you measure the success of {concept} in that situation?"
    ];

    const questions: GeneratedQuestion[] = [];
    const concepts = responseAnalysis.mentionedConcepts.slice(0, count);

    concepts.forEach((concept: string, index: number) => {
      const template = deepeningTemplates[index % deepeningTemplates.length];
      const questionText = template.replace('{concept}', concept);

      const question: GeneratedQuestion = {
        question_id: `gen_deepen_${originalQuestion.question_id}_${index}_${Date.now()}`,
        question_text: questionText,
        question_type: QuestionType.TEXT,
        category: originalQuestion.category,
        difficulty: originalQuestion.difficulty,
        expected_duration: 120,
        context: `Follow-up deepening question for: ${originalQuestion.question_text}`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'contextual_followup',
          confidence: 0.8,
          relevanceScore: 0.85,
          difficultyJustification: 'Deepening understanding of previous response',
          sourceReferences: [originalQuestion.question_id, concept],
          alternatives: []
        }
      };

      questions.push(question);
    });

    return questions;
  }

  private generateChallengeQuestions(
    originalQuestion: ConversationalQuestion,
    responseAnalysis: any,
    count: number
  ): GeneratedQuestion[] {
    const challengeTemplates = [
      "What would you have done differently if {constraint}?",
      "How would you handle a situation where {challenge}?",
      "What if you had to achieve the same result with {limitation}?",
      "How would you adapt your approach if {scenario}?"
    ];

    const questions: GeneratedQuestion[] = [];

    for (let i = 0; i < count; i++) {
      const template = challengeTemplates[i % challengeTemplates.length];
      const questionText = this.populateChallengeTemplate(template, responseAnalysis);

      const question: GeneratedQuestion = {
        question_id: `gen_challenge_${originalQuestion.question_id}_${i}_${Date.now()}`,
        question_text: questionText,
        question_type: QuestionType.TEXT,
        category: QuestionCategory.SITUATIONAL,
        difficulty: this.increaseDifficulty(originalQuestion.difficulty),
        expected_duration: 150,
        context: `Challenge follow-up for: ${originalQuestion.question_text}`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'contextual_followup',
          confidence: 0.75,
          relevanceScore: 0.8,
          difficultyJustification: 'Challenge question to test adaptability',
          sourceReferences: [originalQuestion.question_id],
          alternatives: []
        }
      };

      questions.push(question);
    }

    return questions;
  }

  private generateAlternativeAngleQuestions(
    originalQuestion: ConversationalQuestion,
    responseAnalysis: any,
    count: number
  ): GeneratedQuestion[] {
    const alternativeTemplates = [
      "From a different perspective, how would you approach {topic} if you were {role}?",
      "What would be the stakeholder's view on {topic}?",
      "How might {topic} be different in a {context} environment?",
      "What are the potential risks or downsides of the {approach} you described?"
    ];

    const questions: GeneratedQuestion[] = [];

    for (let i = 0; i < count; i++) {
      const template = alternativeTemplates[i % alternativeTemplates.length];
      const questionText = this.populateAlternativeTemplate(template, originalQuestion, responseAnalysis);

      const question: GeneratedQuestion = {
        question_id: `gen_alt_${originalQuestion.question_id}_${i}_${Date.now()}`,
        question_text: questionText,
        question_type: QuestionType.TEXT,
        category: originalQuestion.category,
        difficulty: originalQuestion.difficulty,
        expected_duration: 140,
        context: `Alternative angle for: ${originalQuestion.question_text}`,
        follow_up_questions: [],
        multimedia_assets: [],
        generationMetadata: {
          source: 'contextual_followup',
          confidence: 0.7,
          relevanceScore: 0.75,
          difficultyJustification: 'Alternative perspective question',
          sourceReferences: [originalQuestion.question_id],
          alternatives: []
        }
      };

      questions.push(question);
    }

    return questions;
  }

  // Utility methods

  private selectBestQuestions(questions: GeneratedQuestion[], count: number): GeneratedQuestion[] {
    // Sort by relevance score and confidence, then select top questions
    return questions
      .sort((a, b) =>
        (b.generationMetadata.relevanceScore * b.generationMetadata.confidence) -
        (a.generationMetadata.relevanceScore * a.generationMetadata.confidence)
      )
      .slice(0, count);
  }

  private optimizeQuestionSelection(
    questions: GeneratedQuestion[],
    count: number,
    diversityFactor: number
  ): GeneratedQuestion[] {
    // Implementation of diversity-aware selection algorithm
    const selected: GeneratedQuestion[] = [];
    const remaining = [...questions];

    while (selected.length < count && remaining.length > 0) {
      let bestIndex = 0;
      let bestScore = -1;

      for (let i = 0; i < remaining.length; i++) {
        const question = remaining[i];
        const baseScore = question.generationMetadata.relevanceScore * question.generationMetadata.confidence;

        // Apply diversity penalty
        const diversityPenalty = this.calculateDiversityPenalty(question, selected, diversityFactor);
        const finalScore = baseScore - diversityPenalty;

        if (finalScore > bestScore) {
          bestScore = finalScore;
          bestIndex = i;
        }
      }

      selected.push(remaining[bestIndex]);
      remaining.splice(bestIndex, 1);
    }

    return selected;
  }

  private calculateDiversityPenalty(
    question: GeneratedQuestion,
    selected: GeneratedQuestion[],
    diversityFactor: number
  ): number {
    let penalty = 0;

    selected.forEach(selectedQuestion => {
      // Category similarity penalty
      if (selectedQuestion.category === question.category) {
        penalty += 0.1 * diversityFactor;
      }

      // Difficulty similarity penalty
      if (selectedQuestion.difficulty === question.difficulty) {
        penalty += 0.05 * diversityFactor;
      }

      // Source similarity penalty
      if (selectedQuestion.generationMetadata.source === question.generationMetadata.source) {
        penalty += 0.15 * diversityFactor;
      }
    });

    return penalty;
  }

  private calculateGenerationMetadata(
    selectedQuestions: GeneratedQuestion[],
    totalGenerated: number
  ): QuestionGenerationResponse['metadata'] {
    const categories: Record<QuestionCategory, number> = {} as any;
    const difficulties: Record<QuestionDifficulty, number> = {} as any;
    const sources: Record<string, number> = {};

    selectedQuestions.forEach(q => {
      categories[q.category] = (categories[q.category] || 0) + 1;
      difficulties[q.difficulty] = (difficulties[q.difficulty] || 0) + 1;
      sources[q.generationMetadata.source] = (sources[q.generationMetadata.source] || 0) + 1;
    });

    const averageRelevance = selectedQuestions.reduce((sum, q) =>
      sum + q.generationMetadata.relevanceScore, 0) / selectedQuestions.length;

    return {
      totalGenerated,
      diversityScore: this.calculateDiversityScore(selectedQuestions),
      averageRelevance,
      coverageAnalysis: { categories, difficulties, sources },
      recommendations: this.generateRecommendations(selectedQuestions)
    };
  }

  // Helper methods for question processing

  private selectQuestionCategory(interviewType: InterviewType): 'technical' | 'behavioral' | 'situational' {
    switch (interviewType) {
      case InterviewType.TECHNICAL:
        return Math.random() > 0.3 ? 'technical' : 'behavioral';
      case InterviewType.BEHAVIORAL:
        return Math.random() > 0.2 ? 'behavioral' : 'situational';
      default:
        const rand = Math.random();
        return rand > 0.6 ? 'technical' : rand > 0.3 ? 'behavioral' : 'situational';
    }
  }

  private populateQuestionTemplate(
    template: string,
    experience: ResumeContent['workExperience'][0],
    category: string
  ): GeneratedQuestion {
    let questionText = template
      .replace(/\{company\}/g, experience.company)
      .replace(/\{position\}/g, experience.position)
      .replace(/\{duration\}/g, this.calculateDuration(experience.startDate, experience.endDate));

    // Replace technology placeholders
    if (experience.technologies.length > 0) {
      questionText = questionText.replace(/\{technology\}/g,
        experience.technologies[Math.floor(Math.random() * experience.technologies.length)]);
      questionText = questionText.replace(/\{specific_technology\/feature\}/g,
        experience.technologies[0]);
    }

    return {
      question_id: `gen_exp_${experience.id}_${Date.now()}`,
      question_text: questionText,
      question_type: QuestionType.TEXT,
      category: this.mapCategoryToEnum(category),
      difficulty: this.calculateExperienceDifficulty(experience),
      expected_duration: 180,
      context: `Generated from work experience at ${experience.company}`,
      follow_up_questions: [],
      multimedia_assets: [],
      generationMetadata: {
        source: 'resume_experience',
        confidence: 0.85,
        relevanceScore: 0.9,
        difficultyJustification: `Based on experience complexity and seniority at ${experience.company}`,
        sourceReferences: [experience.id],
        alternatives: []
      }
    };
  }

  private calculateProjectDifficulty(project: ResumeContent['projects'][0]): QuestionDifficulty {
    let score = 0;

    // Technology complexity
    score += Math.min(project.technologies.length * 0.3, 1);

    // Team size factor
    if (project.teamSize) {
      score += project.teamSize > 5 ? 0.3 : project.teamSize > 1 ? 0.2 : 0.1;
    }

    // Duration factor
    const duration = parseInt(project.duration) || 1;
    score += duration > 12 ? 0.3 : duration > 6 ? 0.2 : 0.1;

    if (score > 0.8) return QuestionDifficulty.HARD;
    if (score > 0.5) return QuestionDifficulty.MEDIUM;
    return QuestionDifficulty.EASY;
  }

  private calculateSkillDifficulty(skill: string, isTechnical: boolean): QuestionDifficulty {
    const advancedSkills = ['machine learning', 'ai', 'blockchain', 'kubernetes', 'microservices', 'system design'];
    const intermediateSkills = ['react', 'angular', 'node.js', 'python', 'java', 'aws', 'docker'];

    if (isTechnical) {
      if (advancedSkills.some(advanced => skill.toLowerCase().includes(advanced))) {
        return QuestionDifficulty.HARD;
      }
      if (intermediateSkills.some(intermediate => skill.toLowerCase().includes(intermediate))) {
        return QuestionDifficulty.MEDIUM;
      }
      return QuestionDifficulty.EASY;
    } else {
      // Soft skills generally medium difficulty
      return QuestionDifficulty.MEDIUM;
    }
  }

  private calculateExperienceDifficulty(experience: ResumeContent['workExperience'][0]): QuestionDifficulty {
    let score = 0;

    // Technology count
    score += Math.min(experience.technologies.length * 0.2, 0.6);

    // Achievement count
    score += Math.min(experience.achievements.length * 0.1, 0.3);

    // Senior positions
    if (experience.position.toLowerCase().includes('senior') ||
        experience.position.toLowerCase().includes('lead') ||
        experience.position.toLowerCase().includes('principal')) {
      score += 0.3;
    }

    if (score > 0.7) return QuestionDifficulty.HARD;
    if (score > 0.4) return QuestionDifficulty.MEDIUM;
    return QuestionDifficulty.EASY;
  }

  private categorizeRequirement(requirement: string): QuestionCategory {
    const technicalKeywords = ['programming', 'development', 'coding', 'technical', 'software', 'system', 'database', 'api'];
    const behavioralKeywords = ['leadership', 'communication', 'teamwork', 'collaboration', 'management'];

    const reqLower = requirement.toLowerCase();

    if (technicalKeywords.some(keyword => reqLower.includes(keyword))) {
      return QuestionCategory.TECHNICAL;
    }
    if (behavioralKeywords.some(keyword => reqLower.includes(keyword))) {
      return QuestionCategory.BEHAVIORAL;
    }

    return QuestionCategory.SITUATIONAL;
  }

  private adjustQuestionComplexity(
    questionText: string,
    currentDifficulty: QuestionDifficulty,
    targetDifficulty: QuestionDifficulty
  ): string {
    if (currentDifficulty === targetDifficulty) return questionText;

    // Simplify if target is easier
    if (this.getDifficultyScore(targetDifficulty) < this.getDifficultyScore(currentDifficulty)) {
      return questionText
        .replace(/comprehensive|detailed|complex/gi, 'simple')
        .replace(/analyze|evaluate|assess/gi, 'describe')
        .replace(/What are the implications/gi, 'What do you think');
    }

    // Complexify if target is harder
    return questionText
      .replace(/describe/gi, 'analyze and evaluate')
      .replace(/What do you think/gi, 'What are the implications')
      .replace(/simple/gi, 'comprehensive');
  }

  private increaseDifficulty(difficulty: QuestionDifficulty): QuestionDifficulty {
    switch (difficulty) {
      case QuestionDifficulty.EASY: return QuestionDifficulty.MEDIUM;
      case QuestionDifficulty.MEDIUM: return QuestionDifficulty.HARD;
      default: return difficulty;
    }
  }

  private decreaseDifficulty(difficulty: QuestionDifficulty): QuestionDifficulty {
    switch (difficulty) {
      case QuestionDifficulty.HARD: return QuestionDifficulty.MEDIUM;
      case QuestionDifficulty.MEDIUM: return QuestionDifficulty.EASY;
      default: return difficulty;
    }
  }

  private getDifficultyScore(difficulty: QuestionDifficulty): number {
    switch (difficulty) {
      case QuestionDifficulty.EASY: return 1;
      case QuestionDifficulty.MEDIUM: return 2;
      case QuestionDifficulty.HARD: return 3;
      default: return 2;
    }
  }

  private mapCategoryToEnum(category: string): QuestionCategory {
    switch (category) {
      case 'technical': return QuestionCategory.TECHNICAL;
      case 'behavioral': return QuestionCategory.BEHAVIORAL;
      case 'situational': return QuestionCategory.SITUATIONAL;
      default: return QuestionCategory.BEHAVIORAL;
    }
  }

  private extractConcepts(response: string): string[] {
    // Enhanced concept extraction with domain-specific patterns
    const technicalTerms = [
      'algorithm', 'architecture', 'database', 'framework', 'microservices', 'api', 'scalability',
      'security', 'performance', 'optimization', 'deployment', 'testing', 'debugging', 'refactoring',
      'integration', 'automation', 'containerization', 'monitoring', 'logging', 'caching'
    ];

    const behavioralTerms = [
      'leadership', 'collaboration', 'communication', 'mentoring', 'conflict', 'decision',
      'responsibility', 'initiative', 'feedback', 'teamwork', 'coordination', 'prioritization',
      'delegation', 'motivation', 'stakeholder', 'negotiation', 'presentation', 'influence'
    ];

    const businessTerms = [
      'requirement', 'deadline', 'budget', 'resource', 'timeline', 'milestone', 'objective',
      'strategy', 'process', 'efficiency', 'quality', 'customer', 'user', 'business', 'value',
      'roi', 'metrics', 'kpi', 'analysis', 'planning'
    ];

    const words = response.toLowerCase().split(/\s+/);
    const allKeywords = [...technicalTerms, ...behavioralTerms, ...businessTerms];

    // Find mentioned keywords and extract surrounding context
    const concepts: Set<string> = new Set();

    words.forEach((word, index) => {
      // Direct keyword matches
      if (allKeywords.includes(word)) {
        concepts.add(word);
      }

      // Compound terms (e.g., "system design", "code review")
      if (index < words.length - 1) {
        const compound = `${word} ${words[index + 1]}`;
        if (compound.includes('system') || compound.includes('code') ||
            compound.includes('data') || compound.includes('user') ||
            compound.includes('team') || compound.includes('project')) {
          concepts.add(compound);
        }
      }

      // Action-oriented phrases
      if (word.endsWith('ing') && word.length > 6) {
        const context = words.slice(Math.max(0, index - 2), index + 3).join(' ');
        if (context.includes('implement') || context.includes('develop') ||
            context.includes('manage') || context.includes('lead')) {
          concepts.add(context);
        }
      }
    });

    // Extract quantifiable achievements
    const numberPattern = /\d+(\.\d+)?/g;
    const numbers = response.match(numberPattern);
    if (numbers) {
      numbers.forEach(num => {
        const numIndex = response.indexOf(num);
        const context = response.substring(Math.max(0, numIndex - 50), numIndex + 50);
        if (context.includes('%') || context.includes('increase') || context.includes('improve') ||
            context.includes('reduce') || context.includes('save') || context.includes('million') ||
            context.includes('thousand') || context.includes('users') || context.includes('performance')) {
          concepts.add(context.trim());
        }
      });
    }

    return Array.from(concepts).slice(0, 5);
  }

  private identifyResponseAreas(response: string): string[] {
    const areas: string[] = [];
    const responseLower = response.toLowerCase();

    // Technical indicators
    const technicalIndicators = [
      'code', 'algorithm', 'database', 'system', 'architecture', 'framework', 'api',
      'server', 'client', 'frontend', 'backend', 'infrastructure', 'deployment', 'testing'
    ];
    if (technicalIndicators.some(indicator => responseLower.includes(indicator))) {
      areas.push('technical');
    }

    // Leadership indicators
    const leadershipIndicators = [
      'lead', 'manage', 'mentor', 'guide', 'coordinate', 'delegate', 'supervise',
      'direct', 'oversee', 'team', 'responsibility', 'decision', 'initiative'
    ];
    if (leadershipIndicators.some(indicator => responseLower.includes(indicator))) {
      areas.push('leadership');
    }

    // Problem-solving indicators
    const problemSolvingIndicators = [
      'problem', 'solution', 'challenge', 'issue', 'debug', 'troubleshoot', 'analyze',
      'investigate', 'resolve', 'fix', 'optimize', 'improve', 'overcome'
    ];
    if (problemSolvingIndicators.some(indicator => responseLower.includes(indicator))) {
      areas.push('problem-solving');
    }

    // Communication indicators
    const communicationIndicators = [
      'explain', 'present', 'discuss', 'communicate', 'collaborate', 'meeting',
      'stakeholder', 'client', 'customer', 'user', 'feedback', 'documentation'
    ];
    if (communicationIndicators.some(indicator => responseLower.includes(indicator))) {
      areas.push('communication');
    }

    // Innovation/creativity indicators
    const innovationIndicators = [
      'create', 'design', 'innovate', 'invent', 'new', 'novel', 'creative',
      'original', 'prototype', 'experiment', 'research', 'explore'
    ];
    if (innovationIndicators.some(indicator => responseLower.includes(indicator))) {
      areas.push('innovation');
    }

    // Project management indicators
    const projectManagementIndicators = [
      'project', 'timeline', 'deadline', 'milestone', 'planning', 'organize',
      'coordinate', 'schedule', 'resource', 'budget', 'scope', 'deliverable'
    ];
    if (projectManagementIndicators.some(indicator => responseLower.includes(indicator))) {
      areas.push('project-management');
    }

    return areas.length > 0 ? areas : ['general'];
  }

  private populateChallengeTemplate(template: string, responseAnalysis: any): string {
    // Context-aware challenge generation based on response analysis
    let constraints: string[] = [];
    let challenges: string[] = [];
    let limitations: string[] = [];
    let scenarios: string[] = [];

    // Technical context challenges
    if (responseAnalysis.areas.includes('technical')) {
      constraints.push('legacy codebase constraints', 'technical debt', 'API rate limits', 'memory constraints');
      challenges.push('system scalability issues', 'performance bottlenecks', 'security vulnerabilities', 'integration complexities');
      limitations.push('older framework versions', 'limited server resources', 'restricted third-party libraries');
      scenarios.push('the production system went down', 'a critical security patch was needed', 'performance degraded significantly');
    }

    // Leadership context challenges
    if (responseAnalysis.areas.includes('leadership')) {
      constraints.push('cross-functional team conflicts', 'executive pressure', 'competing priorities', 'resource allocation disputes');
      challenges.push('team member resistance to change', 'skill gaps in the team', 'conflicting stakeholder expectations', 'cultural differences');
      limitations.push('reduced team size', 'limited authority', 'budget cuts', 'shortened timeline');
      scenarios.push('a key team member left unexpectedly', 'priorities changed mid-project', 'the team disagreed with your approach');
    }

    // Project management context challenges
    if (responseAnalysis.areas.includes('project-management')) {
      constraints.push('fixed scope and timeline', 'vendor dependencies', 'regulatory requirements', 'client change requests');
      challenges.push('scope creep', 'dependency delays', 'quality vs. timeline trade-offs', 'resource conflicts');
      limitations.push('shortened delivery window', 'reduced scope', 'smaller budget', 'fewer resources');
      scenarios.push('the timeline was cut in half', 'requirements changed significantly', 'a critical dependency failed');
    }

    // Communication context challenges
    if (responseAnalysis.areas.includes('communication')) {
      constraints.push('remote team coordination', 'language barriers', 'time zone differences', 'stakeholder availability');
      challenges.push('misaligned expectations', 'information silos', 'conflicting feedback', 'communication breakdowns');
      limitations.push('limited meeting time', 'asynchronous communication only', 'cultural barriers');
      scenarios.push('stakeholders had conflicting views', 'communication channels were limited', 'feedback was unclear');
    }

    // Default general challenges if no specific areas identified
    if (constraints.length === 0) {
      constraints = ['limited resources', 'tight deadline', 'remote work', 'budget constraints'];
      challenges = ['team disagreement', 'technical limitations', 'changing requirements', 'stakeholder conflicts'];
      limitations = ['half the time', 'limited budget', 'smaller team', 'older technology'];
      scenarios = ['requirements changed', 'you had to work remotely', 'you lost a key team member'];
    }

    return template
      .replace('{constraint}', constraints[Math.floor(Math.random() * constraints.length)])
      .replace('{challenge}', challenges[Math.floor(Math.random() * challenges.length)])
      .replace('{limitation}', limitations[Math.floor(Math.random() * limitations.length)])
      .replace('{scenario}', scenarios[Math.floor(Math.random() * scenarios.length)]);
  }

  private populateAlternativeTemplate(
    template: string,
    originalQuestion: ConversationalQuestion,
    responseAnalysis: any
  ): string {
    let roles: string[] = [];
    let contexts: string[] = [];
    let topics: string[] = [];

    // Role selection based on response areas
    if (responseAnalysis.areas.includes('technical')) {
      roles.push('a senior architect', 'a security specialist', 'a performance engineer', 'a DevOps engineer');
      topics.push('the technical approach', 'the architecture design', 'the implementation strategy');
    }

    if (responseAnalysis.areas.includes('leadership')) {
      roles.push('a team lead', 'a project manager', 'a product owner', 'an executive sponsor');
      topics.push('the leadership approach', 'the team dynamics', 'the decision-making process');
    }

    if (responseAnalysis.areas.includes('project-management')) {
      roles.push('a project manager', 'a scrum master', 'a business analyst', 'a stakeholder');
      topics.push('the project approach', 'the timeline management', 'the resource allocation');
    }

    if (responseAnalysis.areas.includes('communication')) {
      roles.push('a client representative', 'a stakeholder', 'a team member', 'a cross-functional partner');
      topics.push('the communication strategy', 'the collaboration approach', 'the information sharing');
    }

    // Context selection based on mentioned concepts
    const concepts = responseAnalysis.mentionedConcepts;
    if (concepts.some((concept: string) => concept.includes('startup') || concept.includes('agile'))) {
      contexts.push('fast-paced startup', 'agile environment', 'rapid iteration');
    }
    if (concepts.some((concept: string) => concept.includes('enterprise') || concept.includes('scale'))) {
      contexts.push('large enterprise', 'highly regulated', 'global scale');
    }
    if (concepts.some((concept: string) => concept.includes('remote') || concept.includes('distributed'))) {
      contexts.push('fully remote', 'distributed team', 'async collaboration');
    }

    // Default values if no specific context found
    if (roles.length === 0) {
      roles = ['a team lead', 'a junior developer', 'a project manager', 'the client'];
    }
    if (contexts.length === 0) {
      contexts = ['startup', 'enterprise', 'remote', 'high-pressure'];
    }
    if (topics.length === 0) {
      topics = ['the approach', 'the solution', 'the strategy'];
    }

    return template
      .replace('{topic}', topics[Math.floor(Math.random() * topics.length)])
      .replace('{role}', roles[Math.floor(Math.random() * roles.length)])
      .replace('{context}', contexts[Math.floor(Math.random() * contexts.length)])
      .replace('{approach}', 'approach');
  }

  private generateAlternativeQuestions(questionText: string, project: ResumeContent['projects'][0]): Array<{
    question: string;
    focus: string;
    difficulty: QuestionDifficulty;
  }> {
    return [
      {
        question: `What technologies would you choose differently for ${project.name} if you started today?`,
        focus: 'technology choices',
        difficulty: QuestionDifficulty.MEDIUM
      },
      {
        question: `What was the biggest lesson learned from ${project.name}?`,
        focus: 'learning outcomes',
        difficulty: QuestionDifficulty.EASY
      }
    ];
  }

  private calculateDuration(startDate: string, endDate?: string): string {
    const start = new Date(startDate);
    const end = endDate ? new Date(endDate) : new Date();
    const months = (end.getFullYear() - start.getFullYear()) * 12 + (end.getMonth() - start.getMonth());

    if (months < 12) return `${months} months`;
    const years = Math.floor(months / 12);
    const remainingMonths = months % 12;
    return remainingMonths > 0 ? `${years} years ${remainingMonths} months` : `${years} years`;
  }

  private calculateDiversityScore(questions: GeneratedQuestion[]): number {
    const categories = new Set(questions.map(q => q.category));
    const difficulties = new Set(questions.map(q => q.difficulty));
    const sources = new Set(questions.map(q => q.generationMetadata.source));

    // Diversity score based on variety in categories, difficulties, and sources
    return (categories.size + difficulties.size + sources.size) / (3 * 4); // Normalized to 0-1
  }

  private generateRecommendations(questions: GeneratedQuestion[]): string[] {
    const recommendations: string[] = [];

    const categoryCount = questions.reduce((acc, q) => {
      acc[q.category] = (acc[q.category] || 0) + 1;
      return acc;
    }, {} as Record<QuestionCategory, number>);

    // Check for balance
    if ((categoryCount[QuestionCategory.TECHNICAL] || 0) > questions.length * 0.7) {
      recommendations.push('Consider adding more behavioral questions for better balance');
    }

    if ((categoryCount[QuestionCategory.BEHAVIORAL] || 0) > questions.length * 0.7) {
      recommendations.push('Consider adding more technical questions to assess skills');
    }

    // Check difficulty distribution
    const difficultyCount = questions.reduce((acc, q) => {
      acc[q.difficulty] = (acc[q.difficulty] || 0) + 1;
      return acc;
    }, {} as Record<QuestionDifficulty, number>);

    if ((difficultyCount[QuestionDifficulty.EASY] || 0) === 0) {
      recommendations.push('Consider adding some easier questions to build candidate confidence');
    }

    if ((difficultyCount[QuestionDifficulty.HARD] || 0) === 0) {
      recommendations.push('Consider adding challenging questions to assess advanced capabilities');
    }

    return recommendations.length > 0 ? recommendations : ['Question set is well-balanced and comprehensive'];
  }
}

export const aiQuestionGenerationService = new AIQuestionGenerationService();