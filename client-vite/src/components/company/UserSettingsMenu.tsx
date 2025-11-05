import { useState, useEffect, useRef } from 'react';
import { User, LogOut, Globe, ChevronDown, ChevronRight } from 'lucide-react';
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
    <div ref={menuRef}>
      {/* User Menu Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`
          flex items-center justify-between w-full gap-3 px-4 py-3 rounded-lg transition-colors
          ${
            isOpen
              ? 'bg-blue-50 text-blue-700 font-medium'
              : 'text-gray-700 hover:bg-gray-100'
          }
        `}
        aria-label="User settings menu"
      >
        <div className="flex items-center gap-3">
          <User className="w-5 h-5" />
          <span>{t('company.userSettings.myAccount')}</span>
        </div>
        {isOpen ? (
          <ChevronDown className="w-4 h-4" />
        ) : (
          <ChevronRight className="w-4 h-4" />
        )}
      </button>

      {/* Submenu */}
      {isOpen && (
        <div className="ml-4 mt-1 space-y-1">
          {/* Language Selection */}
          {languages.map((language) => (
            <button
              key={language.code}
              onClick={() => handleLanguageChange(language.code)}
              className={`
                flex items-center gap-2 px-4 py-2 rounded-lg transition-colors text-sm w-full
                ${
                  currentLanguage === language.code
                    ? 'bg-blue-50 text-blue-700 font-medium'
                    : 'text-gray-600 hover:bg-gray-100'
                }
              `}
            >
              <Globe className="w-4 h-4" />
              <span>{language.name}</span>
            </button>
          ))}

          {/* Logout */}
          <button
            onClick={() => {
              setIsOpen(false);
              onLogout();
            }}
            className="flex items-center gap-2 px-4 py-2 rounded-lg transition-colors text-sm w-full text-red-600 hover:bg-red-50"
          >
            <LogOut className="w-4 h-4" />
            <span>{t('company.userSettings.logout')}</span>
          </button>
        </div>
      )}
    </div>
  );
}

