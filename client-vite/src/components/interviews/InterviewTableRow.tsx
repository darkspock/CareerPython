import React, { memo, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  User,
  Users,
  Calendar,
  Clock,
  Briefcase,
  CheckCircle2,
  Eye,
  ExternalLink,
  Copy,
  AlertTriangle,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { TableCell, TableRow } from '@/components/ui/table';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import type { Interview } from '../../services/companyInterviewService';
import { formatDate, getStatusBadge } from '../../utils/interviewHelpers';

interface InterviewTableRowProps {
  interview: Interview;
  onView: (interviewId: string) => void;
  onGenerateLink: (interviewId: string) => void;
  onCopyLink: (interviewId: string, linkToken?: string) => void;
}

export const InterviewTableRow: React.FC<InterviewTableRowProps> = memo(({
  interview,
  onView,
  onGenerateLink,
  onCopyLink,
}) => {
  const navigate = useNavigate();

  const handleEditClick = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    navigate(`/company/interviews/${interview.id}/edit`);
  }, [navigate, interview.id]);

  const handleViewClick = useCallback(() => {
    onView(interview.id);
  }, [onView, interview.id]);

  const handleGenerateLinkClick = useCallback(() => {
    onGenerateLink(interview.id);
  }, [onGenerateLink, interview.id]);

  const handleCopyLinkClick = useCallback(() => {
    onCopyLink(interview.id, interview.link_token);
  }, [onCopyLink, interview.id, interview.link_token]);

  return (
    <TableRow>
      <TableCell className="font-medium">
        <div className="flex items-center gap-2">
          <User className="w-4 h-4 text-gray-400" />
          {interview.candidate_name || interview.candidate_id}
        </div>
      </TableCell>
      
      <TableCell>
        <div className="flex flex-col">
          {interview.title && interview.title.trim() ? (
            <span className="font-medium text-gray-900">{interview.title}</span>
          ) : interview.interview_template_name ? (
            <span className="font-medium text-gray-900">
              {interview.interview_template_name}
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
            {(interview.interviewer_names || interview.interviewers || []).slice(0, 2).map((interviewerName, idx) => (
              <div key={idx} className="flex items-center gap-1 text-xs text-gray-600">
                <Users className="w-3 h-3" />
                <span>{interviewerName}</span>
              </div>
            ))}
            {((interview.interviewer_names || interview.interviewers || []).length > 2) && (
              <span className="text-xs text-gray-400">
                +{(interview.interviewer_names || interview.interviewers || []).length - 2} más
              </span>
            )}
          </div>
        ) : (interview.required_role_names || interview.required_roles || []).length > 0 ? (
          <div className="flex flex-col gap-1">
            {(interview.required_role_names || interview.required_roles || []).slice(0, 2).map((roleName, idx) => (
              <Badge key={idx} variant="outline" className="text-xs w-fit">
                {roleName}
              </Badge>
            ))}
            {(interview.required_role_names || interview.required_roles || []).length > 2 && (
              <span className="text-xs text-gray-400">
                +{(interview.required_role_names || interview.required_roles || []).length - 2} más
              </span>
            )}
          </div>
        ) : (
          <span className="text-xs text-gray-400">Sin asignar</span>
        )}
      </TableCell>
      
      <TableCell>{getStatusBadge(interview.status)}</TableCell>
      
      <TableCell>
        <div className="flex items-center gap-1">
          <button
            type="button"
            onClick={handleEditClick}
            className="flex items-center gap-2 text-sm text-gray-600 hover:text-blue-600 transition-colors"
          >
            {interview.is_incomplete ? (
              <TooltipProvider delayDuration={0} skipDelayDuration={0}>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <AlertTriangle className="h-5 w-5 text-yellow-500 flex-shrink-0" />
                  </TooltipTrigger>
                  <TooltipContent>
                    {!interview.required_roles || interview.required_roles.length === 0
                      ? 'Faltan roles requeridos'
                      : !interview.interviewers || interview.interviewers.length === 0
                        ? 'Faltan entrevistadores asignados'
                        : 'Falta información requerida'}
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            ) : (
              <Calendar className="w-5 h-5 flex-shrink-0" />
            )}
            {interview.scheduled_at ? formatDate(interview.scheduled_at) : 'N/A'}
          </button>
        </div>
      </TableCell>
      
      <TableCell>
        {interview.deadline_date ? (
          <button
            type="button"
            onClick={handleEditClick}
            className="flex items-center gap-2 text-sm text-gray-600 hover:text-blue-600 transition-colors"
          >
            <Clock className="w-5 h-5 flex-shrink-0" />
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
            {interview.job_position_title || interview.job_position_id}
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
                onClick={handleViewClick}
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
                onClick={handleGenerateLinkClick}
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
                  onClick={handleCopyLinkClick}
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
  );
});

InterviewTableRow.displayName = 'InterviewTableRow';

