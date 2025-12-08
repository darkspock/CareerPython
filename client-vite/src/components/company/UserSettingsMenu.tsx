import { useState, useEffect } from 'react';
import { User, LogOut, Globe, ChevronDown, ChevronRight } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { api } from '../../lib/api';
import { Button } from '@/components/ui/button';

interface UserSettingsMenuProps {
  onLogout: () => void;
}

export default function UserSettingsMenu({ onLogout }: UserSettingsMenuProps) {
  const { i18n, t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState(i18n.language || 'es');

  const languages = [
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'en', name: 'English', flag: '🇺🇸' },
  ];

  // Load user's language preference on mount
  useEffect(() => {
    const loadUserLanguagePreference = async () => {
      // Only try to load from database if user might be authenticated
      const token = localStorage.getItem('access_token');
      if (!token) {
        // Use i18n default detection
        setCurrentLanguage(i18n.language);
        return;
      }

      try {
        const response = await api.getUserLanguagePreference() as { preferred_language?: string; language_code?: string };
        const preferredLanguage = response.preferred_language || response.language_code;

        if (preferredLanguage && preferredLanguage !== i18n.language) {
          await i18n.changeLanguage(preferredLanguage);
          setCurrentLanguage(preferredLanguage);
        } else {
          setCurrentLanguage(i18n.language);
        }
      } catch (error: any) {
        // Silently handle errors - token might be expired or user not authenticated
        // Fallback to localStorage/browser detection which i18n already handles
        setCurrentLanguage(i18n.language);
      }
    };

    loadUserLanguagePreference();
  }, [i18n]);

  const handleLanguageChange = async (languageCode: string) => {
    try {
      await i18n.changeLanguage(languageCode);
      setCurrentLanguage(languageCode);

      // Save language preference to user profile in database (only if authenticated)
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          await api.updateUserLanguagePreference(languageCode);
        } catch (apiError: any) {
          // Silently fail - token might be expired or user not authenticated
          // Language preference is still saved to localStorage as fallback
        }
      }

      // Also save in localStorage as fallback
      localStorage.setItem('preferredLanguage', languageCode);
      localStorage.setItem('i18nextLng', languageCode);

      setIsOpen(false);
    } catch (error) {
      console.error('Failed to change language:', error);
    }
  };

  return (
    <div>
      {/* User Menu Button */}
      <Button
        onClick={() => setIsOpen(!isOpen)}
        variant="ghost"
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
      </Button>

      {/* Submenu */}
      {isOpen && (
        <div className="ml-4 mt-1 space-y-1">
          {/* Language Selection */}
          {languages.map((language) => (
            <Button
              key={language.code}
              onClick={() => handleLanguageChange(language.code)}
              variant="ghost"
              className={`
                flex items-center gap-2 px-4 py-2 rounded-lg transition-colors text-sm w-full justify-start
                ${
                  currentLanguage === language.code
                    ? 'bg-blue-50 text-blue-700 font-medium'
                    : 'text-gray-600 hover:bg-gray-100'
                }
              `}
            >
              <Globe className="w-4 h-4" />
              <span>{language.name}</span>
            </Button>
          ))}

          {/* Logout */}
          <Button
            onClick={() => {
              setIsOpen(false);
              onLogout();
            }}
            variant="ghost"
            className="flex items-center gap-2 px-4 py-2 rounded-lg transition-colors text-sm w-full justify-start text-red-600 hover:bg-red-50 hover:text-red-600"
          >
            <LogOut className="w-4 h-4" />
            <span>{t('company.userSettings.logout')}</span>
          </Button>
        </div>
      )}
    </div>
  );
}
