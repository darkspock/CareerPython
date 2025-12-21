import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import { Plus, Edit, Trash2, FolderOpen, Calendar } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { api } from '../../../lib/api';

interface Project {
  id?: string;
  name: string;
  description: string;
  start_date: string;
  end_date?: string;
  created_at?: string;
  updated_at?: string;
}

interface ProfileProjectsFormProps {
  candidateId?: string;
  onSave?: () => Promise<void>;
  className?: string;
}

// Expose submit method via ref for parent components (e.g., wizard)
export interface ProfileProjectsFormHandle {
  submit: () => Promise<boolean>;
}

const ProfileProjectsForm = forwardRef<ProfileProjectsFormHandle, ProfileProjectsFormProps>(({
  candidateId,
  onSave,
  className = ""
}, ref) => {
  const { t } = useTranslation();
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editingId, setEditingId] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);

  const [formData, setFormData] = useState<Project>({
    name: "",
    description: "",
    start_date: "",
    end_date: ""
  });

  useEffect(() => {
    loadProjects();
  }, [candidateId]);

  // Expose submit method to parent via ref
  // For list-based forms, data is saved per-item, so submit just returns true
  useImperativeHandle(ref, () => ({
    submit: async () => true
  }));

  const loadProjects = async () => {
    try {
      setIsLoading(true);
      setError("");

      // Use the same API method as onboarding system
      const projects = await api.getProjects() as Project[];

      setProjects(Array.isArray(projects) ? projects : []);
    } catch (error) {
      console.error('Error loading projects:', error);
      setError(t('projects.errorLoading'));
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      if (editingId) {
        // Update existing project - use authenticated request like other profile forms
        await api.authenticatedRequest(`/candidate/projects/${editingId}`, {
          method: 'PUT',
          body: JSON.stringify(formData),
        });
        setSuccess(t('projects.projectUpdated'));
      } else {
        // Create new project - use same API method as onboarding system
        await api.createProject(formData);
        setSuccess(t('projects.projectAdded'));
      }

      // Reset form
      setFormData({
        name: "",
        description: "",
        start_date: "",
        end_date: ""
      });
      setEditingId(null);
      setShowAddForm(false);

      // Reload projects
      await loadProjects();

      if (onSave) {
        await onSave();
      }
    } catch (error) {
      console.error('Error saving project:', error);
      setError(t('projects.errorSaving'));
    }
  };

  const handleEdit = (project: Project) => {
    setFormData({
      name: project.name,
      description: project.description,
      start_date: project.start_date,
      end_date: project.end_date || ""
    });
    setEditingId(project.id || null);
    setShowAddForm(true);
  };

  const handleDelete = async (projectId: string) => {
    if (!confirm(t('projects.deleteConfirm'))) {
      return;
    }

    try {
      await api.authenticatedRequest(`/candidate/projects/${projectId}`, {
        method: 'DELETE',
      });
      setSuccess(t('projects.projectDeleted'));
      await loadProjects();
    } catch (error) {
      console.error('Error deleting project:', error);
      setError(t('projects.errorDeleting'));
    }
  };

  const handleCancel = () => {
    setFormData({
      name: "",
      description: "",
      start_date: "",
      end_date: ""
    });
    setEditingId(null);
    setShowAddForm(false);
    setError("");
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('es-ES', {
      month: 'long',
      year: 'numeric'
    });
  };

  if (isLoading) {
    return (
      <div className={`${className} p-6`}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">{t('common.loading')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className={className}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <FolderOpen className="w-6 h-6 text-purple-600" />
          <h2 className="text-xl font-semibold text-gray-900">{t('resume.sections.projects')}</h2>
        </div>
        <button
          onClick={() => setShowAddForm(true)}
          className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          {t('projects.addProject')}
        </button>
      </div>

      {/* Messages */}
      {success && (
        <div className="mb-4 bg-green-50 border border-green-200 rounded-lg p-4">
          <p className="text-sm text-green-800">{success}</p>
        </div>
      )}

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Projects List */}
      <div className="space-y-4 mb-6">
        {projects.map((project) => (
          <div key={project.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-sm transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900">{project.name}</h3>

                <div className="flex items-center gap-2 text-sm text-gray-500 mt-2">
                  <Calendar className="w-4 h-4" />
                  <span>
                    {formatDate(project.start_date)} - {project.end_date ? formatDate(project.end_date) : t('projects.inProgress')}
                  </span>
                </div>

                <p className="text-gray-700 mt-3 leading-relaxed">{project.description}</p>

                {/* Project Badge */}
                <div className="mt-4">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                    {t('projects.personalProject')}
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-2 ml-4">
                <button
                  onClick={() => handleEdit(project)}
                  className="p-2 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-blue-50"
                  title={t('common.edit')}
                >
                  <Edit className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleDelete(project.id!)}
                  className="p-2 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50"
                  title={t('common.delete')}
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {projects.length === 0 && (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <FolderOpen className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">{t('projects.noProjects')}</p>
            <p className="text-sm text-gray-400 mt-1">{t('projects.startAddingProjects')}</p>
          </div>
        )}
      </div>

      {/* Add/Edit Form */}
      {showAddForm && (
        <div className="border-t border-gray-200 pt-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {editingId ? t('projects.editProject') : t('projects.addNewProject')}
          </h3>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                {t('projects.name')}
              </label>
              <input
                type="text"
                id="name"
                name="name"
                required
                value={formData.name}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                placeholder={t('projects.namePlaceholder')}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="start_date" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('projects.startDate')}
                </label>
                <input
                  type="date"
                  id="start_date"
                  name="start_date"
                  required
                  value={formData.start_date}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                />
              </div>

              <div>
                <label htmlFor="end_date" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('projects.endDate')}
                </label>
                <input
                  type="date"
                  id="end_date"
                  name="end_date"
                  value={formData.end_date}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                />
                <p className="text-xs text-gray-500 mt-1">{t('projects.leaveEmptyIfInProgress')}</p>
              </div>
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                {t('projects.description')}
              </label>
              <textarea
                id="description"
                name="description"
                required
                rows={4}
                value={formData.description}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                placeholder={t('projects.descriptionPlaceholder')}
              />
            </div>

            <div className="flex justify-end gap-3">
              <button
                type="button"
                onClick={handleCancel}
                className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                {t('common.cancel')}
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
              >
                {editingId ? t('common.update') : t('common.save')}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
});

ProfileProjectsForm.displayName = 'ProfileProjectsForm';

export default ProfileProjectsForm;