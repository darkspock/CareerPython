import React, { useEffect, useState } from 'react';
import { Users, Plus, X, AlertCircle, CheckCircle } from 'lucide-react';
import { PositionStageAssignmentService } from '../../services/positionStageAssignmentService';
import type { PositionStageAssignment } from '../../types/positionStageAssignment';
import type { WorkflowStage } from '../../types/workflow';

interface StageAssignmentEditorProps {
  positionId: string;
  stages: WorkflowStage[];
  companyUsers: Array<{ id: string; name: string; email: string }>;
  onAssignmentsChange?: (assignments: PositionStageAssignment[]) => void;
  disabled?: boolean;
}

export const StageAssignmentEditor: React.FC<StageAssignmentEditorProps> = ({
  positionId,
  stages,
  companyUsers,
  onAssignmentsChange,
  disabled = false,
}) => {
  const [assignments, setAssignments] = useState<Record<string, string[]>>({});
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    loadAssignments();
  }, [positionId]);

  const loadAssignments = async () => {
    if (!positionId) return;

    setLoading(true);
    setError(null);

    try {
      const result = await PositionStageAssignmentService.listStageAssignments(positionId);

      // Convert array to Record<stageId, userIds[]>
      const assignmentsMap: Record<string, string[]> = {};
      result.forEach(assignment => {
        assignmentsMap[assignment.stage_id] = assignment.assigned_user_ids;
      });

      setAssignments(assignmentsMap);

      if (onAssignmentsChange) {
        onAssignmentsChange(result);
      }
    } catch (err: any) {
      console.error('Error loading stage assignments:', err);
      setError(err.message || 'Failed to load stage assignments');
    } finally {
      setLoading(false);
    }
  };

  const handleAddUser = async (stageId: string, userId: string) => {
    if (!userId || disabled) return;

    setSaving(true);
    setError(null);
    setSuccess(null);

    try {
      await PositionStageAssignmentService.addUserToStage({
        position_id: positionId,
        stage_id: stageId,
        user_id: userId,
      });

      // Update local state
      setAssignments(prev => ({
        ...prev,
        [stageId]: [...(prev[stageId] || []), userId],
      }));

      setSuccess('User added successfully');
      setTimeout(() => setSuccess(null), 3000);

      // Reload to get updated data
      await loadAssignments();
    } catch (err: any) {
      console.error('Error adding user to stage:', err);
      setError(err.message || 'Failed to add user');
    } finally {
      setSaving(false);
    }
  };

  const handleRemoveUser = async (stageId: string, userId: string) => {
    if (disabled) return;

    setSaving(true);
    setError(null);
    setSuccess(null);

    try {
      await PositionStageAssignmentService.removeUserFromStage({
        position_id: positionId,
        stage_id: stageId,
        user_id: userId,
      });

      // Update local state
      setAssignments(prev => ({
        ...prev,
        [stageId]: (prev[stageId] || []).filter(id => id !== userId),
      }));

      setSuccess('User removed successfully');
      setTimeout(() => setSuccess(null), 3000);

      // Reload to get updated data
      await loadAssignments();
    } catch (err: any) {
      console.error('Error removing user from stage:', err);
      setError(err.message || 'Failed to remove user');
    } finally {
      setSaving(false);
    }
  };

  const getAvailableUsers = (stageId: string) => {
    const assignedUserIds = assignments[stageId] || [];
    return companyUsers.filter(user => !assignedUserIds.includes(user.id));
  };

  const getAssignedUsers = (stageId: string) => {
    const assignedUserIds = assignments[stageId] || [];
    return companyUsers.filter(user => assignedUserIds.includes(user.id));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-600">Loading assignments...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Users className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-medium text-gray-900">Stage Assignments</h3>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-md">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
          <span className="text-sm text-red-700">{error}</span>
        </div>
      )}

      {success && (
        <div className="flex items-center gap-2 p-3 bg-green-50 border border-green-200 rounded-md">
          <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
          <span className="text-sm text-green-700">{success}</span>
        </div>
      )}

      <div className="space-y-4">
        {stages.map((stage) => {
          const assignedUsers = getAssignedUsers(stage.id);
          const availableUsers = getAvailableUsers(stage.id);

          return (
            <div
              key={stage.id}
              className="border border-gray-200 rounded-lg p-4 bg-white"
            >
              <div className="flex items-center justify-between mb-3">
                <div>
                  <h4 className="font-medium text-gray-900">{stage.name}</h4>
                  {stage.description && (
                    <p className="text-sm text-gray-500 mt-1">{stage.description}</p>
                  )}
                </div>
                <span className="text-sm text-gray-500">
                  {assignedUsers.length} {assignedUsers.length === 1 ? 'user' : 'users'}
                </span>
              </div>

              {/* Assigned Users */}
              <div className="space-y-2 mb-3">
                {assignedUsers.length > 0 ? (
                  assignedUsers.map((user) => (
                    <div
                      key={user.id}
                      className="flex items-center justify-between p-2 bg-blue-50 rounded-md"
                    >
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {user.name}
                        </div>
                        <div className="text-xs text-gray-500">{user.email}</div>
                      </div>
                      {!disabled && (
                        <button
                          onClick={() => handleRemoveUser(stage.id, user.id)}
                          disabled={saving}
                          className="p-1 text-red-600 hover:text-red-700 hover:bg-red-100 rounded disabled:opacity-50"
                          title="Remove user"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  ))
                ) : (
                  <div className="text-sm text-gray-500 italic">No users assigned</div>
                )}
              </div>

              {/* Add User Dropdown */}
              {!disabled && availableUsers.length > 0 && (
                <div className="flex items-center gap-2">
                  <select
                    onChange={(e) => {
                      if (e.target.value) {
                        handleAddUser(stage.id, e.target.value);
                        e.target.value = ''; // Reset selection
                      }
                    }}
                    disabled={saving}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm text-sm
                             focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                             disabled:bg-gray-100 disabled:cursor-not-allowed"
                  >
                    <option value="">Add user to this stage...</option>
                    {availableUsers.map((user) => (
                      <option key={user.id} value={user.id}>
                        {user.name} ({user.email})
                      </option>
                    ))}
                  </select>
                  <Plus className="w-5 h-5 text-gray-400" />
                </div>
              )}

              {!disabled && availableUsers.length === 0 && assignedUsers.length < companyUsers.length && (
                <div className="text-sm text-gray-500 italic">All users assigned</div>
              )}
            </div>
          );
        })}
      </div>

      {stages.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No workflow stages available. Please select a workflow first.
        </div>
      )}
    </div>
  );
};

export default StageAssignmentEditor;
