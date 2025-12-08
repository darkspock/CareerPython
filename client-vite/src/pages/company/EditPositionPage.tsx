import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Save } from 'lucide-react';
import { PositionService } from '../../services/positionService';
import type { UpdatePositionRequest, Position, JobPositionWorkflow } from '../../types/position';
import { DynamicCustomFields } from '../../components/jobPosition/DynamicCustomFields';
import { PositionQuestionsEditor } from '../../components/jobPosition/PositionQuestionsEditor';
import { WysiwygEditor } from '../../components/common';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

export default function EditPositionPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [, setPosition] = useState<Position | null>(null);
  const [workflows, setWorkflows] = useState<JobPositionWorkflow[]>([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState<JobPositionWorkflow | null>(null);

  const [formData, setFormData] = useState<UpdatePositionRequest>({
    job_position_workflow_id: null,
    stage_id: null,
    phase_workflows: {},
    custom_fields_values: {},
    title: '',
    description: '',
    job_category: 'other',
    visibility: 'hidden',
    open_at: null,
    application_deadline: null,
    public_slug: null,
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
    if (id) {
      loadPosition();
      loadWorkflows();
    }
  }, [id]);

  useEffect(() => {
    if (formData.job_position_workflow_id && workflows.length > 0) {
      const workflow = workflows.find(w => w.id === formData.job_position_workflow_id);
      setSelectedWorkflow(workflow || null);
    } else {
      setSelectedWorkflow(null);
    }
  }, [formData.job_position_workflow_id, workflows]);

  const loadPosition = async () => {
    if (!id) return;

    try {
      setLoading(true);
      const positionData = await PositionService.getPositionById(id);

      // Load workflow if available
      if (positionData.job_position_workflow_id) {
        try {
          const workflowData = await PositionService.getWorkflow(positionData.job_position_workflow_id);
          console.log('[EditPositionPage] Loaded workflow:', workflowData);
          console.log('[EditPositionPage] Workflow custom_fields_config:', workflowData.custom_fields_config);
          setSelectedWorkflow(workflowData);
        } catch (err) {
          console.error('Error loading workflow:', err);
        }
      }

      setPosition(positionData);

      // Convert Position to form data (simplified)
      setFormData({
        job_position_workflow_id: positionData.job_position_workflow_id || null,
        stage_id: positionData.stage_id || null,
        phase_workflows: positionData.phase_workflows || {},
        custom_fields_values: positionData.custom_fields_values || {},
        title: positionData.title,
        description: positionData.description || '',
        job_category: positionData.job_category || 'other',
        visibility: positionData.visibility || 'hidden',
        open_at: positionData.open_at || null,
        application_deadline: positionData.application_deadline || null,
        public_slug: positionData.public_slug || null,
      });

      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load position');
      console.error('Error loading position:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadWorkflows = async () => {
    try {
      const companyId = getCompanyId();
      if (!companyId) return;

      const workflowsList = await PositionService.getWorkflows(companyId);
      setWorkflows(workflowsList);
    } catch (err) {
      console.error('Error loading workflows:', err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!id) {
      setError('Position ID not found');
      return;
    }

    if (!formData.title) {
      setError('Title is required');
      return;
    }

    try {
      setSaving(true);
      await PositionService.updatePosition(id, formData);
      navigate(`/company/positions/${id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to update position');
      console.error('Error updating position:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleWorkflowChange = async (workflowId: string | null) => {
    setFormData({
      ...formData,
      job_position_workflow_id: workflowId,
      stage_id: null, // Reset stage when workflow changes
    });

    if (workflowId) {
      try {
        const workflowData = await PositionService.getWorkflow(workflowId);
        setSelectedWorkflow(workflowData);
      } catch (err) {
        console.error('Error loading workflow:', err);
      }
    } else {
      setSelectedWorkflow(null);
    }
  };

  const currentStage = selectedWorkflow?.stages.find(
    (s) => s.id === formData.stage_id
  ) || null;

  if (loading) {
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
          onClick={() => navigate(`/company/positions/${id}`)}
          className="mb-4"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Position
        </Button>
        <h1 className="text-2xl font-bold text-gray-900">Edit Position</h1>
        <p className="text-gray-600 mt-1">Update job opening details</p>
      </div>

      {/* Error Message */}
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <Card>
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <Label htmlFor="title">
                  Job Title <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="title"
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="e.g., Senior Software Engineer"
                />
              </div>

              <div>
                <Label htmlFor="job_category">Job Category</Label>
                <Select
                  value={formData.job_category}
                  onValueChange={(value) => setFormData({ ...formData, job_category: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="other">Other</SelectItem>
                    <SelectItem value="engineering">Engineering</SelectItem>
                    <SelectItem value="design">Design</SelectItem>
                    <SelectItem value="product">Product</SelectItem>
                    <SelectItem value="marketing">Marketing</SelectItem>
                    <SelectItem value="sales">Sales</SelectItem>
                    <SelectItem value="operations">Operations</SelectItem>
                    <SelectItem value="hr">HR</SelectItem>
                    <SelectItem value="finance">Finance</SelectItem>
                    <SelectItem value="legal">Legal</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="visibility">Visibility</Label>
                <Select
                  value={formData.visibility}
                  onValueChange={(value) => setFormData({ ...formData, visibility: value as any })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="hidden">Hidden</SelectItem>
                    <SelectItem value="internal">Internal</SelectItem>
                    <SelectItem value="public">Public</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Workflow Selector */}
              <div className="md:col-span-2">
                <Label htmlFor="workflow">Workflow</Label>
                <Select
                  value={formData.job_position_workflow_id || ''}
                  onValueChange={(value) => handleWorkflowChange(value || null)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="No Workflow (Legacy)" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="">No Workflow (Legacy)</SelectItem>
                    {workflows.map((workflow) => (
                      <SelectItem key={workflow.id} value={workflow.id}>
                        {workflow.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <p className="mt-1 text-sm text-gray-500">
                  Select a workflow to manage this position through stages
                </p>
              </div>

              {/* Stage Selector */}
              {selectedWorkflow && selectedWorkflow.stages.length > 0 && (
                <div className="md:col-span-2">
                  <Label htmlFor="stage">Current Stage</Label>
                  <Select
                    value={formData.stage_id || ''}
                    onValueChange={(value) => setFormData({ ...formData, stage_id: value || null })}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="No Stage" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">No Stage</SelectItem>
                      {selectedWorkflow.stages.map((stage) => (
                        <SelectItem key={stage.id} value={stage.id}>
                          {stage.name} ({stage.status_mapping})
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <p className="mt-1 text-sm text-gray-500">
                    Current stage in the workflow
                  </p>
                </div>
              )}

              {/* Description */}
              <div className="md:col-span-2">
                <Label htmlFor="description">Job Description</Label>
                <div className="border border-gray-300 rounded-lg overflow-hidden">
                  <WysiwygEditor
                    value={formData.description || ''}
                    onChange={(content) => setFormData({ ...formData, description: content })}
                    placeholder="Describe the role, responsibilities, and what you're looking for..."
                    height={400}
                    className="w-full"
                  />
                </div>
              </div>

              {/* Dates */}
              <div>
                <Label htmlFor="open_at">Open At</Label>
                <Input
                  id="open_at"
                  type="datetime-local"
                  value={formData.open_at ? new Date(formData.open_at).toISOString().slice(0, 16) : ''}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      open_at: e.target.value ? new Date(e.target.value).toISOString() : null,
                    })
                  }
                />
              </div>

              <div>
                <Label htmlFor="application_deadline">Application Deadline</Label>
                <Input
                  id="application_deadline"
                  type="date"
                  value={formData.application_deadline || ''}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      application_deadline: e.target.value || null,
                    })
                  }
                />
              </div>

              {/* Public Slug */}
              <div className="md:col-span-2">
                <Label htmlFor="public_slug">Public Slug (SEO)</Label>
                <Input
                  id="public_slug"
                  type="text"
                  value={formData.public_slug || ''}
                  onChange={(e) => setFormData({ ...formData, public_slug: e.target.value || null })}
                  placeholder="e.g., senior-software-engineer"
                />
                <p className="mt-1 text-sm text-gray-500">
                  URL-friendly identifier for public job board
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Custom Fields */}
        {selectedWorkflow && (
          <Card>
            <CardHeader>
              <CardTitle>Custom Fields</CardTitle>
            </CardHeader>
            <CardContent>
              <DynamicCustomFields
                workflow={selectedWorkflow}
                currentStage={currentStage}
                customFieldsValues={formData.custom_fields_values || {}}
                onChange={(values) => setFormData({ ...formData, custom_fields_values: values })}
                readOnly={false}
              />
            </CardContent>
          </Card>
        )}

        {/* Application Questions */}
        {selectedWorkflow && id && (
          <Card>
            <CardContent className="pt-6">
              <PositionQuestionsEditor
                positionId={id}
                workflowId={selectedWorkflow.id}
              />
            </CardContent>
          </Card>
        )}

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate(`/company/positions/${id}`)}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={saving}>
            <Save className="w-5 h-5 mr-2" />
            {saving ? 'Saving...' : 'Save Changes'}
          </Button>
        </div>
      </form>
    </div>
  );
}
