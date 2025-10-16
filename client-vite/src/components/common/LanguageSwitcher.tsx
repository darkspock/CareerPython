import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Globe, ChevronUp } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { api } from '../../lib/api';

interface Language {
  code: string;
  name: string;
  flag: string;
}

const languages: Language[] = [
  { code: 'es', name: 'Español', flag: '🇪🇸' },
  { code: 'en', name: 'English', flag: '🇺🇸' },
];

const LanguageSwitcher: React.FC = () => {
  const { i18n, t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [isLoadingPreference, setIsLoadingPreference] = useState(false);

  const currentLanguage = languages.find(lang => lang.code === i18n.language) || languages[0];

  // Load user's language preference from database on component mount
  useEffect(() => {
    const loadUserLanguagePreference = async () => {
      // Only try to load from database if user might be authenticated
      const token = localStorage.getItem('access_token');
      if (!token) {
        return; // Use i18n default detection
      }

      try {
        setIsLoadingPreference(true);
        const response = await api.getUserLanguagePreference();
        const preferredLanguage = response.preferred_language;

        if (preferredLanguage && preferredLanguage !== i18n.language) {
          console.log('Loading user language preference from database:', preferredLanguage);
          await i18n.changeLanguage(preferredLanguage);
          // Also update localStorage to keep in sync
          localStorage.setItem('preferredLanguage', preferredLanguage);
          localStorage.setItem('i18nextLng', preferredLanguage);
        }
      } catch (error) {
        console.warn('Failed to load user language preference from database:', error);
        // Fallback to localStorage/browser detection which i18n already handles
      } finally {
        setIsLoadingPreference(false);
      }
    };

    loadUserLanguagePreference();
  }, [i18n]);

  const handleLanguageChange = async (languageCode: string) => {
    try {
      await i18n.changeLanguage(languageCode);

      // Save language preference to user profile in database
      try {
        await api.updateUserLanguagePreference(languageCode);
        console.log('Language preference saved to database:', languageCode);
      } catch (apiError) {
        console.warn('Failed to save language preference to database:', apiError);
        // Continue anyway - localStorage will work as fallback
      }

      // Also save in localStorage as fallback
      localStorage.setItem('preferredLanguage', languageCode);
      localStorage.setItem('i18nextLng', languageCode);

      console.log('Language changed to:', languageCode);
      setIsOpen(false);

      // No need to reload now that localStorage detection is working
    } catch (error) {
      console.error('Failed to change language:', error);
    }
  };

  return (
    <div className="fixed bottom-4 left-4 z-50">
      <div className="relative">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2 px-3 py-2 bg-white border border-gray-200 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 text-sm font-medium text-gray-700 hover:bg-gray-50"
          aria-label={t('language.selectLanguage')}
        >
          <span className="text-lg">{currentLanguage.flag}</span>
          <span>{currentLanguage.name}</span>
          <ChevronUp
            className={`w-4 h-4 transition-transform duration-200 ${
              isOpen ? 'rotate-180' : 'rotate-0'
            }`}
          />
        </button>

        <AnimatePresence>
          {isOpen && (
            <motion.div
              initial={{ opacity: 0, y: 10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 10, scale: 0.95 }}
              transition={{ duration: 0.15 }}
              className="absolute bottom-full left-0 mb-2 w-48 bg-white border border-gray-200 rounded-lg shadow-xl overflow-hidden"
            >
              <div className="py-1">
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
                    <span className="text-lg">{language.flag}</span>
                    <span>{language.name}</span>
                    {i18n.language === language.code && (
                      <div className="ml-auto w-2 h-2 bg-blue-600 rounded-full"></div>
                    )}
                  </button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Click outside to close */}
      {isOpen && (
        <div
          className="fixed inset-0 -z-10"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};

export default LanguageSwitcher;