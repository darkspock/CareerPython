import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Bell, Check, CheckCheck, Trash2, ExternalLink } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { notificationService, type InAppNotification } from '../../services/notificationService';

const priorityColors: Record<string, string> = {
  LOW: 'bg-gray-100 text-gray-600',
  NORMAL: 'bg-blue-100 text-blue-600',
  HIGH: 'bg-orange-100 text-orange-600',
  URGENT: 'bg-red-100 text-red-600',
};


const formatTimeAgo = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'Ahora';
  if (diffMins < 60) return `Hace ${diffMins}m`;
  if (diffHours < 24) return `Hace ${diffHours}h`;
  if (diffDays < 7) return `Hace ${diffDays}d`;
  return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' });
};

export const NotificationBell: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState<InAppNotification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [totalCount, setTotalCount] = useState(0);
  const pollingRef = useRef<NodeJS.Timeout | null>(null);

  const fetchUnreadCount = useCallback(async () => {
    try {
      const response = await notificationService.getUnreadCount();
      setUnreadCount(response.unread_count);
    } catch (error) {
      console.error('Error fetching unread count:', error);
    }
  }, []);

  const fetchNotifications = useCallback(async () => {
    setLoading(true);
    try {
      const response = await notificationService.listNotifications(10, 0, false);
      setNotifications(response.notifications);
      setUnreadCount(response.unread_count);
      setTotalCount(response.total_count);
    } catch (error) {
      console.error('Error fetching notifications:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  // Poll for unread count every 30 seconds
  useEffect(() => {
    fetchUnreadCount();
    pollingRef.current = setInterval(fetchUnreadCount, 30000);

    return () => {
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
      }
    };
  }, [fetchUnreadCount]);

  // Fetch notifications when popover opens
  useEffect(() => {
    if (isOpen) {
      fetchNotifications();
    }
  }, [isOpen, fetchNotifications]);

  const handleMarkAsRead = async (notificationId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await notificationService.markAsRead(notificationId);
      setNotifications(prev =>
        prev.map(n =>
          n.id === notificationId ? { ...n, is_read: true, read_at: new Date().toISOString() } : n
        )
      );
      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await notificationService.markAllAsRead();
      setNotifications(prev =>
        prev.map(n => ({ ...n, is_read: true, read_at: new Date().toISOString() }))
      );
      setUnreadCount(0);
    } catch (error) {
      console.error('Error marking all notifications as read:', error);
    }
  };

  const handleDelete = async (notificationId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await notificationService.deleteNotification(notificationId);
      const deletedNotification = notifications.find(n => n.id === notificationId);
      setNotifications(prev => prev.filter(n => n.id !== notificationId));
      setTotalCount(prev => prev - 1);
      if (deletedNotification && !deletedNotification.is_read) {
        setUnreadCount(prev => Math.max(0, prev - 1));
      }
    } catch (error) {
      console.error('Error deleting notification:', error);
    }
  };

  const handleNotificationClick = (notification: InAppNotification) => {
    if (!notification.is_read) {
      notificationService.markAsRead(notification.id);
      setNotifications(prev =>
        prev.map(n =>
          n.id === notification.id ? { ...n, is_read: true, read_at: new Date().toISOString() } : n
        )
      );
      setUnreadCount(prev => Math.max(0, prev - 1));
    }

    if (notification.link) {
      setIsOpen(false);
      navigate(notification.link);
    }
  };

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <button
          className="relative p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          aria-label={t('notifications.title', 'Notificaciones')}
        >
          <Bell className="w-5 h-5" />
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-[10px] font-medium text-white">
              {unreadCount > 99 ? '99+' : unreadCount}
            </span>
          )}
        </button>
      </PopoverTrigger>
      <PopoverContent
        className="w-96 p-0"
        align="end"
        sideOffset={8}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b">
          <h3 className="font-semibold text-gray-900">
            {t('notifications.title', 'Notificaciones')}
          </h3>
          {unreadCount > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleMarkAllAsRead}
              className="text-xs text-blue-600 hover:text-blue-700"
            >
              <CheckCheck className="w-4 h-4 mr-1" />
              {t('notifications.markAllRead', 'Marcar todo como leído')}
            </Button>
          )}
        </div>

        {/* Notification List */}
        <div className="max-h-[400px] overflow-y-auto">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            </div>
          ) : notifications.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-gray-500">
              <Bell className="w-8 h-8 mb-2 text-gray-300" />
              <p className="text-sm">{t('notifications.empty', 'No tienes notificaciones')}</p>
            </div>
          ) : (
            <ul className="divide-y divide-gray-100">
              {notifications.map((notification) => (
                <li
                  key={notification.id}
                  className={`px-4 py-3 hover:bg-gray-50 cursor-pointer transition-colors ${
                    !notification.is_read ? 'bg-blue-50' : ''
                  }`}
                  onClick={() => handleNotificationClick(notification)}
                >
                  <div className="flex items-start gap-3">
                    {/* Unread indicator */}
                    <div className="flex-shrink-0 mt-1">
                      {!notification.is_read && (
                        <div className="w-2 h-2 rounded-full bg-blue-500" />
                      )}
                      {notification.is_read && <div className="w-2 h-2" />}
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <p className={`text-sm font-medium truncate ${
                          notification.is_read ? 'text-gray-700' : 'text-gray-900'
                        }`}>
                          {notification.title}
                        </p>
                        {notification.priority !== 'NORMAL' && (
                          <Badge
                            variant="secondary"
                            className={`text-[10px] px-1.5 py-0 ${priorityColors[notification.priority]}`}
                          >
                            {notification.priority}
                          </Badge>
                        )}
                      </div>
                      <p className={`text-xs mt-0.5 line-clamp-2 ${
                        notification.is_read ? 'text-gray-500' : 'text-gray-600'
                      }`}>
                        {notification.message}
                      </p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs text-gray-400">
                          {formatTimeAgo(notification.created_at)}
                        </span>
                        {notification.link && (
                          <ExternalLink className="w-3 h-3 text-gray-400" />
                        )}
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex-shrink-0 flex items-center gap-1">
                      {!notification.is_read && (
                        <button
                          onClick={(e) => handleMarkAsRead(notification.id, e)}
                          className="p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-100 rounded transition-colors"
                          title={t('notifications.markRead', 'Marcar como leído')}
                        >
                          <Check className="w-4 h-4" />
                        </button>
                      )}
                      <button
                        onClick={(e) => handleDelete(notification.id, e)}
                        className="p-1 text-gray-400 hover:text-red-600 hover:bg-red-100 rounded transition-colors"
                        title={t('notifications.delete', 'Eliminar')}
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Footer */}
        {totalCount > 10 && (
          <div className="px-4 py-3 border-t text-center">
            <button
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
              onClick={() => {
                setIsOpen(false);
                // Navigate to full notifications page if implemented
                // navigate('/company/notifications');
              }}
            >
              {t('notifications.viewAll', 'Ver todas las notificaciones')} ({totalCount})
            </button>
          </div>
        )}
      </PopoverContent>
    </Popover>
  );
};

export default NotificationBell;
