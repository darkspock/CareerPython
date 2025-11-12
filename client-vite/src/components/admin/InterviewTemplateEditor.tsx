import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ArrowLeft, Plus, ChevronUp, ChevronDown, Edit, MessageSquare, Power, PowerOff, Trash2, X, FileText } from 'lucide-react';
import { api } from '../../lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';

interface InterviewTemplate {
  id: string;
  name: string;
  intro?: string;
  prompt?: string;
  goal?: string;
  status: 'ENABLED' | 'DRAFT' | 'DISABLED';
  type: 'EXTENDED_PROFILE' | 'POSITION_INTERVIEW';
  job_category: string | null;
  tags?: string[];
  allow_ai_questions?: boolean;
  legal_notice?: string;
  sections?: InterviewTemplateSection[];
}

interface InterviewTemplateSection {
  id: string;
  interview_template_id: string;
  name: string;
  intro: string;
  prompt: string;
  goal: string;
  section?: 'EXPERIENCE' | 'EDUCATION' | 'PROJECT' | 'SOFT_SKILL' | 'GENERAL';
  sort_order: number;
  status: 'ENABLED' | 'DRAFT' | 'DISABLED';
  allow_ai_questions?: boolean;
  allow_ai_override_questions?: boolean;
  legal_notice?: string;
}

