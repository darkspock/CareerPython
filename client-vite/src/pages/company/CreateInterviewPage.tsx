import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Calendar, User, Briefcase, FileText } from 'lucide-react';
import { companyInterviewService, type CreateInterviewRequest } from '../../services/companyInterviewService';
import { companyCandidateService } from '../../services/companyCandidateService';
import { PositionService } from '../../services/positionService';
import { companyInterviewTemplateService } from '../../services/companyInterviewTemplateService';
import type { CompanyCandidate } from '../../types/companyCandidate';
import type { Position } from '../../types/position';
import type { InterviewTemplate } from '../../services/companyInterviewTemplateService';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';
import { toast } from 'react-toastify';

export default function CreateInterviewPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<CreateInterviewRequest>({
    candidate_id: '',
    interview_type: 'POSITION_INTERVIEW',
    interview_mode: 'MANUAL',
    job_position_id: undefined,
    interview_template_id: undefined,
    title: '',
    description: '',
    scheduled_at: '',
    interviewers: [],
  });

  const [candidates, setCandidates] = useState<CompanyCandidate[]>([]);
  const [positions, setPositions] = useState<Position[]>([]);
  const [templates, setTemplates] = useState<InterviewTemplate[]>([]);
  const [loadingData, setLoadingData] = useState(true);
  const [interviewerInput, setInterviewerInput] = useState('');

  const interviewTypes = [
    { value: 'POSITION_INTERVIEW', label: 'Job Position Interview' },
    { value: 'RESUME_ENHANCEMENT', label: 'Resume Enhancement' },
    { value: 'TECHNICAL', label: 'Technical Interview' },
    { value: 'BEHAVIORAL', label: 'Behavioral Interview' },
    { value: 'CULTURAL_FIT', label: 'Cultural Fit Interview' },
  ];

  const interviewModes = [
    { value: 'AUTOMATIC', label: 'Automático' },
    { value: 'AI', label: 'IA' },
    { value: 'MANUAL', label: 'Manual' },
  ];

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
    loadData();
  }, []);

  const loadData = async () => {
    const companyId = getCompanyId();
    if (!companyId) {
      setError('Company ID not found');
      setLoadingData(false);
      return;
    }

    try {
      setLoadingData(true);
      
      // Load candidates
      const candidatesData = await companyCandidateService.listByCompany(companyId);
      setCandidates(candidatesData);

      // Load positions
      const positionsData = await PositionService.getPositions({
        company_id: companyId,
        is_active: true,
        page_size: 100,
      });
      setPositions(positionsData.positions);

      // Load templates
      const templatesData = await companyInterviewTemplateService.listTemplates({
        status: 'ENABLED',
        page_size: 100,
      });
      setTemplates(templatesData);
    } catch (err: any) {
      setError(err.message || 'Error al cargar los datos');
      console.error('Error loading data:', err);
    } finally {
      setLoadingData(false);
    }
  };

  const handleAddInterviewer = () => {
    if (interviewerInput.trim() && !formData.interviewers?.includes(interviewerInput.trim())) {
      setFormData({
        ...formData,
        interviewers: [...(formData.interviewers || []), interviewerInput.trim()],
      });
      setInterviewerInput('');
    }
  };

  const handleRemoveInterviewer = (interviewer: string) => {
    setFormData({
      ...formData,
      interviewers: formData.interviewers?.filter(i => i !== interviewer) || [],
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!formData.candidate_id) {
      setError('El candidato es requerido');
      return;
    }

    if (!formData.interview_type) {
      setError('El tipo de entrevista es requerido');
      return;
    }

    if (!formData.interview_mode) {
      setError('El modo de entrevista es requerido');
      return;
    }

    try {
      setLoading(true);
      const response = await companyInterviewService.createInterview(formData);
      toast.success('Entrevista creada correctamente');
      const interviewId = response.interview_id || (response as any).interview?.id;
      if (interviewId) {
        navigate(`/company/interviews/${interviewId}`);
      } else {
        navigate('/company/interviews');
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Error al crear la entrevista';
      setError(errorMessage);
      toast.error(errorMessage);
      console.error('Error creating interview:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loadingData) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Cargando datos...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <Button
          variant="ghost"
          onClick={() => navigate('/company/interviews')}
          className="mb-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Volver a Entrevistas
        </Button>
        <h1 className="text-3xl font-bold text-gray-900">Crear Nueva Entrevista</h1>
        <p className="text-gray-600 mt-1">Programa una nueva entrevista para un candidato</p>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <Card>
          <CardHeader>
            <CardTitle>Información Básica</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="candidate_id" className="flex items-center gap-2 mb-2">
                <User className="w-4 h-4" />
                Candidato *
              </Label>
              <Select
                value={formData.candidate_id}
                onValueChange={(value) => setFormData({ ...formData, candidate_id: value })}
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona un candidato" />
                </SelectTrigger>
                <SelectContent>
                  {candidates.map((candidate) => (
                    <SelectItem key={candidate.candidate_id} value={candidate.candidate_id}>
                      {candidate.candidate_name} ({candidate.candidate_email})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="interview_type" className="flex items-center gap-2 mb-2">
                <FileText className="w-4 h-4" />
                Tipo de Entrevista *
              </Label>
              <Select
                value={formData.interview_type}
                onValueChange={(value) => setFormData({ ...formData, interview_type: value as any })}
                required
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {interviewTypes.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="interview_mode" className="flex items-center gap-2 mb-2">
                <FileText className="w-4 h-4" />
                Modo de Entrevista *
              </Label>
              <Select
                value={formData.interview_mode}
                onValueChange={(value) => setFormData({ ...formData, interview_mode: value as 'AUTOMATIC' | 'AI' | 'MANUAL' })}
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona un modo" />
                </SelectTrigger>
                <SelectContent>
                  {interviewModes.map((mode) => (
                    <SelectItem key={mode.value} value={mode.value}>
                      {mode.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="job_position_id" className="flex items-center gap-2 mb-2">
                <Briefcase className="w-4 h-4" />
                Posición de Trabajo (Opcional)
              </Label>
              <Select
                value={formData.job_position_id || 'none'}
                onValueChange={(value) => setFormData({ ...formData, job_position_id: value === 'none' ? undefined : value })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona una posición" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">Ninguna</SelectItem>
                  {positions.map((position) => (
                    <SelectItem key={position.id} value={position.id}>
                      {position.title}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="interview_template_id" className="flex items-center gap-2 mb-2">
                <FileText className="w-4 h-4" />
                Plantilla de Entrevista (Opcional)
              </Label>
              <Select
                value={formData.interview_template_id || 'none'}
                onValueChange={(value) => setFormData({ ...formData, interview_template_id: value === 'none' ? undefined : value })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona una plantilla" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">Ninguna</SelectItem>
                  {templates.map((template) => (
                    <SelectItem key={template.id} value={template.id}>
                      {template.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Interview Details */}
        <Card>
          <CardHeader>
            <CardTitle>Detalles de la Entrevista</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="title">Título (Opcional)</Label>
              <Input
                id="title"
                type="text"
                value={formData.title || ''}
                onChange={(e) => setFormData({ ...formData, title: e.target.value || undefined })}
                placeholder="Título de la entrevista"
              />
            </div>

            <div>
              <Label htmlFor="description">Descripción (Opcional)</Label>
              <Textarea
                id="description"
                value={formData.description || ''}
                onChange={(e) => setFormData({ ...formData, description: e.target.value || undefined })}
                rows={4}
                placeholder="Descripción o notas sobre la entrevista"
              />
            </div>

            <div>
              <Label htmlFor="scheduled_at" className="flex items-center gap-2 mb-2">
                <Calendar className="w-4 h-4" />
                Fecha y Hora Programada (Opcional)
              </Label>
              <Input
                id="scheduled_at"
                type="datetime-local"
                value={formData.scheduled_at || ''}
                onChange={(e) => setFormData({ ...formData, scheduled_at: e.target.value || undefined })}
              />
            </div>

            <div>
              <Label>Entrevistadores (Opcional)</Label>
              <div className="flex gap-2 mb-2">
                <Input
                  type="text"
                  value={interviewerInput}
                  onChange={(e) => setInterviewerInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      handleAddInterviewer();
                    }
                  }}
                  placeholder="Nombre del entrevistador"
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={handleAddInterviewer}
                  disabled={!interviewerInput.trim()}
                >
                  Agregar
                </Button>
              </div>
              {formData.interviewers && formData.interviewers.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {formData.interviewers.map((interviewer, index) => (
                    <div
                      key={index}
                      className="flex items-center gap-2 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                    >
                      <span>{interviewer}</span>
                      <button
                        type="button"
                        onClick={() => handleRemoveInterviewer(interviewer)}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex justify-end gap-3">
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate('/company/interviews')}
          >
            Cancelar
          </Button>
          <Button type="submit" disabled={loading}>
            {loading ? 'Creando...' : 'Crear Entrevista'}
          </Button>
        </div>
      </form>
    </div>
  );
}

