import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import { useTranslation } from 'react-i18next';
import { Loader2 } from 'lucide-react';
import { api } from '../../../lib/api';
import LanguageSelector, { type Language, convertLanguagesFromBackend, convertLanguagesToBackend } from '../../common/LanguageSelector';
import RoleSelector, { type Role, convertRolesFromBackend, convertRolesToBackend } from '../../common/RoleSelector';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';

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

// Expose submit method via ref for parent components (e.g., wizard)
export interface ProfileBasicInfoFormHandle {
  submit: () => Promise<boolean>;
}

const ProfileBasicInfoForm = forwardRef<ProfileBasicInfoFormHandle, ProfileBasicInfoFormProps>(({
  initialData,
  onSave,
  onCancel,
  showActions = true,
  className = ""
}, ref) => {
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

  // Core submit logic - returns true on success, false on error
  const submitForm = async (): Promise<boolean> => {
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

      await api.updateMyProfile(profileData);
      setSuccess(t("candidateProfile.basicInfoForm.successMessage"));

      if (onSave) {
        await onSave(profileData);
      }
      return true;
    } catch (error) {
      let errorMessage = t("candidateProfile.basicInfoForm.errorMessage");
      if (error instanceof Error) {
        if (error.message.includes("API Error:")) {
          errorMessage = error.message.replace(/^API Error: \d+ [^:]*: ?/, "");
        } else if (error.message && error.message !== "Failed to fetch") {
          errorMessage = error.message;
        }
      }

      setError(errorMessage);
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  // Expose submit method to parent via ref
  useImperativeHandle(ref, () => ({
    submit: submitForm
  }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await submitForm();
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
          <Alert className="bg-green-50 border-green-200">
            <AlertDescription className="text-green-800">{success}</AlertDescription>
          </Alert>
        )}

        {/* Error Message */}
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Form Fields - Grid de dos columnas para desktop, una columna para móvil */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <Label htmlFor="name">{t("candidateProfile.basicInfoForm.fullName")}</Label>
            <Input
              name="name"
              id="name"
              type="text"
              required
              value={formData.name}
              onChange={handleChange}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="dateOfBirth">{t("candidateProfile.basicInfoForm.dateOfBirth")}</Label>
            <Input
              name="dateOfBirth"
              id="dateOfBirth"
              type="date"
              required
              value={formData.dateOfBirth}
              onChange={handleChange}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="city">{t("candidateProfile.basicInfoForm.city")}</Label>
            <Input
              name="city"
              id="city"
              type="text"
              required
              value={formData.city}
              onChange={handleChange}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="country">{t("candidateProfile.basicInfoForm.country")}</Label>
            <Input
              name="country"
              id="country"
              type="text"
              required
              value={formData.country}
              onChange={handleChange}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="phone">{t("candidateProfile.basicInfoForm.phone")}</Label>
            <Input
              name="phone"
              id="phone"
              type="tel"
              required
              value={formData.phone}
              onChange={handleChange}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="jobCategory">{t("candidateProfile.basicInfoForm.jobCategory")}</Label>
            <Select
              value={formData.jobCategory}
              onValueChange={(value) => setFormData(prev => ({ ...prev, jobCategory: value }))}
            >
              <SelectTrigger>
                <SelectValue placeholder={t("candidateProfile.basicInfoForm.selectCategory")} />
              </SelectTrigger>
              <SelectContent>
                {JOB_CATEGORY_KEYS.map((key) => (
                  <SelectItem key={key} value={key}>
                    {t(`candidateProfile.jobCategories.${key}`)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Email ocupa toda la fila */}
        <div className="space-y-2">
          <Label htmlFor="email">{t("candidateProfile.basicInfoForm.email")}</Label>
          <Input
            name="email"
            id="email"
            type="email"
            required
            value={formData.email}
            readOnly
            className="bg-muted cursor-not-allowed"
          />
          <p className="text-xs text-muted-foreground">{t("candidateProfile.basicInfoForm.emailReadOnly")}</p>
        </div>

        {/* Campos adicionales - Grid de dos columnas */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <Label htmlFor="expectedAnnualSalary">{t("candidateProfile.basicInfoForm.expectedSalary")}</Label>
            <Input
              name="expectedAnnualSalary"
              id="expectedAnnualSalary"
              type="number"
              value={formData.expectedAnnualSalary}
              onChange={handleChange}
              placeholder={t("candidateProfile.basicInfoForm.salaryPlaceholder")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="currentAnnualSalary">{t("candidateProfile.basicInfoForm.currentSalary")}</Label>
            <Input
              name="currentAnnualSalary"
              id="currentAnnualSalary"
              type="number"
              value={formData.currentAnnualSalary}
              onChange={handleChange}
              placeholder={t("candidateProfile.basicInfoForm.salaryPlaceholder")}
            />
          </div>
        </div>

        {/* Modalidad de trabajo */}
        <div className="space-y-2">
          <Label>{t("candidateProfile.basicInfoForm.workModality")}</Label>
          <div className="space-y-3">
            {Object.values(WorkModalityEnum).map((key) => (
              <div key={key} className="flex items-center space-x-2">
                <Checkbox
                  id={`modality-${key}`}
                  checked={formData.workModality.includes(key)}
                  onCheckedChange={(checked) => {
                    if (checked) {
                      setFormData(prev => ({ ...prev, workModality: [...prev.workModality, key] }));
                    } else {
                      setFormData(prev => ({ ...prev, workModality: prev.workModality.filter(m => m !== key) }));
                    }
                  }}
                />
                <label htmlFor={`modality-${key}`} className="text-sm text-foreground cursor-pointer">
                  {key === 'remote' ? t("candidateProfile.basicInfoForm.remote") :
                   key === 'on_site' ? t("candidateProfile.basicInfoForm.onSite") :
                   t("candidateProfile.basicInfoForm.hybrid")}
                </label>
              </div>
            ))}
          </div>
        </div>

        {/* Disponibilidad para reubicación */}
        <div className="flex items-center space-x-2">
          <Checkbox
            id="relocation"
            checked={formData.relocation}
            onCheckedChange={(checked) => setFormData(prev => ({ ...prev, relocation: checked === true }))}
          />
          <label htmlFor="relocation" className="text-sm text-foreground cursor-pointer">
            {t("candidateProfile.basicInfoForm.relocation")}
          </label>
        </div>

        {/* Idiomas */}
        <LanguageSelector
          languages={formData.languages}
          onChange={(languages) => setFormData(prev => ({ ...prev, languages }))}
        />

        {/* Habilidades */}
        <div className="space-y-2">
          <Label htmlFor="skills">{t("candidateProfile.basicInfoForm.skills")}</Label>
          <Textarea
            name="skills"
            id="skills"
            rows={3}
            value={formData.skills.join(', ')}
            onChange={(e) => {
              const skillsArray = e.target.value.split(',').map(skill => skill.trim()).filter(skill => skill);
              setFormData(prev => ({ ...prev, skills: skillsArray }));
            }}
            placeholder={t("candidateProfile.basicInfoForm.skillsPlaceholder")}
          />
          <p className="text-xs text-muted-foreground">{t("candidateProfile.basicInfoForm.skillsHint")}</p>
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
              <Button type="button" variant="outline" onClick={onCancel}>
                {t("candidateProfile.basicInfoForm.cancel")}
              </Button>
            )}
            <Button
              type="submit"
              disabled={isLoading || !formData.name || !formData.email || !formData.dateOfBirth}
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  {t("candidateProfile.basicInfoForm.saving")}
                </>
              ) : (
                t("candidateProfile.basicInfoForm.save")
              )}
            </Button>
          </div>
        )}
      </form>
    </div>
  );
});

ProfileBasicInfoForm.displayName = 'ProfileBasicInfoForm';

export default ProfileBasicInfoForm;
