import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import {
  User,
  Briefcase,
  GraduationCap,
  FolderKanban,
  Sparkles,
  FileQuestion,
  AlertTriangle,
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

// Wizard steps configuration
const WIZARD_STEPS = [
  {
    id: "general",
    title: "Datos Generales",
    description: "Información personal básica",
    icon: User,
  },
  {
    id: "experience",
    title: "Experiencia",
    description: "Tu historial laboral",
    icon: Briefcase,
  },
  {
    id: "education",
    title: "Formación",
    description: "Tu formación académica",
    icon: GraduationCap,
  },
  {
    id: "projects",
    title: "Proyectos",
    description: "Proyectos destacados",
    icon: FolderKanban,
  },
  {
    id: "skills",
    title: "Habilidades",
    description: "Tus competencias",
    icon: Sparkles,
  },
  {
    id: "questions",
    title: "Preguntas",
    description: "Preguntas de la oferta",
    icon: FileQuestion,
  },
  {
    id: "killer",
    title: "Preguntas Clave",
    description: "Preguntas importantes",
    icon: AlertTriangle,
  },
  {
    id: "submit",
    title: "Enviar",
    description: "Revisar y enviar",
    icon: Send,
  },
];

// Step indicator component
function StepIndicator({
  steps,
  currentStep,
  onStepClick,
}: {
  steps: typeof WIZARD_STEPS;
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

// Skills step component (placeholder for now)
function SkillsStep() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Sparkles className="w-5 h-5" />
          Habilidades
        </CardTitle>
        <CardDescription>
          Añade tus habilidades técnicas y soft skills
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500 text-center py-8">
          Las habilidades se pueden editar desde tu perfil completo.
          Este paso es opcional.
        </p>
      </CardContent>
    </Card>
  );
}

// Application questions step component (placeholder)
function QuestionsStep() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileQuestion className="w-5 h-5" />
          Preguntas de la Aplicación
        </CardTitle>
        <CardDescription>
          Responde las preguntas específicas de esta oferta
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500 text-center py-8">
          No hay preguntas adicionales para esta oferta.
        </p>
      </CardContent>
    </Card>
  );
}

// Killer questions step component (placeholder)
function KillerQuestionsStep() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertTriangle className="w-5 h-5" />
          Preguntas Clave
        </CardTitle>
        <CardDescription>
          Estas preguntas son importantes para el proceso de selección
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500 text-center py-8">
          No hay preguntas clave configuradas para esta oferta.
        </p>
      </CardContent>
    </Card>
  );
}

// Submit step component
function SubmitStep({ onSubmit, isSubmitting }: { onSubmit: () => void; isSubmitting: boolean }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Send className="w-5 h-5" />
          Revisar y Enviar
        </CardTitle>
        <CardDescription>
          Revisa tu información antes de enviar la candidatura
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-medium text-blue-900 mb-2">Resumen de tu candidatura</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>- Datos personales completados</li>
            <li>- Experiencia laboral añadida</li>
            <li>- Formación académica incluida</li>
            <li>- Proyectos destacados (opcional)</li>
          </ul>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-sm text-yellow-800">
            <strong>Nota:</strong> Todos los pasos son opcionales. Puedes enviar tu
            candidatura ahora y completar tu perfil más tarde.
          </p>
        </div>

        <Button
          onClick={onSubmit}
          disabled={isSubmitting}
          className="w-full"
          size="lg"
        >
          {isSubmitting ? "Enviando candidatura..." : "Enviar Candidatura"}
        </Button>
      </CardContent>
    </Card>
  );
}

export default function ApplicationWizardPage() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Job position ID can be retrieved from URL if needed using useSearchParams()

  // Check authentication
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      toast.error("Por favor, verifica tu email primero");
      navigate("/");
    }
  }, [navigate]);

  const handleNext = () => {
    if (currentStep < WIZARD_STEPS.length - 1) {
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
      toast.success("¡Candidatura enviada correctamente!");
      navigate("/candidate/application/thank-you");
    } catch (error) {
      console.error("Error submitting application:", error);
      toast.error("Error al enviar la candidatura");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSkipAll = () => {
    // Skip directly to submit step
    setCurrentStep(WIZARD_STEPS.length - 1);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Render current step content
  const renderStepContent = () => {
    switch (WIZARD_STEPS[currentStep].id) {
      case "general":
        return <ProfileBasicInfoForm />;
      case "experience":
        return <ProfileExperienceForm />;
      case "education":
        return <ProfileEducationForm />;
      case "projects":
        return <ProfileProjectsForm />;
      case "skills":
        return <SkillsStep />;
      case "questions":
        return <QuestionsStep />;
      case "killer":
        return <KillerQuestionsStep />;
      case "submit":
        return <SubmitStep onSubmit={handleSubmit} isSubmitting={isSubmitting} />;
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
                Completa tu Candidatura
              </h1>
              <p className="text-sm text-gray-500">
                Paso {currentStep + 1} de {WIZARD_STEPS.length}:{" "}
                {WIZARD_STEPS[currentStep].title}
              </p>
            </div>
            <Button variant="ghost" onClick={handleSkipAll}>
              Saltar al final
            </Button>
          </div>

          {/* Step indicator */}
          <StepIndicator
            steps={WIZARD_STEPS}
            currentStep={currentStep}
            onStepClick={handleStepClick}
          />
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-3xl mx-auto px-4 py-8">
        {renderStepContent()}

        {/* Navigation buttons */}
        {WIZARD_STEPS[currentStep].id !== "submit" && (
          <div className="flex justify-between mt-6">
            <Button
              variant="outline"
              onClick={handlePrevious}
              disabled={currentStep === 0}
            >
              <ChevronLeft className="w-4 h-4 mr-1" />
              Anterior
            </Button>

            <Button onClick={handleNext}>
              Siguiente
              <ChevronRight className="w-4 h-4 ml-1" />
            </Button>
          </div>
        )}

        {/* Back button on submit step */}
        {WIZARD_STEPS[currentStep].id === "submit" && (
          <div className="mt-6">
            <Button variant="outline" onClick={handlePrevious}>
              <ChevronLeft className="w-4 h-4 mr-1" />
              Volver a revisar
            </Button>
          </div>
        )}
      </main>
    </div>
  );
}
