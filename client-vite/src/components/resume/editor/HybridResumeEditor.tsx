/**
 * Hybrid Resume Editor Component
 *
 * New resume editor that supports the hybrid structure with:
 * - Fixed GeneralData section
 * - Dynamic VariableSection[] with WYSIWYG editing
 * - Legacy compatibility for gradual migration
 */

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Save,
  Eye,
  EyeOff,
  ArrowLeft,
  RotateCcw,
  Clock,
  AlertCircle,
  User,
  Edit3,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import VariableSectionEditor from './VariableSectionEditor';
import ResumePreview from './ResumePreview';
import { api } from '../../../lib/api';
import type { Resume, GeneralData, VariableSection } from '../../../types/resume';

interface HybridResumeEditorProps {
  resumeId: string;
  onBack?: () => void;
  onSave?: (resumeData: Resume) => void;
  className?: string;
}

const HybridResumeEditor: React.FC<HybridResumeEditorProps> = ({
  resumeId,
  onBack,
  onSave,
  className = ''
}) => {
  const { t } = useTranslation();
  const [resumeData, setResumeData] = useState<Resume | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showPreview, setShowPreview] = useState(true);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [generalInfoExpanded, setGeneralInfoExpanded] = useState(false);
  const [editingGeneralInfo, setEditingGeneralInfo] = useState(false);

  const saveTimeoutRef = useRef<NodeJS.Timeout | undefined>(undefined);
  const initialDataRef = useRef<string>('');

  // Load resume data
  useEffect(() => {
    loadResumeData();
  }, [resumeId]);

  // Auto-save functionality
  useEffect(() => {
    if (hasUnsavedChanges && resumeData) {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }

      saveTimeoutRef.current = setTimeout(() => {
        handleAutoSave();
      }, 2000);
    }

    return () => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
    };
  }, [hasUnsavedChanges, resumeData]);

  const loadResumeData = async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await api.getResume(resumeId) as Resume;

      // Convert legacy format to hybrid format if needed
      const hybridData = {
        ...data,
        content: {
          ...data.content,
          // Ensure general_data exists
          general_data: data.content.general_data || {
            cv_title: data.name || 'Professional Resume',
            name: data.content.datos_personales?.name || '',
            email: data.content.datos_personales?.email || '',
            phone: data.content.datos_personales?.phone || ''
          },
          // Ensure variable_sections exists - always create the 4 basic sections
          variable_sections: data.content.variable_sections || [
            {
              key: 'experience',
              title: t('resume.sections.experience'),
              content: data.content.experiencia_profesional || `<p>${t('resume.sections.addExperienceHere')}</p>`,
              order: 1
            },
            {
              key: 'education',
              title: t('resume.sections.education'),
              content: data.content.educacion || `<p>${t('resume.sections.addEducationHere')}</p>`,
              order: 2
            },
            {
              key: 'skills',
              title: t('resume.sections.skills'),
              content: data.content.habilidades || `<ul><li>${t('resume.sections.addSkillsHere')}</li></ul>`,
              order: 3
            },
            {
              key: 'projects',
              title: t('resume.sections.projects'),
              content: data.content.proyectos || `<p>${t('resume.sections.addProjectsHere')}</p>`,
              order: 4
            }
          ],
          // Keep legacy fields for backward compatibility
          experiencia_profesional: data.content.experiencia_profesional || '',
          educacion: data.content.educacion || '',
          proyectos: data.content.proyectos || '',
          habilidades: data.content.habilidades || '',
          datos_personales: data.content.datos_personales || {}
        }
      };

      setResumeData(hybridData);
      initialDataRef.current = JSON.stringify(hybridData);
      setHasUnsavedChanges(false);
    } catch (error) {
      console.error('Error loading resume:', error);
      setError(t('resume.failedToLoadResumeData'));
    } finally {
      setLoading(false);
    }
  };

  const handleAutoSave = async () => {
    if (!resumeData || saving) return;

    try {
      setSaving(true);
      await saveResumeData(false);
    } catch (error) {
      console.error('Auto-save failed:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleManualSave = async () => {
    if (!resumeData || saving) return;

    try {
      setSaving(true);
      await saveResumeData(true);
    } catch (error) {
      setError(t('resume.failedToSaveResume'));
    } finally {
      setSaving(false);
    }
  };

  const saveResumeData = async (isManual: boolean = false) => {
    if (!resumeData) return;

    try {
      // Send the NEW hybrid format since backend expects it
      const saveData = {
        general_data: resumeData.content.general_data || {
          cv_title: resumeData.name || 'Professional Resume',
          name: resumeData.content.datos_personales?.name || '',
          email: resumeData.content.datos_personales?.email || '',
          phone: resumeData.content.datos_personales?.phone || ''
        },
        variable_sections: resumeData.content.variable_sections || [],
        preserve_ai_content: true
      };

      console.log('💾 Saving resume data (NEW FORMAT):', JSON.stringify(saveData, null, 2));

      await api.updateResumeContent(resumeId, saveData);

      setHasUnsavedChanges(false);
      setLastSaved(new Date());

      if (isManual) {
        onSave?.(resumeData);
      }
    } catch (error) {
      throw error;
    }
  };

  const handleDataChange = (newData: Partial<Resume>) => {
    if (!resumeData) return;

    const updatedData = { ...resumeData, ...newData };
    setResumeData(updatedData);

    const currentDataString = JSON.stringify(updatedData);
    setHasUnsavedChanges(currentDataString !== initialDataRef.current);
  };

  const handleGeneralDataChange = (field: keyof GeneralData, value: string) => {
    if (!resumeData) return;

    const updatedGeneralData = {
      ...resumeData.content.general_data,
      [field]: value
    };

    const updatedContent = {
      ...resumeData.content,
      general_data: updatedGeneralData
    };

    handleDataChange({ content: updatedContent });
  };

  const handleUpdateSection = async (key: string, content: string, title?: string) => {
    if (!resumeData) return;

    console.log(`🔧 Updating section: ${key}`, { content: content.substring(0, 100) + '...', title });

    // Ensure variable_sections exists
    const currentSections = resumeData.content.variable_sections || [];

    // Check if section exists, if not create it
    const sectionExists = currentSections.some(section => section.key === key);

    let updatedSections;
    if (sectionExists) {
      // Update existing section
      updatedSections = currentSections.map(section =>
        section.key === key
          ? { ...section, content, ...(title && { title }) }
          : section
      );
    } else {
      // Create new section if it doesn't exist
      const newSection = {
        key,
        title: title || key.charAt(0).toUpperCase() + key.slice(1),
        content,
        order: currentSections.length + 1
      };
      updatedSections = [...currentSections, newSection];
      console.log(`✨ Created new section: ${key}`, newSection);
    }

    // Also update corresponding legacy fields
    const legacyFieldMap: Record<string, keyof typeof resumeData.content> = {
      'experience': 'experiencia_profesional',
      'education': 'educacion',
      'projects': 'proyectos',
      'skills': 'habilidades'
    };

    const updatedContent = {
      ...resumeData.content,
      variable_sections: updatedSections,
      // Update legacy field if it exists
      ...(legacyFieldMap[key] && { [legacyFieldMap[key]]: content })
    };

    handleDataChange({ content: updatedContent });

    console.log(`✅ Section ${key} updated successfully`);
  };

  const handleAddSection = async (key: string, title: string, content: string) => {
    if (!resumeData) return;

    // Add new section to local state
    const newSection = {
      key,
      title,
      content,
      order: (resumeData.content.variable_sections?.length || 0) + 1
    };

    const updatedSections = [...(resumeData.content.variable_sections || []), newSection];

    const updatedContent = {
      ...resumeData.content,
      variable_sections: updatedSections
    };

    handleDataChange({ content: updatedContent });

    // Auto-save will handle persistence
  };

  const handleRemoveSection = async (key: string) => {
    if (!resumeData) return;

    console.log(`🗑️ Removing section: ${key}`);

    // Ensure variable_sections exists
    const currentSections = resumeData.content.variable_sections || [];

    // Check if section exists before removing
    const sectionExists = currentSections.some(section => section.key === key);

    if (!sectionExists) {
      console.warn(`⚠️ Section ${key} not found, cannot remove`);
      return;
    }

    // Update local state
    const updatedSections = currentSections.filter(section => section.key !== key);

    // Also clear corresponding legacy field
    const legacyFieldMap: Record<string, keyof typeof resumeData.content> = {
      'experience': 'experiencia_profesional',
      'education': 'educacion',
      'projects': 'proyectos',
      'skills': 'habilidades'
    };

    const updatedContent = {
      ...resumeData.content,
      variable_sections: updatedSections,
      // Clear legacy field if it exists
      ...(legacyFieldMap[key] && { [legacyFieldMap[key]]: '' })
    };

    handleDataChange({ content: updatedContent });

    console.log(`✅ Section ${key} removed successfully`);
  };

  const handleReorderSections = async (sectionsOrder: Array<{key: string; order: number}>) => {
    if (!resumeData) return;

    console.log(`🔄 Reordering sections:`, sectionsOrder);

    // Ensure variable_sections exists
    const currentSections = resumeData.content.variable_sections || [];

    if (currentSections.length === 0) {
      console.warn(`⚠️ No sections to reorder`);
      return;
    }

    // Update local state
    const sectionMap = new Map(currentSections.map(s => [s.key, s]));
    const updatedSections = sectionsOrder
      .map(({ key, order }) => {
        const section = sectionMap.get(key);
        if (!section) {
          console.warn(`⚠️ Section ${key} not found during reorder, skipping`);
          return null;
        }
        return { ...section, order };
      })
      .filter(Boolean) as VariableSection[];

    const updatedContent = {
      ...resumeData.content,
      variable_sections: updatedSections
    };

    handleDataChange({ content: updatedContent });

    console.log(`✅ Sections reordered successfully`);
  };

  const handleRevertChanges = () => {
    if (initialDataRef.current) {
      const originalData = JSON.parse(initialDataRef.current);
      setResumeData(originalData);
      setHasUnsavedChanges(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">{t('resume.loadingEditor')}</p>
        </div>
      </div>
    );
  }

  if (error || !resumeData) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 mb-4">{error || t('resume.resumeNotFound')}</p>
          <button
            onClick={loadResumeData}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            {t('resume.tryAgain')}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen bg-gray-50 ${className}`}>
      {/* Editor Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Left side */}
            <div className="flex items-center gap-4">
              {onBack && (
                <button
                  onClick={onBack}
                  className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
                >
                  <ArrowLeft className="w-5 h-5" />
                </button>
              )}

              <div>
                <h1 className="text-lg font-semibold text-gray-900">{resumeData.name}</h1>
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span className="capitalize">{resumeData.resume_type.toLowerCase()} • {resumeData.status}</span>
                  {lastSaved && (
                    <div className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {t('common.lastSaved')}: {lastSaved.toLocaleTimeString()}
                    </div>
                  )}
                  {hasUnsavedChanges && (
                    <span className="text-orange-600">{t('common.unsavedChanges')}</span>
                  )}
                  {saving && (
                    <div className="flex items-center gap-1">
                      <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-blue-600"></div>
                      {t('common.saving')}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Right side */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowPreview(!showPreview)}
                className={`p-2 rounded-lg transition-colors ${
                  showPreview ? 'bg-blue-100 text-blue-600' : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
                }`}
                title={showPreview ? t('resume.hidePreview') : t('resume.showPreview')}
              >
                {showPreview ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>

              {hasUnsavedChanges && (
                <button
                  onClick={handleRevertChanges}
                  className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
                  title={t('resume.revertChanges')}
                >
                  <RotateCcw className="w-5 h-5" />
                </button>
              )}

              <button
                onClick={handleManualSave}
                disabled={saving || !hasUnsavedChanges}
                className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Save className="w-4 h-4 mr-2" />
                {saving ? t('common.saving') : t('common.save')}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Editor Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className={`grid gap-8 ${showPreview ? 'lg:grid-cols-2' : 'grid-cols-1'}`}>
          {/* Editor Panel */}
          <div className="space-y-4">
            {/* General Information Section - Collapsible */}
            <motion.div
              layout
              className="bg-white border border-gray-200 rounded-lg overflow-hidden"
            >
              {/* General Information Header */}
              <div className="flex items-center justify-between p-4 bg-gray-50 border-b border-gray-200">
                <div className="flex items-center gap-3">
                  <User className="w-5 h-5 text-gray-600" />
                  <h4 className="font-medium text-gray-900">{t('resume.generalInformation')}</h4>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => {
                      setEditingGeneralInfo(!editingGeneralInfo);
                      // Auto-expand when clicking pencil to edit
                      if (!editingGeneralInfo) {
                        setGeneralInfoExpanded(true);
                      }
                    }}
                    className="p-1 text-gray-400 hover:text-gray-600"
                    title={t('resume.editGeneralInfo')}
                  >
                    <Edit3 className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setGeneralInfoExpanded(!generalInfoExpanded)}
                    className="p-1 text-gray-400 hover:text-gray-600"
                  >
                    {generalInfoExpanded ? (
                      <ChevronUp className="w-4 h-4" />
                    ) : (
                      <ChevronDown className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>

              {/* General Information Content */}
              <AnimatePresence>
                {generalInfoExpanded && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.3 }}
                    className="p-4"
                  >
                    {editingGeneralInfo ? (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="md:col-span-2">
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            {t('resume.cvTitle')}
                          </label>
                          <input
                            type="text"
                            value={resumeData.content.general_data.cv_title || ''}
                            onChange={(e) => handleGeneralDataChange('cv_title', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder={t('resume.cvTitlePlaceholder')}
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            {t('resume.fullName')}
                          </label>
                          <input
                            type="text"
                            value={resumeData.content.general_data.name || ''}
                            onChange={(e) => handleGeneralDataChange('name', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            {t('common.email')}
                          </label>
                          <input
                            type="email"
                            value={resumeData.content.general_data.email || ''}
                            onChange={(e) => handleGeneralDataChange('email', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            {t('common.phone')}
                          </label>
                          <input
                            type="tel"
                            value={resumeData.content.general_data.phone || ''}
                            onChange={(e) => handleGeneralDataChange('phone', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>
                      </div>
                    ) : (
                      <div className="space-y-2 text-sm text-gray-600">
                        <p><strong>{t('resume.cvTitle')}:</strong> {resumeData.content.general_data.cv_title || t('resume.noTitleSet')}</p>
                        <p><strong>{t('common.name')}:</strong> {resumeData.content.general_data.name || t('resume.noNameSet')}</p>
                        <p><strong>{t('common.email')}:</strong> {resumeData.content.general_data.email || t('resume.noEmailSet')}</p>
                        <p><strong>{t('common.phone')}:</strong> {resumeData.content.general_data.phone || t('resume.noPhoneSet')}</p>
                      </div>
                    )}
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>

            {/* Variable Sections */}
            <VariableSectionEditor
              sections={resumeData.content.variable_sections}
              onUpdateSection={handleUpdateSection}
              onAddSection={handleAddSection}
              onRemoveSection={handleRemoveSection}
              onReorderSections={handleReorderSections}
              disabled={saving}
            />
          </div>

          {/* Preview Panel */}
          {showPreview && (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="lg:sticky lg:top-24 lg:h-fit"
            >
              <ResumePreview
                resumeData={resumeData}
                template={(resumeData.formatting_preferences?.template as 'professional' | 'modern' | 'minimal' | 'creative') || 'professional'}
                onTemplateChange={(template) => {
                  const updatedFormatting = {
                    ...resumeData.formatting_preferences,
                    template
                  };
                  handleDataChange({ formatting_preferences: updatedFormatting });
                }}
                onExport={() => {
                  // Export functionality
                  window.open(`/candidate/profile/resumes/${resumeId}/export`, '_blank');
                }}
                onShare={() => {
                  // Share functionality
                  const shareUrl = `${window.location.origin}/candidate/profile/resumes/${resumeId}/preview`;
                  navigator.clipboard.writeText(shareUrl);
                }}
              />
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HybridResumeEditor;