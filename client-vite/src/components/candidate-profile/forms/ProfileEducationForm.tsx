import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import { Plus, Edit, Trash2, GraduationCap, Calendar } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { api } from '../../../lib/api';

interface Education {
  id?: string;
  degree: string;
  institution: string;
  description: string;
  start_date: string;
  end_date?: string;
  created_at?: string;
  updated_at?: string;
}

interface ProfileEducationFormProps {
  candidateId?: string;
  onSave?: () => Promise<void>;
  className?: string;
}

// Expose submit method via ref for parent components (e.g., wizard)
export interface ProfileEducationFormHandle {
  submit: () => Promise<boolean>;
}

const ProfileEducationForm = forwardRef<ProfileEducationFormHandle, ProfileEducationFormProps>(({
  candidateId,
  onSave,
  className = ""
}, ref) => {
  const { t } = useTranslation();
  const [educations, setEducations] = useState<Education[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editingId, setEditingId] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);

  const [formData, setFormData] = useState<Education>({
    degree: "",
    institution: "",
    description: "",
    start_date: "",
    end_date: ""
  });

  useEffect(() => {
    loadEducations();
  }, [candidateId]);

  // Expose submit method to parent via ref
  // For list-based forms, data is saved per-item, so submit just returns true
  useImperativeHandle(ref, () => ({
    submit: async () => true
  }));

  const loadEducations = async () => {
    try {
      setIsLoading(true);
      setError("");

      // Use the same API method as onboarding system
      const educations = await api.getEducations() as Education[];

      setEducations(Array.isArray(educations) ? educations : []);
    } catch (error) {
      console.error('Error loading educations:', error);
      setError(t('education.errorLoading'));
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
        // Update existing education - use authenticated request like ProfileExperienceForm
        await api.authenticatedRequest(`/candidate/educations/${editingId}`, {
          method: 'PUT',
          body: JSON.stringify(formData),
        });
        setSuccess(t('education.educationUpdated'));
      } else {
        // Create new education - use same API method as onboarding system
        await api.createEducation(formData);
        setSuccess(t('education.educationAdded'));
      }

      // Reset form
      setFormData({
        degree: "",
        institution: "",
        description: "",
        start_date: "",
        end_date: ""
      });
      setEditingId(null);
      setShowAddForm(false);

      // Reload educations
      await loadEducations();

      if (onSave) {
        await onSave();
      }
    } catch (error) {
      console.error('Error saving education:', error);
      setError(t('education.errorSaving'));
    }
  };

  const handleEdit = (education: Education) => {
    setFormData({
      degree: education.degree,
      institution: education.institution,
      description: education.description,
      start_date: education.start_date,
      end_date: education.end_date || ""
    });
    setEditingId(education.id || null);
    setShowAddForm(true);
  };

  const handleDelete = async (educationId: string) => {
    if (!confirm(t('education.deleteConfirm'))) {
      return;
    }

    try {
      await api.authenticatedRequest(`/candidate/educations/${educationId}`, {
        method: 'DELETE',
      });
      setSuccess(t('education.educationDeleted'));
      await loadEducations();
    } catch (error) {
      console.error('Error deleting education:', error);
      setError(t('education.errorDeleting'));
    }
  };

  const handleCancel = () => {
    setFormData({
      degree: "",
      institution: "",
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
          <GraduationCap className="w-6 h-6 text-green-600" />
          <h2 className="text-xl font-semibold text-gray-900">{t('resume.sections.education')}</h2>
        </div>
        <button
          onClick={() => setShowAddForm(true)}
          className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          {t('education.addEducation')}
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

      {/* Education List */}
      <div className="space-y-4 mb-6">
        {educations.map((education) => (
          <div key={education.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-sm transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900">{education.degree}</h3>
                <p className="text-green-600 font-medium">{education.institution}</p>

                <div className="flex items-center gap-2 text-sm text-gray-500 mt-2">
                  <Calendar className="w-4 h-4" />
                  <span>
                    {formatDate(education.start_date)} - {education.end_date ? formatDate(education.end_date) : t('education.currentStudies')}
                  </span>
                </div>

                <p className="text-gray-700 mt-3 leading-relaxed">{education.description}</p>
              </div>

              <div className="flex items-center gap-2 ml-4">
                <button
                  onClick={() => handleEdit(education)}
                  className="p-2 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-blue-50"
                  title={t('common.edit')}
                >
                  <Edit className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleDelete(education.id!)}
                  className="p-2 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50"
                  title={t('common.delete')}
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {educations.length === 0 && (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <GraduationCap className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">{t('education.noEducation')}</p>
            <p className="text-sm text-gray-400 mt-1">{t('education.startAddingEducation')}</p>
          </div>
        )}
      </div>

      {/* Add/Edit Form */}
      {showAddForm && (
        <div className="border-t border-gray-200 pt-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {editingId ? t('education.editEducation') : t('education.addNewEducation')}
          </h3>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="degree" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('education.degree')}
                </label>
                <input
                  type="text"
                  id="degree"
                  name="degree"
                  required
                  value={formData.degree}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  placeholder={t('education.degreePlaceholder')}
                />
              </div>

              <div>
                <label htmlFor="institution" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('education.institution')}
                </label>
                <input
                  type="text"
                  id="institution"
                  name="institution"
                  required
                  value={formData.institution}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  placeholder={t('education.institutionPlaceholder')}
                />
              </div>

              <div>
                <label htmlFor="start_date" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('education.startDate')}
                </label>
                <input
                  type="date"
                  id="start_date"
                  name="start_date"
                  required
                  value={formData.start_date}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                />
              </div>

              <div>
                <label htmlFor="end_date" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('education.endDate')}
                </label>
                <input
                  type="date"
                  id="end_date"
                  name="end_date"
                  value={formData.end_date}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                />
                <p className="text-xs text-gray-500 mt-1">{t('education.leaveEmptyIfCurrentStudies')}</p>
              </div>
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                {t('education.description')}
              </label>
              <textarea
                id="description"
                name="description"
                required
                rows={3}
                value={formData.description}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder={t('education.descriptionPlaceholder')}
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
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
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

ProfileEducationForm.displayName = 'ProfileEducationForm';

export default ProfileEducationForm;