import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, Plus, X, ArrowUp, ArrowDown } from 'lucide-react';
import { PositionService } from '../../services/positionService';
import { api } from '../../lib/api';
import type { CompanyRole } from '../../types/company';
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

interface StageFormData {
  id: string;
  name: string;
  icon: string;
  background_color: string;
  text_color: string;
  role?: string | null;
  status_mapping: string;
  kanban_display: string;
  field_visibility: Record<string, boolean>;
  field_validation: Record<string, any>;
  field_candidate_visibility: Record<string, boolean>;
}

export default function CreateJobPositionWorkflowPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [workflowName, setWorkflowName] = useState('');
  const [defaultView, setDefaultView] = useState('kanban');
  const [companyRoles, setCompanyRoles] = useState<CompanyRole[]>([]);
  const [stages, setStages] = useState<StageFormData[]>([
    {
      id: `stage-${Date.now()}`,
      name: 'Draft',
      icon: '📝',
      background_color: '#E5E7EB',
      text_color: '#374151',
      status_mapping: 'draft',
      kanban_display: 'vertical',
      field_visibility: {},
      field_validation: {},
      field_candidate_visibility: {},
    },
    {
      id: `stage-${Date.now() + 1}`,
      name: 'Active',
      icon: '✅',
      background_color: '#10B981',
      text_color: '#FFFFFF',
      status_mapping: 'active',
      kanban_display: 'vertical',
      field_visibility: {},
      field_validation: {},
      field_candidate_visibility: {},
    },
  ]);

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
    loadCompanyRoles();
  }, []);

  const loadCompanyRoles = async () => {
    const companyId = getCompanyId();
    if (!companyId) return;

    try {
      const response = await api.listCompanyRoles(companyId, false);
      setCompanyRoles(response as CompanyRole[]);
    } catch (err: any) {
      console.error('Error loading company roles:', err);
    }
  };

  const generateStageId = () => {
    return `stage-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  };

  const handleAddStage = () => {
    setStages([
      ...stages,
      {
        id: generateStageId(),
        name: '',
        icon: '📋',
        background_color: '#E5E7EB',
        text_color: '#374151',
        status_mapping: 'draft',
        kanban_display: 'vertical',
        field_visibility: {},
        field_validation: {},
        field_candidate_visibility: {},
      },
    ]);
  };

  const handleRemoveStage = (index: number) => {
    setStages(stages.filter((_, i) => i !== index));
  };

  const handleStageChange = (index: number, field: keyof StageFormData, value: any) => {
    const newStages = [...stages];
    newStages[index] = { ...newStages[index], [field]: value };
    setStages(newStages);
  };

  const handleMoveStageUp = (index: number) => {
    if (index === 0) return;
    const newStages = [...stages];
    [newStages[index - 1], newStages[index]] = [newStages[index], newStages[index - 1]];
    setStages(newStages);
  };

  const handleMoveStageDown = (index: number) => {
    if (index === stages.length - 1) return;
    const newStages = [...stages];
    [newStages[index], newStages[index + 1]] = [newStages[index + 1], newStages[index]];
    setStages(newStages);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const companyId = getCompanyId();
    if (!companyId) {
      setError('Company ID not found');
      return;
    }

    if (!workflowName.trim()) {
      setError('Workflow name is required');
      return;
    }

    if (stages.length === 0) {
      setError('At least one stage is required');
      return;
    }

    // Validate stages
    for (const stage of stages) {
      if (!stage.name.trim()) {
        setError(`Stage ${stages.indexOf(stage) + 1} name is required`);
        return;
      }
    }

    try {
      setLoading(true);
      await PositionService.createWorkflow({
        company_id: companyId,
        name: workflowName,
        default_view: defaultView,
        stages: stages.map((stage) => ({
          id: stage.id,
          name: stage.name,
          icon: stage.icon,
          background_color: stage.background_color,
          text_color: stage.text_color,
          role: stage.role || null,
          status_mapping: stage.status_mapping,
          kanban_display: stage.kanban_display,
          field_visibility: stage.field_visibility,
          field_validation: stage.field_validation,
          field_candidate_visibility: stage.field_candidate_visibility,
        })),
        custom_fields_config: {},
      });

      navigate('/company/settings/job-position-workflows');
    } catch (err: any) {
      setError(err.message || 'Failed to create workflow');
      console.error('Error creating workflow:', err);
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
          onClick={() => navigate('/company/settings/job-position-workflows')}
          className="mb-4"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Workflows
        </Button>
        <h1 className="text-2xl font-bold text-gray-900">Create Job Position Workflow</h1>
        <p className="text-gray-600 mt-1">Create a new workflow for managing job positions</p>
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
                <Label htmlFor="workflow_name">
                  Workflow Name <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="workflow_name"
                  type="text"
                  required
                  value={workflowName}
                  onChange={(e) => setWorkflowName(e.target.value)}
                  placeholder="e.g., Standard Hiring Process"
                />
              </div>

              <div>
                <Label htmlFor="default_view">Default View</Label>
                <Select value={defaultView} onValueChange={setDefaultView}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="kanban">Kanban</SelectItem>
                    <SelectItem value="list">List</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Stages */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Stages</CardTitle>
              <Button
                type="button"
                onClick={handleAddStage}
                size="sm"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Stage
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {stages.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No stages yet. Click "Add Stage" to create one.
              </div>
            ) : (
              <div className="space-y-4">
                {stages.map((stage, index) => (
                  <Card key={stage.id}>
                    <CardContent className="pt-6">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center gap-2">
                          <span className="text-lg">{stage.icon}</span>
                          <h3 className="font-semibold text-gray-900">Stage {index + 1}</h3>
                        </div>
                        <div className="flex items-center gap-2">
                          <Button
                            type="button"
                            variant="ghost"
                            size="sm"
                            onClick={() => handleMoveStageUp(index)}
                            disabled={index === 0}
                            title="Move up"
                          >
                            <ArrowUp className="w-4 h-4" />
                          </Button>
                          <Button
                            type="button"
                            variant="ghost"
                            size="sm"
                            onClick={() => handleMoveStageDown(index)}
                            disabled={index === stages.length - 1}
                            title="Move down"
                          >
                            <ArrowDown className="w-4 h-4" />
                          </Button>
                          <Button
                            type="button"
                            variant="ghost"
                            size="sm"
                            onClick={() => handleRemoveStage(index)}
                            title="Remove stage"
                          >
                            <X className="w-4 h-4 text-red-600" />
                          </Button>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <Label>Stage Name *</Label>
                          <Input
                            type="text"
                            required
                            value={stage.name}
                            onChange={(e) => handleStageChange(index, 'name', e.target.value)}
                          />
                        </div>

                        <div>
                          <Label>Icon (Emoji)</Label>
                          <Input
                            type="text"
                            value={stage.icon}
                            onChange={(e) => handleStageChange(index, 'icon', e.target.value)}
                            placeholder="📝"
                          />
                        </div>

                        <div>
                          <Label>Background Color</Label>
                          <Input
                            type="color"
                            value={stage.background_color}
                            onChange={(e) => handleStageChange(index, 'background_color', e.target.value)}
                            className="h-10"
                          />
                        </div>

                        <div>
                          <Label>Text Color</Label>
                          <Input
                            type="color"
                            value={stage.text_color}
                            onChange={(e) => handleStageChange(index, 'text_color', e.target.value)}
                            className="h-10"
                          />
                        </div>

                        <div>
                          <Label>Status Mapping *</Label>
                          <Select
                            value={stage.status_mapping}
                            onValueChange={(value) => handleStageChange(index, 'status_mapping', value)}
                          >
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="draft">Draft</SelectItem>
                              <SelectItem value="active">Active</SelectItem>
                              <SelectItem value="paused">Paused</SelectItem>
                              <SelectItem value="closed">Closed</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>

                        <div>
                          <Label>Kanban Display</Label>
                          <Select
                            value={stage.kanban_display}
                            onValueChange={(value) => handleStageChange(index, 'kanban_display', value)}
                          >
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="vertical">Vertical (Column)</SelectItem>
                              <SelectItem value="horizontal_bottom">Horizontal (Row)</SelectItem>
                              <SelectItem value="hidden">Hidden</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>

                        <div>
                          <Label>Responsible Role</Label>
                          <Select
                            value={stage.role || ''}
                            onValueChange={(value) => handleStageChange(index, 'role', value || null)}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Not assigned" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="">Not assigned</SelectItem>
                              {companyRoles.map((role) => (
                                <SelectItem key={role.id} value={role.id}>
                                  {role.name}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                      </div>

                      {/* Preview */}
                      <div className="mt-4 p-3 rounded" style={{ backgroundColor: stage.background_color, color: stage.text_color }}>
                        <div className="flex items-center gap-2">
                          <span className="text-lg" dangerouslySetInnerHTML={{ __html: stage.icon }} />
                          <span className="font-semibold">{stage.name}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate('/company/settings/job-position-workflows')}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={loading}>
            <Save className="w-5 h-5 mr-2" />
            {loading ? 'Creating...' : 'Create Workflow'}
          </Button>
        </div>
      </form>
    </div>
  );
}
