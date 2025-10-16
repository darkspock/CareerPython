import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Plus, Edit, Trash2, Briefcase, Calendar } from 'lucide-react';
import { api } from '../../../lib/api';

interface Experience {
  id?: string;
  job_title: string;
  company: string;
  description: string;
  start_date: string;
  end_date?: string;
  created_at?: string;
  updated_at?: string;
}

interface ProfileExperienceFormProps {
  candidateId?: string;
  onSave?: () => Promise<void>;
  className?: string;
}

const ProfileExperienceForm: React.FC<ProfileExperienceFormProps> = ({
  candidateId,
  onSave,
  className = ""
}) => {
  const { t } = useTranslation();
  const [experiences, setExperiences] = useState<Experience[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editingId, setEditingId] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);

  const [formData, setFormData] = useState<Experience>({
    job_title: "",
    company: "",
    description: "",
    start_date: "",
    end_date: ""
  });

  useEffect(() => {
    loadExperiences();
  }, [candidateId]);

  const loadExperiences = async () => {
    try {
      setIsLoading(true);
      setError("");

      // Use the correct API method
      const experiences = await api.getExperiences();

      setExperiences(experiences);
    } catch (error) {
      console.error('Error loading experiences:', error);
      setError(t('experience.errorLoading'));
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
        // Update existing experience
        await api.updateExperience(editingId, formData);
        setSuccess(t('experience.experienceUpdated'));
      } else {
        // Create new experience
        await api.createExperience(formData);
        setSuccess(t('experience.experienceAdded'));
      }

      // Reset form
      setFormData({
        job_title: "",
        company: "",
        description: "",
        start_date: "",
        end_date: ""
      });
      setEditingId(null);
      setShowAddForm(false);

      // Reload experiences
      await loadExperiences();

      if (onSave) {
        await onSave();
      }
    } catch (error) {
      console.error('Error saving experience:', error);
      setError(t('experience.errorSaving'));
    }
  };

  const handleEdit = (experience: Experience) => {
    setFormData({
      job_title: experience.job_title,
      company: experience.company,
      description: experience.description,
      start_date: experience.start_date,
      end_date: experience.end_date || ""
    });
    setEditingId(experience.id || null);
    setShowAddForm(true);
  };

  const handleDelete = async (experienceId: string) => {
    if (!confirm(t('experience.deleteConfirm'))) {
      return;
    }

    try {
      await api.authenticatedRequest(`/candidate/experiences/${experienceId}`, {
        method: 'DELETE',
      });
      setSuccess(t('experience.experienceDeleted'));
      await loadExperiences();
    } catch (error) {
      console.error('Error deleting experience:', error);
      setError(t('experience.errorDeleting'));
    }
  };

  const handleCancel = () => {
    setFormData({
      job_title: "",
      company: "",
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
          <Briefcase className="w-6 h-6 text-blue-600" />
          <h2 className="text-xl font-semibold text-gray-900">{t('profile.workExperience')}</h2>
        </div>
        <button
          onClick={() => setShowAddForm(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          {t('experience.addExperience')}
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

      {/* Experience List */}
      <div className="space-y-4 mb-6">
        {experiences.map((experience) => (
          <div key={experience.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-sm transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900">{experience.job_title}</h3>
                <p className="text-blue-600 font-medium">{experience.company}</p>

                <div className="flex items-center gap-2 text-sm text-gray-500 mt-2">
                  <Calendar className="w-4 h-4" />
                  <span>
                    {formatDate(experience.start_date)} - {experience.end_date ? formatDate(experience.end_date) : t('common.current')}
                  </span>
                </div>

                <p className="text-gray-700 mt-3 leading-relaxed">{experience.description}</p>
              </div>

              <div className="flex items-center gap-2 ml-4">
                <button
                  onClick={() => handleEdit(experience)}
                  className="p-2 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-blue-50"
                  title={t('common.edit')}
                >
                  <Edit className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleDelete(experience.id!)}
                  className="p-2 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50"
                  title={t('common.delete')}
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {experiences.length === 0 && (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <Briefcase className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">{t('profile.noExperience')}</p>
            <p className="text-sm text-gray-400 mt-1">{t('profile.startAddingExperience')}</p>
          </div>
        )}
      </div>

      {/* Add/Edit Form */}
      {showAddForm && (
        <div className="border-t border-gray-200 pt-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {editingId ? t('experience.editExperience') : t('experience.addNewExperience')}
          </h3>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="job_title" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('experience.jobTitle')}
                </label>
                <input
                  type="text"
                  id="job_title"
                  name="job_title"
                  required
                  value={formData.job_title}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder={t('experience.jobTitlePlaceholder')}
                />
              </div>

              <div>
                <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('experience.company')}
                </label>
                <input
                  type="text"
                  id="company"
                  name="company"
                  required
                  value={formData.company}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder={t('experience.companyPlaceholder')}
                />
              </div>

              <div>
                <label htmlFor="start_date" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('experience.startDate')}
                </label>
                <input
                  type="date"
                  id="start_date"
                  name="start_date"
                  required
                  value={formData.start_date}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label htmlFor="end_date" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('experience.endDate')}
                </label>
                <input
                  type="date"
                  id="end_date"
                  name="end_date"
                  value={formData.end_date}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <p className="text-xs text-gray-500 mt-1">{t('experience.currentJob')}</p>
              </div>
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                {t('experience.description')}
              </label>
              <textarea
                id="description"
                name="description"
                required
                rows={4}
                value={formData.description}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder={t('experience.descriptionPlaceholder')}
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
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                {editingId ? t('common.update') : t('common.save')}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default ProfileExperienceForm;