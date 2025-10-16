import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Send, Calendar, User, Plus, Edit } from 'lucide-react';
import { CandidateProfileLayout } from '../components/candidate-profile';
import StatCard from '../components/candidate-profile/StatCard';
import QuickActionCard from '../components/candidate-profile/QuickActionCard';
import RecentActivitySection from '../components/candidate-profile/RecentActivitySection';
import { api } from '../lib/api';

interface DashboardStats {
  resumesCount: number;
  applicationsCount: number;
  interviewsCount: number;
  profileCompleteness: number;
}

const CandidateProfilePage: React.FC = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<DashboardStats>({
    resumesCount: 0,
    applicationsCount: 0,
    interviewsCount: 0,
    profileCompleteness: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);

      // Load resumes count
      try {
        const resumes = await api.getResumes();
        setStats(prev => ({ ...prev, resumesCount: resumes.length }));
      } catch (error) {
        console.log('Could not load resumes:', error);
      }

      // Calculate profile completeness
      try {
        const profile = await api.getMyProfile();
        const completeness = calculateProfileCompleteness(profile);
        setStats(prev => ({ ...prev, profileCompleteness: completeness }));
      } catch (error) {
        console.log('Could not load profile:', error);
      }

      // Mock data for Phase B features (applications and interviews)
      setStats(prev => ({
        ...prev,
        applicationsCount: 0, // Will be implemented in Phase B
        interviewsCount: 0     // Will be implemented in Phase B
      }));

    } catch (error) {
      console.error('Error loading dashboard stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateProfileCompleteness = (profile: any): number => {
    if (!profile) return 0;

    const fields = [
      profile.name,
      profile.email,
      profile.phone,
      profile.city,
      profile.country,
      profile.date_of_birth,
      profile.job_category
    ];

    const completedFields = fields.filter(field => field && field.toString().trim() !== '').length;
    return Math.round((completedFields / fields.length) * 100);
  };

  const handleCreateResume = () => {
    navigate('/candidate/profile/resumes/create');
  };

  const handleEditProfile = () => {
    navigate('/candidate/profile/edit');
  };

  const handleViewResumes = () => {
    navigate('/candidate/profile/resumes');
  };

  const handleViewExperience = () => {
    navigate('/candidate/profile/experience');
  };

  if (loading) {
    return (
      <CandidateProfileLayout
        title="Dashboard"
        subtitle="Cargando información..."
        currentSection="dashboard"
      >
        <div className="p-8 text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando estadísticas...</p>
        </div>
      </CandidateProfileLayout>
    );
  }

  return (
    <CandidateProfileLayout
      title="Dashboard"
      subtitle="Resumen de tu perfil profesional"
      currentSection="dashboard"
    >
      <div className="p-6 space-y-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="CVs Creados"
            value={stats.resumesCount}
            icon={FileText}
            color="blue"
            subtitle="currículos"
          />
          <StatCard
            title="Candidaturas"
            value={stats.applicationsCount}
            icon={Send}
            color="green"
            subtitle="Próximamente"
          />
          <StatCard
            title="Entrevistas"
            value={stats.interviewsCount}
            icon={Calendar}
            color="orange"
            subtitle="Próximamente"
          />
          <StatCard
            title="Perfil Completado"
            value={`${stats.profileCompleteness}%`}
            icon={User}
            color="purple"
          />
        </div>

        {/* Profile Completion Banner */}
        {stats.profileCompleteness < 100 && (
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-blue-900 mb-2">
                  ¡Completa tu perfil para mejores oportunidades!
                </h3>
                <p className="text-blue-700 mb-4">
                  Tu perfil está {stats.profileCompleteness}% completo. Añade más información para destacar ante los reclutadores.
                </p>
                <div className="w-full bg-blue-200 rounded-full h-2 mb-4">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${stats.profileCompleteness}%` }}
                  ></div>
                </div>
              </div>
              <button
                onClick={handleEditProfile}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <Edit className="w-4 h-4" />
                Completar Perfil
              </button>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Acciones Rápidas</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <QuickActionCard
              title="Generar Nuevo CV"
              description="Crea un currículum personalizado basado en tu perfil actualizado"
              icon={Plus}
              action={handleCreateResume}
              buttonText="Crear CV"
              color="blue"
              badge={stats.resumesCount === 0 ? "¡Nuevo!" : undefined}
            />
            <QuickActionCard
              title="Gestionar CVs"
              description="Ve, edita y descarga tus currículos existentes"
              icon={FileText}
              action={handleViewResumes}
              buttonText="Ver CVs"
              color="green"
            />
            <QuickActionCard
              title="Actualizar Experiencia"
              description="Añade o edita tu experiencia laboral y proyectos"
              icon={User}
              action={handleViewExperience}
              buttonText="Editar Experiencia"
              color="purple"
            />
            <QuickActionCard
              title="Completar Perfil"
              description="Mejora tu perfil con información adicional"
              icon={Edit}
              action={handleEditProfile}
              buttonText="Editar Perfil"
              color="orange"
            />
          </div>
        </div>

        {/* Recent Activity */}
        <div>
          <RecentActivitySection />
        </div>

        {/* Getting Started Guide (for new users) */}
        {stats.resumesCount === 0 && stats.profileCompleteness < 50 && (
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">🚀 Primeros Pasos</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  1
                </div>
                <div>
                  <h3 className="font-medium text-gray-900">Completa tu perfil</h3>
                  <p className="text-sm text-gray-600">Añade tu experiencia, educación y habilidades</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  2
                </div>
                <div>
                  <h3 className="font-medium text-gray-900">Crea tu primer CV</h3>
                  <p className="text-sm text-gray-600">Genera un currículum profesional automáticamente</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  3
                </div>
                <div>
                  <h3 className="font-medium text-gray-900">Explora oportunidades</h3>
                  <p className="text-sm text-gray-600">Postúlate a ofertas de trabajo relevantes</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </CandidateProfileLayout>
  );
};

export default CandidateProfilePage;