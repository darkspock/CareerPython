import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
import { ArrowLeft, Save, X, Plus } from 'lucide-react';
import { companyCandidateService } from '../../services/companyCandidateService';
import type { Priority } from '../../types/companyCandidate';
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

export default function EditCandidatePage() {
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
  const { id } = useParams<{ id: string }>();
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [candidateInfo, setCandidateInfo] = useState({
    name: '',
    email: '',
    phone: '',
  });

  const [formData, setFormData] = useState({
    position: '',
    department: '',
    priority: 'MEDIUM' as Priority,
    tags: [] as string[],
    internal_notes: '',
  });

  const [tagInput, setTagInput] = useState('');

  useEffect(() => {
    if (id) {
      loadCandidate();
    }
  }, [id]);

  const loadCandidate = async () => {
    try {
      setLoadingData(true);
      const candidate = await companyCandidateService.getById(id!);

      // Set candidate basic info (read-only)
      setCandidateInfo({
        name: candidate.candidate_name || 'N/A',
        email: candidate.candidate_email || 'N/A',
        phone: candidate.candidate_phone || 'N/A',
      });

      // Set editable form data
      setFormData({
        position: '', // This field doesn't exist in the response, keeping empty
        department: '', // This field doesn't exist in the response, keeping empty
        priority: candidate.priority,
        tags: candidate.tags || [],
        internal_notes: candidate.internal_notes || '',
      });
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load candidate');
      console.error('Error loading candidate:', err);
    } finally {
      setLoadingData(false);
    }
  };

  const handleAddTag = () => {
    if (tagInput.trim() && !formData.tags.includes(tagInput.trim())) {
      setFormData({
        ...formData,
        tags: [...formData.tags, tagInput.trim()],
      });
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setFormData({
      ...formData,
      tags: formData.tags.filter((tag) => tag !== tagToRemove),
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      setLoading(true);

      await companyCandidateService.update(id!, {
        priority: formData.priority,
        tags: formData.tags,
        internal_notes: formData.internal_notes || undefined,
      });

      navigate(getPath(`candidates/${id}`));
    } catch (err: any) {
      setError(err.message || 'Failed to update candidate');
      console.error('Error updating candidate:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loadingData) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <Button
          variant="ghost"
          onClick={() => navigate(getPath(`candidates/${id}`))}
          className="mb-4"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Candidate
        </Button>
        <h1 className="text-2xl font-bold text-gray-900">Edit Candidate</h1>
        <p className="text-gray-600 mt-1">Update candidate information</p>
      </div>

      {/* Error Message */}
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit}>
        <Card>
          <CardContent className="pt-6 space-y-6">
            {/* Candidate Basic Info (Read-only) */}
            <Card className="bg-gray-50">
              <CardHeader>
                <CardTitle className="text-lg">Candidate</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <Label className="text-xs text-gray-500 uppercase mb-1">Name</Label>
                    <p className="text-sm text-gray-900">{candidateInfo.name}</p>
                  </div>
                  <div>
                    <Label className="text-xs text-gray-500 uppercase mb-1">Email</Label>
                    <p className="text-sm text-gray-900">{candidateInfo.email}</p>
                  </div>
                  <div>
                    <Label className="text-xs text-gray-500 uppercase mb-1">Phone</Label>
                    <p className="text-sm text-gray-900">{candidateInfo.phone}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Company-Candidate Relationship Information (Editable) */}
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Position & Department</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Position */}
                <div>
                  <Label htmlFor="position">Position</Label>
                  <Input
                    id="position"
                    type="text"
                    value={formData.position}
                    onChange={(e) =>
                      setFormData({ ...formData, position: e.target.value })
                    }
                    placeholder="e.g., Senior Software Engineer"
                  />
                </div>

                {/* Department */}
                <div>
                  <Label htmlFor="department">Department</Label>
                  <Input
                    id="department"
                    type="text"
                    value={formData.department}
                    onChange={(e) =>
                      setFormData({ ...formData, department: e.target.value })
                    }
                    placeholder="e.g., Engineering"
                  />
                </div>

                {/* Priority */}
                <div className="md:col-span-2">
                  <Label htmlFor="priority">Priority</Label>
                  <Select
                    value={formData.priority}
                    onValueChange={(value) =>
                      setFormData({ ...formData, priority: value as Priority })
                    }
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="LOW">Low</SelectItem>
                      <SelectItem value="MEDIUM">Medium</SelectItem>
                      <SelectItem value="HIGH">High</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>

            {/* Tags */}
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Tags</h2>
              <div className="space-y-3">
                {/* Tag Input */}
                <div className="flex gap-2">
                  <Input
                    type="text"
                    value={tagInput}
                    onChange={(e) => setTagInput(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault();
                        handleAddTag();
                      }
                    }}
                    placeholder="Add a tag (e.g., Frontend, React, Senior)"
                    className="flex-1"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleAddTag}
                    title="Add tag"
                  >
                    <Plus className="w-5 h-5" />
                  </Button>
                </div>

                {/* Tags Display */}
                {formData.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {formData.tags.map((tag, idx) => (
                      <Badge key={idx} variant="secondary" className="gap-2">
                        {tag}
                        <button
                          type="button"
                          onClick={() => handleRemoveTag(tag)}
                          className="hover:text-blue-900"
                          title="Remove tag"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Internal Notes */}
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Internal Notes</h2>
              <Textarea
                value={formData.internal_notes}
                onChange={(e) =>
                  setFormData({ ...formData, internal_notes: e.target.value })
                }
                rows={4}
                placeholder="Add any internal notes about this candidate..."
              />
            </div>

            {/* Actions */}
            <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate(getPath(`candidates/${id}`))}
              >
                Cancel
              </Button>
              <Button type="submit" disabled={loading}>
                <Save className="w-5 h-5 mr-2" />
                {loading ? 'Saving...' : 'Save Changes'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </form>
    </div>
  );
}
