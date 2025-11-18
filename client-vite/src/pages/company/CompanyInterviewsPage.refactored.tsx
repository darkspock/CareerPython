import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar, ChevronDown, ChevronUp, Filter, Plus, Search, X } from 'lucide-react';
import { companyInterviewService } from '../../services/companyInterviewService';
import type { InterviewFilterEnum } from '../../services/companyInterviewService';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { TooltipProvider } from '@/components/ui/tooltip';
import { toast } from 'react-toastify';
import { useInterviews } from '../../hooks/useInterviews';
import { useInterviewFilters } from '../../hooks/useInterviewFilters';
import { InterviewStats } from '../../components/interviews/InterviewStats';
import { InterviewCalendar } from '../../components/interviews/InterviewCalendar';
import { InterviewTableRow } from '../../components/interviews/InterviewTableRow';

const CompanyInterviewsPage: React.FC = () => {
  const navigate = useNavigate();
  
  // Use custom hooks
  const {
    interviews,
    stats,
    calendarInterviews,
    loading,
    calendarLoading,
    error,
    filters,
    total,
    pagination,
    fetchInterviews,
    fetchStats,
    fetchCalendar,
    setFilters,
    setCurrentPage,
    clearError,
  } = useInterviews({ pageSize: 20 });
  
  const {
    positionMap,
    roleMap,
    userMap,
  } = useInterviewFilters();
  
  // Local filter state
  const [candidateNameFilter, setCandidateNameFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  const [processTypeFilter, setProcessTypeFilter] = useState<string>('all');
  const [jobPositionFilter, setJobPositionFilter] = useState<string>('all');
  const [roleFilter, setRoleFilter] = useState<string>('all');
  const [interviewerFilter, setInterviewerFilter] = useState<string>('all');
  const [fromDateFilter, setFromDateFilter] = useState<string>('');
  const [toDateFilter, setToDateFilter] = useState<string>('');
  const [dateFilterBy, setDateFilterBy] = useState<'scheduled' | 'deadline'>('scheduled');
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  
  // Load calendar data on mount
  useEffect(() => {
    const today = new Date();
    const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0, 23, 59, 59);
    fetchCalendar(startOfMonth, endOfMonth);
  }, [fetchCalendar]);
  
  // Update filters when local filter state changes
  useEffect(() => {
    const newFilters: any = {};
    
    if (candidateNameFilter) {
      newFilters.candidate_name = candidateNameFilter;
    }
    if (statusFilter !== 'all') {
      newFilters.status = statusFilter;
    }
    if (typeFilter !== 'all') {
      newFilters.interview_type = typeFilter;
    }
    if (processTypeFilter !== 'all') {
      newFilters.process_type = processTypeFilter;
    }
    if (jobPositionFilter !== 'all') {
      newFilters.job_position_id = jobPositionFilter;
    }
    if (roleFilter !== 'all') {
      newFilters.required_role_id = roleFilter;
    }
    if (interviewerFilter !== 'all') {
      newFilters.interviewer_user_id = interviewerFilter;
    }
    if (fromDateFilter || toDateFilter) {
      newFilters.filter_by = dateFilterBy;
      if (fromDateFilter) {
        newFilters.from_date = fromDateFilter;
      }
      if (toDateFilter) {
        newFilters.to_date = toDateFilter;
      }
    }
    
    setFilters(newFilters);
  }, [
    candidateNameFilter,
    statusFilter,
    typeFilter,
    processTypeFilter,
    jobPositionFilter,
    roleFilter,
    interviewerFilter,
    fromDateFilter,
    toDateFilter,
    dateFilterBy,
    setFilters,
  ]);
  
  // Memoized handlers
  const handleSearch = useCallback(() => {
    setCurrentPage(1);
    fetchInterviews();
  }, [setCurrentPage, fetchInterviews]);
  
  const handleFilterByMetric = useCallback((filterType: string) => {
    setCurrentPage(1);
    
    // Reset all filters first
    setStatusFilter('all');
    setTypeFilter('all');
    setProcessTypeFilter('all');
    setJobPositionFilter('all');
    setRoleFilter('all');
    setInterviewerFilter('all');
    setFromDateFilter('');
    setToDateFilter('');
    setCandidateNameFilter('');
    setDateFilterBy('scheduled');
    
    // Prepare filter overrides
    let filterOverrides: {
      status?: string;
      fromDate?: string;
      toDate?: string;
      filterBy?: InterviewFilterEnum;
    } = {};
    
    switch (filterType) {
      case 'pending_to_plan':
        filterOverrides.filterBy = 'PENDING_TO_PLAN';
        break;
      case 'planned':
        filterOverrides.filterBy = 'PLANNED';
        break;
      case 'in_progress':
        filterOverrides.filterBy = 'IN_PROGRESS';
        break;
      case 'recently_finished':
        filterOverrides.filterBy = 'RECENTLY_FINISHED';
        break;
      case 'overdue':
        filterOverrides.filterBy = 'OVERDUE';
        break;
      case 'pending_feedback':
        filterOverrides.filterBy = 'PENDING_FEEDBACK';
        break;
    }
    
    fetchInterviews(filterOverrides);
  }, [setCurrentPage, fetchInterviews]);
  
  const handleDateClick = useCallback((date: Date) => {
    const dateStr = date.toISOString().split('T')[0];
    setFromDateFilter(dateStr);
    setToDateFilter(dateStr);
    setDateFilterBy('scheduled');
    setCurrentPage(1);
  }, [setCurrentPage]);
  
  const handleViewInterview = useCallback((interviewId: string) => {
    navigate(`/company/interviews/${interviewId}`);
  }, [navigate]);
  
  const handleCreateInterview = useCallback(() => {
    navigate('/company/interviews/create');
  }, [navigate]);
  
  const handleGenerateAndOpenLink = useCallback(async (interviewId: string) => {
    try {
      const response = await companyInterviewService.generateInterviewLink(interviewId);
      let linkToOpen: string;
      
      if (response.link_token) {
        const baseUrl = window.location.origin;
        linkToOpen = `${baseUrl}/interviews/${interviewId}/answer?token=${response.link_token}`;
      } else if (response.link) {
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
  }, []);
  
  const handleCopyLink = useCallback(async (interviewId: string, linkToken?: string) => {
    try {
      let linkToCopy: string;
      
      if (linkToken) {
        const baseUrl = window.location.origin;
        linkToCopy = `${baseUrl}/interviews/${interviewId}/answer?token=${linkToken}`;
      } else {
        const response = await companyInterviewService.generateInterviewLink(interviewId);
        if (response.link_token) {
          const baseUrl = window.location.origin;
          linkToCopy = `${baseUrl}/interviews/${interviewId}/answer?token=${response.link_token}`;
        } else if (response.link) {
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
  }, []);
  
  const handleClearFilters = useCallback(() => {
    setProcessTypeFilter('all');
    setJobPositionFilter('all');
    setRoleFilter('all');
    setInterviewerFilter('all');
    setFromDateFilter('');
    setToDateFilter('');
    setCurrentPage(1);
    setTimeout(() => fetchInterviews(), 100);
  }, [setCurrentPage, fetchInterviews]);
  
  // Check if any advanced filters are active
  const hasActiveAdvancedFilters = useMemo(() => {
    return (
      processTypeFilter !== 'all' ||
      jobPositionFilter !== 'all' ||
      roleFilter !== 'all' ||
      interviewerFilter !== 'all' ||
      fromDateFilter !== '' ||
      toDateFilter !== ''
    );
  }, [processTypeFilter, jobPositionFilter, roleFilter, interviewerFilter, fromDateFilter, toDateFilter]);
  
  return (
    <TooltipProvider delayDuration={0} skipDelayDuration={0}>
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
          
          {/* Header with Metrics and Calendar */}
          {stats && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
              {/* Metrics (Left) */}
              <div className="lg:col-span-2">
                <InterviewStats stats={stats} onFilterClick={handleFilterByMetric} />
              </div>
              
              {/* Calendar (Right) */}
              <div className="lg:col-span-1">
                <InterviewCalendar
                  interviews={calendarInterviews}
                  loading={calendarLoading}
                  onDateClick={handleDateClick}
                />
              </div>
            </div>
          )}
          
          {/* Filters */}
          <Card>
            <CardContent className="pt-6">
              <div className="space-y-4">
                {/* Basic Filters */}
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="flex-1">
                    <Input
                      placeholder="Buscar por nombre de candidato..."
                      value={candidateNameFilter}
                      onChange={(e) => setCandidateNameFilter(e.target.value)}
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
                      <SelectItem value="ENABLED">Habilitada</SelectItem>
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
                      <SelectItem value="CUSTOM">Personalizada</SelectItem>
                      <SelectItem value="TECHNICAL">Técnica</SelectItem>
                      <SelectItem value="BEHAVIORAL">Conductual</SelectItem>
                      <SelectItem value="CULTURAL_FIT">Ajuste Cultural</SelectItem>
                      <SelectItem value="KNOWLEDGE_CHECK">Verificación de Conocimientos</SelectItem>
                      <SelectItem value="EXPERIENCE_CHECK">Verificación de Experiencia</SelectItem>
                    </SelectContent>
                  </Select>
                  <Button onClick={handleSearch} variant="outline" className="flex items-center gap-2">
                    <Search className="w-4 h-4" />
                    Buscar
                  </Button>
                </div>
                
                {/* Advanced Filters Toggle */}
                <div className="flex items-center justify-between">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
                    className="flex items-center gap-2"
                  >
                    <Filter className="w-4 h-4" />
                    Filtros Avanzados
                    {showAdvancedFilters ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </Button>
                  {hasActiveAdvancedFilters && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={handleClearFilters}
                      className="flex items-center gap-2 text-red-600"
                    >
                      <X className="w-4 h-4" />
                      Limpiar Filtros
                    </Button>
                  )}
                </div>
                
                {/* Advanced Filters */}
                {showAdvancedFilters && (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 pt-4 border-t">
                    <div>
                      <Label className="text-xs text-gray-600 mb-1 block">Tipo de Proceso</Label>
                      <Select value={processTypeFilter} onValueChange={setProcessTypeFilter}>
                        <SelectTrigger className="w-full">
                          <SelectValue placeholder="Todos" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="all">Todos</SelectItem>
                          <SelectItem value="CANDIDATE_SIGN_UP">Registro de Candidato</SelectItem>
                          <SelectItem value="CANDIDATE_APPLICATION">Aplicación</SelectItem>
                          <SelectItem value="SCREENING">Screening</SelectItem>
                          <SelectItem value="INTERVIEW">Entrevista</SelectItem>
                          <SelectItem value="FEEDBACK">Feedback</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label className="text-xs text-gray-600 mb-1 block">Posición</Label>
                      <Select value={jobPositionFilter} onValueChange={setJobPositionFilter}>
                        <SelectTrigger className="w-full">
                          <SelectValue placeholder="Todas" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="all">Todas</SelectItem>
                          {Object.entries(positionMap).map(([id, name]) => (
                            <SelectItem key={id} value={id}>
                              {name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label className="text-xs text-gray-600 mb-1 block">Rol Requerido</Label>
                      <Select value={roleFilter} onValueChange={setRoleFilter}>
                        <SelectTrigger className="w-full">
                          <SelectValue placeholder="Todos" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="all">Todos</SelectItem>
                          {Object.entries(roleMap).map(([id, name]) => (
                            <SelectItem key={id} value={id}>
                              {name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label className="text-xs text-gray-600 mb-1 block">Entrevistador</Label>
                      <Select value={interviewerFilter} onValueChange={setInterviewerFilter}>
                        <SelectTrigger className="w-full">
                          <SelectValue placeholder="Todos" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="all">Todos</SelectItem>
                          {Object.entries(userMap).map(([id, email]) => (
                            <SelectItem key={id} value={id}>
                              {email}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label className="text-xs text-gray-600 mb-1 block">Filtrar por Fecha</Label>
                      <Select
                        value={dateFilterBy}
                        onValueChange={(v) => setDateFilterBy(v as 'scheduled' | 'deadline')}
                      >
                        <SelectTrigger className="w-full">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="scheduled">Programada</SelectItem>
                          <SelectItem value="deadline">Fecha Límite</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label className="text-xs text-gray-600 mb-1 block">Desde</Label>
                      <Input
                        type="date"
                        value={fromDateFilter}
                        onChange={(e) => setFromDateFilter(e.target.value)}
                        className="w-full"
                      />
                    </div>
                    
                    <div>
                      <Label className="text-xs text-gray-600 mb-1 block">Hasta</Label>
                      <Input
                        type="date"
                        value={toDateFilter}
                        onChange={(e) => setToDateFilter(e.target.value)}
                        className="w-full"
                      />
                    </div>
                  </div>
                )}
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
              <p className="text-gray-600 mb-6">Crea tu primera entrevista para comenzar</p>
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
                      <TableHead>Asignado</TableHead>
                      <TableHead>Estado</TableHead>
                      <TableHead>Programada</TableHead>
                      <TableHead>Fecha Límite</TableHead>
                      <TableHead>Posición</TableHead>
                      <TableHead>Puntuación</TableHead>
                      <TableHead>Acciones</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {interviews.map((interview) => (
                      <InterviewTableRow
                        key={interview.id}
                        interview={interview}
                        onView={handleViewInterview}
                        onGenerateLink={handleGenerateAndOpenLink}
                        onCopyLink={handleCopyLink}
                      />
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
            
            {/* Pagination */}
            {pagination.totalPages > 1 && (
              <div className="flex items-center justify-center gap-2 mt-6">
                <Button
                  variant="outline"
                  onClick={() => setCurrentPage(pagination.currentPage - 1)}
                  disabled={pagination.currentPage === 1}
                >
                  Anterior
                </Button>
                <span className="text-sm text-gray-600">
                  Página {pagination.currentPage} de {pagination.totalPages}
                </span>
                <Button
                  variant="outline"
                  onClick={() => setCurrentPage(pagination.currentPage + 1)}
                  disabled={pagination.currentPage === pagination.totalPages}
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

