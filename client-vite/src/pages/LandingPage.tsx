import { useState, useEffect } from "react";
import { useNavigate, Link, useSearchParams } from "react-router-dom";
import { Upload, CheckCircle, FileText, Bot, Target } from "lucide-react";
import { api } from "../lib/api";
import { useOnboarding } from "../hooks/useOnboarding";

// Generate random email for testing
const generateRandomEmail = () => {
  const names = ['juan', 'maria', 'carlos', 'ana', 'luis', 'sofia', 'diego', 'lucia', 'pedro', 'carmen'];
  const domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com'];
  const randomName = names[Math.floor(Math.random() * names.length)];
  const randomNumber = Math.floor(Math.random() * 9999);
  const randomDomain = domains[Math.floor(Math.random() * domains.length)];
  return `${randomName}${randomNumber}@${randomDomain}`;
};

export default function LandingPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState(generateRandomEmail()); // Pre-populate with random email for testing
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { updateCandidateData, jobPositionId, clearCandidateData } = useOnboarding();

  // Clear localStorage when landing page loads to start fresh onboarding flow
  useEffect(() => {
    console.log("🧹 Landing page loaded - clearing previous session data");
    console.log("🔍 Previous localStorage contents:");

    // Log existing data before clearing (for debugging)
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      const value = localStorage.getItem(key);
      console.log(`  ${key}: ${value ? value.substring(0, 50) + (value.length > 50 ? '...' : '') : 'null'}`);
    }

    // Clear all authentication and onboarding data
    const keysToRemove = ['access_token', 'candidate_id', 'refresh_token', 'user_id'];
    keysToRemove.forEach(key => {
      if (localStorage.getItem(key)) {
        console.log(`  🗑️ Removing ${key}`);
        localStorage.removeItem(key);
      }
    });

    // Clear onboarding state (no longer uses localStorage)
    console.log("  🗑️ Resetting onboarding state");
    clearCandidateData();

    console.log("✅ Session data cleared - ready for new onboarding");
  }, [clearCandidateData]);

  const isFormValid = email.trim() !== ""; // Only email is required now

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isFormValid) return;

    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('email', email);

      // Add jobPositionId if present
      if (jobPositionId) {
        formData.append('job_position_id', jobPositionId);
      }

      // Add resume file if selected
      if (selectedFile) {
        formData.append('resume_file', selectedFile);
      }

      // Call the new onboarding landing endpoint
      const data = await api.processOnboardingLanding(formData) as {
        success: boolean;
        message: string;
        user_created: boolean;
        candidate_created: boolean;
        application_created: boolean;
        access_token?: string;
        token_type?: string;
        analysis_job_id?: string;
      };

      if (data.success) {
        // Store email in onboarding state for next step
        updateCandidateData({ email });

        // Store JWT token if provided
        if (data.access_token) {
          localStorage.setItem("access_token", data.access_token);
          console.log('✅ Stored JWT token for authenticated onboarding flow');
        }

        // Always navigate to complete-profile page with analysis_job_id if available
        console.log('✅ Onboarding successful, navigating to complete-profile');

        // Build URL with query parameters
        const params = new URLSearchParams();
        if (jobPositionId) params.append('jobPositionId', jobPositionId);
        if (data.analysis_job_id) {
          params.append('analysisJobId', data.analysis_job_id);
          console.log('📄 PDF analysis job will be tracked:', data.analysis_job_id);
        }

        const nextUrl = `/candidate/onboarding/complete-profile${params.toString() ? `?${params.toString()}` : ''}`;

        navigate(nextUrl, {
          state: {
            successMessage: data.message,
            showSuccessMessage: true,
            analysisJobId: data.analysis_job_id,
            hasResumeFile: !!selectedFile
          }
        });
      }
    } catch (error: any) {
      console.error('Error:', error);
      
      let errorMessage = 'Error de conexión. Por favor intenta de nuevo.';
      
      if (error?.message) {
        errorMessage = error.message;
      }
      
      // Si el error es de email duplicado, ofrecer ir al login
      if (errorMessage.includes('ya está registrado') || errorMessage.includes('already exists')) {
        const shouldLogin = confirm(`${errorMessage}\n\n¿Quieres ir a la página de login?`);
        if (shouldLogin) {
          navigate('/candidate/auth/login');
          return;
        }
      } else {
        alert(errorMessage);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="flex items-center justify-between px-6 lg:px-10 py-5 bg-white/80 backdrop-blur-sm border-b border-gray-200">
        <div className="flex items-center gap-3 text-gray-800">
          <div className="h-8 w-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
            <Bot className="h-5 w-5 text-white" />
          </div>
          <h2 className="text-xl font-bold">Resume AI</h2>
        </div>

        <nav className="hidden md:flex items-center gap-8 text-gray-600">
          <a className="text-sm font-medium hover:text-gray-900 transition-colors" href="#inicio">Inicio</a>
          <a className="text-sm font-medium hover:text-gray-900 transition-colors" href="#como-funciona">Cómo funciona</a>
          <a className="text-sm font-medium hover:text-gray-900 transition-colors" href="#precios">Precios</a>
        </nav>

        <Link
          to="/candidate/auth/login"
          className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-2 rounded-full text-sm font-medium transition-all duration-200 transform hover:scale-105"
        >
          Iniciar Sesión
        </Link>
      </header>

      {/* Hero Section */}
      <main className="flex-1">
        <section id="inicio" className="px-6 lg:px-20 py-16 lg:py-24">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-6xl font-black text-gray-900 leading-tight mb-6">
              Mejora tu currículum con{" "}
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Inteligencia Artificial
              </span>
            </h1>

            <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-10">
              Obtén un currículum optimizado para destacar entre la multitud y conseguir el trabajo de tus sueños.
            </p>

            {/* Form */}
            <form onSubmit={handleSubmit} className="max-w-md mx-auto space-y-4">
              <div className="space-y-4">
                {jobPositionId && (
                  <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 text-center">
                    <p className="text-blue-800 text-sm font-medium">
                      🎯 Aplicando a una posición específica
                    </p>
                  </div>
                )}

                <div className="relative">
                  <input
                    type="email"
                    placeholder="tu@email.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-4 py-3 pr-12 rounded-xl border border-gray-300 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setEmail(generateRandomEmail())}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-blue-600 transition-colors"
                    title="Generar email aleatorio para pruebas"
                  >
                    🎲
                  </button>
                </div>
              </div>

              {/* File Upload */}
              <div>
                <label className={`w-full flex items-center justify-center gap-2 rounded-xl h-12 px-4 text-sm font-medium transition-all cursor-pointer ${selectedFile
                  ? "bg-green-100 text-green-700 border-2 border-green-300"
                  : "bg-white border-2 border-gray-300 text-gray-700 hover:border-blue-400 hover:bg-blue-50"
                  }`}>
                  {selectedFile ? (
                    <>
                      <CheckCircle className="w-4 h-4" />
                      <span className="truncate">PDF Seleccionado: {selectedFile.name}</span>
                    </>
                  ) : (
                    <>
                      <Upload className="w-4 h-4" />
                      <span className="truncate">Subir CV (PDF) - Opcional</span>
                    </>
                  )}
                  <input
                    type="file"
                    accept=".pdf"
                    className="hidden"
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) {
                        setSelectedFile(file);
                      }
                    }}
                  />
                </label>
              </div>

              <button
                type="submit"
                disabled={!isFormValid || isLoading}
                className={`w-full h-12 rounded-xl text-base font-bold transition-all transform ${isFormValid && !isLoading
                  ? "bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white hover:scale-105 shadow-lg"
                  : "bg-gray-300 text-gray-500 cursor-not-allowed"
                  }`}
              >
                {isLoading ? "Creando cuenta..." : "Comenzar Gratis"}
              </button>
            </form>
          </div>
        </section>
        {/* How it works Section */}
        <section id="como-funciona" className="px-6 lg:px-20 py-16 lg:py-24 bg-white">
          <div className="max-w-5xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-black text-gray-900 mb-4">
                Cómo funciona
              </h2>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Nuestro proceso es simple y efectivo, guiándote paso a paso para crear un currículum que impresione a los reclutadores.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center p-8 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl border border-blue-100">
                <div className="inline-flex items-center justify-center h-16 w-16 rounded-full bg-gradient-to-br from-blue-600 to-purple-600 text-white mb-6">
                  <FileText className="h-8 w-8" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">1. Sube tu CV</h3>
                <p className="text-gray-600">
                  Sube tu currículum actual en PDF o importa tu perfil de LinkedIn para comenzar.
                </p>
              </div>

              <div className="text-center p-8 bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl border border-purple-100">
                <div className="inline-flex items-center justify-center h-16 w-16 rounded-full bg-gradient-to-br from-purple-600 to-pink-600 text-white mb-6">
                  <Bot className="h-8 w-8" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">2. IA lo optimiza</h3>
                <p className="text-gray-600">
                  Nuestra IA analiza tu perfil y sugiere mejoras basadas en las mejores prácticas del mercado.
                </p>
              </div>

              <div className="text-center p-8 bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl border border-green-100">
                <div className="inline-flex items-center justify-center h-16 w-16 rounded-full bg-gradient-to-br from-green-600 to-emerald-600 text-white mb-6">
                  <Target className="h-8 w-8" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">3. Consigue el trabajo</h3>
                <p className="text-gray-600">
                  Descarga tu currículum optimizado y destaca en tus aplicaciones laborales.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="px-6 lg:px-20 py-16 lg:py-24 bg-gradient-to-br from-gray-50 to-blue-50">
          <div className="max-w-5xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-black text-gray-900 mb-4">
                ¿Por qué elegir Resume AI?
              </h2>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Utilizamos la última tecnología en inteligencia artificial para crear currículums que realmente funcionan.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
                <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <Bot className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">Optimización con IA</h3>
                <p className="text-gray-600">
                  Nuestros algoritmos analizan miles de currículums exitosos para optimizar el tuyo.
                </p>
              </div>

              <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
                <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                  <Target className="h-6 w-6 text-purple-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">Personalización Inteligente</h3>
                <p className="text-gray-600">
                  Adaptamos tu currículum según el tipo de trabajo y la industria que buscas.
                </p>
              </div>

              <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
                <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">Resultados Comprobados</h3>
                <p className="text-gray-600">
                  El 85% de nuestros usuarios consigue más entrevistas después de usar nuestro servicio.
                </p>
              </div>

              <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
                <div className="h-12 w-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
                  <Upload className="h-6 w-6 text-indigo-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">Fácil de Usar</h3>
                <p className="text-gray-600">
                  Solo sube tu CV actual y deja que nuestra IA haga el trabajo pesado por ti.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-12">
          <div className="flex flex-col md:flex-row justify-between items-center gap-8">
            <div className="flex items-center gap-3">
              <div className="h-7 w-7 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Bot className="h-4 w-4 text-white" />
              </div>
              <h2 className="text-lg font-bold text-white">Resume AI</h2>
            </div>

            <nav className="flex flex-wrap justify-center gap-x-6 gap-y-2">
              <a className="text-sm hover:text-white transition-colors" href="#">Política de privacidad</a>
              <a className="text-sm hover:text-white transition-colors" href="#">Términos de servicio</a>
              <a className="text-sm hover:text-white transition-colors" href="#">Contacto</a>
            </nav>

            <p className="text-sm text-gray-400">© 2024 Resume AI. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}