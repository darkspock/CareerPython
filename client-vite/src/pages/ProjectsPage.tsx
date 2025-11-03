import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../lib/api";
import { useOnboarding } from "../hooks/useOnboarding";

interface Project {
  name: string;
  description: string;
  technologies: string;
  startDate: string;
  endDate: string;
  isOngoing: boolean;
  url: string;
  repository: string;
  role: string;
}

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([
    {
      name: "",
      description: "",
      technologies: "",
      startDate: "",
      endDate: "",
      isOngoing: false,
      url: "",
      repository: "",
      role: "",
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

    // Cargar proyectos existentes
    loadExistingProjects();
  }, [navigate]);

  const loadExistingProjects = async () => {
    try {
      const existingProjects = await api.getProjects() as any[];
      
      if (Array.isArray(existingProjects) && existingProjects.length > 0) {
        // Mapear los proyectos del backend al formato del frontend
        const mappedProjects = existingProjects.map((proj: any) => ({
          name: proj.name || "",
          description: proj.description || "",
          technologies: proj.technologies || "",
          startDate: proj.start_date || "",
          endDate: proj.end_date || "",
          isOngoing: !proj.end_date,
          url: proj.url || "",
          repository: proj.repository || "",
          role: proj.role || "",
        }));
        
        setProjects(mappedProjects);
      }
    } catch (error) {
      console.error("Error loading existing projects:", error);
      // Si hay error, mantener el estado inicial con un proyecto vacío
    }
  };

  const addProject = () => {
    setProjects([
      ...projects,
      {
        name: "",
        description: "",
        technologies: "",
        startDate: "",
        endDate: "",
        isOngoing: false,
        url: "",
        repository: "",
        role: "",
      }
    ]);
  };

  const removeProject = (index: number) => {
    if (projects.length > 1) {
      setProjects(projects.filter((_, i) => i !== index));
    }
  };

  const updateProject = (index: number, field: keyof Project, value: string | boolean) => {
    const updated = [...projects];
    updated[index] = { ...updated[index], [field]: value };

    // Si marca como proyecto en curso, limpiar fecha de fin
    if (field === 'isOngoing' && value === true) {
      updated[index].endDate = '';
    }

    setProjects(updated);
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
      // Filtrar proyectos válidos (solo los que tienen nombre y descripción)
      const validProjects = projects.filter(proj =>
        proj.name.trim() && proj.description.trim()
      );

      // Guardar solo los proyectos válidos (si los hay)
      if (validProjects.length > 0) {
        for (const project of validProjects) {
          const projectToSave = {
            name: project.name,
            description: project.description,
            start_date: project.startDate,
            end_date: project.isOngoing ? null : project.endDate,
          };

          await api.createProject(projectToSave);
        }
      }

      // Navegar al próximo paso o dashboard, preservando jobPositionId
      const nextUrl = jobPositionId
        ? `/candidate/profile/resumes?jobPositionId=${jobPositionId}`
        : '/candidate/profile/resumes';
      navigate(nextUrl);
    } catch (error) {
      setError("Error al guardar los proyectos. Inténtalo de nuevo.");
    } finally {
      setIsLoading(false);
    }
  };

  const goBack = () => {
    const backUrl = jobPositionId
      ? `/candidate/profile/education?jobPositionId=${jobPositionId}`
      : '/candidate/profile/education';
    navigate(backUrl);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Proyectos <span className="text-sm font-normal text-gray-500">(Opcional)</span>
          </h2>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-8">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            )}

            {projects.map((project, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-6 space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="text-lg font-medium text-gray-900">
                    Proyecto {index + 1}
                  </h3>
                  {projects.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeProject(index)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Eliminar
                    </button>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Nombre del Proyecto
                    </label>
                    <input
                      type="text"
                      value={project.name}
                      onChange={(e) => updateProject(index, 'name', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Nombre del proyecto"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Tu Rol
                    </label>
                    <input
                      type="text"
                      value={project.role}
                      onChange={(e) => updateProject(index, 'role', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Desarrollador, Líder, Diseñador..."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Tecnologías Utilizadas
                    </label>
                    <input
                      type="text"
                      value={project.technologies}
                      onChange={(e) => updateProject(index, 'technologies', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="React, Node.js, Python, etc."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Fecha de Inicio
                    </label>
                    <input
                      type="date"
                      value={project.startDate}
                      onChange={(e) => updateProject(index, 'startDate', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Fecha de Finalización
                    </label>
                    <input
                      type="date"
                      value={project.endDate}
                      onChange={(e) => updateProject(index, 'endDate', e.target.value)}
                      disabled={project.isOngoing}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      URL del Proyecto (Opcional)
                    </label>
                    <input
                      type="url"
                      value={project.url}
                      onChange={(e) => updateProject(index, 'url', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="https://miproyecto.com"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Repositorio (Opcional)
                    </label>
                    <input
                      type="url"
                      value={project.repository}
                      onChange={(e) => updateProject(index, 'repository', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="https://github.com/usuario/proyecto"
                    />
                  </div>
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id={`ongoing-project-${index}`}
                    checked={project.isOngoing}
                    onChange={(e) => updateProject(index, 'isOngoing', e.target.checked)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label htmlFor={`ongoing-project-${index}`} className="ml-2 block text-sm text-gray-900">
                    Proyecto en curso
                  </label>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Descripción del Proyecto
                  </label>
                  <textarea
                    value={project.description}
                    onChange={(e) => updateProject(index, 'description', e.target.value)}
                    rows={4}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Describe el proyecto, objetivos, desafíos superados y resultados obtenidos..."
                  />
                </div>
              </div>
            ))}

            <button
              type="button"
              onClick={addProject}
              className="w-full py-3 px-4 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-blue-500 hover:text-blue-600 transition duration-200"
            >
              + Agregar otro proyecto
            </button>

            <div className="flex gap-4">
              <button
                type="button"
                onClick={goBack}
                className="flex-1 py-3 px-4 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition duration-200"
              >
                ← Atrás
              </button>

              <button
                type="submit"
                disabled={isLoading}
                className="flex-1 py-3 px-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
              >
                {isLoading ? "Guardando..." : "Finalizar Perfil"}
              </button>
            </div>

            {/* Ayuda visual para el usuario */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-blue-800">
                    <strong>Opcional:</strong> Los proyectos son completamente opcionales. Puedes agregar algunos ahora para enriquecer tu perfil,
                    o completar esta sección más tarde desde tu dashboard.
                  </p>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}