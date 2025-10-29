/**
 * Edit Company Page
 * Allow company to edit their profile information including slug
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Building2, ArrowLeft, Save, AlertCircle, Upload, Image as ImageIcon, Edit3 } from 'lucide-react';
import { recruiterCompanyService } from '../../services/recruiterCompanyService';
import type { RecruiterCompany, UpdateRecruiterCompanyRequest } from '../../types/recruiter-company';
import { ImageEditor } from '../../components/common';

export default function EditCompanyPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [company, setCompany] = useState<RecruiterCompany | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [showImageEditor, setShowImageEditor] = useState(false);
  const [imageToEdit, setImageToEdit] = useState<string | null>(null);

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

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/svg+xml'];
    if (!allowedTypes.includes(file.type)) {
      setError('Invalid file type. Please upload a JPEG, PNG, WebP, or SVG image.');
      return;
    }

    // Validate file size (max 5MB)
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
      setError('File size exceeds 5MB. Please upload a smaller image.');
      return;
    }

    // For SVG files, don't show editor (can't crop SVG)
    if (file.type === 'image/svg+xml') {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
      setError(null);
      return;
    }

    // For other image types, show editor
    const reader = new FileReader();
    reader.onloadend = () => {
      setImageToEdit(reader.result as string);
      setShowImageEditor(true);
    };
    reader.readAsDataURL(file);
    setError(null);
  };

  const handleCropComplete = (croppedImage: string) => {
    console.log('Starting image conversion...');
    
    // Convert base64 to File
    fetch(croppedImage)
      .then(res => res.blob())
      .then(blob => {
        console.log('Blob created:', blob.size, 'bytes');
        const file = new File([blob], 'logo.png', { type: 'image/png' });
        console.log('File created:', file.name, file.size, 'bytes', file.type);
        
        setSelectedFile(file);
        setPreviewUrl(croppedImage);
        
        console.log('File set in state, closing editor');
        // Close editor after successful conversion
        setShowImageEditor(false);
        setImageToEdit(null);
        
        // Auto-upload the cropped image
        console.log('Starting auto-upload...');
        uploadCroppedImage(file);
      })
      .catch(err => {
        console.error('Error converting cropped image:', err);
        setError('Error processing image');
        // Close editor even on error
        setShowImageEditor(false);
        setImageToEdit(null);
      });
  };

  const handleCropCancel = () => {
    setShowImageEditor(false);
    setImageToEdit(null);
  };

  const uploadCroppedImage = async (file: File) => {
    console.log('Auto-uploading file:', file.name, file.size, 'bytes', file.type);

    const companyId = getCompanyId();
    if (!companyId) {
      setError('Company ID not found');
      return;
    }

    try {
      setUploading(true);
      setError(null);

      console.log('Calling upload service...');
      const updatedCompany = await recruiterCompanyService.uploadLogo(companyId, file);
      console.log('Upload successful:', updatedCompany);

      // Update local state
      setCompany(updatedCompany);
      setFormData(prev => ({
        ...prev,
        logo_url: updatedCompany.logo_url || '',
      }));

      // Clear file selection
      setSelectedFile(null);
      setPreviewUrl(null);

      alert('Logo uploaded successfully!');
    } catch (err: any) {
      setError(err.message || 'Failed to upload logo');
      console.error('Error uploading logo:', err);
    } finally {
      setUploading(false);
    }
  };

  const handleUploadLogo = async () => {
    if (!selectedFile) {
      console.log('No file selected for upload');
      return;
    }

    await uploadCroppedImage(selectedFile);
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
              pattern="[a-z0-9\-]*"
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

        {/* Logo Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Company Logo
          </label>

          {/* Current Logo Preview */}
          {(formData.logo_url || previewUrl) && (
            <div className="mb-4">
              <div className="flex items-start gap-4">
                <div className="w-32 h-32 border border-gray-300 rounded-lg overflow-hidden bg-gray-50 flex items-center justify-center">
                  {previewUrl ? (
                    <img
                      src={previewUrl}
                      alt="Logo preview"
                      className="w-full h-full object-contain"
                    />
                  ) : formData.logo_url ? (
                    <img
                      src={formData.logo_url}
                      alt="Current logo"
                      className="w-full h-full object-contain"
                    />
                  ) : (
                    <ImageIcon className="w-12 h-12 text-gray-400" />
                  )}
                </div>
                <div className="flex-1">
                  {previewUrl && (
                    <div className="mb-2">
                      <p className="text-sm font-medium text-gray-700">New logo selected</p>
                      <p className="text-sm text-gray-500">{selectedFile?.name}</p>
                      <button
                        type="button"
                        onClick={() => {
                          setImageToEdit(previewUrl);
                          setShowImageEditor(true);
                        }}
                        className="mt-2 px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors flex items-center gap-1"
                      >
                        <Edit3 className="w-3 h-3" />
                        Edit Image
                      </button>
                    </div>
                  )}
                  {formData.logo_url && !previewUrl && (
                    <div className="mb-2">
                      <p className="text-sm font-medium text-gray-700">Current logo</p>
                      <p className="text-sm text-gray-500 break-all">{formData.logo_url}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* File Upload */}
          <div className="flex gap-3">
            <label className="flex-1">
              <div className="flex items-center justify-center px-4 py-2 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 cursor-pointer transition-colors">
                <Upload className="w-5 h-5 text-gray-400 mr-2" />
                <span className="text-sm text-gray-600">
                  {selectedFile ? selectedFile.name : 'Choose logo image'}
                </span>
              </div>
              <input
                type="file"
                accept="image/jpeg,image/jpg,image/png,image/webp,image/svg+xml"
                onChange={handleFileSelect}
                className="hidden"
              />
            </label>

            {selectedFile && (
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={(e) => {
                    e.preventDefault();
                    console.log('Upload button clicked!');
                    handleUploadLogo();
                  }}
                  disabled={uploading}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {uploading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      Uploading...
                    </>
                  ) : (
                    <>
                      <Upload className="w-4 h-4" />
                      Upload
                    </>
                  )}
                </button>
              </div>
            )}
          </div>

          <p className="text-sm text-gray-500 mt-2">
            Accepted formats: JPEG, PNG, WebP, SVG (max 5MB)
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

      {/* Image Editor Modal */}
      {showImageEditor && imageToEdit && (
        <ImageEditor
          src={imageToEdit}
          onCropComplete={handleCropComplete}
          onCancel={handleCropCancel}
          aspectRatio={1}
          title="Edit Company Logo"
        />
      )}
    </div>
  );
}
