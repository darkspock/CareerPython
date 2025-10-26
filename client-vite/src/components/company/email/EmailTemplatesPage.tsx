/**
 * Email Templates Page Component
 * Phase 7: Main page for managing email templates
 */

import React, { useState, useEffect } from 'react';
import type { EmailTemplate, TriggerEvent } from '@/types/emailTemplate';
import { EmailTemplateCard } from './EmailTemplateCard';
import { EmailTemplateService } from '@/services/emailTemplateService';

interface EmailTemplatesPageProps {
  workflowId: string;
  onCreateNew?: () => void;
  onEditTemplate?: (template: EmailTemplate) => void;
}

type FilterTab = 'all' | 'active' | 'inactive';

export const EmailTemplatesPage: React.FC<EmailTemplatesPageProps> = ({
  workflowId,
  onCreateNew,
  onEditTemplate
}) => {
  const [templates, setTemplates] = useState<EmailTemplate[]>([]);
  const [filteredTemplates, setFilteredTemplates] = useState<EmailTemplate[]>([]);
  const [activeTab, setActiveTab] = useState<FilterTab>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  // Load templates
  const loadTemplates = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const fetchedTemplates = await EmailTemplateService.listTemplatesByWorkflow(workflowId);
      setTemplates(fetchedTemplates);
      setFilteredTemplates(fetchedTemplates);
    } catch (err) {
      setError('Failed to load email templates');
      console.error('Error loading templates:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadTemplates();
  }, [workflowId]);

  // Filter templates based on active tab and search
  useEffect(() => {
    let filtered = templates;

    // Filter by active status
    if (activeTab === 'active') {
      filtered = filtered.filter(t => t.is_active);
    } else if (activeTab === 'inactive') {
      filtered = filtered.filter(t => !t.is_active);
    }

    // Filter by search term
    if (searchTerm) {
      const search = searchTerm.toLowerCase();
      filtered = filtered.filter(
        t =>
          t.template_name.toLowerCase().includes(search) ||
          t.template_key.toLowerCase().includes(search) ||
          t.subject.toLowerCase().includes(search)
      );
    }

    setFilteredTemplates(filtered);
  }, [templates, activeTab, searchTerm]);

  // Handle delete
  const handleDelete = async (templateId: string) => {
    try {
      setActionLoading(templateId);
      await EmailTemplateService.deleteTemplate(templateId);
      await loadTemplates();
    } catch (err) {
      alert('Failed to delete template');
      console.error('Error deleting template:', err);
    } finally {
      setActionLoading(null);
    }
  };

  // Handle toggle active
  const handleToggleActive = async (templateId: string, currentlyActive: boolean) => {
    try {
      setActionLoading(templateId);
      if (currentlyActive) {
        await EmailTemplateService.deactivateTemplate(templateId);
      } else {
        await EmailTemplateService.activateTemplate(templateId);
      }
      await loadTemplates();
    } catch (err) {
      alert('Failed to update template status');
      console.error('Error toggling template status:', err);
    } finally {
      setActionLoading(null);
    }
  };

  // Calculate stats
  const stats = {
    total: templates.length,
    active: templates.filter(t => t.is_active).length,
    inactive: templates.filter(t => !t.is_active).length
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading email templates...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-red-600 font-medium">{error}</p>
          <button
            onClick={loadTemplates}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Email Templates</h1>
          <p className="text-sm text-gray-600 mt-1">
            Manage automated email templates for your workflow
          </p>
        </div>
        {onCreateNew && (
          <button
            onClick={onCreateNew}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
          >
            Create Template
          </button>
        )}
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <p className="text-sm text-gray-600">Total Templates</p>
          <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-green-200 p-4">
          <p className="text-sm text-gray-600">Active</p>
          <p className="text-2xl font-bold text-green-600">{stats.active}</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <p className="text-sm text-gray-600">Inactive</p>
          <p className="text-2xl font-bold text-gray-600">{stats.inactive}</p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        {/* Filter Tabs */}
        <div className="flex items-center gap-2 mb-4">
          <button
            onClick={() => setActiveTab('all')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All ({stats.total})
          </button>
          <button
            onClick={() => setActiveTab('active')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'active'
                ? 'bg-green-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Active ({stats.active})
          </button>
          <button
            onClick={() => setActiveTab('inactive')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'inactive'
                ? 'bg-gray-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Inactive ({stats.inactive})
          </button>
        </div>

        {/* Search */}
        <div>
          <input
            type="text"
            placeholder="Search templates by name, key, or subject..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Templates Grid */}
      {filteredTemplates.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
          <p className="text-gray-500 mb-4">
            {searchTerm
              ? 'No templates match your search'
              : activeTab === 'all'
              ? 'No email templates yet'
              : `No ${activeTab} templates`}
          </p>
          {!searchTerm && activeTab === 'all' && onCreateNew && (
            <button
              onClick={onCreateNew}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Create Your First Template
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredTemplates.map((template) => (
            <EmailTemplateCard
              key={template.id}
              template={template}
              onEdit={onEditTemplate}
              onDelete={handleDelete}
              onToggleActive={handleToggleActive}
              isLoading={actionLoading === template.id}
            />
          ))}
        </div>
      )}
    </div>
  );
};
