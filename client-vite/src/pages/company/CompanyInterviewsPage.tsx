import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, Eye, Calendar, User, Briefcase, Clock, CheckCircle2, ExternalLink, Copy, ChevronDown, ChevronUp, Filter, X, Users } from 'lucide-react';
import { companyInterviewService } from '../../services/companyInterviewService';
import type { Interview, InterviewFilters, InterviewStatsResponse } from '../../services/companyInterviewService';
import { companyCandidateService } from '../../services/companyCandidateService';
import { PositionService } from '../../services/positionService';
import { companyInterviewTemplateService } from '../../services/companyInterviewTemplateService';
import { CompanyUserService } from '../../services/companyUserService';
import { api } from '../../lib/api';
import type { CompanyRole } from '../../types/company';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
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

  // Maps for candidate, position, template, role, and user names
  const [candidateMap, setCandidateMap] = useState<Record<string, string>>({});
  const [positionMap, setPositionMap] = useState<Record<string, string>>({});
  const [templateMap, setTemplateMap] = useState<Record<string, string>>({});
  const [roleMap, setRoleMap] = useState<Record<string, string>>({});
  const [userMap, setUserMap] = useState<Record<string, string>>({});

  // Filters
  const [candidateNameFilter, setCandidateNameFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  const [processTypeFilter, setProcessTypeFilter] = useState<string>('all');
  const [jobPositionFilter, setJobPositionFilter] = useState<string>('all');
  const [roleFilter, setRoleFilter] = useState<string>('all');
  const [interviewerFilter, setInterviewerFilter] = useState<string>('all');
  const [fromDateFilter, setFromDateFilter] = useState<string>('');
  const [toDateFilter, setToDateFilter] = useState<string>('');
  const [dateFilterBy, setDateFilterBy] = useState<'scheduled' | 'deadline' | 'unscheduled'>('scheduled');
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);

  // Calendar state
  const [calendarInterviews, setCalendarInterviews] = useState<Interview[]>([]);
  const [calendarLoading, setCalendarLoading] = useState(false);

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
    loadCalendarData();
  }, [currentPage, statusFilter, typeFilter, processTypeFilter, jobPositionFilter, roleFilter, interviewerFilter, fromDateFilter, toDateFilter, dateFilterBy, candidateNameFilter]);

  useEffect(() => {
    loadCalendarData();
  }, []);

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

      // Load company roles
      const rolesData = await api.listCompanyRoles(companyId, true);
      const roleMapData: Record<string, string> = {};
      (rolesData as CompanyRole[]).forEach((role) => {
        if (role.id && role.name) {
          roleMapData[role.id] = role.name;
        }
      });
      setRoleMap(roleMapData);

      // Load company users
      const usersData = await CompanyUserService.getCompanyUsers(companyId, { active_only: true });
      const userMapData: Record<string, string> = {};
      usersData.forEach((user) => {
        if (user.id && user.email) {
          userMapData[user.id] = user.email;
        }
      });
      setUserMap(userMapData);
    } catch (err) {
      console.error('Error loading candidate/position/template data:', err);
      // Don't show error, just log it
    }
  };

  const loadCalendarData = async () => {
    try {
      setCalendarLoading(true);
      const today = new Date();
      const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
      const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0, 23, 59, 59);
      
      const calendarData = await companyInterviewService.getInterviewCalendar(
        startOfMonth.toISOString(),
        endOfMonth.toISOString()
      );
      setCalendarInterviews(calendarData);
    } catch (err: any) {
      console.error('Error loading calendar data:', err);
    } finally {
      setCalendarLoading(false);
    }
  };

  const loadInterviews = async (overrideFilters?: {
    status?: string;
    fromDate?: string;
    toDate?: string;
    filterBy?: 'scheduled' | 'deadline' | 'unscheduled';
  }) => {
    try {
      setLoading(true);
      setError(null);

      const filters: InterviewFilters = {
        limit: pageSize,
        offset: (currentPage - 1) * pageSize,
      };

      if (candidateNameFilter) {
        filters.candidate_name = candidateNameFilter;
      }

      // Use override filters if provided, otherwise use state
      const effectiveStatus = overrideFilters?.status ?? statusFilter;
      if (effectiveStatus !== 'all') {
        filters.status = effectiveStatus as any;
      }

      if (typeFilter !== 'all') {
        filters.interview_type = typeFilter as any;
      }

      if (processTypeFilter !== 'all') {
        filters.process_type = processTypeFilter as any;
      }

      if (jobPositionFilter !== 'all') {
        filters.job_position_id = jobPositionFilter;
      }

      if (roleFilter !== 'all') {
        filters.required_role_id = roleFilter;
      }

      if (interviewerFilter !== 'all') {
        filters.interviewer_user_id = interviewerFilter;
      }

      // Set filter_by if we have date filters or if it's explicitly set (e.g., for deadline or unscheduled filtering)
      const effectiveFromDate = overrideFilters?.fromDate ?? fromDateFilter;
      const effectiveToDate = overrideFilters?.toDate ?? toDateFilter;
      const effectiveFilterBy = overrideFilters?.filterBy ?? dateFilterBy;
      
      // Set filter_by if we have date filters OR if it's explicitly provided in overrides (e.g., 'unscheduled' or 'deadline')
      if (effectiveFromDate || effectiveToDate) {
        filters.filter_by = effectiveFilterBy;
        if (effectiveFromDate) {
          filters.from_date = effectiveFromDate;
        }
        if (effectiveToDate) {
          filters.to_date = effectiveToDate;
        }
      } else if (overrideFilters?.filterBy) {
        // Set filter_by from overrides if explicitly provided (e.g., 'unscheduled' or 'deadline' filtering)
        filters.filter_by = overrideFilters.filterBy;
      } else if (dateFilterBy && (dateFilterBy === 'unscheduled' || dateFilterBy === 'deadline')) {
        // Also set filter_by if it's a special filter type even without dates
        filters.filter_by = dateFilterBy;
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

  const handleFilterByMetric = (filterType: string) => {
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
    setDateFilterBy('scheduled'); // Reset to default

    // Prepare filter overrides to pass directly to loadInterviews
    // This avoids timing issues with state updates
    let filterOverrides: {
      status?: string;
      fromDate?: string;
      toDate?: string;
      filterBy?: 'scheduled' | 'deadline' | 'unscheduled';
    } = {};

    switch (filterType) {
      case 'pending_to_plan':
        // No scheduled_at or no interviewers
        // Use filter_by=unscheduled to filter interviews without scheduled_at or interviewers
        setStatusFilter('ENABLED');
        setDateFilterBy('unscheduled');
        filterOverrides.status = 'ENABLED';
        filterOverrides.filterBy = 'unscheduled';
        break;
      case 'planned':
        // Have scheduled_at and interviewers
        setStatusFilter('SCHEDULED');
        filterOverrides.status = 'SCHEDULED';
        break;
      case 'in_progress':
        // scheduled_at = today
        const today = new Date();
        const todayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate()).toISOString().split('T')[0];
        const todayEnd = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 23, 59, 59).toISOString();
        setFromDateFilter(todayStart);
        setToDateFilter(todayEnd);
        setDateFilterBy('scheduled');
        filterOverrides.fromDate = todayStart;
        filterOverrides.toDate = todayEnd;
        filterOverrides.filterBy = 'scheduled';
        break;
      case 'recently_finished':
        // finished_at in last 30 days
        const thirtyDaysAgo = new Date();
        thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
        const fromDateStr = thirtyDaysAgo.toISOString().split('T')[0];
        setFromDateFilter(fromDateStr);
        setDateFilterBy('scheduled');
        filterOverrides.fromDate = fromDateStr;
        filterOverrides.filterBy = 'scheduled';
        break;
      case 'overdue':
        // deadline_date < now and not finished
        // Set to_date to now to filter overdue interviews
        const now = new Date();
        setStatusFilter('ENABLED');
        setDateFilterBy('deadline');
        setToDateFilter(now.toISOString());
        setFromDateFilter(''); // No from_date, just get all past deadlines
        filterOverrides.status = 'ENABLED';
        filterOverrides.toDate = now.toISOString();
        filterOverrides.filterBy = 'deadline';
        break;
      case 'pending_feedback':
        // finished but no score or feedback
        setStatusFilter('COMPLETED');
        filterOverrides.status = 'COMPLETED';
        break;
    }
    
    // Load interviews immediately with filter overrides, avoiding state timing issues
    loadInterviews(filterOverrides);
  };

  const handleDateClick = (date: Date) => {
    const dateStr = date.toISOString().split('T')[0];
    setFromDateFilter(dateStr);
    setToDateFilter(dateStr);
    setDateFilterBy('scheduled');
    setCurrentPage(1);
    setTimeout(() => loadInterviews(), 100);
  };

  const getInterviewsForDate = (date: Date): number => {
    return calendarInterviews.filter(interview => {
      if (!interview.scheduled_at) return false;
      const interviewDate = new Date(interview.scheduled_at);
      return (
        interviewDate.getDate() === date.getDate() &&
        interviewDate.getMonth() === date.getMonth() &&
        interviewDate.getFullYear() === date.getFullYear()
      );
    }).length;
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

        {/* Header with Metrics and Calendar */}
        {stats && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            {/* Metrics (Left) */}
            <div className="lg:col-span-2">
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <Card 
                  className="cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => handleFilterByMetric('pending_to_plan')}
                >
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs font-medium text-gray-600">
                      Pendientes de Planificar
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-orange-600">{stats.pending_to_plan || 0}</div>
                  </CardContent>
                </Card>
                <Card 
                  className="cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => handleFilterByMetric('planned')}
                >
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs font-medium text-gray-600">
                      Planificadas
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-blue-600">{stats.planned || 0}</div>
                  </CardContent>
                </Card>
                <Card 
                  className="cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => handleFilterByMetric('in_progress')}
                >
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs font-medium text-gray-600">
                      En Proceso
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-green-600">{stats.in_progress_interviews || 0}</div>
                  </CardContent>
                </Card>
                <Card 
                  className="cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => handleFilterByMetric('recently_finished')}
                >
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs font-medium text-gray-600">
                      Finalizadas Recientes
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-purple-600">{stats.recently_finished || 0}</div>
                  </CardContent>
                </Card>
                <Card 
                  className="cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => handleFilterByMetric('overdue')}
                >
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs font-medium text-gray-600">
                      Pasadas Fecha Límite
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-red-600">{stats.overdue || 0}</div>
                  </CardContent>
                </Card>
                <Card 
                  className="cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => handleFilterByMetric('pending_feedback')}
                >
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs font-medium text-gray-600">
                      Pendiente Feedback
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-yellow-600">{stats.pending_feedback || 0}</div>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Calendar (Right) */}
            <div className="lg:col-span-1">
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-gray-600 flex items-center gap-2">
                    <Calendar className="w-4 h-4" />
                    Calendario
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {calendarLoading ? (
                    <div className="flex items-center justify-center py-8">
                      <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                    </div>
                  ) : (
                    <div className="grid grid-cols-7 gap-1 text-xs">
                      {['L', 'M', 'X', 'J', 'V', 'S', 'D'].map((day) => (
                        <div key={day} className="text-center font-medium text-gray-500 p-1">
                          {day}
                        </div>
                      ))}
                      {Array.from({ length: 35 }, (_, i) => {
                        const date = new Date();
                        date.setDate(1);
                        date.setDate(date.getDate() - date.getDay() + 1 + i);
                        const isCurrentMonth = date.getMonth() === new Date().getMonth();
                        const isToday = date.toDateString() === new Date().toDateString();
                        const interviewCount = getInterviewsForDate(date);
                        
                        return (
                          <div
                            key={i}
                            className={`text-center p-1 cursor-pointer rounded hover:bg-gray-100 ${
                              isCurrentMonth ? 'text-gray-900' : 'text-gray-400'
                            } ${isToday ? 'bg-blue-50 font-bold' : ''}`}
                            onClick={() => handleDateClick(date)}
                            title={`${interviewCount} entrevista(s)`}
                          >
                            <div className="text-xs">{date.getDate()}</div>
                            {interviewCount > 0 && (
                              <div className="text-[8px] text-blue-600 font-bold mt-0.5">
                                {interviewCount}
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </CardContent>
              </Card>
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
                {(processTypeFilter !== 'all' || jobPositionFilter !== 'all' || roleFilter !== 'all' || 
                  interviewerFilter !== 'all' || fromDateFilter || toDateFilter) && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => {
                      setProcessTypeFilter('all');
                      setJobPositionFilter('all');
                      setRoleFilter('all');
                      setInterviewerFilter('all');
                      setFromDateFilter('');
                      setToDateFilter('');
                      setCurrentPage(1);
                      setTimeout(() => loadInterviews(), 100);
                    }}
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
                          <SelectItem key={id} value={id}>{name}</SelectItem>
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
                          <SelectItem key={id} value={id}>{name}</SelectItem>
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
                          <SelectItem key={id} value={id}>{email}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label className="text-xs text-gray-600 mb-1 block">Filtrar por Fecha</Label>
                    <Select value={dateFilterBy} onValueChange={(v) => setDateFilterBy(v as 'scheduled' | 'deadline')}>
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
                            <span className="font-medium text-gray-900">
                              {templateMap[interview.interview_template_id]}
                            </span>
                          ) : (
                            <span className="font-medium text-gray-400 italic">Sin título</span>
                          )}
                          <span className="text-[9px] text-gray-500 mt-0.5">
                            {interview.interview_type.replace('_', ' ')}
                          </span>
                        </div>
                      </TableCell>
                      <TableCell>
                        {interview.interviewers && interview.interviewers.length > 0 ? (
                          <div className="flex flex-col gap-1">
                            {interview.interviewers.slice(0, 2).map((interviewer, idx) => (
                              <div key={idx} className="flex items-center gap-1 text-xs text-gray-600">
                                <Users className="w-3 h-3" />
                                <span>{userMap[interviewer] || interviewer}</span>
                              </div>
                            ))}
                            {interview.interviewers.length > 2 && (
                              <span className="text-xs text-gray-400">+{interview.interviewers.length - 2} más</span>
                            )}
                          </div>
                        ) : interview.required_roles && interview.required_roles.length > 0 ? (
                          <div className="flex flex-col gap-1">
                            {interview.required_roles.slice(0, 2).map((roleId, idx) => (
                              <Badge key={idx} variant="outline" className="text-xs w-fit">
                                {roleMap[roleId] || roleId}
                              </Badge>
                            ))}
                            {interview.required_roles.length > 2 && (
                              <span className="text-xs text-gray-400">+{interview.required_roles.length - 2} más</span>
                            )}
                          </div>
                        ) : (
                          <span className="text-xs text-gray-400">Sin asignar</span>
                        )}
                      </TableCell>
                      <TableCell>{getStatusBadge(interview.status)}</TableCell>
                      <TableCell>
                        {interview.scheduled_at ? (
                          <button
                            type="button"
                            onClick={(e) => {
                              e.preventDefault();
                              e.stopPropagation();
                              navigate(`/company/interviews/${interview.id}/edit`);
                            }}
                            className="flex items-center gap-2 text-sm text-gray-600 hover:text-blue-600 transition-colors"
                          >
                            <Clock className="w-4 h-4" />
                            {formatDate(interview.scheduled_at)}
                          </button>
                        ) : (
                          <button
                            type="button"
                            onClick={(e) => {
                              e.preventDefault();
                              e.stopPropagation();
                              navigate(`/company/interviews/${interview.id}/edit`);
                            }}
                            className="flex items-center gap-2 text-sm text-gray-400 hover:text-blue-600 transition-colors"
                          >
                            <Calendar className="w-4 h-4" />
                            N/A
                          </button>
                        )}
                      </TableCell>
                      <TableCell>
                        {interview.deadline_date ? (
                          <button
                            type="button"
                            onClick={(e) => {
                              e.preventDefault();
                              e.stopPropagation();
                              navigate(`/company/interviews/${interview.id}/edit`);
                            }}
                            className="flex items-center gap-2 text-sm text-gray-600 hover:text-blue-600 transition-colors"
                          >
                            <Clock className="w-4 h-4" />
                            {formatDate(interview.deadline_date)}
                          </button>
                        ) : (
                          <span className="text-sm text-gray-400">N/A</span>
                        )}
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

