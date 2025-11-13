import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, Eye, Calendar, User, Briefcase, Clock, CheckCircle2, ExternalLink, Copy } from 'lucide-react';
import { companyInterviewService } from '../../services/companyInterviewService';
import type { Interview, InterviewFilters, InterviewStatsResponse } from '../../services/companyInterviewService';
import { companyCandidateService } from '../../services/companyCandidateService';
import { PositionService } from '../../services/positionService';
import { companyInterviewTemplateService } from '../../services/companyInterviewTemplateService';
import type { CompanyCandidate } from '../../types/companyCandidate';
import type { Position } from '../../types/position';
import type { InterviewTemplate } from '../../services/companyInterviewTemplateService';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { toast } from 'react-toastify';

const CompanyInterviewsPage: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [stats, setStats] = useState<InterviewStatsResponse | null>(null);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(20);

  // Maps for candidate, position, and template names (using objects instead of Maps for React state)
  const [candidateMap, setCandidateMap] = useState<Record<string, string>>({});
  const [positionMap, setPositionMap] = useState<Record<string, string>>({});
  const [templateMap, setTemplateMap] = useState<Record<string, string>>({});

  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [typeFilter, setTypeFilter] = useState<string>('all');

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
    loadInterviews();
    loadStats();
    loadCandidateAndPositionData();
  }, [currentPage, statusFilter, typeFilter]);

  const loadCandidateAndPositionData = async () => {
    const companyId = getCompanyId();
    if (!companyId) return;

    try {
      // Load candidates
      const candidates = await companyCandidateService.listByCompany(companyId);
      const candidateMapData: Record<string, string> = {};
      candidates.forEach((candidate) => {
        if (candidate.candidate_name && candidate.candidate_id) {
          candidateMapData[candidate.candidate_id] = candidate.candidate_name;
        }
      });
      console.log('Candidate map loaded:', candidateMapData);
      setCandidateMap(candidateMapData);

      // Load positions (both active and inactive to cover all interviews)
      // Load in batches since max page_size is 100
      const positionMapData: Record<string, string> = {};
      let page = 1;
      let hasMore = true;
      
      while (hasMore) {
        const positionsData = await PositionService.getPositions({
          company_id: companyId,
          page: page,
          page_size: 100, // Max allowed page size
        });
        
        positionsData.positions.forEach((position) => {
          if (position.id && position.title) {
            positionMapData[position.id] = position.title;
          }
        });
        
        // Check if there are more pages
        hasMore = positionsData.positions.length === 100 && page * 100 < positionsData.total;
        page++;
      }
      
      console.log('Position map loaded:', positionMapData);
      console.log('Total positions in map:', Object.keys(positionMapData).length);
      setPositionMap(positionMapData);

      // Load interview templates (load all, not just enabled, to cover all interviews)
      const templatesData = await companyInterviewTemplateService.listTemplates({
        page_size: 100, // Max allowed page size
      });
      const templateMapData: Record<string, string> = {};
      templatesData.forEach((template) => {
        if (template.id && template.name) {
          templateMapData[template.id] = template.name;
        }
      });
      console.log('Template map loaded:', templateMapData);
      console.log('Total templates in map:', Object.keys(templateMapData).length);
      setTemplateMap(templateMapData);
    } catch (err) {
      console.error('Error loading candidate/position/template data:', err);
      // Don't show error, just log it
    }
  };

  const loadInterviews = async () => {
    try {
      setLoading(true);
      setError(null);

      const filters: InterviewFilters = {
        limit: pageSize,
        offset: (currentPage - 1) * pageSize,
      };

      if (statusFilter !== 'all') {
        filters.status = statusFilter as any;
      }

      if (typeFilter !== 'all') {
        filters.interview_type = typeFilter as any;
      }

      const response = await companyInterviewService.listInterviews(filters);
      setInterviews(response.interviews);
      setTotal(response.total);
      
      // Debug: log interview data
      console.log('Interviews loaded:', response.interviews.map(i => ({ 
        id: i.id, 
        title: i.title,
        job_position_id: i.job_position_id 
      })));
    } catch (err: any) {
      setError(err.message || 'Error al cargar las entrevistas');
      console.error('Error loading interviews:', err);
      toast.error(err.message || 'Error al cargar las entrevistas');
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await companyInterviewService.getInterviewStats();
      setStats(statsData);
    } catch (err: any) {
      console.error('Error loading stats:', err);
      // Don't show error for stats, just log it
    }
  };

  const handleSearch = () => {
    setCurrentPage(1);
    loadInterviews();
  };

  const handleViewInterview = (interviewId: string) => {
    navigate(`/company/interviews/${interviewId}`);
  };

  const handleCreateInterview = () => {
    navigate('/company/interviews/create');
  };

  const handleGenerateAndOpenLink = async (interviewId: string) => {
    try {
      const response = await companyInterviewService.generateInterviewLink(interviewId);
      let linkToOpen: string;
      
      if (response.link_token) {
        // Construct the link using the answer page route
        const baseUrl = window.location.origin;
        linkToOpen = `${baseUrl}/interviews/${interviewId}/answer?token=${response.link_token}`;
      } else if (response.link) {
        // Backend returns link with /access, convert to /answer
        linkToOpen = response.link.replace('/access', '/answer');
      } else {
        toast.error('No se pudo generar el link');
        return;
      }
      
      window.open(linkToOpen, '_blank');
      toast.success('Link generado y abierto');
    } catch (err: any) {
      toast.error(err.message || 'Error al generar el link');
      console.error('Error generating link:', err);
    }
  };

  const handleCopyLink = async (interviewId: string, linkToken?: string) => {
    try {
      let linkToCopy: string;
      
      if (linkToken) {
        const baseUrl = window.location.origin;
        linkToCopy = `${baseUrl}/interviews/${interviewId}/answer?token=${linkToken}`;
      } else {
        // Generate link first
        const response = await companyInterviewService.generateInterviewLink(interviewId);
        if (response.link_token) {
          const baseUrl = window.location.origin;
          linkToCopy = `${baseUrl}/interviews/${interviewId}/answer?token=${response.link_token}`;
        } else if (response.link) {
          // Backend returns link with /access, convert to /answer
          linkToCopy = response.link.replace('/access', '/answer');
        } else {
          toast.error('No se pudo generar el link');
          return;
        }
      }
      
      await navigator.clipboard.writeText(linkToCopy);
      toast.success('Link copiado al portapapeles');
    } catch (err: any) {
      toast.error(err.message || 'Error al copiar el link');
      console.error('Error copying link:', err);
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
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

    const config = statusConfig[status] || { label: status.replace('_', ' '), variant: 'outline' as const };

    return (
      <Badge variant={config.variant}>
        {config.label}
      </Badge>
    );
  };

  const totalPages = Math.ceil(total / pageSize);

  return (
    <TooltipProvider delayDuration={100} skipDelayDuration={50}>
      <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Entrevistas</h1>
            <p className="text-gray-600 mt-1">
              Gestiona las entrevistas de candidatos
            </p>
          </div>
          <Button onClick={handleCreateInterview} className="flex items-center gap-2">
            <Plus className="w-4 h-4" />
            Nueva Entrevista
          </Button>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-gray-600">
                  Total Entrevistas
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_interviews}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-gray-600">
                  Programadas
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.scheduled_interviews}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-gray-600">
                  En Progreso
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.in_progress_interviews}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-gray-600">
                  Completadas
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.completed_interviews}</div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Filters */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <Input
                  placeholder="Buscar entrevistas..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  className="w-full"
                />
              </div>
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger className="w-full md:w-[180px]">
                  <SelectValue placeholder="Estado" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos los estados</SelectItem>
                  <SelectItem value="SCHEDULED">Programada</SelectItem>
                  <SelectItem value="IN_PROGRESS">En Progreso</SelectItem>
                  <SelectItem value="COMPLETED">Completada</SelectItem>
                  <SelectItem value="CANCELLED">Cancelada</SelectItem>
                  <SelectItem value="PENDING">Pendiente</SelectItem>
                </SelectContent>
              </Select>
              <Select value={typeFilter} onValueChange={setTypeFilter}>
                <SelectTrigger className="w-full md:w-[180px]">
                  <SelectValue placeholder="Tipo" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos los tipos</SelectItem>
                  <SelectItem value="EXTENDED_PROFILE">Perfil Extendido</SelectItem>
                  <SelectItem value="POSITION_INTERVIEW">Entrevista de Posición</SelectItem>
                  <SelectItem value="TECHNICAL">Técnica</SelectItem>
                  <SelectItem value="BEHAVIORAL">Conductual</SelectItem>
                  <SelectItem value="CULTURAL_FIT">Ajuste Cultural</SelectItem>
                </SelectContent>
              </Select>
              <Button onClick={handleSearch} variant="outline" className="flex items-center gap-2">
                <Search className="w-4 h-4" />
                Buscar
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="mb-6">
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-red-800">{error}</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Interviews Table */}
      {loading ? (
        <Card>
          <CardContent className="pt-12 pb-12">
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="ml-3 text-gray-600">Cargando entrevistas...</span>
            </div>
          </CardContent>
        </Card>
      ) : interviews.length === 0 ? (
        <Card>
          <CardContent className="pt-12 pb-12 text-center">
            <Calendar className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              No se encontraron entrevistas
            </h3>
            <p className="text-gray-600 mb-6">
              Crea tu primera entrevista para comenzar
            </p>
            <Button onClick={handleCreateInterview} className="flex items-center gap-2 mx-auto">
              <Plus className="w-4 h-4" />
              Crear Primera Entrevista
            </Button>
          </CardContent>
        </Card>
      ) : (
        <>
          <Card>
            <CardHeader>
              <CardTitle>Lista de Entrevistas ({total})</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Candidato</TableHead>
                    <TableHead>Entrevista</TableHead>
                    <TableHead>Tipo</TableHead>
                    <TableHead>Estado</TableHead>
                    <TableHead>Programada</TableHead>
                    <TableHead>Posición</TableHead>
                    <TableHead>Puntuación</TableHead>
                    <TableHead>Acciones</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {interviews.map((interview) => (
                    <TableRow key={interview.id}>
                      <TableCell className="font-medium">
                        <div className="flex items-center gap-2">
                          <User className="w-4 h-4 text-gray-400" />
                          {candidateMap[interview.candidate_id] || interview.candidate_id}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex flex-col">
                          {interview.title && interview.title.trim() ? (
                            <span className="font-medium text-gray-900">{interview.title}</span>
                          ) : interview.interview_template_id && templateMap[interview.interview_template_id] ? (
                            <span className="text-sm text-gray-500 italic">
                              {templateMap[interview.interview_template_id]}
                            </span>
                          ) : (
                            <span className="text-sm text-gray-400 italic">Sin título</span>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <span className="text-sm text-gray-600">
                          {interview.interview_type.replace('_', ' ')}
                        </span>
                      </TableCell>
                      <TableCell>{getStatusBadge(interview.status)}</TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2 text-sm text-gray-600">
                          <Clock className="w-4 h-4" />
                          {formatDate(interview.scheduled_at)}
                        </div>
                      </TableCell>
                      <TableCell>
                        {interview.job_position_id ? (
                          <div className="flex items-center gap-2 text-sm text-gray-600">
                            <Briefcase className="w-4 h-4" />
                            {positionMap[interview.job_position_id] || interview.job_position_id}
                          </div>
                        ) : (
                          <span className="text-sm text-gray-400">N/A</span>
                        )}
                      </TableCell>
                      <TableCell>
                        {interview.score !== undefined ? (
                          <div className="flex items-center gap-1">
                            <CheckCircle2 className="w-4 h-4 text-green-600" />
                            <span className="font-medium">{interview.score}</span>
                          </div>
                        ) : (
                          <span className="text-sm text-gray-400">-</span>
                        )}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleViewInterview(interview.id)}
                                className="flex items-center justify-center"
                              >
                                <Eye className="w-4 h-4" />
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>
                              <p>Ver entrevista</p>
                            </TooltipContent>
                          </Tooltip>
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleGenerateAndOpenLink(interview.id)}
                                className="flex items-center justify-center"
                              >
                                <ExternalLink className="w-4 h-4" />
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>
                              <p>Responder entrevista</p>
                            </TooltipContent>
                          </Tooltip>
                          {interview.link_token && (
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => handleCopyLink(interview.id, interview.link_token)}
                                  className="flex items-center justify-center"
                                >
                                  <Copy className="w-4 h-4" />
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>Copiar link</p>
                              </TooltipContent>
                            </Tooltip>
                          )}
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2 mt-6">
              <Button
                variant="outline"
                onClick={() => setCurrentPage(currentPage - 1)}
                disabled={currentPage === 1}
              >
                Anterior
              </Button>
              <span className="text-sm text-gray-600">
                Página {currentPage} de {totalPages}
              </span>
              <Button
                variant="outline"
                onClick={() => setCurrentPage(currentPage + 1)}
                disabled={currentPage === totalPages}
              >
                Siguiente
              </Button>
            </div>
          )}
        </>
      )}
      </div>
    </TooltipProvider>
  );
};

export default CompanyInterviewsPage;

