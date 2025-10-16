import React from 'react';
import { Clock, FileText, User, Briefcase } from 'lucide-react';

interface ActivityItem {
  id: string;
  type: 'resume' | 'profile' | 'experience' | 'education' | 'project';
  title: string;
  description: string;
  timestamp: string;
  icon?: React.ReactNode;
}

const RecentActivitySection: React.FC = () => {
  // Mock data - in real app this would come from API
  const recentActivities: ActivityItem[] = [
    {
      id: '1',
      type: 'resume',
      title: 'CV Generado',
      description: 'Creaste "CV para Desarrollador Senior"',
      timestamp: 'Hace 2 horas'
    },
    {
      id: '2',
      type: 'profile',
      title: 'Perfil Actualizado',
      description: 'Actualizaste tu información de contacto',
      timestamp: 'Hace 1 día'
    },
    {
      id: '3',
      type: 'experience',
      title: 'Experiencia Añadida',
      description: 'Añadiste "Senior Developer en TechCorp"',
      timestamp: 'Hace 3 días'
    }
  ];

  const getIcon = (type: string) => {
    switch (type) {
      case 'resume':
        return <FileText className="w-4 h-4 text-blue-600" />;
      case 'profile':
        return <User className="w-4 h-4 text-purple-600" />;
      case 'experience':
        return <Briefcase className="w-4 h-4 text-green-600" />;
      default:
        return <Clock className="w-4 h-4 text-gray-600" />;
    }
  };

  const getBackgroundColor = (type: string) => {
    switch (type) {
      case 'resume':
        return 'bg-blue-50';
      case 'profile':
        return 'bg-purple-50';
      case 'experience':
        return 'bg-green-50';
      default:
        return 'bg-gray-50';
    }
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Actividad Reciente</h2>
        <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
          Ver todo
        </button>
      </div>

      <div className="space-y-4">
        {recentActivities.map((activity) => (
          <div key={activity.id} className="flex items-start gap-4 p-3 rounded-lg hover:bg-gray-50 transition-colors">
            {/* Icon */}
            <div className={`${getBackgroundColor(activity.type)} p-2 rounded-lg`}>
              {getIcon(activity.type)}
            </div>

            {/* Content */}
            <div className="flex-1">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-medium text-gray-900">{activity.title}</h3>
                  <p className="text-sm text-gray-600 mt-1">{activity.description}</p>
                </div>
                <span className="text-xs text-gray-500">{activity.timestamp}</span>
              </div>
            </div>
          </div>
        ))}

        {recentActivities.length === 0 && (
          <div className="text-center py-8">
            <Clock className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No hay actividad reciente</p>
            <p className="text-sm text-gray-400 mt-1">Empieza editando tu perfil o creando un CV</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecentActivitySection;