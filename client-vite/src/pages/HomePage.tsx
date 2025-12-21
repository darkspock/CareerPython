import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { api } from '../lib/api';
import { getUserEmailFromToken, clearAuthData } from '../utils/jwt';

interface UserInfo {
  email: string;
  name?: string;
}

interface CompletionStatus {
  basicInfo: boolean;
  experience: boolean;
  education: boolean;
  projects: boolean;
}

interface CandidateProfile {
  id: string;
  name: string;
  email: string;
  [key: string]: any; // Allow other fields
}

interface ExperienceItem {
  id: string;
  company: string;
  job_title: string;
  [key: string]: any;
}

interface EducationItem {
  id: string;
  institution: string;
  degree: string;
  [key: string]: any;
}

interface ProjectItem {
  id: string;
  name: string;
  description: string;
  [key: string]: any;
}

export default function HomePage() {
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [completionStatus, setCompletionStatus] = useState<CompletionStatus>({
    basicInfo: false,
    experience: false,
    education: false,
    projects: false,
  });
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        // No hay token, redirigir al login
        navigate("/candidate/auth/login");
        return;
      }

      const userEmail = getUserEmailFromToken(token);
      if (!userEmail) {
        console.warn('Could not extract email from token, token may be invalid');
        clearAuthData();
        navigate("/candidate/auth/login");
        return;
      }

      setUserInfo({
        email: userEmail,
        name: "Usuario"
      });

      // Always load completion status from backend
      await loadCompletionStatus();

      setIsLoading(false);
    };

    checkAuth();
  }, [navigate]);

  const loadCompletionStatus = async () => {
    try {
      // Cargar datos en paralelo con tipos apropiados
      const [experiences, educations, projects, profile] = await Promise.all([
        api.getExperiences().catch(() => [] as ExperienceItem[]),
        api.getEducations().catch(() => [] as EducationItem[]),
        api.getProjects().catch(() => [] as ProjectItem[]),
        api.getMyProfile().catch(() => null as CandidateProfile | null),
      ]);

      // Debug: log the profile data to see what fields are available
      console.log('Profile data:', profile);
      console.log('Experiences:', experiences);
      console.log('Educations:', educations);
      console.log('Projects:', projects);

      setCompletionStatus({
        // Check for basic profile info using correct field names from CandidateResponse
        basicInfo: profile && typeof profile === 'object' && 'name' in profile && 'email' in profile && profile.name && profile.email ? true : false,
        experience: Array.isArray(experiences) && experiences.length > 0,
        education: Array.isArray(educations) && educations.length > 0,
        projects: Array.isArray(projects) && projects.length > 0,
      });
    } catch (error) {
      console.error('Error loading completion status:', error);
      // En caso de error, mantener el estado inicial
    }
  };

  const handleLogout = () => {
    clearAuthData();
    navigate("/candidate/auth/login");
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">AI Resume Platform</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                Bienvenido, {userInfo?.email}
              </span>
              <button
                onClick={handleLogout}
                className="text-sm text-red-600 hover:text-red-800 font-medium"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Dashboard</h2>
          <p className="text-gray-600">Gestiona tu perfil profesional y aplicaciones</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Mi Perfil */}
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center mb-4">
              <div className="bg-blue-100 p-3 rounded-lg">
                <svg className="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Mi Perfil</h3>
                <p className="text-sm text-gray-600">Gestiona tu información personal</p>
              </div>
            </div>
            {/* Estado del perfil */}
            <div className="border-t pt-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Link
                    to="/candidate/onboarding/complete-profile"
                    className="block text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    Editar Perfil Básico
                  </Link>
                  <span className={`text-sm font-medium ${completionStatus.basicInfo
                    ? 'text-green-600'
                    : 'text-yellow-600'
                    }`}>
                    {completionStatus.basicInfo ? '✓ Completo' : 'Pendiente'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <Link
                    to="/candidate/profile/experience"
                    className="block text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    Experiencia Laboral
                  </Link>
                  <span className={`text-sm font-medium ${completionStatus.experience
                    ? 'text-green-600'
                    : 'text-yellow-600'
                    }`}>
                    {completionStatus.experience ? '✓ Completo' : 'Pendiente'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <Link
                    to="/candidate/profile/education"
                    className="block text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    Educación
                  </Link>
                  <span className={`text-sm font-medium ${completionStatus.education
                    ? 'text-green-600'
                    : 'text-yellow-600'
                    }`}>
                    {completionStatus.education ? '✓ Completo' : 'Pendiente'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <Link
                    to="/candidate/profile/projects"
                    className="block text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    Proyectos
                  </Link>
                  <span className={`text-sm font-medium ${completionStatus.projects
                    ? 'text-green-600'
                    : 'text-gray-400'
                    }`}>
                    {completionStatus.projects ? '✓ Completo' : 'Opcional'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Candidaturas */}
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center mb-4">
              <div className="bg-green-100 p-3 rounded-lg">
                <svg className="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0H8m8 0v2a2 2 0 01-2 2H10a2 2 0 01-2-2V6m8 0H8" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Candidaturas</h3>
                <p className="text-sm text-gray-600">Gestiona tus aplicaciones a ofertas de trabajo</p>
              </div>
            </div>
            <div className="space-y-2">
              <Link
                to="/job-applications"
                className="block text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                Ver Mis Candidaturas
              </Link>
              <Link
                to="/job-positions"
                className="block text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                Buscar Ofertas de Trabajo
              </Link>
            </div>
          </div>

          {/* Mi CV */}
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center mb-4">
              <div className="bg-purple-100 p-3 rounded-lg">
                <svg className="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Mi CV</h3>
                <p className="text-sm text-gray-600">Descarga y gestiona tus documentos</p>
              </div>
            </div>

            <div className="space-y-3">
              {/* Descargar CV */}
              <button className="w-full flex items-center justify-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors">
                <svg className="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Descargar CV (PDF)
              </button>

              {/* Descargar Carta de Presentación */}
              <button className="w-full flex items-center justify-center px-4 py-2 border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors">
                <svg className="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
                Carta de Presentación
              </button>

              {/* Vista previa */}
              <Link
                to="/resume-preview"
                className="block text-center text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                Vista Previa del CV
              </Link>

              {/* Configurar plantillas */}
              <Link
                to="/resume-templates"
                className="block text-center text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                Cambiar Plantilla
              </Link>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}