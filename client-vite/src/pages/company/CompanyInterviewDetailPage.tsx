import { useParams, useNavigate } from 'react-router-dom';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
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
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useInterviewDetail } from '../../hooks/useInterviewDetail';
import { formatDateDetailed, getStatusBadge, getTypeLabel } from '../../utils/interviewHelpers';

export default function CompanyInterviewDetailPage() {
  const { interviewId } = useParams<{ interviewId: string }>();
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
  
  const {
    interview,
    scoreSummary,
    loading,
    actionLoading,
    error,
    startInterview,
    finishInterview,
  } = useInterviewDetail(interviewId);

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
              onClick={() => navigate(getPath('interviews'))}
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
          onClick={() => navigate(getPath('interviews'))}
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
            {interview.status === 'PENDING' && (
              <Button
                onClick={startInterview}
                disabled={actionLoading}
                className="flex items-center gap-2"
              >
                <Play className="w-4 h-4" />
                Iniciar Entrevista
              </Button>
            )}
            {interview.status === 'IN_PROGRESS' && (
              <Button
                onClick={finishInterview}
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
              onClick={() => navigate(getPath(`interviews/${interviewId}/edit`))}
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
                    {formatDateDetailed(interview.scheduled_at)}
                  </div>
                </div>
                {interview.started_at && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Iniciada</label>
                    <div className="mt-1 flex items-center gap-2 text-gray-900">
                      <Clock className="w-4 h-4" />
                      {formatDateDetailed(interview.started_at)}
                    </div>
                  </div>
                )}
                {interview.completed_at && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Completada</label>
                    <div className="mt-1 flex items-center gap-2 text-gray-900">
                      <CheckCircle2 className="w-4 h-4" />
                      {formatDateDetailed(interview.completed_at)}
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
                  onClick={() => navigate(getPath(`candidates/${interview.candidate_id}`))}
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
                    onClick={() => navigate(getPath(`positions/${interview.job_position_id}`))}
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
                  <div className="text-gray-900">{formatDateDetailed(interview.created_at)}</div>
                </div>
              )}
              {interview.updated_at && (
                <div>
                  <div className="text-gray-500">Actualizada</div>
                  <div className="text-gray-900">{formatDateDetailed(interview.updated_at)}</div>
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

