import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { api } from '../../../lib/api';
import LanguageSelector, { type Language, convertLanguagesFromBackend, convertLanguagesToBackend } from '../../common/LanguageSelector';
import RoleSelector, { type Role, convertRolesFromBackend, convertRolesToBackend } from '../../common/RoleSelector';

// Job category keys for backend mapping
const JOB_CATEGORY_KEYS = [
  "TECHNOLOGY",
  "OPERATIONS",
  "SALES",
  "MARKETING",
  "ADMINISTRATION",
  "HR",
  "FINANCE",
  "CUSTOMER_SERVICE",
  "OTHER",
] as const;

// Mapping for backend values
const JobCategoryMapping: { [key: string]: string } = {
  TECHNOLOGY: "Technology",
  OPERATIONS: "Operations",
  SALES: "Sales",
  MARKETING: "Marketing",
  ADMINISTRATION: "Administration",
  HR: "Human Resources",
  FINANCE: "Finance",
  CUSTOMER_SERVICE: "Customer Service",
  OTHER: "Other",
};

const WorkModalityEnum = {
  REMOTE: 'remote',
  ON_SITE: 'on_site',
  HYBRID: 'hybrid',
} as const;


interface FormData {
  name: string;
  dateOfBirth: string;
  city: string;
  country: string;
  phone: string;
  email: string;
  jobCategory: string;
  languages: Language[];
  skills: string[];
  expectedAnnualSalary: string;
  currentAnnualSalary: string;
  relocation: boolean;
  workModality: string[];
  currentRoles: Role[];
  expectedRoles: Role[];
}

interface CandidateData {
  name?: string;
  date_of_birth?: string;
  city?: string;
  country?: string;
  phone?: string;
  email?: string;
  job_category?: string;
  languages?: Record<string, string>;
  skills?: string[];
  expected_annual_salary?: number;
  current_annual_salary?: number;
  relocation?: boolean;
  work_modality?: string[];
  current_roles?: string[];
  expected_roles?: string[];
}

interface ProfileBasicInfoFormProps {
  initialData?: CandidateData;
  onSave?: (data: CandidateData) => Promise<void>;
  onCancel?: () => void;
  showActions?: boolean;
  className?: string;
}

