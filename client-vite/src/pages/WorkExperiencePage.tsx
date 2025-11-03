import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../lib/api";
import { useOnboarding } from "../hooks/useOnboarding";

interface WorkExperience {
  company: string;
  position: string;
  startDate: string;
  endDate: string;
  isCurrentJob: boolean;
  description: string;
}

export default function WorkExperiencePage() {
  const [experiences, setExperiences] = useState<WorkExperience[]>([
    {
      company: "",
      position: "",
      startDate: "",
      endDate: "",
      isCurrentJob: false,
      description: "",
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { jobPositionId } = useOnboarding();

  useEffect(() => {
    // Verificar que el usuario tenga un token de autenticación
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/");
      return;
    }

    // Cargar experiencias existentes
    loadExistingExperiences();
  }, [navigate]);

  const loadExistingExperiences = async () => {
    try {
      const existingExperiences = await api.getExperiences() as any[];

      if (Array.isArray(existingExperiences) && existingExperiences.length > 0) {
        // Mapear las experiencias del backend al formato del frontend
        const mappedExperiences = existingExperiences.map((exp: any) => ({
          company: exp.company || "",
          position: exp.job_title || "",
          startDate: exp.start_date || "",
          endDate: exp.end_date || "",
          isCurrentJob: !exp.end_date,
          description: exp.description || "",
        }));

        setExperiences(mappedExperiences);
      }
    } catch (error) {
      console.error("Error loading existing experiences:", error);
      // Si hay error, mantener el estado inicial con una experiencia vacía
    }
  };

  const addExperience = () => {
    setExperiences([
      ...experiences,
      {
        company: "",
        position: "",
        startDate: "",
        endDate: "",
        isCurrentJob: false,
        description: "",
      }
    ]);
  };

  const removeExperience = (index: number) => {
    if (experiences.length > 1) {
      setExperiences(experiences.filter((_, i) => i !== index));
    }
  };

  const updateExperience = (index: number, field: keyof WorkExperience, value: string | boolean) => {
    const updated = [...experiences];
    updated[index] = { ...updated[index], [field]: value };
    
    // Si marca como trabajo actual, limpiar fecha de fin
    if (field === 'isCurrentJob' && value === true) {
      updated[index].endDate = '';
    }
    
    setExperiences(updated);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("No autorizado. Por favor, inicia sesión.");
      setIsLoading(false);
      navigate("/");
      return;
    }

    try {
      // Filtrar experiencias vacías
      const validExperiences = experiences.filter(exp => 
        exp.company.trim() && exp.position.trim()
      );

      if (validExperiences.length === 0) {
        setError("Debes agregar al menos una experiencia laboral.");
        setIsLoading(false);
        return;
      }

      // Mapear experiencias al formato que espera el backend
      const experiencesToSave = validExperiences.map(exp => ({
        job_title: exp.position,
        company: exp.company,
        description: exp.description,
        start_date: exp.startDate,
        end_date: exp.isCurrentJob ? null : exp.endDate,
      }));

      // Guardar experiencias en el backend
      if (experiencesToSave.length === 1) {
        await api.createExperience(experiencesToSave[0]);
      } else {
        await api.createMultipleExperiences(experiencesToSave);
      }
      
      // Navegar al siguiente paso (educación), preservando jobPositionId
      const nextUrl = jobPositionId
        ? `/candidate/profile/education?jobPositionId=${jobPositionId}`
        : '/candidate/profile/education';
      navigate(nextUrl);
    } catch (error) {
      setError("Error al guardar la experiencia laboral. Inténtalo de nuevo.");
    } finally {
      setIsLoading(false);
    }
  };

  const skipStep = () => {
    const nextUrl = jobPositionId
      ? `/candidate/profile/education?jobPositionId=${jobPositionId}`
      : '/candidate/profile/education';
    navigate(nextUrl);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Experiencia Laboral
          </h2>
          <p className="text-gray-600">
            Cuéntanos sobre tu experiencia profesional para crear un mejor perfil.
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-8">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            )}

            {experiences.map((experience, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-6 space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="text-lg font-medium text-gray-900">
                    Experiencia {index + 1}
                  </h3>
                  {experiences.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeExperience(index)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Eliminar
                    </button>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Empresa
                    </label>
                    <input
                      type="text"
                      value={experience.company}
                      onChange={(e) => updateExperience(index, 'company', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Nombre de la empresa"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Cargo
                    </label>
                    <input
                      type="text"
                      value={experience.position}
                      onChange={(e) => updateExperience(index, 'position', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Tu cargo o posición"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Fecha de Inicio
                    </label>
                    <input
                      type="date"
                      value={experience.startDate}
                      onChange={(e) => updateExperience(index, 'startDate', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Fecha de Fin
                    </label>
                    <input
                      type="date"
                      value={experience.endDate}
                      onChange={(e) => updateExperience(index, 'endDate', e.target.value)}
                      disabled={experience.isCurrentJob}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                    />
                  </div>
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id={`current-job-${index}`}
                    checked={experience.isCurrentJob}
                    onChange={(e) => updateExperience(index, 'isCurrentJob', e.target.checked)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label htmlFor={`current-job-${index}`} className="ml-2 block text-sm text-gray-900">
                    Trabajo actual
                  </label>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Descripción
                  </label>
                  <textarea
                    value={experience.description}
                    onChange={(e) => updateExperience(index, 'description', e.target.value)}
                    rows={3}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Describe tus responsabilidades y logros en este puesto..."
                  />
                </div>
              </div>
            ))}

            <button
              type="button"
              onClick={addExperience}
              className="w-full py-3 px-4 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-blue-500 hover:text-blue-600 transition duration-200"
            >
              + Agregar otra experiencia
            </button>

            <div className="flex gap-4">
              <button
                type="button"
                onClick={skipStep}
                className="flex-1 py-3 px-4 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition duration-200"
              >
                Omitir por ahora
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="flex-1 py-3 px-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
              >
                {isLoading ? "Guardando..." : "Continuar"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}