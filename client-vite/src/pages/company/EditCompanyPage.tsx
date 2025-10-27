/**
 * Edit Company Page
 * Allow company to edit their profile information including slug
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Building2, ArrowLeft, Save, AlertCircle } from 'lucide-react';
import { recruiterCompanyService } from '../../services/recruiterCompanyService';
import type { RecruiterCompany, UpdateRecruiterCompanyRequest } from '../../types/recruiter-company';

export default function EditCompanyPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [company, setCompany] = useState<RecruiterCompany | null>(null);

  const [formData, setFormData] = useState({
    name: '',
    domain: '',
    slug: '',
    logo_url: '',
  });

  const getCompanyId = () => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_id;
    } catch {
      return null;
    }
  };

  useEffect(() => {
    loadCompany();
  }, []);

  const loadCompany = async () => {
    const companyId = getCompanyId();
    if (!companyId) {
      setError('Company ID not found');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await recruiterCompanyService.getCompany(companyId);
      setCompany(data);
      setFormData({
        name: data.name,
        domain: data.domain,
        slug: data.slug || '',
        logo_url: data.logo_url || '',
      });
    } catch (err: any) {
      setError(err.message || 'Failed to load company information');
      console.error('Error loading company:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const companyId = getCompanyId();
    if (!companyId) {
      setError('Company ID not found');
      return;
    }

    try {
      setSaving(true);
      setError(null);

      const updateData: UpdateRecruiterCompanyRequest = {
        name: formData.name,
        domain: formData.domain,
        slug: formData.slug || null,
        logo_url: formData.logo_url || null,
        settings: company?.settings || {},
      };

      await recruiterCompanyService.updateCompany(companyId, updateData);

      // Navigate back to settings
      navigate('/company/settings');
    } catch (err: any) {
      setError(err.message || 'Failed to update company information');
      console.error('Error updating company:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field: keyof typeof formData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const generateSlugFromName = () => {
    const slug = formData.name
      .toLowerCase()
      .trim()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-');
    setFormData(prev => ({ ...prev, slug }));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/company/settings')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Settings
        </button>

        <div className="flex items-center gap-3 mb-2">
          <Building2 className="w-8 h-8 text-gray-700" />
          <h1 className="text-3xl font-bold text-gray-900">Edit Company Profile</h1>
        </div>
        <p className="text-gray-600">
          Update your company information and public URL
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <p className="text-red-800">{error}</p>
          </div>
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 space-y-6">
        {/* Company Name */}
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
            Company Name <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="name"
            value={formData.name}
            onChange={(e) => handleChange('name', e.target.value)}
            required
            minLength={3}
            maxLength={255}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Enter company name"
          />
          <p className="text-sm text-gray-500 mt-1">
            The official name of your company
          </p>
        </div>

        {/* Domain */}
        <div>
          <label htmlFor="domain" className="block text-sm font-medium text-gray-700 mb-2">
            Company Domain <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="domain"
            value={formData.domain}
            onChange={(e) => handleChange('domain', e.target.value)}
            required
            minLength={3}
            maxLength={255}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="company.com"
          />
          <p className="text-sm text-gray-500 mt-1">
            Your company's email domain (e.g., company.com)
          </p>
        </div>

        {/* Slug */}
        <div>
          <label htmlFor="slug" className="block text-sm font-medium text-gray-700 mb-2">
            Public URL Slug
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              id="slug"
              value={formData.slug}
              onChange={(e) => handleChange('slug', e.target.value)}
              pattern="[a-z0-9-]*"
              maxLength={255}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="your-company"
            />
            <button
              type="button"
              onClick={generateSlugFromName}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors whitespace-nowrap"
            >
              Generate from Name
            </button>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            This will be used in your public job listings URL: /companies/<strong>{formData.slug || 'your-slug'}</strong>/open-positions
          </p>
          <p className="text-sm text-gray-400 mt-1">
            Only lowercase letters, numbers, and hyphens are allowed
          </p>
        </div>

        {/* Logo URL */}
        <div>
          <label htmlFor="logo_url" className="block text-sm font-medium text-gray-700 mb-2">
            Logo URL
          </label>
          <input
            type="url"
            id="logo_url"
            value={formData.logo_url}
            onChange={(e) => handleChange('logo_url', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="https://example.com/logo.png"
          />
          <p className="text-sm text-gray-500 mt-1">
            URL to your company logo image
          </p>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
          <button
            type="button"
            onClick={() => navigate('/company/settings')}
            className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {saving ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Saving...
              </>
            ) : (
              <>
                <Save className="w-4 h-4" />
                Save Changes
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
