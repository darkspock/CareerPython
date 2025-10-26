// Phase 6: Task Dashboard Component
// Main dashboard for viewing and managing assigned tasks

import React, { useState, useEffect } from 'react';
import { AlertCircle, Filter, RefreshCw, Search, CheckCircle, Clock, AlertTriangle } from 'lucide-react';
import { Task, TaskFilters, PriorityLevel, TaskStatus } from '@/types/task';
import TaskService from '@/services/taskService';
import { TaskCard } from './TaskCard';

interface TaskDashboardProps {
  userId: string;
  onTaskAction?: (task: Task, action: 'claimed' | 'unclaimed') => void;
  onViewTaskDetails?: (task: Task) => void;
}

type FilterTab = 'all' | 'high-priority' | 'overdue' | 'in-progress';

/**
 * TaskDashboard Component
 *
 * Main dashboard for task management:
 * - Displays all assigned tasks
 * - Filter by priority, status, stage
 * - Sort by different criteria
 * - Claim/unclaim tasks
 * - Auto-refresh tasks
 *
 * @param userId - ID of the current user
 * @param onTaskAction - Callback when a task is claimed or unclaimed
 * @param onViewTaskDetails - Callback when user wants to view task details
 */
export const TaskDashboard: React.FC<TaskDashboardProps> = ({
  userId,
  onTaskAction,
  onViewTaskDetails
}) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState<boolean>(false);

  // Filters
  const [activeTab, setActiveTab] = useState<FilterTab>('all');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedStage, setSelectedStage] = useState<string>('');

  // Load tasks on mount and when userId changes
  useEffect(() => {
    loadTasks();
  }, [userId]);

  // Apply filters when tasks or filter state changes
  useEffect(() => {
    applyFilters();
  }, [tasks, activeTab, searchTerm, selectedStage]);

  /**
   * Load tasks from API
   */
  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const fetchedTasks = await TaskService.getMyAssignedTasks(userId);
      setTasks(fetchedTasks);
    } catch (err) {
      console.error('Error loading tasks:', err);
      setError('Failed to load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Refresh tasks
   */
  const handleRefresh = async () => {
    setRefreshing(true);
    await loadTasks();
    setRefreshing(false);
  };

  /**
   * Apply filters to tasks
   */
  const applyFilters = () => {
    let filtered = [...tasks];

    // Apply tab filter
    switch (activeTab) {
      case 'high-priority':
        filtered = filtered.filter(
          task => task.priority_level === PriorityLevel.CRITICAL || task.priority_level === PriorityLevel.HIGH
        );
        break;
      case 'overdue':
        filtered = filtered.filter(task => task.is_overdue);
        break;
      case 'in-progress':
        filtered = filtered.filter(task => task.task_status === TaskStatus.IN_PROGRESS);
        break;
      case 'all':
      default:
        // No additional filtering
        break;
    }

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(
        task =>
          task.candidate_name.toLowerCase().includes(term) ||
          task.position_title.toLowerCase().includes(term) ||
          task.candidate_email?.toLowerCase().includes(term)
      );
    }

    // Apply stage filter
    if (selectedStage) {
      filtered = filtered.filter(task => task.current_stage_id === selectedStage);
    }

    setFilteredTasks(filtered);
  };

  /**
   * Handle task claim
   */
  const handleClaimTask = async (task: Task) => {
    try {
      await TaskService.claimTask(task.application_id, userId);

      // Update local state
      setTasks(prevTasks =>
        prevTasks.map(t =>
          t.application_id === task.application_id
            ? { ...t, task_status: TaskStatus.IN_PROGRESS }
            : t
        )
      );

      if (onTaskAction) {
        onTaskAction(task, 'claimed');
      }
    } catch (err) {
      console.error('Error claiming task:', err);
      alert('Failed to claim task. Please try again.');
    }
  };

  /**
   * Handle task unclaim
   */
  const handleUnclaimTask = async (task: Task) => {
    try {
      await TaskService.unclaimTask(task.application_id, userId);

      // Update local state
      setTasks(prevTasks =>
        prevTasks.map(t =>
          t.application_id === task.application_id
            ? { ...t, task_status: TaskStatus.PENDING }
            : t
        )
      );

      if (onTaskAction) {
        onTaskAction(task, 'unclaimed');
      }
    } catch (err) {
      console.error('Error unclaiming task:', err);
      alert('Failed to unclaim task. Please try again.');
    }
  };

  /**
   * Get unique stages from tasks
   */
  const getUniqueStages = () => {
    const stages = new Map<string, string>();
    tasks.forEach(task => {
      if (task.current_stage_id && task.current_stage_name) {
        stages.set(task.current_stage_id, task.current_stage_name);
      }
    });
    return Array.from(stages.entries());
  };

  // Calculate stats
  const stats = {
    total: tasks.length,
    highPriority: tasks.filter(
      t => t.priority_level === PriorityLevel.CRITICAL || t.priority_level === PriorityLevel.HIGH
    ).length,
    overdue: tasks.filter(t => t.is_overdue).length,
    inProgress: tasks.filter(t => t.task_status === TaskStatus.IN_PROGRESS).length
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">My Tasks</h1>
        <p className="text-gray-600">
          Manage and process your assigned application tasks
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Tasks</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
            <CheckCircle className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">High Priority</p>
              <p className="text-2xl font-bold text-orange-600">{stats.highPriority}</p>
            </div>
            <AlertTriangle className="w-8 h-8 text-orange-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Overdue</p>
              <p className="text-2xl font-bold text-red-600">{stats.overdue}</p>
            </div>
            <Clock className="w-8 h-8 text-red-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">In Progress</p>
              <p className="text-2xl font-bold text-blue-600">{stats.inProgress}</p>
            </div>
            <RefreshCw className="w-8 h-8 text-blue-500" />
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        {/* Tab Filters */}
        <div className="flex items-center gap-2 mb-4 overflow-x-auto">
          <button
            onClick={() => setActiveTab('all')}
            className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap ${
              activeTab === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All Tasks ({tasks.length})
          </button>
          <button
            onClick={() => setActiveTab('high-priority')}
            className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap ${
              activeTab === 'high-priority'
                ? 'bg-orange-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            High Priority ({stats.highPriority})
          </button>
          <button
            onClick={() => setActiveTab('overdue')}
            className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap ${
              activeTab === 'overdue'
                ? 'bg-red-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Overdue ({stats.overdue})
          </button>
          <button
            onClick={() => setActiveTab('in-progress')}
            className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap ${
              activeTab === 'in-progress'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            In Progress ({stats.inProgress})
          </button>
        </div>

        {/* Search and Stage Filter */}
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search by candidate name, email, or position..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <select
            value={selectedStage}
            onChange={(e) => setSelectedStage(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">All Stages</option>
            {getUniqueStages().map(([id, name]) => (
              <option key={id} value={id}>
                {name}
              </option>
            ))}
          </select>

          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:bg-gray-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <RefreshCw className="w-8 h-8 text-blue-600 animate-spin" />
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <p className="text-red-800">{error}</p>
          </div>
          <button
            onClick={loadTasks}
            className="mt-2 text-sm text-red-600 hover:text-red-700 font-medium"
          >
            Try again
          </button>
        </div>
      )}

      {/* Tasks List */}
      {!loading && !error && (
        <>
          {filteredTasks.length === 0 ? (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
              <CheckCircle className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No tasks found</h3>
              <p className="text-gray-600">
                {tasks.length === 0
                  ? "You don't have any assigned tasks at the moment."
                  : 'Try adjusting your filters to see more tasks.'}
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredTasks.map(task => (
                <TaskCard
                  key={task.application_id}
                  task={task}
                  onClaim={handleClaimTask}
                  onUnclaim={handleUnclaimTask}
                  onViewDetails={onViewTaskDetails}
                  showActions={true}
                />
              ))}
            </div>
          )}

          {/* Results Count */}
          {filteredTasks.length > 0 && (
            <div className="mt-6 text-center text-sm text-gray-600">
              Showing {filteredTasks.length} of {tasks.length} tasks
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default TaskDashboard;
