import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import { useTranslation } from 'react-i18next';
import { api } from '../../../lib/api';
import { X, Plus } from 'lucide-react';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card';

interface ProfileSkillsFormProps {
  onSuccess?: () => void;
  showActions?: boolean;
}

// Expose submit method via ref for parent components (e.g., wizard)
export interface ProfileSkillsFormHandle {
  submit: () => Promise<boolean>;
}

const ProfileSkillsForm = forwardRef<ProfileSkillsFormHandle, ProfileSkillsFormProps>(({ onSuccess, showActions = true }, ref) => {
  const { t } = useTranslation();
  const [skills, setSkills] = useState<string[]>([]);
  const [newSkill, setNewSkill] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const profile = await api.getMyProfile() as any;
      setSkills(profile.skills || []);
    } catch (err) {
      console.error('Error loading profile:', err);
      setError(t("candidateProfile.skillsForm.errorLoading"));
    } finally {
      setLoading(false);
    }
  };

  const handleAddSkill = () => {
    const trimmedSkill = newSkill.trim();
    if (trimmedSkill && !skills.includes(trimmedSkill)) {
      setSkills([...skills, trimmedSkill]);
      setNewSkill('');
    }
  };

  const handleRemoveSkill = (skillToRemove: string) => {
    setSkills(skills.filter(skill => skill !== skillToRemove));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddSkill();
    }
  };

  // Core submit logic - returns true on success, false on error
  const submitForm = async (): Promise<boolean> => {
    try {
      setSaving(true);
      setError('');

      // Get current profile to preserve other fields
      const profile = await api.getMyProfile() as any;

      await api.updateMyProfile({
        ...profile,
        skills,
      });

      setSuccess(t("candidateProfile.skillsForm.successMessage"));
      setTimeout(() => setSuccess(''), 3000);
      onSuccess?.();
      return true;
    } catch (err) {
      console.error('Error saving skills:', err);
      setError(t("candidateProfile.skillsForm.errorSaving"));
      return false;
    } finally {
      setSaving(false);
    }
  };

  // Expose submit method to parent via ref
  useImperativeHandle(ref, () => ({
    submit: submitForm
  }));

  const handleSave = async () => {
    await submitForm();
  };

  if (loading) {
    return (
      <Card>
        <CardContent className="py-8">
          <p className="text-center text-gray-500">{t("candidateProfile.skillsForm.loading")}</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t("candidateProfile.skillsForm.title")}</CardTitle>
        <CardDescription>
          {t("candidateProfile.skillsForm.description")}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {success && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
            {success}
          </div>
        )}

        {/* Add skill input */}
        <div className="flex gap-2">
          <Input
            type="text"
            value={newSkill}
            onChange={(e) => setNewSkill(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={t("candidateProfile.skillsForm.placeholder")}
            className="flex-1"
          />
          <Button
            type="button"
            onClick={handleAddSkill}
            disabled={!newSkill.trim()}
            variant="outline"
          >
            <Plus className="w-4 h-4 mr-1" />
            {t("candidateProfile.skillsForm.add")}
          </Button>
        </div>

        {/* Skills list */}
        <div className="flex flex-wrap gap-2">
          {skills.map((skill, index) => (
            <div
              key={index}
              className="flex items-center gap-1 bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
            >
              <span>{skill}</span>
              <button
                type="button"
                onClick={() => handleRemoveSkill(skill)}
                className="hover:text-blue-600 ml-1"
              >
                <X className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>

        {skills.length === 0 && (
          <p className="text-gray-500 text-center py-4">
            {t("candidateProfile.skillsForm.noSkills")}
          </p>
        )}

        {/* Suggestions */}
        <div className="border-t pt-4">
          <p className="text-sm text-gray-600 mb-2">{t("candidateProfile.skillsForm.suggestions")}</p>
          <div className="flex flex-wrap gap-2">
            {['JavaScript', 'Python', 'React', 'SQL', 'Excel', 'Communication', 'Leadership', 'Teamwork']
              .filter(s => !skills.includes(s))
              .slice(0, 6)
              .map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  onClick={() => setSkills([...skills, suggestion])}
                  className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-full text-sm transition-colors"
                >
                  + {suggestion}
                </button>
              ))}
          </div>
        </div>

        {/* Save button */}
        {showActions && (
          <div className="flex justify-end pt-4 border-t">
            <Button
              onClick={handleSave}
              disabled={saving}
            >
              {saving ? t("candidateProfile.skillsForm.saving") : t("candidateProfile.skillsForm.save")}
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
});

ProfileSkillsForm.displayName = 'ProfileSkillsForm';

export default ProfileSkillsForm;
