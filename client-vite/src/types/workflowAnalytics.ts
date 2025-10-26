/**
 * Workflow Analytics Types
 * Phase 9: TypeScript interfaces for workflow analytics
 */

export interface StageAnalytics {
  stage_id: string;
  stage_name: string;
  stage_order: number;
  total_applications: number;
  current_applications: number;
  completed_applications: number;
  rejected_applications: number;
  average_time_hours: number | null;
  median_time_hours: number | null;
  min_time_hours: number | null;
  max_time_hours: number | null;
  conversion_rate_to_next: number | null; // Percentage (0-100)
  dropout_rate: number | null; // Percentage (0-100)
}

export interface StageBottleneck {
  stage_id: string;
  stage_name: string;
  stage_order: number;
  current_applications: number;
  average_time_hours: number;
  expected_time_hours: number;
  time_variance_percentage: number;
  conversion_rate: number;
  expected_conversion_rate: number;
  conversion_variance_percentage: number;
  bottleneck_score: number; // 0-100, higher = worse bottleneck
  bottleneck_reasons: string[];
}

export interface WorkflowPerformance {
  workflow_id: string;
  workflow_name: string;
  total_applications: number;
  active_applications: number;
  completed_applications: number;
  rejected_applications: number;
  withdrawn_applications: number;
  average_completion_time_hours: number | null;
  median_completion_time_hours: number | null;
  overall_conversion_rate: number | null; // Percentage (0-100)
  cost_per_hire: number | null;
  time_to_hire_days: number | null;
  applications_per_stage: Record<string, number>;
}

export interface WorkflowAnalytics {
  workflow_id: string;
  workflow_name: string;
  company_id: string;
  analysis_date: string;
  date_range_start: string | null;
  date_range_end: string | null;

  // Overall performance
  performance: WorkflowPerformance;

  // Per-stage analytics
  stage_analytics: StageAnalytics[];

  // Identified bottlenecks
  bottlenecks: StageBottleneck[];

  // Summary insights
  total_stages: number;
  fastest_stage: string | null;
  slowest_stage: string | null;
  highest_conversion_stage: string | null;
  lowest_conversion_stage: string | null;

  // Recommendations
  recommendations: string[];
}

// Helper function to get bottleneck severity color
export function getBottleneckSeverityColor(score: number): string {
  if (score >= 70) return 'text-red-600 bg-red-50 border-red-200';
  if (score >= 50) return 'text-orange-600 bg-orange-50 border-orange-200';
  if (score >= 30) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
  return 'text-gray-600 bg-gray-50 border-gray-200';
}

// Helper function to get bottleneck severity label
export function getBottleneckSeverityLabel(score: number): string {
  if (score >= 70) return 'Critical';
  if (score >= 50) return 'High';
  if (score >= 30) return 'Medium';
  return 'Low';
}

// Helper function to format conversion rate
export function formatConversionRate(rate: number | null): string {
  if (rate === null) return 'N/A';
  return `${rate.toFixed(1)}%`;
}

// Helper function to format time in hours to human-readable format
export function formatTimeHours(hours: number | null): string {
  if (hours === null) return 'N/A';

  if (hours < 1) {
    const minutes = Math.round(hours * 60);
    return `${minutes}m`;
  }

  if (hours < 24) {
    return `${hours.toFixed(1)}h`;
  }

  const days = Math.floor(hours / 24);
  const remainingHours = Math.round(hours % 24);

  if (remainingHours === 0) {
    return `${days}d`;
  }

  return `${days}d ${remainingHours}h`;
}

// Helper function to get conversion rate color
export function getConversionRateColor(rate: number | null): string {
  if (rate === null) return 'text-gray-500';
  if (rate >= 70) return 'text-green-600';
  if (rate >= 50) return 'text-yellow-600';
  if (rate >= 30) return 'text-orange-600';
  return 'text-red-600';
}

// Helper function to format date for display
export function formatAnalysisDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// Helper function to calculate health score (0-100, higher is better)
export function calculateWorkflowHealthScore(analytics: WorkflowAnalytics): number {
  let score = 100;

  // Deduct points for bottlenecks
  const avgBottleneckScore = analytics.bottlenecks.length > 0
    ? analytics.bottlenecks.reduce((sum, b) => sum + b.bottleneck_score, 0) / analytics.bottlenecks.length
    : 0;
  score -= avgBottleneckScore * 0.3; // Max 30 points deducted

  // Deduct points for low conversion rate
  const conversionRate = analytics.performance.overall_conversion_rate ?? 0;
  if (conversionRate < 20) {
    score -= (20 - conversionRate) * 2; // Up to 40 points
  }

  // Deduct points if too many active applications (stuck)
  const activePercentage = analytics.performance.total_applications > 0
    ? (analytics.performance.active_applications / analytics.performance.total_applications) * 100
    : 0;
  if (activePercentage > 70) {
    score -= (activePercentage - 70); // Up to 30 points
  }

  return Math.max(0, Math.min(100, score));
}

// Helper function to get health score color
export function getHealthScoreColor(score: number): string {
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  if (score >= 40) return 'text-orange-600';
  return 'text-red-600';
}

// Helper function to get health score label
export function getHealthScoreLabel(score: number): string {
  if (score >= 80) return 'Excellent';
  if (score >= 60) return 'Good';
  if (score >= 40) return 'Fair';
  return 'Needs Attention';
}
