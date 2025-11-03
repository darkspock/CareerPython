import { useState, useEffect, useRef } from "react";
import { useNavigate, useSearchParams, useLocation } from "react-router-dom";
import { toast } from 'react-toastify';
import { api } from "../lib/api";
import { OnboardingLayout } from "../components/onboarding";
import { useOnboarding } from "../hooks/useOnboarding";
import { getUserEmailFromToken } from "../utils/jwt";
import { SuccessMessage } from "../components/common/SuccessMessage";
import LanguageSelector, { type Language, convertLanguagesFromBackend, convertLanguagesToBackend } from "../components/common/LanguageSelector";
import RoleSelector, { type Role, convertRolesFromBackend, convertRolesToBackend } from "../components/common/RoleSelector";

const JobCategory = {
  TECHNOLOGY: "Technology",
  OPERATIONS: "Operations", 
  SALES: "Sales",
  MARKETING: "Marketing",
  ADMINISTRATION: "Administration",
  HR: "Human Resources",
  FINANCE: "Finance",
  CUSTOMER_SERVICE: "Customer Service",
  OTHER: "Other",
};

// Mapeo para convertir las keys a los valores que espera el backend
const JobCategoryMapping: { [key: string]: string } = {
  TECHNOLOGY: "Technology",
  OPERATIONS: "Operations",
  SALES: "Sales",
  MARKETING: "Marketing",
  ADMINISTRATION: "Administration",
  HR: "Human Resources",
  FINANCE: "Finance",
  CUSTOMER_SERVICE: "Customer Service",
  OTHER: "Other",
};


const WorkModalityEnum = {
  REMOTE: 'remote',
  ON_SITE: 'on_site',
  HYBRID: 'hybrid',
} as const;

const WorkModalityLabels = {
  [WorkModalityEnum.REMOTE]: 'Remoto',
  [WorkModalityEnum.ON_SITE]: 'Presencial',
  [WorkModalityEnum.HYBRID]: 'Híbrido',
} as const;


interface FormData {
  name: string;
  dateOfBirth: string;
  city: string;
  country: string;
  phone: string;
  email: string;
  linkedinUrl: string;
  jobCategory: string;
  languages: Language[];
  skills: string[];
  expectedAnnualSalary: string;
  currentAnnualSalary: string;
  relocation: boolean;
  workModality: string[];
  currentRoles: Role[];
  expectedRoles: Role[];
}

// interface ProcessingStatusResponse {
//   status: string;
//   message: string;
//   error?: string;
//   asset_id?: string;
// }

interface CandidateData {
  name?: string;
  date_of_birth?: string;
  city?: string;
  country?: string;
  phone?: string;
  email?: string;
  linkedin_url?: string;
  job_category?: string;
  languages?: Record<string, string>;
  skills?: string[];
  expected_annual_salary?: number;
  current_annual_salary?: number;
  relocation?: boolean;
  work_modality?: string[];
  current_roles?: string[];
  expected_roles?: string[];
  // Frontend-only fields
  linkedinUrl?: string;
  dateOfBirth?: string;
  jobCategory?: string;
  currentAnnualSalary?: string;
  expectedAnnualSalary?: string;
  workModality?: string[];
  currentRoles?: Role[];
  expectedRoles?: Role[];
}

