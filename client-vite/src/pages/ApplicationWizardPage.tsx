import { useState, useEffect } from "react";
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

// Import existing form components
import ProfileBasicInfoForm from "../components/candidate-profile/forms/ProfileBasicInfoForm";
import ProfileExperienceForm from "../components/candidate-profile/forms/ProfileExperienceForm";
import ProfileEducationForm from "../components/candidate-profile/forms/ProfileEducationForm";
import ProfileProjectsForm from "../components/candidate-profile/forms/ProfileProjectsForm";
import ProfileSkillsForm from "../components/candidate-profile/forms/ProfileSkillsForm";

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


// Application questions step component (placeholder)
function QuestionsStep({ t }: { t: (key: string) => string }) {
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
      <CardContent>
        <p className="text-gray-500 text-center py-8">
          {t("applicationWizard.questionsStep.noQuestions")}
        </p>
      </CardContent>
    </Card>
  );
}

// Submit step component
function SubmitStep({ onSubmit, isSubmitting, t }: { onSubmit: () => void; isSubmitting: boolean; t: (key: string) => string }) {
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
          <ul className="text-sm text-blue-800 space-y-1">
            <li>- {t("applicationWizard.submitStep.summaryItems.personalData")}</li>
            <li>- {t("applicationWizard.submitStep.summaryItems.experience")}</li>
            <li>- {t("applicationWizard.submitStep.summaryItems.education")}</li>
            <li>- {t("applicationWizard.submitStep.summaryItems.projects")}</li>
          </ul>
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

  // Build wizard steps with translations
  const wizardSteps: WizardStep[] = STEP_IDS
    .filter(id => id !== "questions" || hasQuestions)
    .map(id => ({
      id,
      title: t(`applicationWizard.steps.${id}.title`),
      description: t(`applicationWizard.steps.${id}.description`),
      icon: STEP_ICONS[id],
    }));

  // Check authentication and load job position questions
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      toast.error(t("applicationWizard.verifyEmailFirst"));
      navigate("/");
      return;
    }

    // Check if there are questions for this job position
    const checkQuestions = async () => {
      try {
        const jobPositionId = localStorage.getItem("job_position_id");
        if (jobPositionId) {
          // Fetch questions for the job position
          const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/public/positions/${jobPositionId}/questions`);
          if (response.ok) {
            const questions = await response.json();
            setHasQuestions(Array.isArray(questions) && questions.length > 0);
          }
        }
      } catch (error) {
        console.error("Error checking questions:", error);
      } finally {
        setLoading(false);
      }
    };

    checkQuestions();
  }, [navigate, t]);

  const handleNext = () => {
    if (currentStep < wizardSteps.length - 1) {
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
      // The application was already created during verification
      // Here we just navigate to the thank you page
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
        return <ProfileBasicInfoForm />;
      case "experience":
        return <ProfileExperienceForm />;
      case "education":
        return <ProfileEducationForm />;
      case "projects":
        return <ProfileProjectsForm />;
      case "skills":
        return <ProfileSkillsForm />;
      case "questions":
        return <QuestionsStep t={t} />;
      case "submit":
        return <SubmitStep onSubmit={handleSubmit} isSubmitting={isSubmitting} t={t} />;
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