const ProfileBasicInfoForm: React.FC<ProfileBasicInfoFormProps> = ({
  initialData,
  onSave,
  onCancel,
  showActions = true,
  className = ""
}) => {
  const { t } = useTranslation();
  const [formData, setFormData] = useState<FormData>({
    name: "",
    dateOfBirth: "1990-01-01",
    city: "",
    country: "",
    phone: "",
    email: "",
    jobCategory: "OTHER",
    languages: [],
    skills: [],
    expectedAnnualSalary: "",
    currentAnnualSalary: "",
    relocation: false,
    workModality: [],
    currentRoles: [],
    expectedRoles: [],
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    if (initialData) {

      // Map job category from backend format to frontend format
      let jobCategoryKey = "OTHER";
      if (initialData.job_category) {
        // Find the key that matches the value
        const categoryEntry = Object.entries(JobCategoryMapping).find(
          ([_key, value]) => value === initialData.job_category
        );
        if (categoryEntry) {
          jobCategoryKey = categoryEntry[0];
        }
      }

      const convertedLanguages = convertLanguagesFromBackend(initialData.languages);

      const newFormData = {
        name: initialData.name || "",
        dateOfBirth: initialData.date_of_birth || "1990-01-01",
        city: initialData.city || "",
        country: initialData.country || "",
        phone: initialData.phone || "",
        email: initialData.email || "",
        jobCategory: jobCategoryKey,
        languages: convertedLanguages,
        skills: initialData.skills || [],
        expectedAnnualSalary: initialData.expected_annual_salary?.toString() || "",
        currentAnnualSalary: initialData.current_annual_salary?.toString() || "",
        relocation: initialData.relocation || false,
        workModality: initialData.work_modality || [],
        currentRoles: convertRolesFromBackend(initialData.current_roles),
        expectedRoles: convertRolesFromBackend(initialData.expected_roles),
      };

      setFormData(newFormData);
    }
  }, [initialData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setIsLoading(true);

    try {
      const profileData = {
        name: formData.name,
        date_of_birth: formData.dateOfBirth,
        city: formData.city,
        country: formData.country,
        phone: formData.phone,
        email: formData.email,
        job_category: JobCategoryMapping[formData.jobCategory] || formData.jobCategory,
        languages: convertLanguagesToBackend(formData.languages),
        skills: formData.skills,
        expected_annual_salary: formData.expectedAnnualSalary ? parseInt(formData.expectedAnnualSalary) : undefined,
        current_annual_salary: formData.currentAnnualSalary ? parseInt(formData.currentAnnualSalary) : undefined,
        relocation: formData.relocation,
        work_modality: formData.workModality,
        current_roles: convertRolesToBackend(formData.currentRoles),
        expected_roles: convertRolesToBackend(formData.expectedRoles),
      };

      console.log('🚀 DEBUGGING - About to send to API:', profileData);
      console.log('🚀 DEBUGGING - Form data languages:', formData.languages);
      console.log('🚀 DEBUGGING - Converted languages:', profileData.languages);
      const response = await api.updateMyProfile(profileData);
      console.log('✅ DEBUGGING - API Response:', response);
      setSuccess(t("candidateProfile.basicInfoForm.successMessage"));

      if (onSave) {
        await onSave(profileData);
      }
    } catch (error) {
      console.error('Error updating profile:', error);

      let errorMessage = t("candidateProfile.basicInfoForm.errorMessage");
      if (error instanceof Error) {
        if (error.message.includes("API Error:")) {
          errorMessage = error.message.replace(/^API Error: \d+ [^:]*: ?/, "");
        } else if (error.message && error.message !== "Failed to fetch") {
          errorMessage = error.message;
        }
      }

      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };


  return (
    <div className={className}>
      <form className="space-y-6" onSubmit={handleSubmit}>
        {/* Success Message */}
        {success && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-green-800">{success}</p>
              </div>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3 flex-1">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Form Fields - Grid de dos columnas para desktop, una columna para móvil */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              {t("candidateProfile.basicInfoForm.fullName")}
            </label>
            <input
              name="name"
              id="name"
              type="text"
              required
              value={formData.name}
              onChange={handleChange}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label htmlFor="dateOfBirth" className="block text-sm font-medium text-gray-700 mb-2">
              {t("candidateProfile.basicInfoForm.dateOfBirth")}
            </label>
            <input
              name="dateOfBirth"
              id="dateOfBirth"
              type="date"
              required
              value={formData.dateOfBirth}
              onChange={handleChange}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label htmlFor="city" className="block text-sm font-medium text-gray-700 mb-2">
              {t("candidateProfile.basicInfoForm.city")}
            </label>
            <input
              name="city"
              id="city"
              type="text"
              required
              value={formData.city}
              onChange={handleChange}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label htmlFor="country" className="block text-sm font-medium text-gray-700 mb-2">
              {t("candidateProfile.basicInfoForm.country")}
            </label>
            <input
              name="country"
              id="country"
              type="text"
              required
              value={formData.country}
              onChange={handleChange}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
              {t("candidateProfile.basicInfoForm.phone")}
            </label>
            <input
              name="phone"
              id="phone"
              type="tel"
              required
              value={formData.phone}
              onChange={handleChange}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label htmlFor="jobCategory" className="block text-sm font-medium text-gray-700 mb-2">
              {t("candidateProfile.basicInfoForm.jobCategory")}
            </label>
            <select
              name="jobCategory"
              id="jobCategory"
              required
              value={formData.jobCategory}
              onChange={handleChange}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">{t("candidateProfile.basicInfoForm.selectCategory")}</option>
              {JOB_CATEGORY_KEYS.map((key) => (
                <option key={key} value={key}>{t(`candidateProfile.jobCategories.${key}`)}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Email ocupa toda la fila */}
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
            {t("candidateProfile.basicInfoForm.email")}
          </label>
          <input
            name="email"
            id="email"
            type="email"
            required
            value={formData.email}
            readOnly
            className="w-full px-3 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-600 cursor-not-allowed"
          />
          <p className="text-xs text-gray-500 mt-1">{t("candidateProfile.basicInfoForm.emailReadOnly")}</p>
        </div>

        {/* Campos adicionales - Grid de dos columnas */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="expectedAnnualSalary" className="block text-sm font-medium text-gray-700 mb-2">{t("candidateProfile.basicInfoForm.expectedSalary")}</label>
            <input
              name="expectedAnnualSalary"
              id="expectedAnnualSalary"
              type="number"
              value={formData.expectedAnnualSalary}
              onChange={handleChange}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder={t("candidateProfile.basicInfoForm.salaryPlaceholder")}
            />
          </div>

          <div>
            <label htmlFor="currentAnnualSalary" className="block text-sm font-medium text-gray-700 mb-2">{t("candidateProfile.basicInfoForm.currentSalary")}</label>
            <input
              name="currentAnnualSalary"
              id="currentAnnualSalary"
              type="number"
              value={formData.currentAnnualSalary}
              onChange={handleChange}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder={t("candidateProfile.basicInfoForm.salaryPlaceholder")}
            />
          </div>
        </div>

        {/* Modalidad de trabajo */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">{t("candidateProfile.basicInfoForm.workModality")}</label>
          <div className="space-y-2">
            {Object.values(WorkModalityEnum).map((key) => (
              <label key={key} className="flex items-center">
                <input
                  type="checkbox"
                  checked={formData.workModality.includes(key)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setFormData(prev => ({ ...prev, workModality: [...prev.workModality, key] }));
                    } else {
                      setFormData(prev => ({ ...prev, workModality: prev.workModality.filter(m => m !== key) }));
                    }
                  }}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="ml-2 text-sm text-gray-900">
                  {key === 'remote' ? t("candidateProfile.basicInfoForm.remote") :
                   key === 'on_site' ? t("candidateProfile.basicInfoForm.onSite") :
                   t("candidateProfile.basicInfoForm.hybrid")}
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Disponibilidad para reubicación */}
        <div>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={formData.relocation}
              onChange={(e) => setFormData(prev => ({ ...prev, relocation: e.target.checked }))}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <span className="ml-2 text-sm text-gray-900">{t("candidateProfile.basicInfoForm.relocation")}</span>
          </label>
        </div>

        {/* Idiomas */}
        <LanguageSelector
          languages={formData.languages}
          onChange={(languages) => setFormData(prev => ({ ...prev, languages }))}
        />

        {/* Habilidades */}
        <div>
          <label htmlFor="skills" className="block text-sm font-medium text-gray-700 mb-2">{t("candidateProfile.basicInfoForm.skills")}</label>
          <textarea
            name="skills"
            id="skills"
            rows={3}
            value={formData.skills.join(', ')}
            onChange={(e) => {
              const skillsArray = e.target.value.split(',').map(skill => skill.trim()).filter(skill => skill);
              setFormData(prev => ({ ...prev, skills: skillsArray }));
            }}
            className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder={t("candidateProfile.basicInfoForm.skillsPlaceholder")}
          />
          <p className="text-xs text-gray-500 mt-1">{t("candidateProfile.basicInfoForm.skillsHint")}</p>
        </div>

        {/* Roles - Grid de dos columnas */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Roles Actuales */}
          <RoleSelector
            roles={formData.currentRoles}
            onChange={(roles) => setFormData(prev => ({ ...prev, currentRoles: roles }))}
            title={t("candidateProfile.basicInfoForm.currentRoles")}
            placeholder={t("candidateProfile.basicInfoForm.selectCurrentRole")}
          />

          {/* Roles Deseados */}
          <RoleSelector
            roles={formData.expectedRoles}
            onChange={(roles) => setFormData(prev => ({ ...prev, expectedRoles: roles }))}
            title={t("candidateProfile.basicInfoForm.expectedRoles")}
            placeholder={t("candidateProfile.basicInfoForm.selectExpectedRole")}
          />
        </div>

        {/* Action Buttons */}
        {showActions && (
          <div className="flex justify-end gap-3 pt-4">
            {onCancel && (
              <button
                type="button"
                onClick={onCancel}
                className="px-6 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 font-medium"
              >
                {t("candidateProfile.basicInfoForm.cancel")}
              </button>
            )}
            <button
              type="submit"
              disabled={isLoading || !formData.name || !formData.email || !formData.dateOfBirth}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center gap-2"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  {t("candidateProfile.basicInfoForm.saving")}
                </>
              ) : (
                t("candidateProfile.basicInfoForm.save")
              )}
            </button>
          </div>
        )}
      </form>
    </div>
  );
};

export default ProfileBasicInfoForm;