import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../../lib/api';

// Tooltip component
const Tooltip: React.FC<{ text: string; children: React.ReactNode }> = ({ text, children }) => {
  return (
    <div className="relative group">
      {children}
      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap pointer-events-none z-10">
        {text}
        <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-gray-900"></div>
      </div>
    </div>
  );
};

interface InterviewTemplate {
  id: string;
  name: string;
  intro?: string;
  prompt?: string;
  goal?: string;
  status: 'ENABLED' | 'DRAFT' | 'DISABLED';
  type: 'EXTENDED_PROFILE' | 'POSITION_INTERVIEW';
  job_category: string;
  section: 'EXPERIENCE' | 'EDUCATION' | 'PROJECT' | 'SOFT_SKILL' | 'GENERAL';
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
  const navigate = useNavigate();
  const { templateId } = useParams<{ templateId?: string }>();
  const isEditing = !!templateId;

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    intro: '',
    prompt: '',
    goal: '',
    type: 'EXTENDED_PROFILE' as 'EXTENDED_PROFILE' | 'POSITION_INTERVIEW',
    job_category: 'Other',
    section: 'GENERAL' as 'EXPERIENCE' | 'EDUCATION' | 'PROJECT' | 'SOFT_SKILL' | 'GENERAL',
    tags: [] as string[],
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
    { value: 'EXTENDED_PROFILE', label: 'Extended Profile' },
    { value: 'POSITION_INTERVIEW', label: 'Position Interview' }
  ];

  const jobCategories = [
    { value: 'Technology', label: 'Technology' },
    { value: 'Operations', label: 'Operations' },
    { value: 'Sales', label: 'Sales' },
    { value: 'Marketing', label: 'Marketing' },
    { value: 'Administration', label: 'Administration' },
    { value: 'Human Resources', label: 'Human Resources' },
    { value: 'Finance', label: 'Finance' },
    { value: 'Customer Service', label: 'Customer Service' },
    { value: 'Other', label: 'Other' }
  ];

  const sectionOptions = [
    { value: 'EXPERIENCE', label: 'Experience' },
    { value: 'EDUCATION', label: 'Education' },
    { value: 'PROJECT', label: 'Project' },
    { value: 'SOFT_SKILL', label: 'Soft Skill' },
    { value: 'GENERAL', label: 'General' }
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
      const template = await api.authenticatedRequest(`/admin/interview-templates/${templateId}`);
      setFormData({
        name: template.name,
        intro: template.intro || '',
        prompt: template.prompt || '',
        goal: template.goal || '',
        type: template.type,
        job_category: template.job_category,
        section: template.section,
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
      setError(err.message || 'Failed to fetch template');
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
      const templateDataWithSections = {
        ...formData,
        sections: sections
      };

      if (isEditing) {
        await api.authenticatedRequest(`/admin/interview-templates/${templateId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(templateDataWithSections)
        });
      } else {
        await api.authenticatedRequest('/admin/interview-templates', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(templateDataWithSections)
        });
      }

      navigate('/admin/interview-templates');
    } catch (err: any) {
      setError(err.message || 'Failed to save template');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    navigate('/admin/interview-templates');
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
    if (confirm('Are you sure you want to permanently delete this section? This action cannot be undone.')) {
      try {
        // If it's a real section (not temp), call API to delete
        if (!sectionId.startsWith('temp-')) {
          try {
            await api.authenticatedRequest(`/admin/interview-template-sections/${sectionId}`, {
              method: 'DELETE',
              headers: { 'Content-Type': 'application/json' }
            });
          } catch (err) {
            console.warn('Failed to delete section via API, removing locally');
          }
        }

        setSections(sections.filter(s => s.id !== sectionId));
      } catch (err: any) {
        setError(err.message || 'Failed to delete section');
      }
    }
  };

  const handleSaveSection = async (sectionData: Omit<InterviewTemplateSection, 'id' | 'interview_template_id'>) => {
    try {
      if (editingSection) {
        // Update existing section - if it's a real section, call API
        if (!editingSection.id.startsWith('temp-')) {
          try {
            await api.authenticatedRequest(`/admin/interview-template-sections/${editingSection.id}`, {
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
            const createdSection = await api.authenticatedRequest('/admin/interview-template-sections', {
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
      setError(err.message || 'Failed to save section');
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
          await api.authenticatedRequest(`/admin/interview-template-sections/${sectionId}/enable`, {
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
      setError(err.message || 'Failed to enable section');
    }
  };

  const handleDisableSection = async (sectionId: string) => {
    if (!confirm('Are you sure you want to disable this section?')) return;

    try {
      // If it's a real section (not temp), call API to disable
      if (!sectionId.startsWith('temp-')) {
        try {
          await api.authenticatedRequest(`/admin/interview-template-sections/${sectionId}/disable`, {
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
      setError(err.message || 'Failed to disable section');
    }
  };

  const handleMoveSectionUp = async (sectionId: string) => {
    try {
      // If it's a real section (not temp), call API
      if (!sectionId.startsWith('temp-')) {
        try {
          await api.authenticatedRequest(`/admin/interview-template-sections/${sectionId}/move-up`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
          });
          // Refresh the template data to get the updated order
          if (templateId) {
            const template = await api.authenticatedRequest(`/admin/interview-templates/${templateId}`);
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
      setError(err.message || 'Failed to move section up');
    }
  };

  const handleMoveSectionDown = async (sectionId: string) => {
    try {
      // If it's a real section (not temp), call API
      if (!sectionId.startsWith('temp-')) {
        try {
          await api.authenticatedRequest(`/admin/interview-template-sections/${sectionId}/move-down`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
          });
          // Refresh the template data to get the updated order
          if (templateId) {
            const template = await api.authenticatedRequest(`/admin/interview-templates/${templateId}`);
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
      setError(err.message || 'Failed to move section down');
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
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={handleCancel}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                title="Back to templates"
              >
                <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  {isEditing ? 'Edit Template' : 'Create New Template'}
                </h1>
                <p className="text-sm text-gray-500">
                  {isEditing ? 'Modify interview template settings and content' : 'Create a new interview template'}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={handleCancel}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={saving}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {saving ? 'Saving...' : (isEditing ? 'Update Template' : 'Create Template')}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Alert */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-red-800">{error}</span>
              <button
                onClick={() => setError(null)}
                className="ml-auto text-red-600 hover:text-red-800"
              >
                ×
              </button>
            </div>
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-8">
          {/* Basic Information */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Basic Information</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="lg:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Template Name *</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter template name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Type</label>
                <select
                  value={formData.type}
                  onChange={(e) => setFormData({ ...formData, type: e.target.value as 'EXTENDED_PROFILE' | 'POSITION_INTERVIEW' })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  {templateTypes.map(type => (
                    <option key={type.value} value={type.value}>{type.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Job Category</label>
                <select
                  value={formData.job_category}
                  onChange={(e) => setFormData({ ...formData, job_category: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  {jobCategories.map(category => (
                    <option key={category.value} value={category.value}>{category.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Section</label>
                <select
                  value={formData.section || ''}
                  onChange={(e) => setFormData({ ...formData, section: (e.target.value || null) as 'EXPERIENCE' | 'EDUCATION' | 'PROJECT' | 'SOFT_SKILL' | 'GENERAL' | null })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Select a section (optional)</option>
                  {sectionOptions.map(section => (
                    <option key={section.value} value={section.value}>{section.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Tags</label>
                <input
                  type="text"
                  value={formData.tags.join(', ')}
                  onChange={(e) => setFormData({ ...formData, tags: e.target.value.split(', ').filter(tag => tag.trim() !== '') })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter tags separated by commas"
                />
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Template Content</h2>
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Introduction</label>
                <textarea
                  value={formData.intro}
                  onChange={(e) => setFormData({ ...formData, intro: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  rows={4}
                  placeholder="Introduction text that will be shown to candidates before the interview"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Goal/Objective</label>
                <textarea
                  value={formData.goal}
                  onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  rows={4}
                  placeholder="What should this interview template achieve? What insights should it provide?"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">AI Prompt</label>
                <textarea
                  value={formData.prompt}
                  onChange={(e) => setFormData({ ...formData, prompt: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
                  rows={12}
                  placeholder="Detailed prompt for AI to generate interview questions. Be specific about:
- Question types and difficulty level
- Topics to cover
- Desired response format
- Evaluation criteria
- Any special instructions"
                />
              </div>
              <div>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.allow_ai_questions}
                    onChange={(e) => setFormData({ ...formData, allow_ai_questions: e.target.checked })}
                    className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-sm font-medium text-gray-700">Allow AI to generate additional questions</span>
                </label>
                <p className="mt-1 text-xs text-gray-500 ml-6">
                  If enabled, AI can create additional questions beyond the predefined ones
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Legal Notice</label>
                <textarea
                  value={formData.legal_notice}
                  onChange={(e) => setFormData({ ...formData, legal_notice: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  rows={4}
                  placeholder="Legal text that will be displayed to users for compliance purposes (GDPR, data processing, etc.)"
                />
                <p className="mt-1 text-xs text-gray-500">
                  This text will be shown to candidates before starting the interview
                </p>
              </div>
            </div>
          </div>

          {/* Template Sections */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Template Sections</h2>
              <button
                type="button"
                onClick={handleAddSection}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Add Section
              </button>
            </div>

            {/* Sections List */}
            <div className="space-y-4">
              {sections.map((section, index) => (
                <div key={section.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="font-medium text-gray-900">{section.name}{section.sort_order}</h3>
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          section.status === 'ENABLED'
                            ? 'bg-green-100 text-green-800'
                            : section.status === 'DRAFT'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {section.status}
                        </span>
                        {section.section && (
                          <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                            {section.section}
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{section.intro}</p>
                      <p className="text-xs text-gray-500">{section.goal}</p>
                    </div>
                    <div className="flex items-center space-x-2 ml-4">
                      {/* Move up/down buttons - at the front */}
                      <Tooltip text={index === 0 ? "Already at the top" : "Move section up in the list"}>
                        <button
                          type="button"
                          onClick={() => handleMoveSectionUp(section.id)}
                          disabled={index === 0}
                          className={`p-1 rounded transition-colors ${
                            index === 0
                              ? 'text-gray-300 cursor-not-allowed'
                              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                          }`}
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                          </svg>
                        </button>
                      </Tooltip>

                      <Tooltip text={index >= sections.length - 1 ? "Already at the bottom" : "Move section down in the list"}>
                        <button
                          type="button"
                          onClick={() => handleMoveSectionDown(section.id)}
                          disabled={index >= sections.length - 1}
                          className={`p-1 rounded transition-colors ${
                            index >= sections.length - 1
                              ? 'text-gray-300 cursor-not-allowed'
                              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                          }`}
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                          </svg>
                        </button>
                      </Tooltip>

                      <Tooltip text="Edit section details, intro, and goals">
                        <button
                          type="button"
                          onClick={() => handleEditSection(section)}
                          className="text-blue-600 hover:text-blue-900 p-1 rounded hover:bg-blue-50 transition-colors"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                      </Tooltip>

                      <Tooltip text="Manage questions for this section">
                        <button
                          type="button"
                          onClick={() => handleEditQuestions(section)}
                          className="text-purple-600 hover:text-purple-900 p-1 rounded hover:bg-purple-50 transition-colors"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </button>
                      </Tooltip>

                      {/* Enable/Disable buttons for sections */}
                      {section.status === 'ENABLED' ? (
                        <Tooltip text="Disable section - it won't be used in interviews">
                          <button
                            type="button"
                            onClick={() => handleDisableSection(section.id)}
                            className="text-orange-600 hover:text-orange-900 p-1 rounded hover:bg-orange-50 transition-colors"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728L5.636 5.636m12.728 12.728L18.364 5.636M5.636 18.364l12.728-12.728" />
                            </svg>
                          </button>
                        </Tooltip>
                      ) : (
                        <Tooltip text="Enable section - make it active for interviews">
                          <button
                            type="button"
                            onClick={() => handleEnableSection(section.id)}
                            className="text-green-600 hover:text-green-900 p-1 rounded hover:bg-green-50 transition-colors"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                            </svg>
                          </button>
                        </Tooltip>
                      )}

                      {/* Delete button - only show when section is disabled */}
                      {section.status === 'DISABLED' && (
                        <Tooltip text="Permanently delete this section and all its questions">
                          <button
                            type="button"
                            onClick={() => handleDeleteSection(section.id)}
                            className="text-red-600 hover:text-red-900 p-1 rounded hover:bg-red-50 transition-colors"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        </Tooltip>
                      )}
                    </div>
                  </div>
                </div>
              ))}

              {sections.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <svg className="w-12 h-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <p>No sections added yet</p>
                  <p className="text-sm">Click "Add Section" to create your first section</p>
                </div>
              )}
            </div>
          </div>
        </form>

        {/* Section Form Modal */}
        {showSectionForm && (
          <SectionFormModal
            section={editingSection}
            onSave={handleSaveSection}
            onCancel={handleCancelSectionForm}
          />
        )}

        {/* Questions Modal */}
        {showQuestionsModal && editingQuestions && (
          <QuestionsModal
            section={editingQuestions}
            onClose={handleCancelQuestionsModal}
          />
        )}
      </div>
    </div>
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
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg font-semibold text-gray-900">
              {section ? 'Edit Section' : 'Add New Section'}
            </h3>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Section Name *</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter section name"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Section Type</label>
              <select
                value={formData.section}
                onChange={(e) => setFormData({ ...formData, section: e.target.value as any })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                {sectionOptions.map(option => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Introduction</label>
              <textarea
                value={formData.intro}
                onChange={(e) => setFormData({ ...formData, intro: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                rows={3}
                placeholder="Introduction text for this section"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Goal/Objective</label>
              <textarea
                value={formData.goal}
                onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                rows={3}
                placeholder="What should this section achieve?"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">AI Prompt</label>
              <textarea
                value={formData.prompt}
                onChange={(e) => setFormData({ ...formData, prompt: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
                rows={6}
                placeholder="AI prompt for generating questions in this section"
              />
            </div>

            <div className="space-y-3">
              <div>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.allow_ai_questions}
                    onChange={(e) => setFormData({ ...formData, allow_ai_questions: e.target.checked })}
                    className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-sm font-medium text-gray-700">Allow AI to generate additional questions</span>
                </label>
                <p className="mt-1 text-xs text-gray-500 ml-6">
                  AI can create additional questions for this section
                </p>
              </div>

              <div>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.allow_ai_override_questions}
                    onChange={(e) => setFormData({ ...formData, allow_ai_override_questions: e.target.checked })}
                    className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-sm font-medium text-gray-700">Allow AI to reformulate existing questions</span>
                </label>
                <p className="mt-1 text-xs text-gray-500 ml-6">
                  AI can modify and improve the wording of predefined questions
                </p>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Legal Notice</label>
              <textarea
                value={formData.legal_notice}
                onChange={(e) => setFormData({ ...formData, legal_notice: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                rows={3}
                placeholder="Legal text specific to this section (if needed)"
              />
              <p className="mt-1 text-xs text-gray-500">
                Optional legal notice that will be shown for this section
              </p>
            </div>

            <div className="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                onClick={onCancel}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                {section ? 'Update Section' : 'Add Section'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

// Questions Modal Component
interface QuestionsModalProps {
  section: InterviewTemplateSection;
  onClose: () => void;
}

const QuestionsModal: React.FC<QuestionsModalProps> = ({ section, onClose }) => {
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
      const response = await api.authenticatedRequest(`/admin/interview-template-sections/${section.id}/questions`);
      setQuestions(response || []);
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
        await api.authenticatedRequest(`/admin/interview-template-questions/${editingQuestion.id}`, {
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

        await api.authenticatedRequest('/admin/interview-template-questions', {
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
        await api.authenticatedRequest(`/admin/interview-template-questions/${questionId}`, {
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
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                Questions for "{section.name}"
              </h3>
              <p className="text-sm text-gray-500 mt-1">
                Manage questions for this section
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center">
                <svg className="w-5 h-5 text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-red-800">{error}</span>
              </div>
            </div>
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
                <button
                  onClick={handleAddQuestion}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  Add Question
                </button>
              </div>

              {questions.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <svg className="w-12 h-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p>No questions added yet</p>
                  <p className="text-sm">Click "Add Question" to create your first question</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {questions.map((question, index) => (
                    <div key={question.id || index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h5 className="font-medium text-gray-900">{question.name}</h5>
                          <p className="text-sm text-gray-600 mt-1">{question.description}</p>
                        </div>
                        <div className="flex items-center space-x-2 ml-4">
                          {/* Move up/down buttons for questions */}
                          <Tooltip text={index === 0 ? "Already at the top" : "Move question up in the list"}>
                            <button
                              onClick={() => handleMoveQuestionUp(question.id)}
                              disabled={index === 0}
                              className={`p-1 rounded transition-colors ${
                                index === 0
                                  ? 'text-gray-300 cursor-not-allowed'
                                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                              }`}
                            >
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                              </svg>
                            </button>
                          </Tooltip>

                          <Tooltip text={index >= questions.length - 1 ? "Already at the bottom" : "Move question down in the list"}>
                            <button
                              onClick={() => handleMoveQuestionDown(question.id)}
                              disabled={index >= questions.length - 1}
                              className={`p-1 rounded transition-colors ${
                                index >= questions.length - 1
                                  ? 'text-gray-300 cursor-not-allowed'
                                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                              }`}
                            >
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                              </svg>
                            </button>
                          </Tooltip>

                          <Tooltip text="Edit question text, type, and settings">
                            <button
                              onClick={() => handleEditQuestion(question)}
                              className="text-blue-600 hover:text-blue-900 p-1 rounded hover:bg-blue-50 transition-colors"
                            >
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                              </svg>
                            </button>
                          </Tooltip>

                          <Tooltip text="Permanently delete this question">
                            <button
                              onClick={() => handleDeleteQuestion(question.id)}
                              className="text-red-600 hover:text-red-900 p-1 rounded hover:bg-red-50 transition-colors"
                            >
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          </Tooltip>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              <div className="flex justify-end pt-4 border-t">
                <button
                  onClick={onClose}
                  className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          )}

          {/* Question Form Modal */}
          {showQuestionForm && (
            <QuestionFormModal
              question={editingQuestion}
              sectionId={section.id}
              onSave={handleSaveQuestion}
              onCancel={handleCancelQuestionForm}
            />
          )}
        </div>
      </div>
    </div>
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
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[60]">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg font-semibold text-gray-900">
              {question ? 'Edit Question' : 'Add New Question'}
            </h3>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Question Name *</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter question name"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                rows={3}
                placeholder="Describe the question"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Scope</label>
                <select
                  value={formData.scope}
                  onChange={(e) => setFormData({ ...formData, scope: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  {scopeOptions.map(option => (
                    <option key={option.value} value={option.value}>{option.label}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Data Type</label>
                <select
                  value={formData.data_type}
                  onChange={(e) => setFormData({ ...formData, data_type: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  {dataTypeOptions.map(option => (
                    <option key={option.value} value={option.value}>{option.label}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Question Code (optional)</label>
              <input
                type="text"
                value={formData.code}
                onChange={(e) => setFormData({ ...formData, code: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Unique code for the question (optional)"
              />
            </div>

            <div>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={formData.allow_ai_followup}
                  onChange={(e) => setFormData({ ...formData, allow_ai_followup: e.target.checked })}
                  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <span className="text-sm font-medium text-gray-700">Allow AI to generate follow-up questions</span>
              </label>
              <p className="mt-1 text-xs text-gray-500 ml-6">
                AI can create additional follow-up questions based on candidate responses
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Legal Notice</label>
              <textarea
                value={formData.legal_notice}
                onChange={(e) => setFormData({ ...formData, legal_notice: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                rows={3}
                placeholder="Legal text specific to this question (if needed)"
              />
              <p className="mt-1 text-xs text-gray-500">
                Optional legal notice for sensitive questions (background checks, personal data, etc.)
              </p>
            </div>

            <div className="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                onClick={onCancel}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                {question ? 'Update Question' : 'Add Question'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default InterviewTemplateEditor;