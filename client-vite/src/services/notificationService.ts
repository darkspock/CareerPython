import api from '@/lib/api';

export interface InAppNotification {
  id: string;
  user_id: string;
  company_id: string;
  notification_type: string;
  title: string;
  message: string;
  priority: 'LOW' | 'NORMAL' | 'HIGH' | 'URGENT';
  is_read: boolean;
  created_at: string;
  read_at: string | null;
  link: string | null;
  metadata: Record<string, unknown> | null;
}

export interface NotificationListResponse {
  notifications: InAppNotification[];
  total_count: number;
  unread_count: number;
}

export interface UnreadCountResponse {
  unread_count: number;
}

export const notificationService = {
  /**
   * Get list of notifications for the current user
   */
  async listNotifications(
    limit: number = 20,
    offset: number = 0,
    unreadOnly: boolean = false
  ): Promise<NotificationListResponse> {
    const params = new URLSearchParams({
      limit: limit.toString(),
      offset: offset.toString(),
      unread_only: unreadOnly.toString(),
    });
    const response = await api.get(`/company/notifications/?${params}`);
    return response.data;
  },

  /**
   * Get unread notification count
   */
  async getUnreadCount(): Promise<UnreadCountResponse> {
    const response = await api.get('/company/notifications/unread-count');
    return response.data;
  },

  /**
   * Mark a notification as read
   */
  async markAsRead(notificationId: string): Promise<void> {
    await api.post(`/company/notifications/${notificationId}/read`);
  },

  /**
   * Mark all notifications as read
   */
  async markAllAsRead(): Promise<void> {
    await api.post('/company/notifications/read-all');
  },

  /**
   * Delete a notification
   */
  async deleteNotification(notificationId: string): Promise<void> {
    await api.delete(`/company/notifications/${notificationId}`);
  },
};

export default notificationService;
