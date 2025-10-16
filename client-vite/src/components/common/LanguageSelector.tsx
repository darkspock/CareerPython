import React from 'react';
import { Trash2 } from 'lucide-react';

// Language enums matching backend
const LanguageEnum = {
  ENGLISH: 'english',
  SPANISH: 'spanish',
  PORTUGUESE: 'portuguese',
  ITALIAN: 'italian',
  FRENCH: 'french',
  CHINESE: 'chinese',
  GERMAN: 'german',
  JAPANESE: 'japanese',
  RUSSIAN: 'russian',
  ARABIC: 'arabic',
} as const;

const LanguageLabels = {
  [LanguageEnum.ENGLISH]: 'Inglés',
  [LanguageEnum.SPANISH]: 'Español',
  [LanguageEnum.PORTUGUESE]: 'Portugués',
  [LanguageEnum.ITALIAN]: 'Italiano',
  [LanguageEnum.FRENCH]: 'Francés',
  [LanguageEnum.CHINESE]: 'Chino',
  [LanguageEnum.GERMAN]: 'Alemán',
  [LanguageEnum.JAPANESE]: 'Japonés',
  [LanguageEnum.RUSSIAN]: 'Ruso',
  [LanguageEnum.ARABIC]: 'Árabe',
} as const;

const LanguageLevelEnum = {
  NONE: 'none',
  BASIC: 'basic',
  CONVERSATIONAL: 'conversational',
  PROFESSIONAL: 'professional',
} as const;

const LanguageLevelLabels = {
  [LanguageLevelEnum.NONE]: 'Sin conocimiento',
  [LanguageLevelEnum.BASIC]: 'Básico',
  [LanguageLevelEnum.CONVERSATIONAL]: 'Conversacional',
  [LanguageLevelEnum.PROFESSIONAL]: 'Profesional',
} as const;

export interface Language {
  language: string;
  level: string;
}

interface LanguageSelectorProps {
  languages: Language[];
  onChange: (languages: Language[]) => void;
  className?: string;
}

const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  languages,
  onChange,
  className = ""
}) => {
  const addLanguage = () => {
    onChange([...languages, { language: '', level: LanguageLevelEnum.NONE }]);
  };

  const removeLanguage = (index: number) => {
    onChange(languages.filter((_, i) => i !== index));
  };

  const updateLanguage = (index: number, field: keyof Language, value: string) => {
    const updated = [...languages];
    updated[index] = { ...updated[index], [field]: value };
    onChange(updated);
  };

  return (
    <div className={className}>
      <label className="block text-sm font-medium text-gray-700 mb-2">Idiomas</label>
      <div className="space-y-3">
        {languages.map((lang, index) => (
          <div key={index} className="flex items-center gap-3">
            <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <select
                  value={lang.language}
                  onChange={(e) => updateLanguage(index, 'language', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Selecciona un idioma</option>
                  {Object.entries(LanguageLabels).map(([langKey, langLabel]) => (
                    <option key={langKey} value={langKey}>{langLabel}</option>
                  ))}
                </select>
              </div>
              <div>
                <select
                  value={lang.level}
                  onChange={(e) => updateLanguage(index, 'level', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  {Object.entries(LanguageLevelLabels).map(([levelKey, levelLabel]) => (
                    <option key={levelKey} value={levelKey}>{levelLabel}</option>
                  ))}
                </select>
              </div>
            </div>
            <button
              type="button"
              onClick={() => removeLanguage(index)}
              className="p-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg transition-colors"
              title="Eliminar idioma"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        ))}

        <button
          type="button"
          onClick={addLanguage}
          className="w-full py-3 px-4 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-blue-500 hover:text-blue-600 transition duration-200"
        >
          + Agregar idioma
        </button>
      </div>
    </div>
  );
};

export default LanguageSelector;

// Export utility functions for data conversion
export const convertLanguagesFromBackend = (languages: Record<string, string> | undefined): Language[] => {
  if (!languages) return [];
  return Object.entries(languages)
    .filter(([key, value]) => value !== LanguageLevelEnum.NONE)
    .map(([key, value]) => ({ language: key, level: value }));
};

export const convertLanguagesToBackend = (languages: Language[]): Record<string, string> => {
  return languages.reduce((acc, lang) => {
    if (lang.language && lang.level) {
      acc[lang.language] = lang.level;
    }
    return acc;
  }, {} as Record<string, string>);
};