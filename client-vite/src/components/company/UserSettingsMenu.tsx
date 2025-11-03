import { useState, useEffect, useRef } from 'react';
import { User, LogOut, Globe, ChevronDown } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { api } from '../../lib/api';

interface UserSettingsMenuProps {
  onLogout: () => void;
}

export default function UserSettingsMenu({ onLogout }: UserSettingsMenuProps) {
  const { i18n, t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState(i18n.language || 'es');
  const menuRef = useRef<HTMLDivElement>(null);

  const languages = [
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'en', name: 'English', flag: '🇺🇸' },
  ];

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  // Load user's language preference on mount
  useEffect(() => {
    const loadUserLanguagePreference = async () => {
      try {
        const response = await api.getUserLanguagePreference() as { preferred_language?: string; language_code?: string };
        const preferredLanguage = response.preferred_language || response.language_code;
        
        if (preferredLanguage && preferredLanguage !== i18n.language) {
          await i18n.changeLanguage(preferredLanguage);
          setCurrentLanguage(preferredLanguage);
        } else {
          setCurrentLanguage(i18n.language);
        }
      } catch (error) {
        console.warn('Failed to load user language preference:', error);
        setCurrentLanguage(i18n.language);
      }
    };

    loadUserLanguagePreference();
  }, [i18n]);

  const handleLanguageChange = async (languageCode: string) => {
    try {
      await i18n.changeLanguage(languageCode);
      setCurrentLanguage(languageCode);

      // Save language preference to user profile in database
      try {
        await api.updateUserLanguagePreference(languageCode);
      } catch (apiError) {
        console.warn('Failed to save language preference to database:', apiError);
      }

      // Also save in localStorage as fallback
      localStorage.setItem('preferredLanguage', languageCode);
      localStorage.setItem('i18nextLng', languageCode);
      
      setIsOpen(false);
    } catch (error) {
      console.error('Failed to change language:', error);
    }
  };

  // const _currentLang = languages.find(lang => lang.code === currentLanguage) || languages[0];

  return (
    <div className="relative" ref={menuRef}>
      {/* User Menu Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
        aria-label="User settings menu"
      >
        <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-medium text-sm">
          <User className="w-4 h-4" />
        </div>
        <ChevronDown className={`w-4 h-4 text-gray-600 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute right-0 top-full mt-2 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-[100]">
          {/* Header */}
          <div className="px-4 py-3 border-b border-gray-200">
            <p className="text-sm font-medium text-gray-900">{t('company.userSettings.title')}</p>
          </div>

          {/* Language Selection */}
          <div className="px-4 py-2">
            <div className="flex items-center gap-2 mb-2">
              <Globe className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700">{t('company.userSettings.language')}</span>
            </div>
            <div className="space-y-1">
              {languages.map((language) => (
                <button
                  key={language.code}
                  onClick={() => handleLanguageChange(language.code)}
                  className={`w-full flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors ${
                    currentLanguage === language.code
                      ? 'bg-blue-50 text-blue-600 font-medium'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <span className="text-lg">{language.flag}</span>
                  <span>{language.name}</span>
                  {currentLanguage === language.code && (
                    <div className="ml-auto w-2 h-2 bg-blue-600 rounded-full"></div>
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Divider */}
          <div className="border-t border-gray-200"></div>

          {/* Logout */}
          <div className="px-4 py-2">
            <button
              onClick={() => {
                setIsOpen(false);
                onLogout();
              }}
              className="w-full flex items-center gap-3 px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            >
              <LogOut className="w-4 h-4" />
              <span>{t('company.userSettings.logout')}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

