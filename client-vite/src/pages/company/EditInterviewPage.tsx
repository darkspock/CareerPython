import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Calendar, FileText } from 'lucide-react';
import { companyInterviewService, type UpdateInterviewRequest } from '../../services/companyInterviewService';
import type { Interview } from '../../services/companyInterviewService';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';
import { toast } from 'react-toastify';

export default function EditInterviewPage() {
  const { interviewId } = useParams<{ interviewId: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [interview, setInterview] = useState<Interview | null>(null);

  const [formData, setFormData] = useState<UpdateInterviewRequest>({
    title: undefined,
    description: undefined,
    scheduled_at: undefined,
    interviewers: [],
  });

  const [interviewerInput, setInterviewerInput] = useState('');

  useEffect(() => {
    if (interviewId) {
      loadInterview();
    }
  }, [interviewId]);

  const loadInterview = async () => {
    if (!interviewId) return;

    try {
      setLoadingData(true);
      setError(null);
      const data = await companyInterviewService.getInterview(interviewId);
      setInterview(data);
      
      // Populate form with existing data
      setFormData({
        title: data.title || undefined,
        description: data.description || undefined,
        scheduled_at: data.scheduled_at ? formatDateForInput(data.scheduled_at) : undefined,
        interviewers: data.interviewers || [],
      });
    } catch (err: any) {
      setError(err.message || 'Error al cargar la entrevista');
      console.error('Error loading interview:', err);
      toast.error(err.message || 'Error al cargar la entrevista');
    } finally {
      setLoadingData(false);
    }
  };

  const formatDateForInput = (dateString: string): string => {
    // Convert ISO date string to datetime-local format (YYYY-MM-DDTHH:mm)
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
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

    if (!interviewId) {
      setError('ID de entrevista no encontrado');
      return;
    }

    try {
      setLoading(true);
      await companyInterviewService.updateInterview(interviewId, formData);
      toast.success('Entrevista actualizada correctamente');
      navigate(`/company/interviews/${interviewId}`);
    } catch (err: any) {
      const errorMessage = err.message || 'Error al actualizar la entrevista';
      setError(errorMessage);
      toast.error(errorMessage);
      console.error('Error updating interview:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loadingData) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Cargando entrevista...</span>
        </div>
      </div>
    );
  }

  if (!interview) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>No se pudo cargar la entrevista</AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <Button
          variant="ghost"
          onClick={() => navigate(`/company/interviews/${interviewId}`)}
          className="mb-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Volver a Detalle de Entrevista
        </Button>
        <h1 className="text-3xl font-bold text-gray-900">Editar Entrevista</h1>
        <p className="text-gray-600 mt-1">Actualiza la información de la entrevista</p>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Read-only Information */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Información de Solo Lectura</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-gray-600">
          <div>
            <span className="font-medium">Candidato:</span> {interview.candidate_id}
          </div>
          <div>
            <span className="font-medium">Tipo:</span> {interview.interview_type}
          </div>
          {interview.job_position_id && (
            <div>
              <span className="font-medium">Posición:</span> {interview.job_position_id}
            </div>
          )}
          {interview.interview_template_id && (
            <div>
              <span className="font-medium">Plantilla:</span> {interview.interview_template_id}
            </div>
          )}
        </CardContent>
      </Card>

      <form onSubmit={handleSubmit} className="space-y-6">
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
            onClick={() => navigate(`/company/interviews/${interviewId}`)}
          >
            Cancelar
          </Button>
          <Button type="submit" disabled={loading}>
            {loading ? 'Guardando...' : 'Guardar Cambios'}
          </Button>
        </div>
      </form>
    </div>
  );
}