const InterviewTemplateEditor: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { templateId } = useParams<{ templateId?: string }>();
  const isEditing = !!templateId;
  
  // Only company context - admin doesn't have templates
  const basePath = '/company/interview-templates';
  const apiBasePath = '/api/company/interview-templates';

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  // Form state
  const [formData, setFormData] = useState<{
    name: string;
    intro: string;
    prompt: string;
    goal: string;
    type: 'EXTENDED_PROFILE' | 'POSITION_INTERVIEW';
    job_category: string | null;
    tags: string[];
    allow_ai_questions: boolean;
    legal_notice: string;
  }>({
    name: '',
    intro: '',
    prompt: '',
    goal: '',
    type: 'EXTENDED_PROFILE',
    job_category: null,
    tags: [],
    allow_ai_questions: false,
    legal_notice: ''
  });

  // Sections state
  const [sections, setSections] = useState<InterviewTemplateSection[]>([]);
  const [editingSection, setEditingSection] = useState<InterviewTemplateSection | null>(null);
  const [showSectionForm, setShowSectionForm] = useState(false);

  // Questions state
  const [editingQuestions, setEditingQuestions] = useState<InterviewTemplateSection | null>(null);
  const [showQuestionsModal, setShowQuestionsModal] = useState(false);

  const templateTypes = [
    { value: 'EXTENDED_PROFILE', label: t('company.interviewTemplateEditor.templateTypes.EXTENDED_PROFILE') },
    { value: 'POSITION_INTERVIEW', label: t('company.interviewTemplateEditor.templateTypes.POSITION_INTERVIEW') }
  ];

  const jobCategories = [
    { value: 'all', label: t('company.interviewTemplateEditor.jobCategories.all') },
    { value: 'Technology', label: t('company.interviewTemplateEditor.jobCategories.Technology') },
    { value: 'Operations', label: t('company.interviewTemplateEditor.jobCategories.Operations') },
    { value: 'Sales', label: t('company.interviewTemplateEditor.jobCategories.Sales') },
    { value: 'Marketing', label: t('company.interviewTemplateEditor.jobCategories.Marketing') },
    { value: 'Administration', label: t('company.interviewTemplateEditor.jobCategories.Administration') },
    { value: 'Human Resources', label: t('company.interviewTemplateEditor.jobCategories.Human Resources') },
    { value: 'Finance', label: t('company.interviewTemplateEditor.jobCategories.Finance') },
    { value: 'Customer Service', label: t('company.interviewTemplateEditor.jobCategories.Customer Service') },
    { value: 'Other', label: t('company.interviewTemplateEditor.jobCategories.Other') }
  ];

  useEffect(() => {
    if (isEditing && templateId) {
      fetchTemplate();
    }
  }, [templateId, isEditing]);

  const fetchTemplate = async () => {
    try {
      setLoading(true);
      setError(null);
      const template = await api.authenticatedRequest<InterviewTemplate>(`${apiBasePath}/${templateId}`);
      setFormData({
        name: template.name,
        intro: template.intro || '',
        prompt: template.prompt || '',
        goal: template.goal || '',
        type: template.type,
        job_category: template.job_category ?? null,
        tags: template.tags || [],
        allow_ai_questions: template.allow_ai_questions || false,
        legal_notice: template.legal_notice || ''
      });

      // Load sections if template has them
      if (template.sections) {
        // Sort sections by sort_order to ensure proper display order
        const sortedSections = [...template.sections].sort((a, b) => a.sort_order - b.sort_order);
        setSections(sortedSections);
      }
    } catch (err: any) {
      setError(err.message || t('company.interviewTemplateEditor.errors.loadTemplate'));
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSaving(true);
      setError(null);

      // Save template data (template + sections will be handled by backend)
      // Convert "all" to null for job_category
      const templateDataWithSections = {
        ...formData,
        job_category: formData.job_category === 'all' || formData.job_category === null ? null : formData.job_category,
        sections: sections
      };

      if (isEditing) {
        await api.authenticatedRequest(`${apiBasePath}/${templateId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(templateDataWithSections)
        });
      } else {
        await api.authenticatedRequest(apiBasePath, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(templateDataWithSections)
        });
      }

      navigate(basePath);
    } catch (err: any) {
      setError(err.message || t('company.interviewTemplateEditor.errors.saveTemplate'));
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    navigate(basePath);
  };

  // Section management functions
  const handleAddSection = () => {
    setEditingSection(null);
    setShowSectionForm(true);
  };

  const handleEditSection = (section: InterviewTemplateSection) => {
    setEditingSection(section);
    setShowSectionForm(true);
  };

  const handleDeleteSection = async (sectionId: string) => {
    if (confirm(t('company.interviewTemplateEditor.confirmations.deleteSection'))) {
      try {
        // If it's a real section (not temp), call API to delete
        if (!sectionId.startsWith('temp-')) {
          try {
            await api.authenticatedRequest(`/api/company/interview-templates/sections/${sectionId}`, {
              method: 'DELETE',
              headers: { 'Content-Type': 'application/json' }
            });
          } catch (err) {
            console.warn('Failed to delete section via API, removing locally');
          }
        }

        setSections(sections.filter(s => s.id !== sectionId));
      } catch (err: any) {
        setError(err.message || t('company.interviewTemplateEditor.errors.deleteSection'));
      }
    }
  };

  const handleSaveSection = async (sectionData: Omit<InterviewTemplateSection, 'id' | 'interview_template_id'>) => {
    try {
      if (editingSection) {
        // Update existing section - if it's a real section, call API
        if (!editingSection.id.startsWith('temp-')) {
          try {
            await api.authenticatedRequest(`/api/company/interview-templates/sections/${editingSection.id}`, {
              method: 'PUT',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(sectionData)
            });
          } catch (err) {
            // If API fails, update locally for now
            console.warn('Failed to update section via API, updating locally');
          }
        }

        const updatedSection = { ...editingSection, ...sectionData };
        setSections(sections.map(s => s.id === editingSection.id ? updatedSection : s));
      } else {
        // Add new section - calculate next sort_order
        const nextSortOrder = sections.length > 0 ? Math.max(...sections.map(s => s.sort_order)) + 1 : 0;
        const sectionDataWithOrder = {
          ...sectionData,
          sort_order: nextSortOrder
        };

        let newSection: InterviewTemplateSection;

        if (templateId) {
          try {
            const createdSection = await api.authenticatedRequest<InterviewTemplateSection>('/api/company/interview-templates/sections', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                ...sectionDataWithOrder,
                interview_template_id: templateId
              })
            });
            newSection = createdSection;
          } catch (err) {
            // If API fails, create locally with temp ID
            console.warn('Failed to create section via API, creating locally');
            newSection = {
              id: `temp-${Date.now()}`,
              interview_template_id: templateId,
              ...sectionDataWithOrder
            };
          }
        } else {
          // No template ID yet, create with temp ID
          newSection = {
            id: `temp-${Date.now()}`,
            interview_template_id: '',
            ...sectionDataWithOrder
          };
        }

        setSections([...sections, newSection]);
      }
      setShowSectionForm(false);
      setEditingSection(null);
    } catch (err: any) {
      setError(err.message || t('company.interviewTemplateEditor.errors.saveSection'));
    }
  };

  const handleCancelSectionForm = () => {
    setShowSectionForm(false);
    setEditingSection(null);
  };

  // Questions management functions
  const handleEditQuestions = (section: InterviewTemplateSection) => {
    setEditingQuestions(section);
    setShowQuestionsModal(true);
  };

  const handleCancelQuestionsModal = () => {
    setShowQuestionsModal(false);
    setEditingQuestions(null);
  };

  const handleEnableSection = async (sectionId: string) => {
    try {
      // If it's a real section (not temp), call API to enable
      if (!sectionId.startsWith('temp-')) {
        try {
          await api.authenticatedRequest(`${apiBasePath}/sections/${sectionId}/enable`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
          });
        } catch (err) {
          console.warn('Failed to enable section via API, updating locally');
        }
      }

      // Update local state
      setSections(sections.map(s => s.id === sectionId ? { ...s, status: 'ENABLED' } : s));
    } catch (err: any) {
      setError(err.message || t('company.interviewTemplateEditor.errors.enableSection'));
    }
  };

  const handleDisableSection = async (sectionId: string) => {
    if (!confirm(t('company.interviewTemplateEditor.confirmations.disableSection'))) return;

    try {
      // If it's a real section (not temp), call API to disable
      if (!sectionId.startsWith('temp-')) {
        try {
          await api.authenticatedRequest(`${apiBasePath}/sections/${sectionId}/disable`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
          });
        } catch (err) {
          console.warn('Failed to disable section via API, updating locally');
        }
      }

      // Update local state
      setSections(sections.map(s => s.id === sectionId ? { ...s, status: 'DISABLED' } : s));
    } catch (err: any) {
      setError(err.message || t('company.interviewTemplateEditor.errors.disableSection'));
    }
  };

  const handleMoveSectionUp = async (sectionId: string) => {
    try {
      // If it's a real section (not temp), call API
      if (!sectionId.startsWith('temp-')) {
        try {
          await api.authenticatedRequest(`${apiBasePath}/sections/${sectionId}/move-up`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
          });
          // Refresh the template data to get the updated order
          if (templateId) {
            const template = await api.authenticatedRequest<InterviewTemplate>(`${apiBasePath}/${templateId}`);
            const sortedSections = template.sections ? [...template.sections].sort((a, b) => a.sort_order - b.sort_order) : [];
            setSections(sortedSections);
          }
        } catch (err) {
          console.error('Failed to move section up via API:', err);
        }
      } else {
        // Handle temp sections locally
        const currentIndex = sections.findIndex(s => s.id === sectionId);
        if (currentIndex > 0) {
          const newSections = [...sections];
          [newSections[currentIndex - 1], newSections[currentIndex]] = [newSections[currentIndex], newSections[currentIndex - 1]];
          setSections(newSections);
        }
      }
    } catch (err: any) {
      setError(err.message || t('company.interviewTemplateEditor.errors.moveSectionUp'));
    }
  };

  const handleMoveSectionDown = async (sectionId: string) => {
    try {
      // If it's a real section (not temp), call API
      if (!sectionId.startsWith('temp-')) {
        try {
          await api.authenticatedRequest(`${apiBasePath}/sections/${sectionId}/move-down`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
          });
          // Refresh the template data to get the updated order
          if (templateId) {
            const template = await api.authenticatedRequest<InterviewTemplate>(`${apiBasePath}/${templateId}`);
            const sortedSections = template.sections ? [...template.sections].sort((a, b) => a.sort_order - b.sort_order) : [];
            setSections(sortedSections);
          }
        } catch (err) {
          console.error('Failed to move section down via API:', err);
        }
      } else {
        // Handle temp sections locally
        const currentIndex = sections.findIndex(s => s.id === sectionId);
        if (currentIndex < sections.length - 1) {
          const newSections = [...sections];
          [newSections[currentIndex], newSections[currentIndex + 1]] = [newSections[currentIndex + 1], newSections[currentIndex]];
          setSections(newSections);
        }
      }
    } catch (err: any) {
      setError(err.message || t('company.interviewTemplateEditor.errors.moveSectionDown'));
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <TooltipProvider>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center space-x-4">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={handleCancel}
                  title="Back to templates"
                >
                  <ArrowLeft className="w-6 h-6" />
                </Button>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    {isEditing ? t('company.interviewTemplateEditor.title.edit') : t('company.interviewTemplateEditor.title.create')}
                  </h1>
                  <p className="text-sm text-gray-500">
                    {isEditing ? t('company.interviewTemplateEditor.subtitle.edit') : t('company.interviewTemplateEditor.subtitle.create')}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Button variant="outline" onClick={handleCancel}>
                  {t('company.interviewTemplateEditor.buttons.cancel')}
                </Button>
                <Button onClick={handleSave} disabled={saving}>
                  {saving ? t('company.interviewTemplateEditor.buttons.save') : (isEditing ? t('company.interviewTemplateEditor.buttons.update') : t('company.interviewTemplateEditor.buttons.create'))}
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Error Alert */}
          {error && (
            <Alert variant="destructive" className="mb-6">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription className="flex items-center justify-between">
                <span>{error}</span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setError(null)}
                  className="h-auto p-0 ml-2"
                >
                  <X className="h-4 w-4" />
                </Button>
              </AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleSave} className="space-y-8">
            {/* Basic Information */}
            <Card>
              <CardHeader>
                <CardTitle>{t('company.interviewTemplateEditor.sections.basicInfo')}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="lg:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">{t('company.interviewTemplateEditor.fields.templateName')} *</label>
                    <Input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      placeholder={t('company.interviewTemplateEditor.placeholders.templateName')}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">{t('company.interviewTemplateEditor.fields.visibility')}</label>
                    <Select
                      value={formData.type}
                      onValueChange={(value) => setFormData({ ...formData, type: value as 'EXTENDED_PROFILE' | 'POSITION_INTERVIEW' })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {templateTypes.map(type => (
                          <SelectItem key={type.value} value={type.value}>{type.label}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">{t('company.interviewTemplateEditor.fields.jobCategory')}</label>
                    <Select
                      value={formData.job_category || 'all'}
                      onValueChange={(value) => setFormData({ ...formData, job_category: value === 'all' ? null : value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {jobCategories.map(category => (
                          <SelectItem key={category.value} value={category.value}>{category.label}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">{t('company.interviewTemplateEditor.fields.tags')}</label>
                    <Input
                      type="text"
                      value={formData.tags.join(', ')}
                      onChange={(e) => setFormData({ ...formData, tags: e.target.value.split(', ').filter(tag => tag.trim() !== '') })}
                      placeholder={t('company.interviewTemplateEditor.placeholders.tags')}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Content */}
            <Card>
              <CardHeader>
                <CardTitle>{t('company.interviewTemplateEditor.sections.content')}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">{t('company.interviewTemplateEditor.fields.introduction')}</label>
                  <Textarea
                    value={formData.intro}
                    onChange={(e) => setFormData({ ...formData, intro: e.target.value })}
                    rows={4}
                    placeholder={t('company.interviewTemplateEditor.placeholders.introduction')}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">{t('company.interviewTemplateEditor.fields.goal')}</label>
                  <Textarea
                    value={formData.goal}
                    onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
                    rows={4}
                    placeholder={t('company.interviewTemplateEditor.placeholders.goal')}
                  />
                </div>
                <div>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="allow_ai_questions"
                      checked={formData.allow_ai_questions}
                      onCheckedChange={(checked) => setFormData({ ...formData, allow_ai_questions: checked === true })}
                    />
                    <label
                      htmlFor="allow_ai_questions"
                      className="text-sm font-medium text-gray-700 cursor-pointer"
                    >
                      {t('company.interviewTemplateEditor.labels.allowAIQuestions')}
                    </label>
                  </div>
                  <p className="mt-1 text-xs text-gray-500 ml-6">
                    {t('company.interviewTemplateEditor.labels.allowAIQuestionsDescription')}
                  </p>
                </div>
                {formData.allow_ai_questions && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">{t('company.interviewTemplateEditor.fields.aiPrompt')}</label>
                    <Textarea
                      value={formData.prompt}
                      onChange={(e) => setFormData({ ...formData, prompt: e.target.value })}
                      className="font-mono text-sm"
                      rows={12}
                      placeholder={t('company.interviewTemplateEditor.placeholders.aiPrompt')}
                    />
                  </div>
                )}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">{t('company.interviewTemplateEditor.fields.legalNotice')}</label>
                  <Textarea
                    value={formData.legal_notice}
                    onChange={(e) => setFormData({ ...formData, legal_notice: e.target.value })}
                    rows={4}
                    placeholder={t('company.interviewTemplateEditor.placeholders.legalNotice')}
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    {t('company.interviewTemplateEditor.labels.legalNoticeDescription')}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Template Sections */}
            <Card>
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle>{t('company.interviewTemplateEditor.sections.templateSections')}</CardTitle>
                  <Button
                    type="button"
                    onClick={handleAddSection}
                    className="flex items-center gap-2"
                  >
                    <Plus className="w-4 h-4" />
                    {t('company.interviewTemplateEditor.sectionsList.addSection')}
                  </Button>
                </div>
              </CardHeader>
              <CardContent>

                {/* Sections List */}
                <div className="space-y-4">
                  {sections.map((section, index) => (
                    <Card key={section.id}>
                      <CardContent className="pt-6">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                              <h3 className="font-medium text-gray-900">{section.name}</h3>
                              <Badge variant={
                                section.status === 'ENABLED' ? 'default' :
                                section.status === 'DRAFT' ? 'secondary' : 'destructive'
                              }>
                                {section.status}
                              </Badge>
                              {section.section && (
                                <Badge variant="outline">{section.section}</Badge>
                              )}
                            </div>
                            <p className="text-sm text-gray-600 mb-2">{section.intro}</p>
                            <p className="text-xs text-gray-500">{section.goal}</p>
                          </div>
                          <div className="flex items-center space-x-2 ml-4">
                            {/* Move up/down buttons */}
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button
                                  type="button"
                                  variant="ghost"
                                  size="icon"
                                  onClick={() => handleMoveSectionUp(section.id)}
                                  disabled={index === 0}
                                >
                                  <ChevronUp className="w-4 h-4" />
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                {index === 0 ? "Already at the top" : "Move section up in the list"}
                              </TooltipContent>
                            </Tooltip>

                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button
                                  type="button"
                                  variant="ghost"
                                  size="icon"
                                  onClick={() => handleMoveSectionDown(section.id)}
                                  disabled={index >= sections.length - 1}
                                >
                                  <ChevronDown className="w-4 h-4" />
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                {index >= sections.length - 1 ? "Already at the bottom" : "Move section down in the list"}
                              </TooltipContent>
                            </Tooltip>

                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button
                                  type="button"
                                  variant="ghost"
                                  size="icon"
                                  onClick={() => handleEditSection(section)}
                                >
                                  <Edit className="w-4 h-4" />
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>Edit section details, intro, and goals</TooltipContent>
                            </Tooltip>

                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button
                                  type="button"
                                  variant="ghost"
                                  size="icon"
                                  onClick={() => handleEditQuestions(section)}
                                >
                                  <MessageSquare className="w-4 h-4" />
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>Manage questions for this section</TooltipContent>
                            </Tooltip>

                            {/* Enable/Disable buttons */}
                            {section.status === 'ENABLED' ? (
                              <Tooltip>
                                <TooltipTrigger asChild>
                                  <Button
                                    type="button"
                                    variant="ghost"
                                    size="icon"
                                    onClick={() => handleDisableSection(section.id)}
                                  >
                                    <PowerOff className="w-4 h-4" />
                                  </Button>
                                </TooltipTrigger>
                                <TooltipContent>Disable section - it won't be used in interviews</TooltipContent>
                              </Tooltip>
                            ) : (
                              <Tooltip>
                                <TooltipTrigger asChild>
                                  <Button
                                    type="button"
                                    variant="ghost"
                                    size="icon"
                                    onClick={() => handleEnableSection(section.id)}
                                  >
                                    <Power className="w-4 h-4" />
                                  </Button>
                                </TooltipTrigger>
                                <TooltipContent>Enable section - make it active for interviews</TooltipContent>
                              </Tooltip>
                            )}

                            {/* Delete button - only show when section is disabled */}
                            {section.status === 'DISABLED' && (
                              <Tooltip>
                                <TooltipTrigger asChild>
                                  <Button
                                    type="button"
                                    variant="ghost"
                                    size="icon"
                                    onClick={() => handleDeleteSection(section.id)}
                                  >
                                    <Trash2 className="w-4 h-4" />
                                  </Button>
                                </TooltipTrigger>
                                <TooltipContent>Permanently delete this section and all its questions</TooltipContent>
                              </Tooltip>
                            )}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}

                  {sections.length === 0 && (
                    <div className="text-center py-8 text-gray-500">
                      <FileText className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                      <p>No sections added yet</p>
                      <p className="text-sm">Click "Add Section" to create your first section</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </form>

          {/* Section Form Modal */}
          <Dialog open={showSectionForm} onOpenChange={(open) => !open && handleCancelSectionForm()}>
            <SectionFormModal
              section={editingSection}
              onSave={handleSaveSection}
              onCancel={handleCancelSectionForm}
            />
          </Dialog>

          {/* Questions Modal */}
          <Dialog open={showQuestionsModal} onOpenChange={(open) => !open && handleCancelQuestionsModal()}>
            {editingQuestions && (
              <QuestionsModal
                section={editingQuestions}
                onClose={handleCancelQuestionsModal}
                apiBasePath={apiBasePath}
              />
            )}
          </Dialog>
        </div>
      </div>
    </TooltipProvider>
  );
};

// Section Form Modal Component
interface SectionFormModalProps {
  section: InterviewTemplateSection | null;
  onSave: (sectionData: Omit<InterviewTemplateSection, 'id' | 'interview_template_id'>) => void;
  onCancel: () => void;
}

const SectionFormModal: React.FC<SectionFormModalProps> = ({ section, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    name: section?.name || '',
    intro: section?.intro || '',
    prompt: section?.prompt || '',
    goal: section?.goal || '',
    section: section?.section || 'GENERAL' as 'EXPERIENCE' | 'EDUCATION' | 'PROJECT' | 'SOFT_SKILL' | 'GENERAL',
    sort_order: section?.sort_order || 0,
    status: section?.status || 'DRAFT' as 'ENABLED' | 'DRAFT' | 'DISABLED',
    allow_ai_questions: section?.allow_ai_questions || false,
    allow_ai_override_questions: section?.allow_ai_override_questions || false,
    legal_notice: section?.legal_notice || ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);
  };


  const sectionOptions = [
    { value: 'EXPERIENCE', label: 'Experience' },
    { value: 'EDUCATION', label: 'Education' },
    { value: 'PROJECT', label: 'Project' },
    { value: 'SOFT_SKILL', label: 'Soft Skill' },
    { value: 'GENERAL', label: 'General' }
  ];

  return (
    <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>{section ? 'Edit Section' : 'Add New Section'}</DialogTitle>
        <DialogDescription>
          {section ? 'Modify section details and settings' : 'Create a new section for this interview template'}
        </DialogDescription>
      </DialogHeader>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Section Name *</label>
          <Input
            type="text"
            required
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="Enter section name"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Section Type</label>
          <Select
            value={formData.section}
            onValueChange={(value) => setFormData({ ...formData, section: value as any })}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {sectionOptions.map(option => (
                <SelectItem key={option.value} value={option.value}>{option.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Introduction</label>
          <Textarea
            value={formData.intro}
            onChange={(e) => setFormData({ ...formData, intro: e.target.value })}
            rows={3}
            placeholder="Introduction text for this section"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Goal/Objective</label>
          <Textarea
            value={formData.goal}
            onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
            rows={3}
            placeholder="What should this section achieve?"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">AI Prompt</label>
          <Textarea
            value={formData.prompt}
            onChange={(e) => setFormData({ ...formData, prompt: e.target.value })}
            className="font-mono text-sm"
            rows={6}
            placeholder="AI prompt for generating questions in this section"
          />
        </div>

        <div className="space-y-3">
          <div>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="allow_ai_questions"
                checked={formData.allow_ai_questions}
                onCheckedChange={(checked) => setFormData({ ...formData, allow_ai_questions: checked === true })}
              />
              <label
                htmlFor="allow_ai_questions"
                className="text-sm font-medium text-gray-700 cursor-pointer"
              >
                Allow AI to generate additional questions
              </label>
            </div>
            <p className="mt-1 text-xs text-gray-500 ml-6">
              AI can create additional questions for this section
            </p>
          </div>

          <div>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="allow_ai_override_questions"
                checked={formData.allow_ai_override_questions}
                onCheckedChange={(checked) => setFormData({ ...formData, allow_ai_override_questions: checked === true })}
              />
              <label
                htmlFor="allow_ai_override_questions"
                className="text-sm font-medium text-gray-700 cursor-pointer"
              >
                Allow AI to reformulate existing questions
              </label>
            </div>
            <p className="mt-1 text-xs text-gray-500 ml-6">
              AI can modify and improve the wording of predefined questions
            </p>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Legal Notice</label>
          <Textarea
            value={formData.legal_notice}
            onChange={(e) => setFormData({ ...formData, legal_notice: e.target.value })}
            rows={3}
            placeholder="Legal text specific to this section (if needed)"
          />
          <p className="mt-1 text-xs text-gray-500">
            Optional legal notice that will be shown for this section
          </p>
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" onClick={onCancel}>
            Cancel
          </Button>
          <Button type="submit">
            {section ? 'Update Section' : 'Add Section'}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  );
};

// Questions Modal Component
interface QuestionsModalProps {
  section: InterviewTemplateSection;
  onClose: () => void;
  apiBasePath: string;
}

const QuestionsModal: React.FC<QuestionsModalProps> = ({ section, onClose, apiBasePath }) => {
  const [questions, setQuestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showQuestionForm, setShowQuestionForm] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState<any>(null);

  useEffect(() => {
    fetchQuestions();
  }, [section.id]);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.authenticatedRequest<unknown[]>(`${apiBasePath}/sections/${section.id}/questions`);
      setQuestions(Array.isArray(response) ? response : []);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch questions');
    } finally {
      setLoading(false);
    }
  };

  const handleAddQuestion = () => {
    setEditingQuestion(null);
    setShowQuestionForm(true);
  };

  const handleEditQuestion = (question: any) => {
    setEditingQuestion(question);
    setShowQuestionForm(true);
  };

  const handleCancelQuestionForm = () => {
    setShowQuestionForm(false);
    setEditingQuestion(null);
  };

  const handleSaveQuestion = async (questionData: any) => {
    try {
      if (editingQuestion) {
        // Update existing question
        await api.authenticatedRequest(`${apiBasePath}/questions/${editingQuestion.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(questionData)
        });
      } else {
        // Create new question with automatic sort_order
        const nextSortOrder = questions.length; // Auto-calculate sort_order
        const questionDataWithOrder = {
          ...questionData,
          interview_template_section_id: section.id,
          sort_order: nextSortOrder
        };

        await api.authenticatedRequest(`${apiBasePath}/questions`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(questionDataWithOrder)
        });
      }

      setShowQuestionForm(false);
      setEditingQuestion(null);
      // Refresh questions list from backend
      await fetchQuestions();
    } catch (err: any) {
      setError(err.message || 'Failed to save question');
    }
  };

  const handleDeleteQuestion = async (questionId: string) => {
    if (confirm('Are you sure you want to delete this question? This action cannot be undone.')) {
      try {
        await api.authenticatedRequest(`${apiBasePath}/questions/${questionId}`, {
          method: 'DELETE'
        });

        // Refresh questions list from backend
        await fetchQuestions();
      } catch (err: any) {
        setError(err.message || 'Failed to delete question');
      }
    }
  };

  const handleMoveQuestionUp = async (questionId: string) => {
    try {
      // For now, handle locally by swapping sort_order
      const currentIndex = questions.findIndex(q => q.id === questionId);
      if (currentIndex > 0) {
        const updatedQuestions = [...questions];
        // Swap with previous question
        [updatedQuestions[currentIndex - 1], updatedQuestions[currentIndex]] =
        [updatedQuestions[currentIndex], updatedQuestions[currentIndex - 1]];

        // Update sort_order values
        updatedQuestions.forEach((q, index) => {
          q.sort_order = index;
        });

        setQuestions(updatedQuestions);

        // TODO: Implement API call to persist the new order
        // await api.authenticatedRequest(`/admin/interview-template-questions/${questionId}/move-up`, {
        //   method: 'POST'
        // });
      }
    } catch (err: any) {
      setError(err.message || 'Failed to move question up');
    }
  };

  const handleMoveQuestionDown = async (questionId: string) => {
    try {
      // For now, handle locally by swapping sort_order
      const currentIndex = questions.findIndex(q => q.id === questionId);
      if (currentIndex < questions.length - 1) {
        const updatedQuestions = [...questions];
        // Swap with next question
        [updatedQuestions[currentIndex], updatedQuestions[currentIndex + 1]] =
        [updatedQuestions[currentIndex + 1], updatedQuestions[currentIndex]];

        // Update sort_order values
        updatedQuestions.forEach((q, index) => {
          q.sort_order = index;
        });

        setQuestions(updatedQuestions);

        // TODO: Implement API call to persist the new order
        // await api.authenticatedRequest(`/admin/interview-template-questions/${questionId}/move-down`, {
        //   method: 'POST'
        // });
      }
    } catch (err: any) {
      setError(err.message || 'Failed to move question down');
    }
  };

  return (
    <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>Questions for "{section.name}"</DialogTitle>
        <DialogDescription>Manage questions for this section</DialogDescription>
      </DialogHeader>

      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {loading ? (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">Loading questions...</span>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h4 className="text-lg font-medium text-gray-900">Questions ({questions.length})</h4>
            <Button onClick={handleAddQuestion} className="flex items-center gap-2">
              <Plus className="w-4 h-4" />
              Add Question
            </Button>
          </div>

          {questions.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <MessageSquare className="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p>No questions added yet</p>
              <p className="text-sm">Click "Add Question" to create your first question</p>
            </div>
          ) : (
            <div className="space-y-3">
              {questions.map((question, index) => (
                <Card key={question.id || index}>
                  <CardContent className="pt-6">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h5 className="font-medium text-gray-900">{question.name}</h5>
                        <p className="text-sm text-gray-600 mt-1">{question.description}</p>
                      </div>
                      <div className="flex items-center space-x-2 ml-4">
                        {/* Move up/down buttons for questions */}
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() => handleMoveQuestionUp(question.id)}
                              disabled={index === 0}
                            >
                              <ChevronUp className="w-4 h-4" />
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            {index === 0 ? "Already at the top" : "Move question up in the list"}
                          </TooltipContent>
                        </Tooltip>

                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() => handleMoveQuestionDown(question.id)}
                              disabled={index >= questions.length - 1}
                            >
                              <ChevronDown className="w-4 h-4" />
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            {index >= questions.length - 1 ? "Already at the bottom" : "Move question down in the list"}
                          </TooltipContent>
                        </Tooltip>

                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() => handleEditQuestion(question)}
                            >
                              <Edit className="w-4 h-4" />
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>Edit question text, type, and settings</TooltipContent>
                        </Tooltip>

                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() => handleDeleteQuestion(question.id)}
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>Permanently delete this question</TooltipContent>
                        </Tooltip>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      )}

      <DialogFooter>
        <Button variant="outline" onClick={onClose}>
          Close
        </Button>
      </DialogFooter>

      {/* Question Form Modal */}
      {showQuestionForm && (
        <Dialog open={showQuestionForm} onOpenChange={(open) => !open && handleCancelQuestionForm()}>
          <QuestionFormModal
            question={editingQuestion}
            sectionId={section.id}
            onSave={handleSaveQuestion}
            onCancel={handleCancelQuestionForm}
          />
        </Dialog>
      )}
    </DialogContent>
  );
};

