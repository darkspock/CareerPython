import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, Eye, EyeOff } from 'lucide-react';
import { WysiwygEditor } from '../../components/common';
import { companyPageService } from '../../services/companyPageService';
import type { CreateCompanyPageRequest } from '../../types/companyPage';
import { PageType, LANGUAGE_OPTIONS } from '../../types/companyPage';
import { PAGE_TYPE_OPTIONS } from '../../types/companyPage';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';

export default function CreateCompanyPagePage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [previewMode, setPreviewMode] = useState(false);

  const [formData, setFormData] = useState<CreateCompanyPageRequest>({
    page_type: PageType.PUBLIC_COMPANY_DESCRIPTION, // Use the value (lowercase)
    title: '',
    html_content: '',
    meta_description: '',
    meta_keywords: [],
    language: 'en',
    is_default: false,
  });

  const [keywordInput, setKeywordInput] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.title.trim()) {
      setError('Title is required');
      return;
    }

    if (!formData.html_content.trim()) {
      setError('Content is required');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      await companyPageService.createPage(formData);
      navigate('/company/pages');
    } catch (err: any) {
      setError(err.message || 'Error creating page');
      console.error('Error creating page:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddKeyword = () => {
    if (keywordInput.trim() && !(formData.meta_keywords || []).includes(keywordInput.trim())) {
      setFormData(prev => ({
        ...prev,
        meta_keywords: [...(prev.meta_keywords || []), keywordInput.trim()]
      }));
      setKeywordInput('');
    }
  };

  const handleRemoveKeyword = (keyword: string) => {
    setFormData(prev => ({
      ...prev,
      meta_keywords: (prev.meta_keywords || []).filter(k => k !== keyword)
    }));
  };

  const handleKeywordKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddKeyword();
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            onClick={() => navigate('/company/pages')}
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Create New Page</h1>
            <p className="text-gray-600 mt-1">Create a new content page for your company</p>
          </div>
        </div>
        <Button
          variant="outline"
          onClick={() => setPreviewMode(!previewMode)}
        >
          {previewMode ? <EyeOff className="w-5 h-5 mr-2" /> : <Eye className="w-5 h-5 mr-2" />}
          {previewMode ? 'Edit' : 'Preview'}
        </Button>
      </div>

      {/* Error Message */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Basic Information */}
            <Card>
              <CardHeader>
                <CardTitle>Basic Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Page Type */}
                <div>
                  <Label htmlFor="page_type">
                    Page Type <span className="text-red-500">*</span>
                  </Label>
                  <Select
                    value={formData.page_type}
                    onValueChange={(value) => setFormData(prev => ({ ...prev, page_type: value as typeof PageType[keyof typeof PageType] }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {PAGE_TYPE_OPTIONS.map(option => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Title */}
                <div>
                  <Label htmlFor="title">
                    Title <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="title"
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                    placeholder="Page title"
                    required
                  />
                </div>

                {/* Language */}
                <div>
                  <Label htmlFor="language">Language</Label>
                  <Select
                    value={formData.language}
                    onValueChange={(value) => setFormData(prev => ({ ...prev, language: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {LANGUAGE_OPTIONS.map(option => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Default Page */}
                <div className="flex items-center gap-3">
                  <Checkbox
                    id="is_default"
                    checked={formData.is_default}
                    onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_default: checked as boolean }))}
                  />
                  <Label htmlFor="is_default" className="text-sm font-medium cursor-pointer">
                    Set as default page for this type
                  </Label>
                </div>
              </CardContent>
            </Card>

            {/* Content Editor */}
            <Card>
              <CardHeader>
                <CardTitle>Contenido</CardTitle>
              </CardHeader>
              <CardContent>
                {previewMode ? (
                  <div
                    className="prose max-w-none min-h-[400px] p-4 border border-gray-200 rounded-lg bg-gray-50"
                    dangerouslySetInnerHTML={{ __html: formData.html_content || '<p class="text-gray-500 italic">No hay contenido para mostrar</p>' }}
                  />
                ) : (
                  <WysiwygEditor
                    value={formData.html_content}
                    onChange={(content) => setFormData(prev => ({ ...prev, html_content: content }))}
                    placeholder="Write your page content here..."
                    height={400}
                  />
                )}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* SEO Settings */}
            <Card>
              <CardHeader>
                <CardTitle>SEO Configuration</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Meta Description */}
                <div>
                  <Label htmlFor="meta_description">Meta Description</Label>
                  <Textarea
                    id="meta_description"
                    value={formData.meta_description || ''}
                    onChange={(e) => setFormData(prev => ({ ...prev, meta_description: e.target.value }))}
                    rows={3}
                    placeholder="Description for search engines (max 160 characters)"
                    maxLength={160}
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    {(formData.meta_description || '').length}/160 characters
                  </p>
                </div>

                {/* Keywords */}
                <div>
                  <Label htmlFor="keywords">Keywords</Label>
                  <div className="flex gap-2 mb-2">
                    <Input
                      id="keywords"
                      type="text"
                      value={keywordInput}
                      onChange={(e) => setKeywordInput(e.target.value)}
                      onKeyPress={handleKeywordKeyPress}
                      placeholder="Add keyword"
                      className="flex-1"
                    />
                    <Button
                      type="button"
                      onClick={handleAddKeyword}
                      size="sm"
                    >
                      Add
                    </Button>
                  </div>

                  {(formData.meta_keywords || []).length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {(formData.meta_keywords || []).map((keyword, index) => (
                        <Badge key={index} variant="secondary" className="gap-1">
                          {keyword}
                          <button
                            type="button"
                            onClick={() => handleRemoveKeyword(keyword)}
                            className="text-blue-600 hover:text-blue-800"
                          >
                            ×
                          </button>
                        </Badge>
                      ))}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button
                  type="submit"
                  disabled={loading}
                  className="w-full"
                >
                  <Save className="w-5 h-5 mr-2" />
                  {loading ? 'Creating...' : 'Create Page'}
                </Button>

                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate('/company/pages')}
                  className="w-full"
                >
                  Cancel
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </form>
    </div>
  );
}
