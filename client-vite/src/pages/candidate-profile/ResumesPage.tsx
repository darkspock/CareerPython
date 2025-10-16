import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Eye, Edit, Trash2, FileText, Calendar, Download } from 'lucide-react';
import { CandidateProfileLayout } from '../../components/candidate-profile';
import { api } from '../../lib/api';

interface ResumeData {
  id: string;
  name: string;
  resume_type: string;
  status: string;
  ai_enhancement_status: string;
  created_at: string;
  updated_at: string;
  content?: {
    experiencia_profesional: string;
    educacion: string;
    proyectos: string;
    habilidades: string;
    datos_personales: Record<string, any>;
  };
  general_data?: Record<string, any>;
  custom_content?: Record<string, any>;
}

interface ResumeListResponse {
  resumes: ResumeData[];
  total_count: number;
  message?: string;
}

const ResumesPage: React.FC = () => {
  const navigate = useNavigate();
  const [resumes, setResumes] = useState<ResumeData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState<string | null>(null);

  useEffect(() => {
    loadResumes();
  }, []);

  const loadResumes = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getResumes();
      setResumes(data.resumes || []);
    } catch (error) {
      console.error('Error loading resumes:', error);
      setError('Error al cargar los CVs');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateResume = () => {
    navigate('/candidate/profile/resumes/create');
  };

  const handleViewResume = (resumeId: string) => {
    navigate(`/candidate/profile/resumes/${resumeId}/preview`);
  };

  const handleEditResume = (resumeId: string) => {
    navigate(`/candidate/profile/resumes/${resumeId}/edit`);
  };

  const handleDeleteResume = async (resumeId: string, resumeName: string) => {
    if (!confirm(`¿Estás seguro de que quieres eliminar el CV "${resumeName}"?`)) {
      return;
    }

    try {
      setDeleting(resumeId);
      await api.deleteResume(resumeId);
      setResumes(prev => prev.filter(resume => resume.id !== resumeId));
    } catch (error) {
      console.error('Error deleting resume:', error);
      setError('Error al eliminar el CV');
    } finally {
      setDeleting(null);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'COMPLETED':
        return <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Completado</span>;
      case 'GENERATING':
        return <span className="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">Generando</span>;
      case 'DRAFT':
        return <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded-full">Borrador</span>;
      case 'ERROR':
        return <span className="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">Error</span>;
      default:
        return <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-600 rounded-full">{status}</span>;
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <CandidateProfileLayout
        title="Mis Currículos"
        subtitle="Cargando CVs..."
        currentSection="resumes"
      >
        <div className="p-8 text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando currículos...</p>
        </div>
      </CandidateProfileLayout>
    );
  }

  return (
    <CandidateProfileLayout
      title="Mis Currículos"
      subtitle="Gestiona y crea nuevos CVs personalizados"
      currentSection="resumes"
    >
      <div className="p-6">
        {/* Header Actions */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <FileText className="w-6 h-6 text-blue-600" />
            <div>
              <h2 className="text-lg font-semibold text-gray-900">
                Currículos ({resumes.length})
              </h2>
              <p className="text-sm text-gray-500">
                Crea y gestiona diferentes versiones de tu CV
              </p>
            </div>
          </div>

          <button
            onClick={handleCreateResume}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            Crear Nuevo CV
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        {/* Resumes Grid */}
        {resumes.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {resumes.map((resume) => (
              <div
                key={resume.id}
                className="bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
              >
                {/* Resume Header */}
                <div className="p-4 border-b border-gray-100">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 mb-1 line-clamp-2">
                        {resume.name}
                      </h3>
                      <div className="flex items-center gap-2 mb-2">
                        {getStatusBadge(resume.status)}
                        <span className="text-xs text-gray-500 capitalize">
                          {resume.resume_type.toLowerCase()}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 text-xs text-gray-500">
                    <Calendar className="w-3 h-3" />
                    <span>Creado: {formatDate(resume.created_at)}</span>
                  </div>
                </div>

                {/* Resume Content Preview */}
                <div className="p-4">
                  <div className="text-sm text-gray-600 space-y-2">
                    {resume.content?.datos_personales?.name && (
                      <div>
                        <span className="font-medium">Candidato: </span>
                        <span className="text-gray-500">{resume.content.datos_personales.name}</span>
                      </div>
                    )}

                    {resume.content?.habilidades && resume.content.habilidades.trim() && (
                      <div>
                        <span className="font-medium">Habilidades: </span>
                        <span className="text-gray-500">
                          {resume.content.habilidades.substring(0, 50)}
                          {resume.content.habilidades.length > 50 && '...'}
                        </span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Actions */}
                <div className="px-4 pb-4">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleViewResume(resume.id)}
                      className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors"
                      title="Ver CV"
                    >
                      <Eye className="w-4 h-4" />
                      Ver
                    </button>

                    <button
                      onClick={() => handleEditResume(resume.id)}
                      className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-gray-50 text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
                      title="Editar CV"
                    >
                      <Edit className="w-4 h-4" />
                      Editar
                    </button>

                    <button
                      onClick={() => handleDeleteResume(resume.id, resume.name)}
                      disabled={deleting === resume.id}
                      className="p-2 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50 transition-colors disabled:opacity-50"
                      title="Eliminar CV"
                    >
                      {deleting === resume.id ? (
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-red-600"></div>
                      ) : (
                        <Trash2 className="w-4 h-4" />
                      )}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          /* Empty State */
          <div className="text-center py-16">
            <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No has creado ningún CV
            </h3>
            <p className="text-gray-600 mb-6 max-w-md mx-auto">
              Crea tu primer currículum utilizando la información de tu perfil.
              Podrás personalizarlo y generar diferentes versiones.
            </p>
            <button
              onClick={handleCreateResume}
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-5 h-5" />
              Crear Mi Primer CV
            </button>
          </div>
        )}

        {/* Help Section */}
        {resumes.length > 0 && (
          <div className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">
              💡 Consejos para tus CVs
            </h3>
            <div className="text-blue-800 space-y-2 text-sm">
              <p>• <strong>CV General:</strong> Ideal para aplicaciones masivas y networking</p>
              <p>• <strong>CV Específico:</strong> Personaliza para cada oferta de trabajo</p>
              <p>• <strong>Mantén actualizado:</strong> Revisa y actualiza regularmente tu información</p>
              <p>• <strong>Diferentes formatos:</strong> Descarga en PDF para aplicaciones formales</p>
            </div>
          </div>
        )}
      </div>
    </CandidateProfileLayout>
  );
};

export default ResumesPage;