// Question Form Modal Component
interface QuestionFormModalProps {
  question: any | null;
  sectionId: string;
  onSave: (questionData: any) => void;
  onCancel: () => void;
}

const QuestionFormModal: React.FC<QuestionFormModalProps> = ({ question, sectionId, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    name: question?.name || '',
    description: question?.description || '',
    code: question?.code || '',
    sort_order: question?.sort_order || 0,
    scope: question?.scope || 'global',
    data_type: question?.data_type || 'short_string',
    allow_ai_followup: question?.allow_ai_followup || false,
    legal_notice: question?.legal_notice || ''
  });

  const scopeOptions = [
    { value: 'global', label: 'Global' },
    { value: 'item', label: 'Item' }
  ];

  const dataTypeOptions = [
    { value: 'short_string', label: 'Short String' },
    { value: 'large_string', label: 'Large String' },
    { value: 'int', label: 'Integer' },
    { value: 'date', label: 'Date' }
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave({
      ...formData,
      interview_template_section_id: sectionId
    });
  };

  return (
    <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>{question ? 'Edit Question' : 'Add New Question'}</DialogTitle>
        <DialogDescription>
          {question ? 'Modify question details and settings' : 'Create a new question for this section'}
        </DialogDescription>
      </DialogHeader>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Question Name *</label>
          <Input
            type="text"
            required
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="Enter question name"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
          <Textarea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            rows={3}
            placeholder="Describe the question"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Scope</label>
            <Select
              value={formData.scope}
              onValueChange={(value) => setFormData({ ...formData, scope: value })}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {scopeOptions.map(option => (
                  <SelectItem key={option.value} value={option.value}>{option.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Data Type</label>
            <Select
              value={formData.data_type}
              onValueChange={(value) => setFormData({ ...formData, data_type: value })}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {dataTypeOptions.map(option => (
                  <SelectItem key={option.value} value={option.value}>{option.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Question Code (optional)</label>
          <Input
            type="text"
            value={formData.code}
            onChange={(e) => setFormData({ ...formData, code: e.target.value })}
            placeholder="Unique code for the question (optional)"
          />
        </div>

        <div>
          <div className="flex items-center space-x-2">
            <Checkbox
              id="allow_ai_followup"
              checked={formData.allow_ai_followup}
              onCheckedChange={(checked) => setFormData({ ...formData, allow_ai_followup: checked === true })}
            />
            <label
              htmlFor="allow_ai_followup"
              className="text-sm font-medium text-gray-700 cursor-pointer"
            >
              Allow AI to generate follow-up questions
            </label>
          </div>
          <p className="mt-1 text-xs text-gray-500 ml-6">
            AI can create additional follow-up questions based on candidate responses
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Legal Notice</label>
          <Textarea
            value={formData.legal_notice}
            onChange={(e) => setFormData({ ...formData, legal_notice: e.target.value })}
            rows={3}
            placeholder="Legal text specific to this question (if needed)"
          />
          <p className="mt-1 text-xs text-gray-500">
            Optional legal notice for sensitive questions (background checks, personal data, etc.)
          </p>
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" onClick={onCancel}>
            Cancel
          </Button>
          <Button type="submit">
            {question ? 'Update Question' : 'Add Question'}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  );
};

export default InterviewTemplateEditor;