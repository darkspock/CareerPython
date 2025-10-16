import { useState, useEffect } from "react";
import { useNavigate, useSearchParams, useLocation } from "react-router-dom";
import { FileText, CheckCircle, AlertCircle, Clock } from "lucide-react";
import { api } from "../lib/api";

interface ProcessingStatusResponse {
  status: string;
  message: string;
  error?: string;
  asset_id?: string;
}

export default function PDFProcessingPage() {
  const [processingStatus, setProcessingStatus] = useState<string>("processing");
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [hasTimedOut, setHasTimedOut] = useState(false);
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const location = useLocation();

  // Get job_id from URL parameters
  const jobId = searchParams.get('jobId');
  const jobPositionId = location.state?.jobPositionId;

  // If no job_id provided, redirect to complete-profile
  useEffect(() => {
    if (!jobId) {
      console.error('No job ID provided, redirecting to complete-profile');
      const nextUrl = jobPositionId
        ? `/candidate/onboarding/complete-profile?jobPositionId=${jobPositionId}`
        : '/candidate/onboarding/complete-profile';
      navigate(nextUrl);
      return;
    }
  }, [jobId, jobPositionId, navigate]);

  const checkProcessingStatus = async () => {
    if (!jobId) return false;

    try {
      const statusData = await api.getAnalysisStatus(jobId) as ProcessingStatusResponse;
      setProcessingStatus(statusData.status);
      
      // Log detailed status for debugging
      console.log('Processing status:', statusData);
      
      if (statusData.status === 'completed') {
        // PDF procesado exitosamente por XAI
        console.log('XAI processing completed successfully');
        setTimeout(() => {
          const nextUrl = jobPositionId
            ? `/candidate/onboarding/complete-profile?processed=true&jobPositionId=${jobPositionId}`
            : '/candidate/onboarding/complete-profile?processed=true';
          navigate(nextUrl);
        }, 1500); // Pequeña pausa para mostrar el éxito
        return true;
      } else if (statusData.status === 'failed') {
        // Error en el procesamiento XAI
        console.log('XAI processing failed:', statusData.error);
        setTimeout(() => {
          const nextUrl = jobPositionId
            ? `/candidate/onboarding/complete-profile?error=processing_failed&jobPositionId=${jobPositionId}`
            : '/candidate/onboarding/complete-profile?error=processing_failed';
          navigate(nextUrl);
        }, 2000);
        return true;
      } else if (statusData.status === 'timeout') {
        // Timeout del procesamiento XAI
        console.log('XAI processing timed out');
        setTimeout(() => {
          const nextUrl = jobPositionId
            ? `/candidate/onboarding/complete-profile?error=timeout&jobPositionId=${jobPositionId}`
            : '/candidate/onboarding/complete-profile?error=timeout';
          navigate(nextUrl);
        }, 2000);
        return true;
      } else if (statusData.status === 'processing') {
        // XAI está procesando activamente
        console.log('XAI is actively processing PDF');
        return false;
      } else if (statusData.status === 'pending') {
        // En cola para procesamiento
        console.log('PDF pending XAI processing');
        return false;
      }
      
      return false; // Continuar esperando
    } catch (error) {
      console.error('Error checking processing status:', error);
      // En caso de error de API, continuar al siguiente paso
      setTimeout(() => {
        const nextUrl = jobPositionId
          ? `/candidate/onboarding/complete-profile?error=status_check_failed&jobPositionId=${jobPositionId}`
          : '/candidate/onboarding/complete-profile?error=status_check_failed';
        navigate(nextUrl);
      }, 1000);
      return true;
    }
  };

  useEffect(() => {
    let pollInterval: NodeJS.Timeout;
    let timeoutTimer: NodeJS.Timeout;
    let timeCounter: NodeJS.Timeout;

    const startProcessing = async () => {
      // Verificar estado inicial
      const isCompleted = await checkProcessingStatus();
      
      if (!isCompleted) {
        // Iniciar polling cada 2 segundos
        pollInterval = setInterval(async () => {
          const completed = await checkProcessingStatus();
          if (completed) {
            clearInterval(pollInterval);
            clearTimeout(timeoutTimer);
            clearInterval(timeCounter);
          }
        }, 2000);

        // Contador de tiempo
        timeCounter = setInterval(() => {
          setTimeElapsed(prev => prev + 1);
        }, 1000);

        // Timeout de 60 segundos para dar más tiempo a XAI
        timeoutTimer = setTimeout(() => {
          setHasTimedOut(true);
          clearInterval(pollInterval);
          clearInterval(timeCounter);

          // Continuar al siguiente paso con indicación de timeout
          setTimeout(() => {
            const nextUrl = jobPositionId
              ? `/candidate/onboarding/complete-profile?error=timeout&jobPositionId=${jobPositionId}`
              : '/candidate/onboarding/complete-profile?error=timeout';
            navigate(nextUrl);
          }, 3000);
        }, 60000);
      }
    };

    startProcessing();

    // Cleanup
    return () => {
      if (pollInterval) clearInterval(pollInterval);
      if (timeoutTimer) clearTimeout(timeoutTimer);
      if (timeCounter) clearInterval(timeCounter);
    };
  }, [navigate]);

  const getStatusIcon = () => {
    if (hasTimedOut) {
      return <AlertCircle className="h-16 w-16 text-yellow-500" />;
    }
    
    switch (processingStatus) {
      case 'completed':
        return <CheckCircle className="h-16 w-16 text-green-500" />;
      case 'failed':
        return <AlertCircle className="h-16 w-16 text-red-500" />;
      default:
        return (
          <div className="relative">
            <FileText className="h-16 w-16 text-blue-500" />
            <div className="absolute -top-1 -right-1">
              <div className="animate-spin rounded-full h-6 w-6 border-2 border-blue-500 border-t-transparent"></div>
            </div>
          </div>
        );
    }
  };

  const getStatusMessage = () => {
    if (hasTimedOut) {
      return {
        title: "Procesamiento Demorado",
        description: "El análisis con IA está tomando más tiempo del esperado. Continuaremos al siguiente paso donde podrás completar tu información manualmente mientras procesamos en segundo plano.",
        color: "text-yellow-700"
      };
    }

    switch (processingStatus) {
      case 'completed':
        return {
          title: "¡IA Completó el Análisis!",
          description: "Nuestra Inteligencia Artificial ha extraído exitosamente tu información del PDF. Te redirigiremos para que puedas revisar los datos extraídos.",
          color: "text-green-700"
        };
      case 'failed':
        return {
          title: "Error en el Análisis con IA",
          description: "Nuestra IA no pudo extraer la información del PDF automáticamente. Te redirigiremos para que puedas completar los datos manualmente.",
          color: "text-red-700"
        };
      case 'timeout':
        return {
          title: "Análisis IA Demorado",
          description: "El procesamiento con IA está tomando más tiempo del esperado. Continuaremos en segundo plano mientras completas manualmente.",
          color: "text-yellow-700"
        };
      case 'processing':
        return {
          title: "IA Analizando tu CV...",
          description: "Nuestra Inteligencia Artificial está analizando tu PDF y extrayendo información estructurada. Este proceso puede tomar hasta 60 segundos.",
          color: "text-blue-700"
        };
      case 'pending':
        return {
          title: "Preparando Análisis IA...",
          description: "Tu PDF está en cola para ser procesado por nuestra Inteligencia Artificial. Iniciando análisis...",
          color: "text-blue-700"
        };
      default:
        return {
          title: "Procesando tu CV...",
          description: "Estamos preparando el análisis de tu PDF con Inteligencia Artificial. Esto puede tomar unos segundos.",
          color: "text-blue-700"
        };
    }
  };

  const statusMessage = getStatusMessage();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 text-center">
          {/* Icono de estado */}
          <div className="flex justify-center mb-6">
            {getStatusIcon()}
          </div>

          {/* Título y descripción */}
          <h2 className={`text-2xl font-bold mb-4 ${statusMessage.color}`}>
            {statusMessage.title}
          </h2>
          
          <p className="text-gray-600 mb-6 leading-relaxed">
            {statusMessage.description}
          </p>

          {/* Indicador de tiempo si está procesando */}
          {processingStatus === 'processing' && !hasTimedOut && (
            <div className="bg-blue-50 rounded-lg p-4 mb-6">
              <div className="flex items-center justify-center gap-2 text-blue-700">
                <Clock className="h-4 w-4" />
                <span className="text-sm font-medium">
                  Tiempo transcurrido: {timeElapsed}s
                </span>
              </div>
              <div className="mt-2">
                <div className="w-full bg-blue-200 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full transition-all duration-1000"
                    style={{ width: `${Math.min((timeElapsed / 60) * 100, 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          )}

          {/* Mensaje de timeout */}
          {hasTimedOut && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
              <p className="text-sm text-yellow-800">
                <strong>Continuando automáticamente...</strong> Te redirigiremos en unos segundos para que puedas completar tu información.
              </p>
            </div>
          )}

          {/* Botón de continuar manualmente (solo si ha pasado más de 30 segundos) */}
          {processingStatus === 'processing' && timeElapsed > 30 && !hasTimedOut && (
            <button
              onClick={() => {
                const nextUrl = jobPositionId
                  ? `/candidate/onboarding/complete-profile?error=manual_skip&jobPositionId=${jobPositionId}`
                  : '/candidate/onboarding/complete-profile?error=manual_skip';
                navigate(nextUrl);
              }}
              className="w-full py-3 px-4 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-lg transition duration-200"
            >
              Continuar Manualmente
            </button>
          )}

          {/* Indicador de redirección */}
          {(processingStatus === 'completed' || processingStatus === 'failed' || hasTimedOut) && (
            <div className="flex items-center justify-center gap-2 text-gray-500">
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-gray-400 border-t-transparent"></div>
              <span className="text-sm">Redirigiendo...</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}