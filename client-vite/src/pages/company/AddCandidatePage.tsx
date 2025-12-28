import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
import { ArrowLeft, Save, Plus, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { companyCandidateService } from '../../services/companyCandidateService';
import { PositionService } from '../../services/positionService';
import type { Priority } from '../../types/companyCandidate';
import type { Position } from '../../types/position';

export default function AddCandidatePage() {
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    candidate_name: '',
    candidate_email: '',
    candidate_phone: '',
    priority: 'MEDIUM' as Priority,
    tags: [] as string[],
    internal_notes: '',
    job_position_id: undefined as string | undefined,
  });

  const [tagInput, setTagInput] = useState('');
  const [positions, setPositions] = useState<Position[]>([]);
  const [loadingPositions, setLoadingPositions] = useState(false);

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

  const getCompanyUserId = () => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_user_id || payload.sub;
    } catch {
      return null;
    }
  };

  useEffect(() => {
    const loadActivePositions = async () => {
      const companyId = getCompanyId();
      if (!companyId) return;

      try {
        setLoadingPositions(true);
        const response = await PositionService.getPositions({
          company_id: companyId,
          page_size: 100,
          is_active: true,
        });
        setPositions(response.positions);
      } catch (err) {
        console.error('Error loading positions:', err);
        try {
          const response = await PositionService.getPositions({
            company_id: companyId,
            page_size: 100,
          });
          setPositions(response.positions);
        } catch (err2) {
          console.error('Error loading positions (fallback):', err2);
        }
      } finally {
        setLoadingPositions(false);
      }
    };

    loadActivePositions();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const companyId = getCompanyId();
    const companyUserId = getCompanyUserId();

    if (!companyId) {
      setError('Company ID not found');
      return;
    }

    if (!companyUserId) {
      setError('Company User ID not found');
      return;
    }

    if (!formData.candidate_name || !formData.candidate_email) {
      setError('Candidate name and email are required');
      return;
    }

    if (!formData.job_position_id) {
      setError('Job position is required');
      return;
    }

    try {
      setLoading(true);

      await companyCandidateService.create({
        company_id: companyId,
        candidate_name: formData.candidate_name,
        candidate_email: formData.candidate_email,
        candidate_phone: formData.candidate_phone || undefined,
        priority: formData.priority,
        tags: formData.tags,
        internal_notes: formData.internal_notes || undefined,
        created_by_user_id: companyUserId,
        job_position_id: formData.job_position_id || undefined,
      });

      navigate(getPath('candidates'));
    } catch (err: any) {
      setError(err.message || 'Failed to add candidate');
      console.error('Error adding candidate:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <Button
          variant="ghost"
          onClick={() => navigate(getPath('candidates'))}
          className="mb-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Candidates
        </Button>
        <h1 className="text-2xl font-bold text-gray-900">Add New Candidate</h1>
        <p className="text-muted-foreground mt-1">Create a new candidate profile</p>
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
          <CardHeader>
            <CardTitle>Candidate Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Basic Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Name */}
              <div className="md:col-span-2 space-y-2">
                <Label htmlFor="candidate_name">
                  Full Name <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="candidate_name"
                  type="text"
                  required
                  value={formData.candidate_name}
                  onChange={(e) =>
                    setFormData({ ...formData, candidate_name: e.target.value })
                  }
                  placeholder="John Doe"
                />
              </div>

              {/* Email */}
              <div className="space-y-2">
                <Label htmlFor="candidate_email">
                  Email <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="candidate_email"
                  type="email"
                  required
                  value={formData.candidate_email}
                  onChange={(e) =>
                    setFormData({ ...formData, candidate_email: e.target.value })
                  }
                  placeholder="john@example.com"
                />
              </div>

              {/* Phone */}
              <div className="space-y-2">
                <Label htmlFor="candidate_phone">Phone</Label>
                <Input
                  id="candidate_phone"
                  type="tel"
                  value={formData.candidate_phone}
                  onChange={(e) =>
                    setFormData({ ...formData, candidate_phone: e.target.value })
                  }
                  placeholder="+1 234 567 8900"
                />
              </div>

              {/* Priority */}
              <div className="space-y-2">
                <Label htmlFor="priority">Priority</Label>
                <Select
                  value={formData.priority}
                  onValueChange={(value) =>
                    setFormData({ ...formData, priority: value as Priority })
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select priority" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="LOW">Low</SelectItem>
                    <SelectItem value="MEDIUM">Medium</SelectItem>
                    <SelectItem value="HIGH">High</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Job Position */}
              <div className="space-y-2">
                <Label htmlFor="job_position_id">
                  Job Position <span className="text-red-500">*</span>
                </Label>
                <Select
                  value={formData.job_position_id || ''}
                  onValueChange={(value) =>
                    setFormData({ ...formData, job_position_id: value || undefined })
                  }
                  disabled={loadingPositions}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select a position" />
                  </SelectTrigger>
                  <SelectContent>
                    {positions.map((position) => (
                      <SelectItem key={position.id} value={position.id}>
                        {position.title}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {loadingPositions && (
                  <p className="text-xs text-muted-foreground">Loading positions...</p>
                )}
              </div>
            </div>

            {/* Tags */}
            <div className="space-y-3">
              <Label>Tags</Label>
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
                  variant="secondary"
                  onClick={handleAddTag}
                  size="icon"
                >
                  <Plus className="w-4 h-4" />
                </Button>
              </div>

              {formData.tags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {formData.tags.map((tag, idx) => (
                    <Badge
                      key={idx}
                      variant="secondary"
                      className="flex items-center gap-1"
                    >
                      {tag}
                      <button
                        type="button"
                        onClick={() => handleRemoveTag(tag)}
                        className="ml-1 hover:text-destructive"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </Badge>
                  ))}
                </div>
              )}
            </div>

            {/* Internal Notes */}
            <div className="space-y-2">
              <Label htmlFor="internal_notes">Internal Notes</Label>
              <Textarea
                id="internal_notes"
                value={formData.internal_notes}
                onChange={(e) =>
                  setFormData({ ...formData, internal_notes: e.target.value })
                }
                rows={4}
                placeholder="Add any internal notes about this candidate..."
              />
            </div>

            {/* Actions */}
            <div className="flex items-center justify-end gap-3 pt-4 border-t">
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate(getPath('candidates'))}
              >
                Cancel
              </Button>
              <Button type="submit" disabled={loading}>
                <Save className="w-4 h-4 mr-2" />
                {loading ? 'Adding...' : 'Add Candidate'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </form>
    </div>
  );
}
