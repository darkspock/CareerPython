import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Calendar,
  User,
  Briefcase,
  Clock,
  CheckCircle2,
  XCircle,
  FileText,
  MessageSquare,
  Play,
  Square,
  Edit
} from 'lucide-react';
import { companyInterviewService } from '../../services/companyInterviewService';
import type { Interview, InterviewScoreSummaryResponse } from '../../services/companyInterviewService';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'react-toastify';
import { Badge } from '@/components/ui/badge';

export default function CompanyInterviewDetailPage() {
  const { interviewId } = useParams<{ interviewId: string }>();
  const navigate = useNavigate();
  const [interview, setInterview] = useState<Interview | null>(null);
  const [scoreSummary, setScoreSummary] = useState<InterviewScoreSummaryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    if (interviewId) {
      loadInterview();
      loadScoreSummary();
    }
  }, [interviewId]);

  const loadInterview = async () => {
    if (!interviewId) return;

    try {
      setLoading(true);
      setError(null);
      const data = await companyInterviewService.getInterview(interviewId);
      setInterview(data);
    } catch (err: any) {
      setError(err.message || 'Error al cargar la entrevista');
      console.error('Error loading interview:', err);
      toast.error(err.message || 'Error al cargar la entrevista');
    } finally {
      setLoading(false);
    }
  };

  const loadScoreSummary = async () => {
    if (!interviewId) return;

    try {
      const summary = await companyInterviewService.getInterviewScoreSummary(interviewId);
      setScoreSummary(summary);
    } catch (err: any) {
      console.warn('Could not load score summary:', err);
      // Don't fail if score summary can't be loaded
    }
  };

  const handleStartInterview = async () => {
    if (!interviewId) return;

    try {
      setActionLoading(true);
      await companyInterviewService.startInterview(interviewId);
      toast.success('Entrevista iniciada correctamente');
      await loadInterview();
    } catch (err: any) {
      toast.error(err.message || 'Error al iniciar la entrevista');
    } finally {
      setActionLoading(false);
    }
  };

  const handleFinishInterview = async () => {
    if (!interviewId) return;

    try {
      setActionLoading(true);
      await companyInterviewService.finishInterview(interviewId);
      toast.success('Entrevista finalizada correctamente');
      await loadInterview();
      await loadScoreSummary();
    } catch (err: any) {
      toast.error(err.message || 'Error al finalizar la entrevista');
    } finally {
      setActionLoading(false);
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return dateString;
    }
  };

  const getStatusBadge = (status: string) => {
    const statusConfig: Record<string, { label: string; variant: 'default' | 'secondary' | 'destructive' | 'outline' }> = {
      SCHEDULED: { label: 'Programada', variant: 'default' },
      IN_PROGRESS: { label: 'En Progreso', variant: 'secondary' },
      COMPLETED: { label: 'Completada', variant: 'default' },
      CANCELLED: { label: 'Cancelada', variant: 'destructive' },
      PENDING: { label: 'Pendiente', variant: 'outline' },
    };

    const config = statusConfig[status] || { label: status, variant: 'outline' as const };

    return (
      <Badge variant={config.variant}>
        {config.label}
      </Badge>
    );
  };

  const getTypeLabel = (type: string) => {
    const typeLabels: Record<string, string> = {
      EXTENDED_PROFILE: 'Perfil Extendido',
      POSITION_INTERVIEW: 'Entrevista de Posición',
      TECHNICAL: 'Técnica',
      BEHAVIORAL: 'Conductual',
      CULTURAL_FIT: 'Ajuste Cultural',
    };

    return typeLabels[type] || type.replace('_', ' ');
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Cargando entrevista...</span>
        </div>
      </div>
    );
  }

  if (error || !interview) {
    return (
      <div className="max-w-6xl mx-auto">
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <XCircle className="w-5 h-5 text-red-600" />
              <p className="text-red-800">{error || 'Entrevista no encontrada'}</p>
            </div>
            <Button
              variant="outline"
              onClick={() => navigate('/company/interviews')}
              className="mt-4"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Volver a Entrevistas
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
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

        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {interview.title || 'Entrevista'}
            </h1>
            <div className="flex items-center gap-4 text-sm text-gray-600">
              <div className="flex items-center gap-2">
                {getStatusBadge(interview.status)}
              </div>
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4" />
                {getTypeLabel(interview.interview_type)}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {interview.status === 'SCHEDULED' && (
              <Button
                onClick={handleStartInterview}
                disabled={actionLoading}
                className="flex items-center gap-2"
              >
                <Play className="w-4 h-4" />
                Iniciar Entrevista
              </Button>
            )}
            {interview.status === 'IN_PROGRESS' && (
              <Button
                onClick={handleFinishInterview}
                disabled={actionLoading}
                variant="outline"
                className="flex items-center gap-2"
              >
                <Square className="w-4 h-4" />
                Finalizar Entrevista
              </Button>
            )}
            <Button
              variant="outline"
              onClick={() => navigate(`/company/interviews/${interviewId}/edit`)}
              className="flex items-center gap-2"
            >
              <Edit className="w-4 h-4" />
              Editar
            </Button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Description */}
          {interview.description && (
            <Card>
              <CardHeader>
                <CardTitle>Descripción</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 whitespace-pre-wrap">{interview.description}</p>
              </CardContent>
            </Card>
          )}

          {/* Interview Details */}
          <Card>
            <CardHeader>
              <CardTitle>Detalles de la Entrevista</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-500">Estado</label>
                  <div className="mt-1">{getStatusBadge(interview.status)}</div>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Tipo</label>
                  <div className="mt-1 text-gray-900">{getTypeLabel(interview.interview_type)}</div>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Programada</label>
                  <div className="mt-1 flex items-center gap-2 text-gray-900">
                    <Calendar className="w-4 h-4" />
                    {formatDate(interview.scheduled_at)}
                  </div>
                </div>
                {interview.started_at && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Iniciada</label>
                    <div className="mt-1 flex items-center gap-2 text-gray-900">
                      <Clock className="w-4 h-4" />
                      {formatDate(interview.started_at)}
                    </div>
                  </div>
                )}
                {interview.completed_at && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Completada</label>
                    <div className="mt-1 flex items-center gap-2 text-gray-900">
                      <CheckCircle2 className="w-4 h-4" />
                      {formatDate(interview.completed_at)}
                    </div>
                  </div>
                )}
                {interview.score !== undefined && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Puntuación</label>
                    <div className="mt-1 flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-green-600" />
                      <span className="text-lg font-semibold text-gray-900">{interview.score}</span>
                      <span className="text-sm text-gray-500">/ 10</span>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Notes */}
          {interview.notes && (
            <Card>
              <CardHeader>
                <CardTitle>Notas</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 whitespace-pre-wrap">{interview.notes}</p>
              </CardContent>
            </Card>
          )}

          {/* Score Summary */}
          {scoreSummary && scoreSummary.total_questions > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Resumen de Puntuación</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Preguntas Totales</label>
                    <div className="mt-1 text-2xl font-bold text-gray-900">
                      {scoreSummary.total_questions}
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Respondidas</label>
                    <div className="mt-1 text-2xl font-bold text-gray-900">
                      {scoreSummary.answered_questions}
                    </div>
                  </div>
                  {scoreSummary.overall_score !== undefined && (
                    <div>
                      <label className="text-sm font-medium text-gray-500">Puntuación General</label>
                      <div className="mt-1 text-2xl font-bold text-gray-900">
                        {scoreSummary.overall_score.toFixed(1)}
                      </div>
                    </div>
                  )}
                  <div>
                    <label className="text-sm font-medium text-gray-500">Completitud</label>
                    <div className="mt-1 text-2xl font-bold text-gray-900">
                      {scoreSummary.completion_percentage.toFixed(0)}%
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Candidate Info */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="w-5 h-5" />
                Candidato
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="text-sm text-gray-500">ID del Candidato</div>
                <div className="text-gray-900 font-medium">{interview.candidate_id}</div>
                <Button
                  variant="link"
                  size="sm"
                  onClick={() => navigate(`/company/candidates/${interview.candidate_id}`)}
                  className="p-0 h-auto mt-2"
                >
                  Ver perfil del candidato →
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Job Position Info */}
          {interview.job_position_id && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Briefcase className="w-5 h-5" />
                  Posición de Trabajo
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="text-sm text-gray-500">ID de la Posición</div>
                  <div className="text-gray-900 font-medium">{interview.job_position_id}</div>
                  <Button
                    variant="link"
                    size="sm"
                    onClick={() => navigate(`/company/positions/${interview.job_position_id}`)}
                    className="p-0 h-auto mt-2"
                  >
                    Ver posición →
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Interviewers */}
          {interview.interviewers && interview.interviewers.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MessageSquare className="w-5 h-5" />
                  Entrevistadores
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {interview.interviewers.map((interviewer, index) => (
                    <div key={index} className="text-gray-900">
                      {interviewer}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Metadata */}
          <Card>
            <CardHeader>
              <CardTitle>Información Adicional</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              {interview.created_at && (
                <div>
                  <div className="text-gray-500">Creada</div>
                  <div className="text-gray-900">{formatDate(interview.created_at)}</div>
                </div>
              )}
              {interview.updated_at && (
                <div>
                  <div className="text-gray-500">Actualizada</div>
                  <div className="text-gray-900">{formatDate(interview.updated_at)}</div>
                </div>
              )}
              {interview.created_by && (
                <div>
                  <div className="text-gray-500">Creada por</div>
                  <div className="text-gray-900">{interview.created_by}</div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

