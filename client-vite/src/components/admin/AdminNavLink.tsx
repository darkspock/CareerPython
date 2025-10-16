import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../../lib/api';

const AdminNavLink: React.FC = () => {
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAdminAccess = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          setIsAdmin(false);
          setLoading(false);
          return;
        }

        await api.authenticatedRequest('/admin/health');
        setIsAdmin(true);
      } catch (error) {
        setIsAdmin(false);
      } finally {
        setLoading(false);
      }
    };

    checkAdminAccess();
  }, []);

  if (loading || !isAdmin) {
    return null;
  }

  return (
    <Link
      to="/admin/dashboard"
      className="text-sm font-medium text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition-colors bg-yellow-50 border border-yellow-200 hover:bg-yellow-100"
    >
      🔧 Admin Panel
    </Link>
  );
};

export default AdminNavLink;