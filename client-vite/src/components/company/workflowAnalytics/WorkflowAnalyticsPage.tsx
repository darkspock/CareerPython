/**
 * Workflow Analytics Page Component
 * Phase 9: Main page for viewing workflow analytics and bottlenecks
 */

import React, { useState, useEffect } from 'react';
import type { WorkflowAnalytics, StageAnalytics, StageBottleneck } from '@/types/workflowAnalytics';
import {
  formatConversionRate,
  formatTimeHours,
  getConversionRateColor,
  getBottleneckSeverityColor,
  getBottleneckSeverityLabel,
  formatAnalysisDate,
  calculateWorkflowHealthScore,
  getHealthScoreColor,
  getHealthScoreLabel
} from '@/types/workflowAnalytics';
import { WorkflowAnalyticsService } from '@/services/workflowAnalyticsService';

interface WorkflowAnalyticsPageProps {
  workflowId: string;
  workflowName?: string;
}

type DateRangeFilter = 'all' | '30days' | '90days' | 'custom';

export const WorkflowAnalyticsPage: React.FC<WorkflowAnalyticsPageProps> = ({
  workflowId,
  workflowName
}) => {
  const [analytics, setAnalytics] = useState<WorkflowAnalytics | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dateRange, setDateRange] = useState<DateRangeFilter>('all');
  const [customStartDate, setCustomStartDate] = useState('');
  const [customEndDate, setCustomEndDate] = useState('');

  // Load analytics
  const loadAnalytics = async () => {
    try {
      setIsLoading(true);
      setError(null);

      let result: WorkflowAnalytics;

      if (dateRange === '30days') {
        result = await WorkflowAnalyticsService.getAnalyticsLast30Days(workflowId);
      } else if (dateRange === '90days') {
        result = await WorkflowAnalyticsService.getAnalyticsLast90Days(workflowId);
      } else if (dateRange === 'custom' && customStartDate && customEndDate) {
        result = await WorkflowAnalyticsService.getWorkflowAnalytics(workflowId, {
          date_range_start: new Date(customStartDate).toISOString(),
          date_range_end: new Date(customEndDate).toISOString()
        });
      } else {
        result = await WorkflowAnalyticsService.getWorkflowAnalytics(workflowId);
      }

      setAnalytics(result);
    } catch (err) {
      setError('Failed to load workflow analytics');
      console.error('Error loading analytics:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, [workflowId, dateRange, customStartDate, customEndDate]);

  if (isLoading && !analytics) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (error || !analytics) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-red-600 font-medium">{error || 'Analytics not available'}</p>
          <button
            onClick={loadAnalytics}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const healthScore = calculateWorkflowHealthScore(analytics);

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          Workflow Analytics: {analytics.workflow_name}
        </h1>
        <p className="text-sm text-gray-600 mt-1">
          Analysis generated: {formatAnalysisDate(analytics.analysis_date)}
        </p>
      </div>

      {/* Date Range Filter */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <div className="flex flex-wrap items-center gap-4">
          <label className="text-sm font-medium text-gray-700">Date Range:</label>

          <button
            onClick={() => setDateRange('all')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              dateRange === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All Time
          </button>

          <button
            onClick={() => setDateRange('30days')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              dateRange === '30days'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Last 30 Days
          </button>

          <button
            onClick={() => setDateRange('90days')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              dateRange === '90days'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Last 90 Days
          </button>

          <button
            onClick={() => setDateRange('custom')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              dateRange === 'custom'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Custom Range
          </button>

          {dateRange === 'custom' && (
            <>
              <input
                type="date"
                value={customStartDate}
                onChange={(e) => setCustomStartDate(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg"
              />
              <span className="text-gray-600">to</span>
              <input
                type="date"
                value={customEndDate}
                onChange={(e) => setCustomEndDate(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg"
              />
            </>
          )}
        </div>
      </div>

      {/* Health Score Card */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Workflow Health Score</h2>
        <div className="flex items-center gap-6">
          <div className="text-center">
            <div className={`text-5xl font-bold ${getHealthScoreColor(healthScore)}`}>
              {healthScore.toFixed(0)}
            </div>
            <div className="text-sm text-gray-600 mt-2">out of 100</div>
          </div>
          <div className="flex-1">
            <div className={`text-xl font-semibold ${getHealthScoreColor(healthScore)}`}>
              {getHealthScoreLabel(healthScore)}
            </div>
            <p className="text-sm text-gray-600 mt-2">
              Based on conversion rates, bottlenecks, and application flow
            </p>
          </div>
        </div>
      </div>

      {/* Performance Overview */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Performance Overview</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="border border-gray-200 rounded-lg p-4">
            <p className="text-sm text-gray-600">Total Applications</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">
              {analytics.performance.total_applications}
            </p>
          </div>

          <div className="border border-green-200 rounded-lg p-4">
            <p className="text-sm text-gray-600">Active</p>
            <p className="text-2xl font-bold text-green-600 mt-1">
              {analytics.performance.active_applications}
            </p>
          </div>

          <div className="border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-gray-600">Completed</p>
            <p className="text-2xl font-bold text-blue-600 mt-1">
              {analytics.performance.completed_applications}
            </p>
          </div>

          <div className="border border-red-200 rounded-lg p-4">
            <p className="text-sm text-gray-600">Rejected</p>
            <p className="text-2xl font-bold text-red-600 mt-1">
              {analytics.performance.rejected_applications}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mt-4">
          <div className="border border-gray-200 rounded-lg p-4">
            <p className="text-sm text-gray-600">Overall Conversion Rate</p>
            <p className={`text-xl font-bold mt-1 ${getConversionRateColor(analytics.performance.overall_conversion_rate)}`}>
              {formatConversionRate(analytics.performance.overall_conversion_rate)}
            </p>
          </div>

          <div className="border border-gray-200 rounded-lg p-4">
            <p className="text-sm text-gray-600">Avg Completion Time</p>
            <p className="text-xl font-bold text-gray-900 mt-1">
              {formatTimeHours(analytics.performance.average_completion_time_hours)}
            </p>
          </div>

          <div className="border border-gray-200 rounded-lg p-4">
            <p className="text-sm text-gray-600">Time to Hire</p>
            <p className="text-xl font-bold text-gray-900 mt-1">
              {analytics.performance.time_to_hire_days
                ? `${analytics.performance.time_to_hire_days.toFixed(1)} days`
                : 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Bottlenecks */}
      {analytics.bottlenecks.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Identified Bottlenecks ({analytics.bottlenecks.length})
          </h2>
          <div className="space-y-4">
            {analytics.bottlenecks.map((bottleneck) => (
              <div
                key={bottleneck.stage_id}
                className={`border rounded-lg p-4 ${getBottleneckSeverityColor(bottleneck.bottleneck_score)}`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold">{bottleneck.stage_name}</h3>
                    <p className="text-sm opacity-80">Stage {bottleneck.stage_order + 1}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold">
                      {bottleneck.bottleneck_score.toFixed(0)}
                    </div>
                    <div className="text-xs font-medium">
                      {getBottleneckSeverityLabel(bottleneck.bottleneck_score)}
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4 mb-3 text-sm">
                  <div>
                    <span className="opacity-80">Stuck Applications:</span>
                    <span className="font-semibold ml-2">{bottleneck.current_applications}</span>
                  </div>
                  <div>
                    <span className="opacity-80">Conversion Rate:</span>
                    <span className="font-semibold ml-2">{formatConversionRate(bottleneck.conversion_rate)}</span>
                  </div>
                  <div>
                    <span className="opacity-80">Expected:</span>
                    <span className="font-semibold ml-2">{formatConversionRate(bottleneck.expected_conversion_rate)}</span>
                  </div>
                </div>

                <div className="text-sm">
                  <p className="font-medium mb-1">Reasons:</p>
                  <ul className="list-disc list-inside space-y-1">
                    {bottleneck.bottleneck_reasons.map((reason, idx) => (
                      <li key={idx} className="opacity-80">{reason}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Stage Analytics */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Stage-by-Stage Analysis</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Stage</th>
                <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Current</th>
                <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Total</th>
                <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Conversion</th>
                <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Dropout</th>
                <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Avg Time</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {analytics.stage_analytics.map((stage) => (
                <tr key={stage.stage_id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm font-medium text-gray-900">
                    {stage.stage_name}
                    <span className="ml-2 text-xs text-gray-500">(Stage {stage.stage_order + 1})</span>
                  </td>
                  <td className="px-4 py-3 text-sm text-right text-gray-700">
                    {stage.current_applications}
                  </td>
                  <td className="px-4 py-3 text-sm text-right text-gray-700">
                    {stage.total_applications}
                  </td>
                  <td className={`px-4 py-3 text-sm text-right font-semibold ${getConversionRateColor(stage.conversion_rate_to_next)}`}>
                    {formatConversionRate(stage.conversion_rate_to_next)}
                  </td>
                  <td className="px-4 py-3 text-sm text-right text-gray-700">
                    {formatConversionRate(stage.dropout_rate)}
                  </td>
                  <td className="px-4 py-3 text-sm text-right text-gray-700">
                    {formatTimeHours(stage.average_time_hours)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recommendations */}
      {analytics.recommendations.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-blue-900 mb-4">
            Recommendations
          </h2>
          <ul className="space-y-2">
            {analytics.recommendations.map((recommendation, idx) => (
              <li key={idx} className="flex items-start gap-2 text-sm text-blue-800">
                <span className="text-blue-600 font-bold">•</span>
                <span>{recommendation}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
