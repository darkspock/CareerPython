import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { toast } from "react-toastify";
import {
  User,
  Briefcase,
  GraduationCap,
  FolderKanban,
  Sparkles,
  FileText,
  Check,
  ChevronLeft,
  ChevronRight,
  ArrowLeft,
  Download,
  Bot,
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { cn } from "../lib/utils";
import { api } from "../lib/api";

// Import existing form components
import ProfileBasicInfoForm from "../components/candidate-profile/forms/ProfileBasicInfoForm";
import ProfileExperienceForm from "../components/candidate-profile/forms/ProfileExperienceForm";
import ProfileEducationForm from "../components/candidate-profile/forms/ProfileEducationForm";
import ProfileProjectsForm from "../components/candidate-profile/forms/ProfileProjectsForm";
import ProfileSkillsForm from "../components/candidate-profile/forms/ProfileSkillsForm";

// Step IDs for the CV builder wizard
const STEP_IDS = ["intro", "general", "experience", "education", "projects", "skills", "generate"] as const;
type StepId = typeof STEP_IDS[number];

// Icons for each step
const STEP_ICONS: Record<StepId, React.ComponentType<{ className?: string }>> = {
  intro: Bot,
  general: User,
  experience: Briefcase,
  education: GraduationCap,
  projects: FolderKanban,
  skills: Sparkles,
  generate: FileText,
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
                disabled={index > currentStep + 1}
                className={cn(
                  "flex flex-col items-center gap-1 p-2 rounded-lg transition-all",
                  isActive && "bg-purple-50",
                  !isActive && index <= currentStep && "hover:bg-gray-50",
                  index > currentStep + 1 && "opacity-50 cursor-not-allowed"
                )}
              >
                <div
                  className={cn(
                    "w-10 h-10 rounded-full flex items-center justify-center transition-all",
                    isActive && "bg-purple-600 text-white",
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
                    isActive && "text-purple-600",
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

// Intro step component
function IntroStep({ onStart, email, setEmail, isLoading }: {
  onStart: () => void;
  email: string;
  setEmail: (email: string) => void;
  isLoading: boolean;
}) {
  const { t } = useTranslation();

  return (
    <Card className="border-purple-200 bg-gradient-to-br from-purple-50 to-indigo-50">
      <CardHeader className="text-center">
        <div className="mx-auto mb-4 h-16 w-16 bg-gradient-to-br from-purple-600 to-indigo-600 rounded-full flex items-center justify-center">
          <Bot className="h-8 w-8 text-white" />
        </div>
        <CardTitle className="text-2xl">
          {t("cvBuilder.intro.title", "Vamos a crear tu CV profesional")}
        </CardTitle>
        <CardDescription className="text-base">
          {t("cvBuilder.intro.description", "Te guiaremos paso a paso para crear un currículum que destaque")}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="bg-white rounded-lg p-6 border border-purple-100">
          <h3 className="font-medium text-gray-900 mb-4">{t("cvBuilder.intro.whatWeNeed", "Lo que necesitamos de ti:")}</h3>
          <ul className="space-y-3 text-gray-600">
            <li className="flex items-start gap-3">
              <User className="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" />
              <span>{t("cvBuilder.intro.step1", "Datos personales básicos (nombre, email, teléfono)")}</span>
            </li>
            <li className="flex items-start gap-3">
              <Briefcase className="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" />
              <span>{t("cvBuilder.intro.step2", "Tu experiencia laboral (puedes añadir varias)")}</span>
            </li>
            <li className="flex items-start gap-3">
              <GraduationCap className="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" />
              <span>{t("cvBuilder.intro.step3", "Tu formación académica")}</span>
            </li>
            <li className="flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" />
              <span>{t("cvBuilder.intro.step4", "Tus habilidades y competencias")}</span>
            </li>
          </ul>
        </div>

        <div className="space-y-4">
          <label className="block text-sm font-medium text-gray-700">
            {t("cvBuilder.intro.emailLabel", "Tu email para comenzar")}
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="tu@email.com"
            className="w-full px-4 py-3 rounded-xl border border-gray-300 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all"
            required
          />
        </div>

        <Button
          onClick={onStart}
          disabled={!email.trim() || isLoading}
          className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700"
          size="lg"
        >
          {isLoading ? t("cvBuilder.intro.creating", "Creando cuenta...") : t("cvBuilder.intro.startButton", "Empezar a crear mi CV")}
        </Button>

        <p className="text-sm text-gray-500 text-center">
          {t("cvBuilder.intro.alreadyHaveCV", "¿Ya tienes un CV?")} {" "}
          <Link to="/" className="text-purple-600 hover:underline">
            {t("cvBuilder.intro.uploadInstead", "Súbelo aquí")}
          </Link>
        </p>
      </CardContent>
    </Card>
  );
}

// Generate CV step component
function GenerateStep({ onGenerate, isGenerating }: {
  onGenerate: () => void;
  isGenerating: boolean;
}) {
  const { t } = useTranslation();

  return (
    <Card className="border-green-200 bg-gradient-to-br from-green-50 to-emerald-50">
      <CardHeader className="text-center">
        <div className="mx-auto mb-4 h-16 w-16 bg-gradient-to-br from-green-600 to-emerald-600 rounded-full flex items-center justify-center">
          <FileText className="h-8 w-8 text-white" />
        </div>
        <CardTitle className="text-2xl">
          {t("cvBuilder.generate.title", "¡Tu CV está listo para generar!")}
        </CardTitle>
        <CardDescription className="text-base">
          {t("cvBuilder.generate.description", "Hemos recopilado toda tu información. Ahora crearemos un CV profesional para ti.")}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="bg-white rounded-lg p-6 border border-green-100">
          <h3 className="font-medium text-gray-900 mb-4">{t("cvBuilder.generate.summary", "Resumen de tu perfil:")}</h3>
          <ul className="space-y-2 text-gray-600 text-sm">
            <li className="flex items-center gap-2">
              <Check className="w-4 h-4 text-green-600" />
              {t("cvBuilder.generate.personalData", "Datos personales completados")}
            </li>
            <li className="flex items-center gap-2">
              <Check className="w-4 h-4 text-green-600" />
              {t("cvBuilder.generate.experience", "Experiencia laboral añadida")}
            </li>
            <li className="flex items-center gap-2">
              <Check className="w-4 h-4 text-green-600" />
              {t("cvBuilder.generate.education", "Formación académica registrada")}
            </li>
            <li className="flex items-center gap-2">
              <Check className="w-4 h-4 text-green-600" />
              {t("cvBuilder.generate.skills", "Habilidades definidas")}
            </li>
          </ul>
        </div>

        <Button
          onClick={onGenerate}
          disabled={isGenerating}
          className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700"
          size="lg"
        >
          {isGenerating ? (
            <>
              <span className="animate-spin mr-2">
                <Bot className="w-5 h-5" />
              </span>
              {t("cvBuilder.generate.generating", "Generando CV...")}
            </>
          ) : (
            <>
              <Download className="w-5 h-5 mr-2" />
              {t("cvBuilder.generate.button", "Generar mi CV profesional")}
            </>
          )}
        </Button>
      </CardContent>
    </Card>
  );
}

export default function CVBuilderPage() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [currentStep, setCurrentStep] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [email, setEmail] = useState("");

  // Build wizard steps with translations
  const wizardSteps: WizardStep[] = STEP_IDS.map(id => ({
    id,
    title: t(`cvBuilder.steps.${id}.title`, getDefaultTitle(id)),
    description: t(`cvBuilder.steps.${id}.description`, ""),
    icon: STEP_ICONS[id],
  }));

  // Check if user is already authenticated
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      // Skip intro step if already authenticated
      setCurrentStep(1);
    }
  }, []);

  const handleStart = async () => {
    if (!email.trim()) return;

    setIsLoading(true);
    try {
      // Create account using registration flow
      const formData = new FormData();
      formData.append('email', email);
      formData.append('gdpr_consent', 'true');

      const data = await api.initiateRegistration(formData);

      if (data.success) {
        toast.success(t("cvBuilder.messages.checkEmail", "¡Revisa tu correo para verificar tu email!"));
        // Store that user came from CV builder
        localStorage.setItem("cv_builder_flow", "true");
        // Show success message
        toast.info(t("cvBuilder.messages.afterVerify", "Después de verificar tu email, podrás continuar creando tu CV"));
      }
    } catch (error: any) {
      console.error('Error:', error);
      if (error?.message?.includes('ya está registrado') || error?.message?.includes('already exists')) {
        toast.info(t("cvBuilder.messages.alreadyRegistered", "Ya tienes una cuenta. Por favor inicia sesión."));
        navigate('/candidate/auth/login');
      } else {
        toast.error(error?.message || t("cvBuilder.messages.error", "Error al crear la cuenta"));
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      // Call API to generate CV
      const candidateId = localStorage.getItem("candidate_id");
      const candidateName = localStorage.getItem("candidate_name") || "CV";
      if (!candidateId) {
        throw new Error("No candidate ID found");
      }

      // Create a general resume with proper parameters
      const response = await api.createGeneralResume({
        candidate_id: candidateId,
        name: `${candidateName} - CV`,
        include_ai_enhancement: true,
      });

      if (response && (response as { resume_id?: string }).resume_id) {
        toast.success(t("cvBuilder.messages.cvGenerated", "¡Tu CV ha sido generado!"));
        // Navigate to resume view or download
        navigate(`/candidate/profile?tab=resumes&generated=${(response as { resume_id: string }).resume_id}`);
      } else {
        toast.success(t("cvBuilder.messages.cvGenerated", "¡Tu CV ha sido generado!"));
        navigate('/candidate/profile?tab=resumes');
      }
    } catch (error: unknown) {
      console.error('Error generating CV:', error);
      const errorMessage = error instanceof Error ? error.message : t("cvBuilder.messages.generateError", "Error al generar el CV");
      toast.error(errorMessage);
    } finally {
      setIsGenerating(false);
    }
  };

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
    if (index <= currentStep + 1) {
      setCurrentStep(index);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  // Render current step content
  const renderStepContent = () => {
    switch (wizardSteps[currentStep].id) {
      case "intro":
        return (
          <IntroStep
            onStart={handleStart}
            email={email}
            setEmail={setEmail}
            isLoading={isLoading}
          />
        );
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
      case "generate":
        return <GenerateStep onGenerate={handleGenerate} isGenerating={isGenerating} />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-indigo-50 to-blue-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <Link to="/" className="text-gray-500 hover:text-gray-700">
                <ArrowLeft className="w-5 h-5" />
              </Link>
              <div>
                <h1 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-purple-600" />
                  {t("cvBuilder.title", "Creador de CV")}
                </h1>
                <p className="text-sm text-gray-500">
                  {t("cvBuilder.stepOf", { current: currentStep + 1, total: wizardSteps.length, defaultValue: `Paso ${currentStep + 1} de ${wizardSteps.length}` })}:{" "}
                  {wizardSteps[currentStep].title}
                </p>
              </div>
            </div>
          </div>

          {/* Step indicator (hide on intro step) */}
          {currentStep > 0 && (
            <StepIndicator
              steps={wizardSteps.slice(1)} // Hide intro from indicator
              currentStep={currentStep - 1}
              onStepClick={(index) => handleStepClick(index + 1)}
            />
          )}
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-3xl mx-auto px-4 py-8">
        {renderStepContent()}

        {/* Navigation buttons (hide on intro and generate steps) */}
        {currentStep > 0 && wizardSteps[currentStep].id !== "generate" && (
          <div className="flex justify-between mt-6">
            <Button
              variant="outline"
              onClick={handlePrevious}
            >
              <ChevronLeft className="w-4 h-4 mr-1" />
              {t("cvBuilder.previous", "Anterior")}
            </Button>

            <Button
              onClick={handleNext}
              className="bg-purple-600 hover:bg-purple-700"
            >
              {t("cvBuilder.next", "Siguiente")}
              <ChevronRight className="w-4 h-4 ml-1" />
            </Button>
          </div>
        )}

        {/* Back button on generate step */}
        {wizardSteps[currentStep].id === "generate" && (
          <div className="mt-6">
            <Button variant="outline" onClick={handlePrevious}>
              <ChevronLeft className="w-4 h-4 mr-1" />
              {t("cvBuilder.backToEdit", "Volver a editar")}
            </Button>
          </div>
        )}
      </main>
    </div>
  );
}

// Helper function for default titles
function getDefaultTitle(id: StepId): string {
  const defaults: Record<StepId, string> = {
    intro: "Inicio",
    general: "Datos personales",
    experience: "Experiencia",
    education: "Formación",
    projects: "Proyectos",
    skills: "Habilidades",
    generate: "Generar CV",
  };
  return defaults[id];
}
