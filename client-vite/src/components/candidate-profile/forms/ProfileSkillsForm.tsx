import React, { useState, useEffect } from 'react';
import { api } from '../../../lib/api';
import { X, Plus } from 'lucide-react';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card';

interface ProfileSkillsFormProps {
  onSuccess?: () => void;
}

const ProfileSkillsForm: React.FC<ProfileSkillsFormProps> = ({ onSuccess }) => {
  const [skills, setSkills] = useState<string[]>([]);
  const [newSkill, setNewSkill] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const profile = await api.getMyProfile() as any;
      setSkills(profile.skills || []);
    } catch (err) {
      console.error('Error loading profile:', err);
      setError('Error al cargar las habilidades');
    } finally {
      setLoading(false);
    }
  };

  const handleAddSkill = () => {
    const trimmedSkill = newSkill.trim();
    if (trimmedSkill && !skills.includes(trimmedSkill)) {
      setSkills([...skills, trimmedSkill]);
      setNewSkill('');
    }
  };

  const handleRemoveSkill = (skillToRemove: string) => {
    setSkills(skills.filter(skill => skill !== skillToRemove));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddSkill();
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      setError('');

      // Get current profile to preserve other fields
      const profile = await api.getMyProfile() as any;

      await api.updateMyProfile({
        ...profile,
        skills,
      });

      setSuccess('Habilidades guardadas correctamente');
      setTimeout(() => setSuccess(''), 3000);
      onSuccess?.();
    } catch (err) {
      console.error('Error saving skills:', err);
      setError('Error al guardar las habilidades');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <Card>
        <CardContent className="py-8">
          <p className="text-center text-gray-500">Cargando habilidades...</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Habilidades</CardTitle>
        <CardDescription>
          Añade tus habilidades técnicas y competencias profesionales
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {success && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
            {success}
          </div>
        )}

        {/* Add skill input */}
        <div className="flex gap-2">
          <Input
            type="text"
            value={newSkill}
            onChange={(e) => setNewSkill(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Escribe una habilidad y presiona Enter"
            className="flex-1"
          />
          <Button
            type="button"
            onClick={handleAddSkill}
            disabled={!newSkill.trim()}
            variant="outline"
          >
            <Plus className="w-4 h-4 mr-1" />
            Añadir
          </Button>
        </div>

        {/* Skills list */}
        <div className="flex flex-wrap gap-2">
          {skills.map((skill, index) => (
            <div
              key={index}
              className="flex items-center gap-1 bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
            >
              <span>{skill}</span>
              <button
                type="button"
                onClick={() => handleRemoveSkill(skill)}
                className="hover:text-blue-600 ml-1"
              >
                <X className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>

        {skills.length === 0 && (
          <p className="text-gray-500 text-center py-4">
            No has añadido ninguna habilidad todavía
          </p>
        )}

        {/* Suggestions */}
        <div className="border-t pt-4">
          <p className="text-sm text-gray-600 mb-2">Sugerencias populares:</p>
          <div className="flex flex-wrap gap-2">
            {['JavaScript', 'Python', 'React', 'SQL', 'Excel', 'Comunicación', 'Liderazgo', 'Trabajo en equipo']
              .filter(s => !skills.includes(s))
              .slice(0, 6)
              .map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  onClick={() => setSkills([...skills, suggestion])}
                  className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-full text-sm transition-colors"
                >
                  + {suggestion}
                </button>
              ))}
          </div>
        </div>

        {/* Save button */}
        <div className="flex justify-end pt-4 border-t">
          <Button
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? 'Guardando...' : 'Guardar habilidades'}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default ProfileSkillsForm;
