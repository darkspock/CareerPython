import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { ArrowLeft, Save } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { PositionService } from '../../services/positionService';
import type { CreatePositionRequest, JobPositionWorkflow } from '../../types/position';
import { PhaseWorkflowSelector } from '../../components/workflow';
import { WysiwygEditor } from '../../components/common';

export default function CreatePositionPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentWorkflow, setCurrentWorkflow] = useState<JobPositionWorkflow | null>(null);
  const [loadingWorkflow, setLoadingWorkflow] = useState(false);

  const [formData, setFormData] = useState<CreatePositionRequest>({
    company_id: '',
    job_position_workflow_id: null,
    phase_workflows: {},
    title: '',
    description: '',
    job_category: 'Other',
    custom_fields_values: {},
    application_deadline: '',
    visibility: 'hidden',
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
    const loadWorkflow = async () => {
      const companyId = getCompanyId();
      if (!companyId) {
        return;
      }

      const workflowId = searchParams.get('workflow_id');

      if (!workflowId) {
        try {
          setLoadingWorkflow(true);
          const workflows = await PositionService.getWorkflows(companyId);
          if (workflows.length > 0) {
            const defaultWorkflow = workflows[0];
            const fullWorkflow = await PositionService.getWorkflow(defaultWorkflow.id);
            setCurrentWorkflow(fullWorkflow);
            setFormData(prev => ({
              ...prev,
              job_position_workflow_id: defaultWorkflow.id,
              stage_id: fullWorkflow.stages && fullWorkflow.stages.length > 0 ? fullWorkflow.stages[0].id : undefined
            }));
          } else {
            setError('No workflows available. Please create a workflow first.');
          }
        } catch (err: any) {
          console.error('Error loading default workflow:', err);
          setError('Failed to load workflow. Please go back and select a workflow.');
        } finally {
          setLoadingWorkflow(false);
        }
        return;
      }

      try {
        setLoadingWorkflow(true);
        const fullWorkflow = await PositionService.getWorkflow(workflowId);
        setCurrentWorkflow(fullWorkflow);

        setFormData(prev => ({
          ...prev,
          job_position_workflow_id: workflowId,
          stage_id: fullWorkflow.stages && fullWorkflow.stages.length > 0 ? fullWorkflow.stages[0].id : undefined
        }));
      } catch (err: any) {
        console.error('Error loading workflow:', err);
        setError('Failed to load workflow. Please go back and select a workflow.');
      } finally {
        setLoadingWorkflow(false);
      }
    };

    loadWorkflow();
  }, [searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const companyId = getCompanyId();
    if (!companyId) {
      setError('Company ID not found');
      return;
    }

    if (loadingWorkflow) {
      setError('Please wait while the workflow is being loaded...');
      return;
    }

    if (!formData.title) {
      setError('Title is required');
      return;
    }

    const workflowIdFromUrl = searchParams.get('workflow_id');
    if (!formData.job_position_workflow_id) {
      if (workflowIdFromUrl) {
        setError('Workflow is still loading. Please wait a moment and try again.');
        return;
      }

      try {
        setLoadingWorkflow(true);
        const workflows = await PositionService.getWorkflows(companyId);
        if (workflows.length > 0) {
          const defaultWorkflow = workflows[0];
          const fullWorkflow = await PositionService.getWorkflow(defaultWorkflow.id);
          setCurrentWorkflow(fullWorkflow);
          setFormData(prev => ({
            ...prev,
            job_position_workflow_id: defaultWorkflow.id,
            stage_id: fullWorkflow.stages && fullWorkflow.stages.length > 0 ? fullWorkflow.stages[0].id : undefined
          }));
        } else {
          setError('No workflows available. Please create a workflow first.');
          setLoadingWorkflow(false);
          return;
        }
      } catch (err: any) {
        console.error('Error loading default workflow:', err);
        setError('Failed to load workflow. Please go back and select a workflow.');
        setLoadingWorkflow(false);
        return;
      } finally {
        setLoadingWorkflow(false);
      }
    }

    try {
      setLoading(true);

      const finalWorkflowId = formData.job_position_workflow_id || workflowIdFromUrl;
      if (!finalWorkflowId) {
        setError('Opening Flow (Job Position Workflow) is required. Please go back and select a workflow.');
        return;
      }

      const requestData: CreatePositionRequest = {
        ...formData,
        company_id: companyId,
        job_position_workflow_id: finalWorkflowId,
      };

      await PositionService.createPosition(requestData);
      navigate('/company/positions');
    } catch (err: any) {
      setError(err.message || 'Failed to create position');
      console.error('Error creating position:', err);
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
          onClick={() => navigate('/company/positions')}
          className="mb-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Positions
        </Button>
        <h1 className="text-2xl font-bold text-gray-900">
          Create Job Position
          {currentWorkflow && !loadingWorkflow && (
            <span className="text-lg font-normal text-muted-foreground"> ({currentWorkflow.name})</span>
          )}
        </h1>
        <p className="text-muted-foreground mt-1">Post a new job opening</p>
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
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Title */}
              <div className="space-y-2">
                <Label htmlFor="title">
                  Job Title <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="title"
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                  placeholder="e.g., Senior Software Engineer"
                />
              </div>

              {/* Application Deadline */}
              <div className="space-y-2">
                <Label htmlFor="application_deadline">Application Deadline</Label>
                <Input
                  id="application_deadline"
                  type="date"
                  value={formData.application_deadline || ''}
                  onChange={(e) => setFormData(prev => ({ ...prev, application_deadline: e.target.value }))}
                />
              </div>

              {/* Job Category */}
              <div className="space-y-2">
                <Label htmlFor="job_category">
                  Job Category <span className="text-red-500">*</span>
                </Label>
                <Select
                  value={formData.job_category || 'Other'}
                  onValueChange={(value) => setFormData(prev => ({ ...prev, job_category: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Technology">Technology</SelectItem>
                    <SelectItem value="Operations">Operations</SelectItem>
                    <SelectItem value="Sales">Sales</SelectItem>
                    <SelectItem value="Marketing">Marketing</SelectItem>
                    <SelectItem value="Administration">Administration</SelectItem>
                    <SelectItem value="Human Resources">Human Resources</SelectItem>
                    <SelectItem value="Finance">Finance</SelectItem>
                    <SelectItem value="Customer Service">Customer Service</SelectItem>
                    <SelectItem value="Other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Visibility Options */}
              <div className="md:col-span-2 space-y-2">
                <Label>
                  Visibility <span className="text-red-500">*</span>
                </Label>
                <div className="flex flex-wrap items-center gap-6">
                  <div className="flex items-center gap-2">
                    <input
                      type="radio"
                      id="visibility-hidden"
                      name="visibility"
                      value="hidden"
                      checked={formData.visibility === 'hidden'}
                      onChange={(e) => setFormData(prev => ({ ...prev, visibility: e.target.value as 'hidden' | 'internal' | 'public' }))}
                      className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                    />
                    <Label htmlFor="visibility-hidden" className="font-normal">
                      Hidden - Only visible internally
                    </Label>
                  </div>
                  <div className="flex items-center gap-2">
                    <input
                      type="radio"
                      id="visibility-internal"
                      name="visibility"
                      value="internal"
                      checked={formData.visibility === 'internal'}
                      onChange={(e) => setFormData(prev => ({ ...prev, visibility: e.target.value as 'hidden' | 'internal' | 'public' }))}
                      className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                    />
                    <Label htmlFor="visibility-internal" className="font-normal">
                      Internal - Visible to company users
                    </Label>
                  </div>
                  <div className="flex items-center gap-2">
                    <input
                      type="radio"
                      id="visibility-public"
                      name="visibility"
                      value="public"
                      checked={formData.visibility === 'public'}
                      onChange={(e) => setFormData(prev => ({ ...prev, visibility: e.target.value as 'hidden' | 'internal' | 'public' }))}
                      className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                    />
                    <Label htmlFor="visibility-public" className="font-normal">
                      Public - Visible on job board (for candidates)
                    </Label>
                  </div>
                </div>
              </div>

              {/* Workflow Info */}
              {loadingWorkflow && (
                <div className="md:col-span-2">
                  <Alert className="border-blue-200 bg-blue-50">
                    <AlertDescription className="text-blue-800">
                      <span className="font-medium">Opening Flow:</span> Loading workflow...
                    </AlertDescription>
                  </Alert>
                </div>
              )}
              {currentWorkflow && !loadingWorkflow && (
                <div className="md:col-span-2">
                  <Alert className="border-blue-200 bg-blue-50">
                    <AlertDescription className="text-blue-800">
                      <span className="font-medium">Opening Flow:</span> {currentWorkflow.name}
                    </AlertDescription>
                  </Alert>
                </div>
              )}

              {/* Phase-Workflow Configuration */}
              <div className="md:col-span-2">
                <PhaseWorkflowSelector
                  companyId={getCompanyId() || ''}
                  phaseWorkflows={formData.phase_workflows || {}}
                  onChange={(phaseWorkflows) => setFormData(prev => ({ ...prev, phase_workflows: phaseWorkflows }))}
                  label="Interview Process Flow Configuration"
                />
              </div>

              {/* Description */}
              <div className="md:col-span-2 space-y-2">
                <Label htmlFor="description">
                  Job Description <span className="text-red-500">*</span>
                </Label>
                <div className="border rounded-lg overflow-hidden">
                  <WysiwygEditor
                    value={formData.description || ''}
                    onChange={(content) => setFormData(prev => ({ ...prev, description: content }))}
                    placeholder="Describe the role, responsibilities, and what you're looking for..."
                    height={400}
                    className="w-full"
                  />
                </div>
                <p className="text-sm text-muted-foreground">
                  Use the toolbar above to format text, add images, create lists, and structure your job description.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate('/company/positions')}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            disabled={loading || loadingWorkflow || (!formData.job_position_workflow_id && !searchParams.get('workflow_id'))}
          >
            <Save className="w-4 h-4 mr-2" />
            {loadingWorkflow ? 'Loading workflow...' : loading ? 'Creating...' : 'Create Position'}
          </Button>
        </div>
      </form>
    </div>
  );
}
