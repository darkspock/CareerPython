import { useState, useEffect } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { CheckCircle, XCircle, Loader2, AlertTriangle } from "lucide-react";
import { api } from "../lib/api";
import { clearAuthData } from "../utils/jwt";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";

type VerificationStatus = "loading" | "success" | "error" | "expired";

interface VerificationResult {
  success: boolean;
  message: string;
  user_id: string | null;
  candidate_id: string | null;
  is_new_user: boolean;
  has_job_application: boolean;
  job_position_id: string | null;
  access_token: string | null;
  redirect_url: string;
  wants_cv_help: boolean;
  has_pdf: boolean;
}

export default function VerifyRegistrationPage() {
  const { token } = useParams<{ token: string }>();
  const navigate = useNavigate();
  const [status, setStatus] = useState<VerificationStatus>("loading");
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setErrorMessage("Token de verificación no encontrado");
      return;
    }

    // Clear any existing session data before verification
    // This ensures the verification link works regardless of who was logged in
    clearAuthData();

    const verifyRegistration = async () => {
      try {
        const data = await api.verifyRegistration(token);

        if (data.success) {
          setResult(data);
          setStatus("success");

          // Store access token if provided
          if (data.access_token) {
            localStorage.setItem("access_token", data.access_token);
          }

          // Store candidate_id for later use
          if (data.candidate_id) {
            localStorage.setItem("candidate_id", data.candidate_id);
          }

          // Store job_position_id for wizard to check questions
          if (data.job_position_id) {
            localStorage.setItem("job_position_id", data.job_position_id);
          }

          // Store wants_cv_help flag for wizard
          localStorage.setItem("wants_cv_help", data.wants_cv_help ? 'true' : 'false');

          // Store has_pdf flag for wizard to determine which sections to show
          localStorage.setItem("has_pdf", data.has_pdf ? 'true' : 'false');

          // Auto-redirect after 3 seconds
          setTimeout(() => {
            // Redirect to application wizard if has job application, otherwise to profile
            if (data.has_job_application) {
              navigate("/candidate/application/wizard");
            } else {
              navigate("/candidate/onboarding/complete-profile");
            }
          }, 3000);
        } else {
          setStatus("error");
          setErrorMessage(data.message || "Error al verificar el registro");
        }
      } catch (error: any) {
        console.error("Verification error:", error);

        const message = error?.message || "Error al verificar el registro";

        if (message.toLowerCase().includes("expired") || message.toLowerCase().includes("expirado")) {
          setStatus("expired");
          setErrorMessage("El enlace de verificación ha expirado");
        } else {
          setStatus("error");
          setErrorMessage(message);
        }
      }
    };

    verifyRegistration();
  }, [token, navigate]);

  const handleContinue = () => {
    if (result?.has_job_application) {
      navigate("/candidate/application/wizard");
    } else {
      navigate("/candidate/onboarding/complete-profile");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          {status === "loading" && (
            <>
              <div className="mx-auto mb-4">
                <Loader2 className="h-16 w-16 text-blue-600 animate-spin" />
              </div>
              <CardTitle className="text-xl">Verificando tu email...</CardTitle>
              <CardDescription>Por favor espera un momento</CardDescription>
            </>
          )}

          {status === "success" && (
            <>
              <div className="mx-auto mb-4 h-16 w-16 bg-green-100 rounded-full flex items-center justify-center">
                <CheckCircle className="h-10 w-10 text-green-600" />
              </div>
              <CardTitle className="text-xl text-green-800">
                ¡Email verificado correctamente!
              </CardTitle>
              <CardDescription>
                {result?.is_new_user
                  ? "Tu cuenta ha sido creada. Serás redirigido automáticamente."
                  : "Tu email ha sido verificado. Serás redirigido automáticamente."}
              </CardDescription>
            </>
          )}

          {status === "expired" && (
            <>
              <div className="mx-auto mb-4 h-16 w-16 bg-yellow-100 rounded-full flex items-center justify-center">
                <AlertTriangle className="h-10 w-10 text-yellow-600" />
              </div>
              <CardTitle className="text-xl text-yellow-800">
                Enlace expirado
              </CardTitle>
              <CardDescription>{errorMessage}</CardDescription>
            </>
          )}

          {status === "error" && (
            <>
              <div className="mx-auto mb-4 h-16 w-16 bg-red-100 rounded-full flex items-center justify-center">
                <XCircle className="h-10 w-10 text-red-600" />
              </div>
              <CardTitle className="text-xl text-red-800">
                Error de verificación
              </CardTitle>
              <CardDescription>{errorMessage}</CardDescription>
            </>
          )}
        </CardHeader>

        <CardContent className="space-y-4">
          {status === "success" && (
            <>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-blue-800">
                {result?.has_job_application ? (
                  <p>
                    Tienes una candidatura pendiente. A continuación podrás
                    completar tu perfil y responder las preguntas de la aplicación.
                  </p>
                ) : (
                  <p>
                    A continuación podrás completar tu perfil profesional.
                  </p>
                )}
              </div>

              <Button onClick={handleContinue} className="w-full">
                Continuar al{" "}
                {result?.has_job_application
                  ? "asistente de aplicación"
                  : "perfil"}
              </Button>
            </>
          )}

          {status === "expired" && (
            <>
              <p className="text-sm text-gray-600 text-center">
                El enlace de verificación ha expirado. Por favor, regresa a la
                página de aplicación y envía tu candidatura nuevamente.
              </p>
              <Link to="/">
                <Button variant="outline" className="w-full">
                  Volver al inicio
                </Button>
              </Link>
            </>
          )}

          {status === "error" && (
            <>
              <p className="text-sm text-gray-600 text-center">
                Ha ocurrido un error al verificar tu email. Por favor,
                inténtalo de nuevo o contacta con soporte.
              </p>
              <div className="flex flex-col gap-2">
                <Link to="/">
                  <Button variant="outline" className="w-full">
                    Volver al inicio
                  </Button>
                </Link>
                <Link to="/candidate/auth/login">
                  <Button variant="ghost" className="w-full">
                    Ir a iniciar sesión
                  </Button>
                </Link>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
