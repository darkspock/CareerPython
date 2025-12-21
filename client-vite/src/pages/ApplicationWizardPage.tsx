import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { toast } from "react-toastify";
import {
  User,
  Briefcase,
  GraduationCap,
  FolderKanban,
  Sparkles,
  FileQuestion,
  Send,
  Check,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { cn } from "../lib/utils";

// Import existing form components with their handle types
import ProfileBasicInfoForm, { type ProfileBasicInfoFormHandle } from "../components/candidate-profile/forms/ProfileBasicInfoForm";
import ProfileExperienceForm, { type ProfileExperienceFormHandle } from "../components/candidate-profile/forms/ProfileExperienceForm";
import ProfileEducationForm, { type ProfileEducationFormHandle } from "../components/candidate-profile/forms/ProfileEducationForm";
import ProfileProjectsForm, { type ProfileProjectsFormHandle } from "../components/candidate-profile/forms/ProfileProjectsForm";
import ProfileSkillsForm, { type ProfileSkillsFormHandle } from "../components/candidate-profile/forms/ProfileSkillsForm";

// Step IDs for the wizard
const STEP_IDS = ["general", "experience", "education", "projects", "skills", "questions", "submit"] as const;
type StepId = typeof STEP_IDS[number];

// Icons for each step
const STEP_ICONS: Record<StepId, React.ComponentType<{ className?: string }>> = {
  general: User,
  experience: Briefcase,
  education: GraduationCap,
  projects: FolderKanban,
  skills: Sparkles,
  questions: FileQuestion,
  submit: Send,
};

interface WizardStep {
  id: StepId;
  title: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
}

// Step indicator component
function StepIndicator({
  steps,
  currentStep,
  onStepClick,
}: {
  steps: WizardStep[];
  currentStep: number;
  onStepClick: (index: number) => void;
}) {
  return (
    <div className="w-full overflow-x-auto pb-2">
      <div className="flex items-center justify-between min-w-max px-4">
        {steps.map((step, index) => {
          const Icon = step.icon;
          const isActive = index === currentStep;
          const isCompleted = index < currentStep;

          return (
            <div key={step.id} className="flex items-center">
              <button
                onClick={() => onStepClick(index)}
                className={cn(
                  "flex flex-col items-center gap-1 p-2 rounded-lg transition-all",
                  isActive && "bg-blue-50",
                  !isActive && "hover:bg-gray-50"
                )}
              >
                <div
                  className={cn(
                    "w-10 h-10 rounded-full flex items-center justify-center transition-all",
                    isActive && "bg-blue-600 text-white",
                    isCompleted && "bg-green-500 text-white",
                    !isActive && !isCompleted && "bg-gray-200 text-gray-500"
                  )}
                >
                  {isCompleted ? (
                    <Check className="w-5 h-5" />
                  ) : (
                    <Icon className="w-5 h-5" />
                  )}
                </div>
                <span
                  className={cn(
                    "text-xs font-medium whitespace-nowrap",
                    isActive && "text-blue-600",
                    isCompleted && "text-green-600",
                    !isActive && !isCompleted && "text-gray-500"
                  )}
                >
                  {step.title}
                </span>
              </button>
              {index < steps.length - 1 && (
                <div
                  className={cn(
                    "w-8 h-0.5 mx-1",
                    index < currentStep ? "bg-green-500" : "bg-gray-200"
                  )}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}


// Question type definition
interface ApplicationQuestion {
  id: string;
  field_key: string;
  label: string;
  field_type: string;
  description?: string;
  options?: Array<{ label: string; value: string }>;
  is_required: boolean;
  sort_order: number;
}

// Application questions step component
function QuestionsStep({
  t,
  questions,
  answers,
  onAnswerChange,
}: {
  t: (key: string, options?: Record<string, unknown>) => string;
  questions: ApplicationQuestion[];
  answers: Record<string, unknown>;
  onAnswerChange: (questionId: string, value: unknown) => void;
}) {
  if (questions.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileQuestion className="w-5 h-5" />
            {t("applicationWizard.questionsStep.title")}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-500 text-center py-8">
            {t("applicationWizard.questionsStep.noQuestions")}
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileQuestion className="w-5 h-5" />
          {t("applicationWizard.questionsStep.title")}
        </CardTitle>
        <CardDescription>
          {t("applicationWizard.questionsStep.description")}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {questions.map((question) => (
          <div key={question.id} className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {question.label}
              {question.is_required && <span className="text-red-500 ml-1">*</span>}
            </label>
            {question.description && (
              <p className="text-sm text-gray-500">{question.description}</p>
            )}

            {/* Render different input types */}
            {question.field_type === 'text' && (
              <input
                type="text"
                value={(answers[question.id] as string) || ''}
                onChange={(e) => onAnswerChange(question.id, e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required={question.is_required}
              />
            )}

            {question.field_type === 'textarea' && (
              <textarea
                value={(answers[question.id] as string) || ''}
                onChange={(e) => onAnswerChange(question.id, e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required={question.is_required}
              />
            )}

            {question.field_type === 'select' && question.options && (
              <select
                value={(answers[question.id] as string) || ''}
                onChange={(e) => onAnswerChange(question.id, e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required={question.is_required}
              >
                <option value="">{t("applicationWizard.questionsStep.selectOption", { defaultValue: "Select an option" })}</option>
                {question.options.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            )}

            {question.field_type === 'boolean' && (
              <div className="flex items-center gap-4">
                <label className="flex items-center gap-2">
                  <input
                    type="radio"
                    name={question.id}
                    checked={answers[question.id] === true}
                    onChange={() => onAnswerChange(question.id, true)}
                    className="w-4 h-4 text-blue-600"
                  />
                  {t("applicationWizard.questionsStep.yes", { defaultValue: "Yes" })}
                </label>
                <label className="flex items-center gap-2">
                  <input
                    type="radio"
                    name={question.id}
                    checked={answers[question.id] === false}
                    onChange={() => onAnswerChange(question.id, false)}
                    className="w-4 h-4 text-blue-600"
                  />
                  {t("applicationWizard.questionsStep.no", { defaultValue: "No" })}
                </label>
              </div>
            )}

            {question.field_type === 'number' && (
              <input
                type="number"
                value={(answers[question.id] as number) || ''}
                onChange={(e) => onAnswerChange(question.id, e.target.value ? Number(e.target.value) : null)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required={question.is_required}
              />
            )}
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

// Submit step component
function SubmitStep({
  onSubmit,
  isSubmitting,
  t,
  showProfileSteps
}: {
  onSubmit: () => void;
  isSubmitting: boolean;
  t: (key: string, options?: Record<string, unknown>) => string;
  showProfileSteps: boolean;
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Send className="w-5 h-5" />
          {t("applicationWizard.submitStep.title")}
        </CardTitle>
        <CardDescription>
          {t("applicationWizard.submitStep.description")}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-medium text-blue-900 mb-2">{t("applicationWizard.submitStep.summaryTitle")}</h3>
          {showProfileSteps ? (
            <ul className="text-sm text-blue-800 space-y-1">
              <li>- {t("applicationWizard.submitStep.summaryItems.personalData")}</li>
              <li>- {t("applicationWizard.submitStep.summaryItems.experience")}</li>
              <li>- {t("applicationWizard.submitStep.summaryItems.education")}</li>
              <li>- {t("applicationWizard.submitStep.summaryItems.projects")}</li>
            </ul>
          ) : (
            <p className="text-sm text-blue-800">
              {t("applicationWizard.submitStep.summaryItems.cvOnly", { defaultValue: "Tu CV ha sido recibido y será revisado por el equipo de selección." })}
            </p>
          )}
        </div>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-sm text-yellow-800">
            <strong>{t("applicationWizard.submitStep.note")}</strong> {t("applicationWizard.submitStep.noteText")}
          </p>
        </div>

        <Button
          onClick={onSubmit}
          disabled={isSubmitting}
          className="w-full"
          size="lg"
        >
          {isSubmitting ? t("applicationWizard.submitStep.submitting") : t("applicationWizard.submitStep.submitButton")}
        </Button>
      </CardContent>
    </Card>
  );
}

export default function ApplicationWizardPage() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [currentStep, setCurrentStep] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [hasQuestions, setHasQuestions] = useState(false);
  const [loading, setLoading] = useState(true);
  const [questions, setQuestions] = useState<ApplicationQuestion[]>([]);
  const [questionAnswers, setQuestionAnswers] = useState<Record<string, unknown>>({});
  const [_applicationMode, setApplicationMode] = useState<string>('full');
  const [wantsCVHelp, setWantsCVHelp] = useState(false);
  const [hasPdf, setHasPdf] = useState(false);
  const [requiredSections, setRequiredSections] = useState<string[]>([]);

  // Refs for form components to call submit programmatically
  const basicInfoFormRef = useRef<ProfileBasicInfoFormHandle>(null);
  const experienceFormRef = useRef<ProfileExperienceFormHandle>(null);
  const educationFormRef = useRef<ProfileEducationFormHandle>(null);
  const projectsFormRef = useRef<ProfileProjectsFormHandle>(null);
  const skillsFormRef = useRef<ProfileSkillsFormHandle>(null);

  // All profile steps
  const ALL_PROFILE_STEPS: StepId[] = ["general", "experience", "education", "projects", "skills"];

  // Business rule: Company ALWAYS needs a CV
  // If no PDF uploaded OR wants CV help → show ALL profile sections to generate CV
  // Otherwise → show only required_sections from job position (if any)
  const mustShowAllSections = !hasPdf || wantsCVHelp;

  // Determine which profile steps to show
  const sectionsToShow: StepId[] = mustShowAllSections
    ? ALL_PROFILE_STEPS
    : (requiredSections.length > 0 ? requiredSections as StepId[] : []);

  // For SubmitStep component - true if any profile sections are shown
  const showProfileSteps = sectionsToShow.length > 0;

  // Build wizard steps with translations
  const wizardSteps: WizardStep[] = STEP_IDS
    .filter(id => {
      // Filter out questions step if no questions
      if (id === "questions" && !hasQuestions) return false;
      // Filter out profile steps that are not in sectionsToShow
      if (ALL_PROFILE_STEPS.includes(id) && !sectionsToShow.includes(id)) return false;
      return true;
    })
    .map(id => ({
      id,
      title: t(`applicationWizard.steps.${id}.title`),
      description: t(`applicationWizard.steps.${id}.description`),
      icon: STEP_ICONS[id],
    }));

  // Check authentication and load job position data
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      toast.error(t("applicationWizard.verifyEmailFirst"));
      navigate("/");
      return;
    }

    // Read wants_cv_help from localStorage
    const cvHelpFlag = localStorage.getItem("wants_cv_help");
    setWantsCVHelp(cvHelpFlag === 'true');

    // Read has_pdf from localStorage
    const hasPdfFlag = localStorage.getItem("has_pdf");
    setHasPdf(hasPdfFlag === 'true');

    // Load job position data and questions
    const loadJobPositionData = async () => {
      try {
        let jobPositionId = localStorage.getItem("job_position_id");

        // If job_position_id not in localStorage, try to get it from user's applications
        if (!jobPositionId) {
          const token = localStorage.getItem("access_token");
          if (token) {
            try {
              const appsResponse = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/candidate/application?limit=1`, {
                headers: { 'Authorization': `Bearer ${token}` }
              });
              if (appsResponse.ok) {
                const apps = await appsResponse.json();
                if (apps && apps.length > 0) {
                  jobPositionId = apps[0].job_position_id;
                  // Store for future use
                  if (jobPositionId) {
                    localStorage.setItem("job_position_id", jobPositionId);
                  }
                }
              }
            } catch (err) {
              console.error("Error fetching applications:", err);
            }
          }
        }

        if (jobPositionId) {
          // Fetch job position details to get application_mode and killer_questions
          const positionResponse = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/public/positions/${jobPositionId}`);
          if (positionResponse.ok) {
            const positionData = await positionResponse.json();
            setApplicationMode(positionData.application_mode || 'full');
            setRequiredSections(positionData.required_sections || []);

            // Convert killer_questions to ApplicationQuestion format
            const killerQuestions = positionData.killer_questions || [];
            const convertedQuestions: ApplicationQuestion[] = killerQuestions.map((kq: {
              id: string;
              name: string;
              description?: string;  // Internal notes for recruiters - NOT shown to candidates
              data_type: string;
              scoring_values?: Array<{ label: string; scoring: number }>;
              is_killer?: boolean;
              sort_order?: number;
            }) => {
              // Map data_type to field_type
              // short_string → textarea (for open-ended questions)
              // scoring → select (for scored options)
              // text → text (single line input)
              let fieldType = kq.data_type;
              if (kq.data_type === 'scoring') {
                fieldType = 'select';
              } else if (kq.data_type === 'short_string' || kq.data_type === 'long_string') {
                fieldType = 'textarea';
              }

              return {
                id: kq.id,
                field_key: kq.id,
                label: kq.name,
                field_type: fieldType,
                // NOTE: description is intentionally NOT passed - it contains internal recruiter notes
                description: undefined,
                options: kq.scoring_values?.map(sv => ({
                  label: sv.label,
                  value: sv.label
                })),
                is_required: kq.is_killer ?? true,
                sort_order: kq.sort_order ?? 0
              };
            });

            setQuestions(convertedQuestions);
            setHasQuestions(convertedQuestions.length > 0);
          }
        }
      } catch (error) {
        console.error("Error loading job position data:", error);
      } finally {
        setLoading(false);
      }
    };

    loadJobPositionData();
  }, [navigate, t]);

  // Handle answer change
  const handleAnswerChange = (questionId: string, value: unknown) => {
    setQuestionAnswers((prev) => ({
      ...prev,
      [questionId]: value,
    }));
  };

  const handleNext = async () => {
    if (currentStep < wizardSteps.length - 1) {
      // Save current step before advancing
      const currentStepId = wizardSteps[currentStep].id;

      // Try to save the current form if it has a submit method
      let success = true;
      switch (currentStepId) {
        case "general":
          if (basicInfoFormRef.current) {
            success = await basicInfoFormRef.current.submit();
          }
          break;
        case "experience":
          if (experienceFormRef.current) {
            success = await experienceFormRef.current.submit();
          }
          break;
        case "education":
          if (educationFormRef.current) {
            success = await educationFormRef.current.submit();
          }
          break;
        case "projects":
          if (projectsFormRef.current) {
            success = await projectsFormRef.current.submit();
          }
          break;
        case "skills":
          if (skillsFormRef.current) {
            success = await skillsFormRef.current.submit();
          }
          break;
      }

      // Don't advance if save failed
      if (!success) {
        return;
      }

      setCurrentStep(currentStep + 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleStepClick = (index: number) => {
    setCurrentStep(index);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const applicationId = localStorage.getItem("application_id");
      const token = localStorage.getItem("access_token");

      // Save question answers if we have any
      if (applicationId && Object.keys(questionAnswers).length > 0) {
        const answersPayload = {
          answers: Object.entries(questionAnswers).map(([questionId, value]) => ({
            question_id: questionId,
            answer_value: value,
          })),
        };

        const response = await fetch(
          `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/applications/${applicationId}/answers`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(answersPayload),
          }
        );

        if (!response.ok) {
          throw new Error('Failed to save answers');
        }
      }

      toast.success(t("applicationWizard.messages.submitSuccess"));
      navigate("/candidate/application/thank-you");
    } catch (error) {
      console.error("Error submitting application:", error);
      toast.error(t("applicationWizard.messages.submitError"));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSkipAll = () => {
    // Skip directly to submit step
    setCurrentStep(wizardSteps.length - 1);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Show loading while checking questions
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-500">{t("applicationWizard.loading")}</p>
      </div>
    );
  }

  // Render current step content
  const renderStepContent = () => {
    switch (wizardSteps[currentStep].id) {
      case "general":
        return <ProfileBasicInfoForm ref={basicInfoFormRef} showActions={false} />;
      case "experience":
        return <ProfileExperienceForm ref={experienceFormRef} />;
      case "education":
        return <ProfileEducationForm ref={educationFormRef} />;
      case "projects":
        return <ProfileProjectsForm ref={projectsFormRef} />;
      case "skills":
        return <ProfileSkillsForm ref={skillsFormRef} showActions={false} />;
      case "questions":
        return (
          <QuestionsStep
            t={t}
            questions={questions}
            answers={questionAnswers}
            onAnswerChange={handleAnswerChange}
          />
        );
      case "submit":
        return <SubmitStep onSubmit={handleSubmit} isSubmitting={isSubmitting} t={t} showProfileSteps={showProfileSteps} />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                {t("applicationWizard.title")}
              </h1>
              <p className="text-sm text-gray-500">
                {t("applicationWizard.stepOf", { current: currentStep + 1, total: wizardSteps.length })}:{" "}
                {wizardSteps[currentStep].title}
              </p>
            </div>
            <Button variant="ghost" onClick={handleSkipAll}>
              {t("applicationWizard.skipToEnd")}
            </Button>
          </div>

          {/* Step indicator */}
          <StepIndicator
            steps={wizardSteps}
            currentStep={currentStep}
            onStepClick={handleStepClick}
          />
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-3xl mx-auto px-4 py-8">
        {renderStepContent()}

        {/* Navigation buttons */}
        {wizardSteps[currentStep].id !== "submit" && (
          <div className="flex justify-between mt-6">
            <Button
              variant="outline"
              onClick={handlePrevious}
              disabled={currentStep === 0}
            >
              <ChevronLeft className="w-4 h-4 mr-1" />
              {t("applicationWizard.previous")}
            </Button>

            <Button onClick={handleNext}>
              {t("applicationWizard.next")}
              <ChevronRight className="w-4 h-4 ml-1" />
            </Button>
          </div>
        )}

        {/* Back button on submit step */}
        {wizardSteps[currentStep].id === "submit" && (
          <div className="mt-6">
            <Button variant="outline" onClick={handlePrevious}>
              <ChevronLeft className="w-4 h-4 mr-1" />
              {t("applicationWizard.backToReview")}
            </Button>
          </div>
        )}
      </main>
    </div>
  );
}
