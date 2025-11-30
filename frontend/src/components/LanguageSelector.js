import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Globe, ChevronDown } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { getSupportedLanguages } from '../services/api';

const LanguageSelector = () => {
  const { i18n } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [languages, setLanguages] = useState({
    en: 'English',
    hi: 'Hindi',
    mr: 'Marathi',
    gu: 'Gujarati',
    ta: 'Tamil',
    te: 'Telugu',
    kn: 'Kannada',
    bn: 'Bengali'
  });

  useEffect(() => {
    // Fetch supported languages from backend
    getSupportedLanguages().then(langs => {
      if (langs && Object.keys(langs).length > 0) {
        setLanguages(langs);
      }
    }).catch(err => {
      console.error('Failed to load languages:', err);
    });
  }, []);

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    setIsOpen(false);
  };

  const currentLanguage = languages[i18n.language] || 'English';

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-white border-2 border-gray-200 rounded-lg hover:border-primary-500 transition-colors"
      >
        <Globe className="w-5 h-5 text-primary-600" />
        <span className="text-sm font-medium text-gray-700">
          {currentLanguage}
        </span>
        <ChevronDown className={`w-4 h-4 text-gray-500 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="absolute right-0 mt-2 w-48 bg-white border-2 border-gray-200 rounded-lg shadow-xl z-50 overflow-hidden"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            <div className="py-2">
              {Object.entries(languages).map(([code, name]) => (
                <button
                  key={code}
                  onClick={() => changeLanguage(code)}
                  className={`
                    w-full text-left px-4 py-2 text-sm transition-colors
                    ${i18n.language === code 
                      ? 'bg-primary-50 text-primary-700 font-semibold' 
                      : 'text-gray-700 hover:bg-gray-50'
                    }
                  `}
                >
                  {name}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};

export default LanguageSelector;
