/**
 * LanguageSelector Component
 * 
 * Simple language selector for the landing page (no authentication required)
 * 
 * @component
 */
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Globe, ChevronDown } from 'lucide-react';

const languages = [
  { code: 'es', name: 'Español', flag: '🇪🇸' },
  { code: 'en', name: 'English', flag: '🇺🇸' },
];

export default function LanguageSelector() {
  const { i18n } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);

  const currentLanguage = languages.find(lang => lang.code === i18n.language) || languages[0];

  const handleLanguageChange = (languageCode: string) => {
    i18n.changeLanguage(languageCode);
    localStorage.setItem('i18nextLng', languageCode);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 transition bg-transparent border-none cursor-pointer"
        aria-label="Select language"
      >
        <Globe className="w-4 h-4" />
        <span className="text-sm">{currentLanguage.flag} {currentLanguage.code.toUpperCase()}</span>
        <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute right-0 top-full mt-2 w-40 bg-white border border-gray-200 rounded-lg shadow-lg overflow-hidden z-20">
            {languages.map((language) => (
              <button
                key={language.code}
                onClick={() => handleLanguageChange(language.code)}
                className={`w-full flex items-center gap-3 px-4 py-2 text-sm text-left hover:bg-gray-50 transition-colors ${
                  i18n.language === language.code
                    ? 'bg-blue-50 text-blue-600 font-medium'
                    : 'text-gray-700'
                }`}
              >
                <span>{language.flag}</span>
                <span>{language.name}</span>
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

