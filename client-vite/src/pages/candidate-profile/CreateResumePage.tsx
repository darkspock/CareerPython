import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Wand2, Clock, ArrowRight } from 'lucide-react';
import { CandidateProfileLayout } from '../../components/candidate-profile';
import { api } from '../../lib/api';

interface CreateResumeFormData {
  name: string;
  include_ai_enhancement: boolean;
  general_data: {
    experience?: string;
    focus_areas?: string[];
    target_role?: string;
  };
}

const CreateResumePage: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<CreateResumeFormData>({
    name: '',
    include_ai_enhancement: false,
    general_data: {
      experience: '',
      focus_areas: [],
      target_role: ''
    }
  });
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsCreating(true);

    try {
      // Create the resume using the existing API
      const resume = await api.createResume({
        name: formData.name,
        include_ai_enhancement: formData.include_ai_enhancement,
        general_data: formData.general_data
      });

      // Navigate to the preview page
      const resumeData = resume as { id: string };
      navigate(`/candidate/profile/resumes/${resumeData.id}/preview`, {
        state: {
          showSuccessMessage: true,
          successMessage: 'CV creado correctamente'
        }
      });
    } catch (error) {
      console.error('Error creating resume:', error);
      setError('Error al crear el CV. Por favor, inténtalo de nuevo.');
    } finally {
      setIsCreating(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;

    if (type === 'checkbox') {
      const checkbox = e.target as HTMLInputElement;
      setFormData(prev => ({
        ...prev,
        [name]: checkbox.checked
      }));
    } else if (name.startsWith('general_data.')) {
      const fieldName = name.split('.')[1];
      setFormData(prev => ({
        ...prev,
        general_data: {
          ...prev.general_data,
          [fieldName]: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleCancel = () => {
    navigate('/candidate/profile/resumes');
  };

  // Generate default name based on current date
  const generateDefaultName = () => {
    const today = new Date();
    const dateStr = today.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long'
    });
    return `CV General - ${dateStr}`;
  };

  // Set default name if empty
  React.useEffect(() => {
    if (!formData.name) {
      setFormData(prev => ({
        ...prev,
        name: generateDefaultName()
      }));
    }
  }, []);

  return (
    <CandidateProfileLayout
      title="Crear Nuevo CV"
      subtitle="Genera un currículum personalizado basado en tu perfil"
      currentSection="resumes"
    >
      <div className="p-6">
        <form onSubmit={handleSubmit} className="max-w-2xl mx-auto space-y-8">
          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {/* Step 1: Basic Information */}
          <div className="bg-gray-50 rounded-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                1
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Información Básica</h3>
            </div>

            <div className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre del CV *
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  required
                  value={formData.name}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="ej. CV para Desarrollador Senior"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Dale un nombre descriptivo para identificarlo fácilmente
                </p>
              </div>
            </div>
          </div>

          {/* Step 2: Customization Options */}
          <div className="bg-gray-50 rounded-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                2
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Personalización</h3>
            </div>

            <div className="space-y-4">
              <div>
                <label htmlFor="general_data.target_role" className="block text-sm font-medium text-gray-700 mb-2">
                  Rol Objetivo
                </label>
                <input
                  type="text"
                  id="general_data.target_role"
                  name="general_data.target_role"
                  value={formData.general_data.target_role}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="ej. Desarrollador Full Stack Senior"
                />
                <p className="text-xs text-gray-500 mt-1">
                  El tipo de posición que buscas (opcional)
                </p>
              </div>

              <div>
                <label htmlFor="general_data.experience" className="block text-sm font-medium text-gray-700 mb-2">
                  Experiencia a Destacar
                </label>
                <textarea
                  id="general_data.experience"
                  name="general_data.experience"
                  rows={3}
                  value={formData.general_data.experience}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="ej. Desarrollo de aplicaciones web con React y Node.js, gestión de equipos..."
                />
                <p className="text-xs text-gray-500 mt-1">
                  Aspectos específicos de tu experiencia que quieres resaltar (opcional)
                </p>
              </div>
            </div>
          </div>

          {/* Step 3: AI Enhancement */}
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                3
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Mejora con IA</h3>
              <span className="px-2 py-1 text-xs font-medium bg-purple-100 text-purple-800 rounded-full">
                Próximamente
              </span>
            </div>

            <div className="space-y-4">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 mt-1">
                  <input
                    type="checkbox"
                    id="include_ai_enhancement"
                    name="include_ai_enhancement"
                    checked={formData.include_ai_enhancement}
                    onChange={handleInputChange}
                    disabled={true} // Disabled for MVP
                    className="h-4 w-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500 disabled:opacity-50"
                  />
                </div>
                <div className="flex-1">
                  <label htmlFor="include_ai_enhancement" className="text-sm font-medium text-gray-700">
                    Optimizar contenido con Inteligencia Artificial
                  </label>
                  <p className="text-sm text-gray-500 mt-1">
                    La IA mejorará automáticamente el contenido de tu CV para hacerlo más atractivo.
                    Esta característica estará disponible en futuras actualizaciones.
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2 text-sm text-purple-600">
                <Wand2 className="w-4 h-4" />
                <span>Mejora automática de texto</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-purple-600">
                <Clock className="w-4 h-4" />
                <span>Optimización de palabras clave</span>
              </div>
            </div>
          </div>

          {/* Preview Information */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <FileText className="w-5 h-5 text-blue-600 mt-0.5" />
              <div>
                <h4 className="text-sm font-medium text-blue-900">¿Qué incluirá tu CV?</h4>
                <ul className="text-sm text-blue-800 mt-2 space-y-1">
                  <li>• Tu información personal y de contacto</li>
                  <li>• Experiencia laboral completa</li>
                  <li>• Formación académica y certificaciones</li>
                  <li>• Proyectos y logros destacados</li>
                  <li>• Habilidades técnicas y blandas</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-between pt-6 border-t border-gray-200">
            <button
              type="button"
              onClick={handleCancel}
              className="px-6 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancelar
            </button>

            <button
              type="submit"
              disabled={isCreating || !formData.name.trim()}
              className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isCreating ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                  Creando CV...
                </>
              ) : (
                <>
                  Crear CV
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </CandidateProfileLayout>
  );
};

export default CreateResumePage;