export default function CompleteProfilePage() {
  const [formData, setFormData] = useState<FormData>({
    name: "",
    dateOfBirth: "",
    city: "",
    country: "",
    phone: "",
    email: "",
    linkedinUrl: "",
    jobCategory: "",
    languages: [],
    skills: [],
    expectedAnnualSalary: "",
    currentAnnualSalary: "",
    relocation: false,
    workModality: [],
    currentRoles: [],
    expectedRoles: [],
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [isReviewMode, _setIsReviewMode] = useState(false);
  const [isLoadingCandidate, setIsLoadingCandidate] = useState(false);
  const [processingStatus, setProcessingStatus] = useState<string | null>(null);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  // New state for PDF analysis polling and countdown
  const [_analysisJobId, setAnalysisJobId] = useState<string | null>(null);
  const [isPollingAnalysis, setIsPollingAnalysis] = useState(false);
  const [analysisCompleted, setAnalysisCompleted] = useState(false);
  const [countdown, setCountdown] = useState(30); // Reduced to 30s
  const [countdownActive, setCountdownActive] = useState(false);
  const [userTriedToContinue, setUserTriedToContinue] = useState(false); // New: track if user tried to continue early
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const countdownIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const toastShownRef = useRef(false);

  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const location = useLocation();
  const { updateCandidateData: _updateCandidateData, jobPositionId: _jobPositionId, candidateData: _candidateDataFromHook, nextStep } = useOnboarding();

  // Cleanup function for intervals
  const clearIntervals = () => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
      pollingIntervalRef.current = null;
    }
    if (countdownIntervalRef.current) {
      clearInterval(countdownIntervalRef.current);
      countdownIntervalRef.current = null;
    }
  };

  // Start countdown when user tries to continue early
  const startCountdownForEarlyContinue = () => {
    console.log('⏰ User tried to continue early - starting 30s countdown');
    setUserTriedToContinue(true);
    setCountdownActive(true);
    setCountdown(30);

    countdownIntervalRef.current = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          setCountdownActive(false);
          setUserTriedToContinue(false);
          if (countdownIntervalRef.current) {
            clearInterval(countdownIntervalRef.current);
            countdownIntervalRef.current = null;
          }
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  // Start polling the analysis job status (no countdown until user tries to continue)
  const startPollingAnalysis = (jobId: string) => {
    console.log('🔄 Starting PDF analysis polling for job:', jobId);
    setIsPollingAnalysis(true);
    setAnalysisCompleted(false);

    // Show toast notification if not already shown
    if (!toastShownRef.current) {
      toast.info('📄 Estamos analizando el PDF, mientras tanto vaya rellenando la información', {
        position: "top-center",
        autoClose: false,
        hideProgressBar: false,
        closeOnClick: false,
        pauseOnHover: false,
        draggable: false,
        toastId: 'pdf-analysis-toast'
      });
      toastShownRef.current = true;
    }

    // Don't start countdown automatically - only when user tries to continue

    // Start polling
    const poll = async () => {
      try {
        const response = await api.getJobStatus(jobId) as { status: string; message?: string; error?: string; asset_id?: string };
        console.log('📊 Analysis job status:', response);

        if (response.status === 'completed') {
          console.log('✅ PDF analysis completed successfully');
          setAnalysisCompleted(true);
          setIsPollingAnalysis(false);
          setCountdownActive(false);
          clearIntervals();

          // Dismiss the toast
          toast.dismiss('pdf-analysis-toast');

          // Show success toast
          toast.success('🎉 ¡PDF analizado correctamente! La información se ha extraído automáticamente', {
            position: "top-center",
            autoClose: 3000,
          });

          // Reload candidate data to get the extracted information
          await loadCandidateData();

        } else if (response.status === 'failed') {
          console.log('❌ PDF analysis failed');
          setIsPollingAnalysis(false);
          clearIntervals();

          // Dismiss the toast
          toast.dismiss('pdf-analysis-toast');

          // Show error toast
          toast.warning('⚠️ No se pudo analizar el PDF completamente. Puedes continuar rellenando manualmente', {
            position: "top-center",
            autoClose: 5000,
          });
        }
        // Continue polling if status is still 'pending' or 'processing'
      } catch (error) {
        console.error('Error polling analysis status:', error);
        // Continue polling even on error - might be temporary network issue
      }
    };

    // Initial poll
    poll();

    // Set up polling interval (every 3 seconds)
    pollingIntervalRef.current = setInterval(poll, 3000);
  };

  // const _checkProcessingStatus = async () => {
  //   // PDF processing status is now handled by PDFProcessingPage
  //   // CompleteProfilePage only receives completed/failed status via URL params
  //   console.log('PDF processing status is handled by PDFProcessingPage - loading candidate data');
  //   await loadCandidateData();
  //   return true; // Always return true since we only arrive here after processing
  // };

  const loadCandidateData = async (userEmail?: string) => {
    setIsLoadingCandidate(true);
    try {
      // Try to get full profile summary first
      let candidateDataFromBackend: CandidateData;
      try {
        const profileSummary = await api.getMyProfileSummary() as any;
        candidateDataFromBackend = profileSummary.candidate;
        console.log('Loaded profile summary:', profileSummary);
      } catch (summaryError) {
        console.log('Profile summary not available, trying basic profile:', summaryError);
        candidateDataFromBackend = await api.getMyProfile() as CandidateData;
      }
      
      // Map job category from backend format to frontend format
      let jobCategoryKey = "OTHER";
      if (candidateDataFromBackend.job_category) {
        // Find the key that matches the value
        const categoryEntry = Object.entries(JobCategoryMapping).find(
          ([_key, value]) => value === candidateDataFromBackend.job_category
        );
        if (categoryEntry) {
          jobCategoryKey = categoryEntry[0];
        }
      }
      
      setFormData({
        name: candidateDataFromBackend.name || "",
        dateOfBirth: candidateDataFromBackend.date_of_birth || "1990-01-01",
        city: candidateDataFromBackend.city || "",
        country: candidateDataFromBackend.country || "",
        phone: candidateDataFromBackend.phone || "",
        email: userEmail || candidateDataFromBackend.email || "",
        linkedinUrl: candidateDataFromBackend.linkedin_url || "",
        jobCategory: jobCategoryKey,
        languages: convertLanguagesFromBackend(candidateDataFromBackend.languages),
        skills: candidateDataFromBackend.skills || [],
        expectedAnnualSalary: candidateDataFromBackend.expected_annual_salary?.toString() || "",
        currentAnnualSalary: candidateDataFromBackend.current_annual_salary?.toString() || "",
        relocation: candidateDataFromBackend.relocation || false,
        workModality: candidateDataFromBackend.work_modality || [],
        currentRoles: candidateDataFromBackend.current_roles ? convertRolesFromBackend(candidateDataFromBackend.current_roles) : [],
        expectedRoles: candidateDataFromBackend.expected_roles ? convertRolesFromBackend(candidateDataFromBackend.expected_roles) : [],
      });
    } catch (error) {
      console.error('Error loading candidate data:', error);
      // Si hay error, usar datos por defecto
      setFormData({
        name: "",
        dateOfBirth: "1990-01-01",
        city: "",
        country: "",
        phone: "",
        email: userEmail || "",
        linkedinUrl: "",
        jobCategory: "OTHER",
        languages: [],
        skills: [],
        expectedAnnualSalary: "",
        currentAnnualSalary: "",
        relocation: false,
        workModality: [],
        currentRoles: [],
        expectedRoles: [],
      });
    } finally {
      setIsLoadingCandidate(false);
    }
  };

  useEffect(() => {
    // Handle success message from navigation state
    if (location.state?.showSuccessMessage && location.state?.successMessage) {
      setSuccessMessage(location.state.successMessage);
      setShowSuccessMessage(true);

      // Clear the state to prevent showing the message again on refresh
      window.history.replaceState({}, document.title);
    }

    // Check for analysisJobId in query parameters and start polling
    const jobId = searchParams.get('analysisJobId');
    if (jobId && !isPollingAnalysis && !analysisCompleted) {
      console.log('🎯 Found analysisJobId in query params:', jobId);
      setAnalysisJobId(jobId);
      startPollingAnalysis(jobId);
    }

    const loadUserData = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) return;

      // Obtener email desde el estado del hook primero, luego desde el JWT token
      console.log('🔍 CompleteProfile - candidateData:', _candidateDataFromHook);
      let userEmail = _candidateDataFromHook?.email || "";
      console.log('📧 Email from candidateData:', userEmail);

      if (!userEmail) {
        // Fallback: intentar extraer del JWT token
        userEmail = getUserEmailFromToken(token);
        console.log('📧 Email from JWT token:', userEmail);
        if (!userEmail) {
          console.warn('Could not extract email from token or onboarding state');
          localStorage.removeItem("access_token");
          return;
        }
      }

      const processedParam = searchParams.get('processed');
      const errorParam = searchParams.get('error');

      // Check if we're coming from PDF processing
      if (processedParam === 'true' || errorParam) {
        // We're coming from PDF processing - load the processed data
        console.log('Coming from PDF processing, processed:', processedParam, 'error:', errorParam);

        // Set processing status based on parameters
        if (errorParam) {
          switch (errorParam) {
            case 'timeout':
              setProcessingStatus('timeout');
              break;
            case 'processing_failed':
              setProcessingStatus('failed');
              break;
            case 'status_check_failed':
              setProcessingStatus('error');
              break;
            case 'manual_skip':
              setProcessingStatus('skipped');
              break;
            default:
              setProcessingStatus('completed');
          }
        } else {
          setProcessingStatus('completed');
        }

        // Load candidate data after PDF processing
        await loadCandidateData(userEmail);
      } else {
        // En modo normal, pre-llenar con datos del estado del hook (incluyendo email)
        const newFormData = {
          name: _candidateDataFromHook?.name || "",
          dateOfBirth: _candidateDataFromHook?.dateOfBirth || "1990-01-01",
          city: _candidateDataFromHook?.city || "",
          country: _candidateDataFromHook?.country || "",
          phone: _candidateDataFromHook?.phone || "",
          email: userEmail,
          linkedinUrl: _candidateDataFromHook?.linkedinUrl || "",
          jobCategory: _candidateDataFromHook?.jobCategory || "OTHER",
          languages: _candidateDataFromHook?.languages ? convertLanguagesFromBackend(_candidateDataFromHook.languages) : [],
          skills: _candidateDataFromHook?.skills || [],
          expectedAnnualSalary: _candidateDataFromHook?.expectedAnnualSalary?.toString() || "",
          currentAnnualSalary: _candidateDataFromHook?.currentAnnualSalary?.toString() || "",
          relocation: _candidateDataFromHook?.relocation || false,
          workModality: _candidateDataFromHook?.workModality || [],
          currentRoles: [],
          expectedRoles: [],
        };
        console.log('🎯 Setting form data:', newFormData);
        setFormData(newFormData);
      }
    };

    loadUserData();
  }, [searchParams, _candidateDataFromHook?.email, _candidateDataFromHook?.name, isPollingAnalysis, analysisCompleted]);

  // Cleanup intervals when component unmounts
  useEffect(() => {
    return () => {
      clearIntervals();
      toast.dismiss('pdf-analysis-toast');
    };
  }, []);

  // Separate useEffect to update form data when candidateDataFromHook changes
  useEffect(() => {
    if (_candidateDataFromHook?.email) {
      console.log('✅ Pre-filling form with email:', _candidateDataFromHook.email);
      setFormData(prev => ({
        ...prev,
        email: _candidateDataFromHook.email || prev.email,
        name: _candidateDataFromHook.name || prev.name,
        city: _candidateDataFromHook.city || prev.city,
        country: _candidateDataFromHook.country || prev.country,
        phone: _candidateDataFromHook.phone || prev.phone,
        linkedinUrl: _candidateDataFromHook.linkedinUrl || prev.linkedinUrl,
        jobCategory: _candidateDataFromHook.jobCategory || prev.jobCategory || "OTHER",
        dateOfBirth: _candidateDataFromHook.dateOfBirth || prev.dateOfBirth || "1990-01-01",
        languages: _candidateDataFromHook.languages ?
          Object.entries(_candidateDataFromHook.languages)
            .filter(([_key, value]) => value !== 'none')
            .map(([key, value]) => ({ language: key, level: value })) : prev.languages,
        skills: _candidateDataFromHook.skills || prev.skills,
        expectedAnnualSalary: _candidateDataFromHook.expectedAnnualSalary?.toString() || prev.expectedAnnualSalary,
        currentAnnualSalary: _candidateDataFromHook.currentAnnualSalary?.toString() || prev.currentAnnualSalary,
        relocation: _candidateDataFromHook.relocation !== undefined ? _candidateDataFromHook.relocation : prev.relocation,
        workModality: _candidateDataFromHook.workModality || prev.workModality,
        currentRoles: prev.currentRoles, // Keep existing roles
        expectedRoles: prev.expectedRoles, // Keep existing roles
      }));
    }
  }, [_candidateDataFromHook?.email, _candidateDataFromHook?.name, _candidateDataFromHook?.city, _candidateDataFromHook?.country, _candidateDataFromHook?.phone, _candidateDataFromHook?.jobCategory, _candidateDataFromHook?.dateOfBirth]);

  const handleSubmit = async (e?: React.FormEvent) => {
    if (e) {
      e.preventDefault();
    }

    // Check if analysis is in progress and user hasn't tried to continue yet
    if (isPollingAnalysis && !analysisCompleted && !userTriedToContinue) {
      console.log('⚠️ Analysis in progress - starting countdown');
      startCountdownForEarlyContinue();
      return; // Don't proceed with form submission
    }

    // If countdown is active, don't allow submission
    if (countdownActive) {
      console.log('⏰ Countdown active - blocking submission');
      return;
    }

    // Normal form submission logic
    setError("");
    setIsLoading(true);

    const token = localStorage.getItem("access_token");
    if (!token) {
      setError("No autorizado. Por favor, inicia sesión.");
      setIsLoading(false);
      navigate("/auth/login");
      return;
    }

    try {
      const profileData = {
        name: formData.name,
        date_of_birth: formData.dateOfBirth,
        city: formData.city,
        country: formData.country,
        phone: formData.phone,
        email: formData.email,
        linkedin_url: formData.linkedinUrl,
        job_category: JobCategoryMapping[formData.jobCategory] || formData.jobCategory,
        languages: convertLanguagesToBackend(formData.languages),
        skills: formData.skills,
        expected_annual_salary: formData.expectedAnnualSalary ? parseInt(formData.expectedAnnualSalary) : null,
        current_annual_salary: formData.currentAnnualSalary ? parseInt(formData.currentAnnualSalary) : null,
        relocation: formData.relocation,
        work_modality: formData.workModality,
        current_roles: convertRolesToBackend(formData.currentRoles),
        expected_roles: convertRolesToBackend(formData.expectedRoles),
      };

      let responseData;

      if (isReviewMode) {
        // En modo revisión, actualizar el candidato existente
        responseData = await api.updateMyProfile(profileData) as { id: string };
        console.log('Profile updated successfully:', responseData);
      } else {
        // En modo normal, actualizar el candidato que ya fue creado en el landing
        // El candidato ya existe desde el paso anterior, simplemente lo actualizamos
        responseData = await api.updateMyProfile(profileData) as { id: string };
        console.log('Candidate profile updated successfully:', responseData);
      }

      // Backend already updated above - no need for second API call
      // Local state will be refreshed when navigating to next step

      // Navigate to next step
      if (isReviewMode) {
        // If in review mode, go to dashboard
        navigate('/candidate/profile', {
          state: {
            showSuccessMessage: true,
            successMessage: 'Perfil actualizado correctamente. ¡Bienvenido a tu dashboard!'
          }
        });
      } else {
        // Normal onboarding flow - use centralized navigation
        nextStep();
      }
    } catch (error) {
      console.error(isReviewMode ? 'Error updating profile:' : 'Error creating candidate:', error);
      
      // Extraer el mensaje de error específico
      let errorMessage = "Error de conexión. Inténtalo de nuevo.";
      
      if (error instanceof Error) {
        // En modo revisión, no debería haber errores de email duplicado
        if (!isReviewMode && error.message.includes("email") && (error.message.includes("already exists") || error.message.includes("ya está registrado"))) {
          errorMessage = "Este email ya está registrado. ¿Ya tienes una cuenta? Puedes iniciar sesión.";
        } else if (error.message.includes("API Error:")) {
          // Remover el prefijo "API Error: " si existe
          errorMessage = error.message.replace(/^API Error: \d+ [^:]*: ?/, "");
        } else if (error.message && error.message !== "Failed to fetch") {
          errorMessage = error.message;
        }
      }
      
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  // Calculate next button text with countdown (only show when user tried to continue early)
  const getNextButtonText = () => {
    if (userTriedToContinue && countdownActive && countdown > 0) {
      return `Siguiente (${countdown}s)`;
    }
    return "Siguiente";
  };


  return (
    <>
      {/* Success Message */}
      <SuccessMessage
        message={successMessage}
        isVisible={showSuccessMessage}
        onClose={() => setShowSuccessMessage(false)}
        autoHideDelay={5000}
      />

      <OnboardingLayout
        title={processingStatus === 'completed' ? 'Revisa y Confirma tus Datos' : 'Completa tu Perfil de Candidato'}
        subtitle={processingStatus === 'completed'
          ? 'Hemos extraído esta información de tu CV. Revísala y corrígela si es necesario.'
          : 'Necesitamos algunos datos más para empezar.'
        }
        nextButtonDisabled={isLoading || !formData.name || !formData.email || !formData.dateOfBirth || countdownActive}
        nextButtonText={getNextButtonText()}
        onNext={handleSubmit}
      >
      <div>
          {processingStatus === 'completed' && !isLoadingCandidate && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-blue-800">
                    <strong>¡PDF procesado exitosamente!</strong> Hemos extraído automáticamente tu información.
                    Revisa que todo esté correcto antes de continuar.
                  </p>
                </div>
              </div>
            </div>
          )}

          {(processingStatus === 'processing' || processingStatus === 'pending' || isLoadingCandidate) && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="animate-spin h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-yellow-800">
                    <strong>Analizando PDF...</strong> Estamos extrayendo tu información automáticamente. 
                    Esto puede tomar unos segundos.
                  </p>
                </div>
              </div>
            </div>
          )}

          {processingStatus === 'failed' && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-red-800">
                    <strong>Error al procesar PDF.</strong> No pudimos extraer la información automáticamente.
                    Por favor, completa los datos manualmente.
                  </p>
                </div>
              </div>
            </div>
          )}

          {processingStatus === 'timeout' && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-yellow-800">
                    <strong>Procesamiento demorado.</strong> El análisis de tu PDF está tomando más tiempo del esperado.
                    Por favor, completa los datos manualmente mientras procesamos en segundo plano.
                  </p>
                </div>
              </div>
            </div>
          )}

          {(processingStatus === 'error' || processingStatus === 'skipped') && (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-gray-700">
                    <strong>Completar manualmente.</strong> Por favor, ingresa tu información en el formulario a continuación.
                  </p>
                </div>
              </div>
            </div>
          )}

          
          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 md:col-span-2">
                <div className="flex items-start">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3 flex-1">
                    <p className="text-sm text-red-800">{error}</p>
                    {error.includes("email ya está registrado") && (
                      <div className="mt-2">
                        <button
                          type="button"
                          onClick={() => navigate("/auth/login")}
                          className="text-sm text-red-600 hover:text-red-500 underline font-medium"
                        >
                          Ir al inicio de sesión
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Grid de dos columnas para desktop, una columna para móvil */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">Nombre Completo</label>
                <input
                  name="name"
                  id="name"
                  type="text"
                  required
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label htmlFor="dateOfBirth" className="block text-sm font-medium text-gray-700 mb-2">Fecha de Nacimiento</label>
                <input
                  name="dateOfBirth"
                  id="dateOfBirth"
                  type="date"
                  required
                  value={formData.dateOfBirth}
                  onChange={handleChange}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label htmlFor="city" className="block text-sm font-medium text-gray-700 mb-2">Ciudad</label>
                <input
                  name="city"
                  id="city"
                  type="text"
                  required
                  value={formData.city}
                  onChange={handleChange}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label htmlFor="country" className="block text-sm font-medium text-gray-700 mb-2">País</label>
                <input
                  name="country"
                  id="country"
                  type="text"
                  required
                  value={formData.country}
                  onChange={handleChange}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">Teléfono</label>
                <input
                  name="phone"
                  id="phone"
                  type="tel"
                  required
                  value={formData.phone}
                  onChange={handleChange}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label htmlFor="jobCategory" className="block text-sm font-medium text-gray-700 mb-2">Categoría Profesional</label>
                <select
                  name="jobCategory"
                  id="jobCategory"
                  required
                  value={formData.jobCategory}
                  onChange={handleChange}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Selecciona una categoría</option>
                  {Object.entries(JobCategory).map(([key, value]) => (
                    <option key={key} value={key}>{value}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Email y LinkedIn en dos columnas */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input
                  name="email"
                  id="email"
                  type="email"
                  required
                  value={formData.email}
                  readOnly
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-600 cursor-not-allowed"
                />
                <p className="text-xs text-gray-500 mt-1">El email no se puede cambiar</p>
              </div>

              <div>
                <label htmlFor="linkedinUrl" className="block text-sm font-medium text-gray-700 mb-2">LinkedIn</label>
                <input
                  name="linkedinUrl"
                  id="linkedinUrl"
                  type="url"
                  value={formData.linkedinUrl}
                  onChange={handleChange}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="linkedin.com/in/tu-perfil"
                />
              </div>
            </div>

            {/* Campos adicionales - Grid de dos columnas */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="expectedAnnualSalary" className="block text-sm font-medium text-gray-700 mb-2">Salario Esperado (€)</label>
                <input
                  name="expectedAnnualSalary"
                  id="expectedAnnualSalary"
                  type="number"
                  value={formData.expectedAnnualSalary}
                  onChange={handleChange}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="ej. 45000"
                />
              </div>

              <div>
                <label htmlFor="currentAnnualSalary" className="block text-sm font-medium text-gray-700 mb-2">Salario Actual (€)</label>
                <input
                  name="currentAnnualSalary"
                  id="currentAnnualSalary"
                  type="number"
                  value={formData.currentAnnualSalary}
                  onChange={handleChange}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="ej. 40000"
                />
              </div>
            </div>

            {/* Modalidad de trabajo */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Modalidad de Trabajo Preferida</label>
              <div className="space-y-2">
                {Object.entries(WorkModalityLabels).map(([key, label]) => (
                  <label key={key} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.workModality.includes(key)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setFormData(prev => ({ ...prev, workModality: [...prev.workModality, key] }));
                        } else {
                          setFormData(prev => ({ ...prev, workModality: prev.workModality.filter(m => m !== key) }));
                        }
                      }}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <span className="ml-2 text-sm text-gray-900">{label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Disponibilidad para reubicación */}
            <div>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={formData.relocation}
                  onChange={(e) => setFormData(prev => ({ ...prev, relocation: e.target.checked }))}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="ml-2 text-sm text-gray-900">Disponible para reubicación</span>
              </label>
            </div>

            {/* Idiomas */}
            <LanguageSelector
              languages={formData.languages}
              onChange={(languages) => setFormData(prev => ({ ...prev, languages }))}
            />

            {/* Habilidades */}
            <div>
              <label htmlFor="skills" className="block text-sm font-medium text-gray-700 mb-2">Habilidades</label>
              <textarea
                name="skills"
                id="skills"
                rows={3}
                value={formData.skills.join(', ')}
                onChange={(e) => {
                  const skillsArray = e.target.value.split(',').map(skill => skill.trim()).filter(skill => skill);
                  setFormData(prev => ({ ...prev, skills: skillsArray }));
                }}
                className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="ej. JavaScript, Python, React, Node.js, SQL (separadas por comas)"
              />
              <p className="text-xs text-gray-500 mt-1">Separa las habilidades con comas</p>
            </div>

            {/* Roles - Grid de dos columnas */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Roles Actuales */}
              <RoleSelector
                roles={formData.currentRoles}
                onChange={(roles) => setFormData(prev => ({ ...prev, currentRoles: roles }))}
                title="Roles Actuales"
                placeholder="Selecciona tu rol actual"
              />

              {/* Roles Deseados */}
              <RoleSelector
                roles={formData.expectedRoles}
                onChange={(roles) => setFormData(prev => ({ ...prev, expectedRoles: roles }))}
                title="Roles Deseados"
                placeholder="Selecciona roles que te interesan"
              />
            </div>

            {/* Remove the submit button since OnboardingLayout handles navigation */}
          </form>
        </div>
      </OnboardingLayout>
    </>
  );
}