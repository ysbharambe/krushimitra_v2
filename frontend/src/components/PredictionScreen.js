import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { 
  CheckCircle, AlertTriangle, Volume2, RotateCcw, 
  ChevronDown, ChevronUp, Leaf, Droplet, Loader2
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

const PredictionScreen = ({ data, imageUrl, onReset }) => {
  const { t, i18n } = useTranslation();
  const [expandedSection, setExpandedSection] = useState(null);
  const [speaking, setSpeaking] = useState(false);
  const [translatedData, setTranslatedData] = useState(null);
  const [isTranslating, setIsTranslating] = useState(false);
  const audioRef = useRef(null);

  const { disease_name, confidence, recommendations } = translatedData || data;

  // Translate content when language changes
  useEffect(() => {
    const translateContent = async () => {
      const currentLang = i18n.language;
      
      // If English, no need to translate
      if (currentLang === 'en') {
        setTranslatedData(null);
        return;
      }

      setIsTranslating(true);
      
      try {
        const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
        
        // Translate disease name
        const diseaseResponse = await axios.post(`${apiUrl}/translate/`, {
          text: disease_name.replace(/_/g, ' '),
          source_language: 'en',
          target_language: currentLang
        });
        
        // Translate description
        let translatedDescription = data.description || '';
        if (data.description) {
          const descResponse = await axios.post(`${apiUrl}/translate/`, {
            text: data.description,
            source_language: 'en',
            target_language: currentLang
          });
          translatedDescription = descResponse.data.translated_text;
        }
        
        // Translate chemical treatment name
        const chemicalNameResponse = await axios.post(`${apiUrl}/translate/`, {
          text: recommendations.chemical.name,
          source_language: 'en',
          target_language: currentLang
        });
        
        // Translate chemical description
        const chemicalDescResponse = await axios.post(`${apiUrl}/translate/`, {
          text: recommendations.chemical.description,
          source_language: 'en',
          target_language: currentLang
        });
        
        // Translate chemical application steps
        const chemicalStepsResponse = await axios.post(`${apiUrl}/translate/`, {
          text: recommendations.chemical.application_steps,
          source_language: 'en',
          target_language: currentLang
        });
        
        // Translate organic treatment name
        const organicNameResponse = await axios.post(`${apiUrl}/translate/`, {
          text: recommendations.organic.name,
          source_language: 'en',
          target_language: currentLang
        });
        
        // Translate organic description
        const organicDescResponse = await axios.post(`${apiUrl}/translate/`, {
          text: recommendations.organic.description,
          source_language: 'en',
          target_language: currentLang
        });
        
        // Translate organic application steps
        const organicStepsResponse = await axios.post(`${apiUrl}/translate/`, {
          text: recommendations.organic.application_steps,
          source_language: 'en',
          target_language: currentLang
        });
        
        // Translate preventive measures
        let translatedPreventiveMeasures = recommendations.preventive_measures || [];
        if (recommendations.preventive_measures && recommendations.preventive_measures.length > 0) {
          const preventiveResponse = await axios.post(`${apiUrl}/translate/`, {
            text: recommendations.preventive_measures.join('. '),
            source_language: 'en',
            target_language: currentLang
          });
          translatedPreventiveMeasures = preventiveResponse.data.translated_text.split('. ').filter(t => t.trim());
        }
        
        setTranslatedData({
          disease_name: diseaseResponse.data.translated_text,
          confidence: confidence,
          description: translatedDescription,
          severity: data.severity,
          crop_type: data.crop_type,
          recommendations: {
            chemical: {
              name: chemicalNameResponse.data.translated_text,
              description: chemicalDescResponse.data.translated_text,
              application_steps: chemicalStepsResponse.data.translated_text,
              where_to_buy: recommendations.chemical.where_to_buy
            },
            organic: {
              name: organicNameResponse.data.translated_text,
              description: organicDescResponse.data.translated_text,
              application_steps: organicStepsResponse.data.translated_text,
              where_to_buy: recommendations.organic.where_to_buy
            },
            preventive_measures: translatedPreventiveMeasures
          }
        });
      } catch (error) {
        console.error('Translation error:', error);
        setTranslatedData(null);
      } finally {
        setIsTranslating(false);
      }
    };
    
    translateContent();
  }, [i18n.language, data]);

  const toggleSection = (section) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  // Map language codes to speech synthesis voices
  const getVoiceForLanguage = (lang) => {
    const voiceMap = {
      'hi': 'hi-IN',
      'mr': 'mr-IN',
      'gu': 'gu-IN',
      'ta': 'ta-IN',
      'te': 'te-IN',
      'kn': 'kn-IN',
      'bn': 'bn-IN',
      'pa': 'pa-IN',
      'ml': 'ml-IN',
      'en': 'en-IN'
    };
    return voiceMap[lang] || 'en-IN';
  };

  const speakResult = async () => {
    setSpeaking(true);
    
    try {
      // Clean disease name: replace underscores with spaces
      const cleanDiseaseName = disease_name.replace(/_/g, ' ');
      
      // Build comprehensive speech text using translated content if available
      const currentLang = i18n.language;
      let speechText = ``;
      
      // Use translated text if available
      if (translatedData && currentLang !== 'en') {
        // Add title for disease
        speechText += `${t('result.disease')}: ${translatedData.disease_name}. `;
        
        // Add confidence
        speechText += `${t('result.confidence')}: ${confidence.toFixed(1)} percent. `;
        
        // Add description with title
        if (translatedData.description) {
          speechText += `What is happening to your plant. ${translatedData.description}. `;
        }
        
        // Add chemical treatment with title
        if (translatedData.recommendations.chemical) {
          speechText += `Chemical treatment option. `;
          speechText += `Medicine name: ${translatedData.recommendations.chemical.name}. `;
          speechText += `What it does: ${translatedData.recommendations.chemical.description}. `;
          speechText += `How to use: ${translatedData.recommendations.chemical.application_steps}. `;
        }
        
        // Add organic treatment with title
        if (translatedData.recommendations.organic) {
          speechText += `Natural treatment option. `;
          speechText += `Treatment name: ${translatedData.recommendations.organic.name}. `;
          speechText += `What it does: ${translatedData.recommendations.organic.description}. `;
          speechText += `How to use: ${translatedData.recommendations.organic.application_steps}. `;
        }
        
        // Add preventive measures in translated language
        if (translatedData.recommendations.preventive_measures && translatedData.recommendations.preventive_measures.length > 0) {
          speechText += `Prevention tips: ${translatedData.recommendations.preventive_measures.join('. ')}. `;
        }
      } else {
        // English speech with clear section titles
        speechText = `Plant disease detection result. `;
        speechText += `Disease name: ${cleanDiseaseName}. `;
        
        // Add description with title
        if (data.description) {
          speechText += `What is happening to your plant. ${data.description}. `;
        }
        
        speechText += `Confidence level: ${confidence.toFixed(1)} percent. `;
        
        // Add chemical treatment with clear titles
        if (recommendations.chemical && recommendations.chemical.name) {
          speechText += `Chemical treatment option. `;
          speechText += `Medicine name: ${recommendations.chemical.name}. `;
          if (recommendations.chemical.description) {
            speechText += `What it does: ${recommendations.chemical.description}. `;
          }
          if (recommendations.chemical.application_steps) {
            speechText += `How to use: ${recommendations.chemical.application_steps}. `;
          }
          if (recommendations.chemical.where_to_buy) {
            speechText += `Where to buy: ${recommendations.chemical.where_to_buy}. `;
          }
        }
        
        // Add organic treatment with clear titles
        if (recommendations.organic && recommendations.organic.name) {
          speechText += `Natural treatment option. `;
          speechText += `Treatment name: ${recommendations.organic.name}. `;
          if (recommendations.organic.description) {
            speechText += `What it does: ${recommendations.organic.description}. `;
          }
          if (recommendations.organic.application_steps) {
            speechText += `How to use: ${recommendations.organic.application_steps}. `;
          }
        }
        
        // Add preventive measures
        if (recommendations.preventive_measures && recommendations.preventive_measures.length > 0) {
          speechText += `Prevention tips: ${recommendations.preventive_measures.join('. ')}. `;
        }
      }
      
      // Use Google Cloud TTS if available
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
      
      try {
        const ttsResponse = await axios.post(`${apiUrl}/text-to-speech/`, {
          text: speechText,
          language: currentLang,
          voice_gender: 'NEUTRAL'
        });
        
        if (ttsResponse.data.audio_content) {
          // Play the audio from base64
          const audio = new Audio(`data:audio/mp3;base64,${ttsResponse.data.audio_content}`);
          audioRef.current = audio;
          audio.onended = () => {
            setSpeaking(false);
            audioRef.current = null;
          };
          audio.onerror = () => {
            setSpeaking(false);
            audioRef.current = null;
            console.error('Audio playback failed');
          };
          await audio.play();
        }
      } catch (ttsError) {
        console.warn('Google Cloud TTS not available, using browser TTS:', ttsError);
        
        // Fallback to browser TTS
        if ('speechSynthesis' in window) {
          const utterance = new SpeechSynthesisUtterance(speechText);
          utterance.rate = 0.8;
          utterance.pitch = 1.0;
          utterance.volume = 1.0;
          
          const targetLang = getVoiceForLanguage(currentLang);
          utterance.lang = targetLang;
          
          const voices = window.speechSynthesis.getVoices();
          const langVoice = voices.find(voice => voice.lang.startsWith(currentLang)) ||
                           voices.find(voice => voice.lang.startsWith(targetLang.split('-')[0]));
          if (langVoice) {
            utterance.voice = langVoice;
          }
          
          utterance.onend = () => setSpeaking(false);
          window.speechSynthesis.speak(utterance);
        } else {
          setSpeaking(false);
        }
      }
    } catch (error) {
      console.error('TTS error:', error);
      setSpeaking(false);
    }
  };

  const stopSpeaking = () => {
    // Stop Google Cloud TTS audio if playing
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      audioRef.current = null;
    }
    
    // Stop browser TTS if playing
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    
    setSpeaking(false);
  };

  const getConfidenceColor = (conf) => {
    if (conf >= 80) return 'text-green-600';
    if (conf >= 60) return 'text-yellow-600';
    return 'text-orange-600';
  };

  const getConfidenceBgColor = (conf) => {
    if (conf >= 80) return 'bg-green-100';
    if (conf >= 60) return 'bg-yellow-100';
    return 'bg-orange-100';
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <motion.div
        className="text-center mb-8"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="inline-flex flex-col items-center gap-2 text-primary-600 mb-4">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-8 h-8" />
            <h2 className="text-3xl font-bold">{t('result.title')}</h2>
          </div>
          {isTranslating && (
            <div className="flex items-center gap-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-semibold animate-pulse">
              <Loader2 className="w-4 h-4 animate-spin" />
              Translating content...
            </div>
          )}
        </div>
      </motion.div>

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        {/* Image Preview */}
        <motion.div
          className="card"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
        >
          <img 
            src={imageUrl} 
            alt="Analyzed crop" 
            className="w-full h-64 object-cover rounded-lg shadow-md"
          />
        </motion.div>

        {/* Detection Results */}
        <motion.div
          className="card"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-600 mb-2 flex items-center gap-2">
                {t('result.disease')}
                {isTranslating && (
                  <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
                )}
              </p>
              <h3 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                <AlertTriangle className="w-6 h-6 text-orange-500" />
                {translatedData ? translatedData.disease_name : disease_name.replace(/_/g, ' ')}
              </h3>
            </div>

            <div>
              <p className="text-sm text-gray-600 mb-2">{t('result.confidence')}</p>
              <div className="flex items-center gap-3">
                <div className="flex-1 bg-gray-200 rounded-full h-3 overflow-hidden">
                  <motion.div
                    className={`h-full ${getConfidenceBgColor(confidence)}`}
                    initial={{ width: 0 }}
                    animate={{ width: `${confidence}%` }}
                    transition={{ duration: 1, delay: 0.3 }}
                  />
                </div>
                <span className={`text-xl font-bold ${getConfidenceColor(confidence)}`}>
                  {confidence.toFixed(1)}%
                </span>
              </div>
            </div>

            {/* Disease Description */}
            {(data.description || (translatedData && translatedData.description)) && (
              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                <p className="text-sm font-semibold text-blue-800 mb-1">What's happening to your plant:</p>
                <p className="text-sm text-blue-900">
                  {translatedData && translatedData.description ? translatedData.description : data.description}
                </p>
              </div>
            )}

            <div className="flex gap-3 pt-4">
              <button
                onClick={speaking ? stopSpeaking : speakResult}
                className={`flex-1 ${speaking ? 'btn-secondary' : 'btn-primary'} flex items-center justify-center gap-2`}
              >
                <Volume2 className="w-5 h-5" />
                {speaking ? 'Stop' : t('result.listen')}
              </button>
              <button
                onClick={onReset}
                className="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transition-all"
              >
                <RotateCcw className="w-5 h-5 inline mr-2" />
                {t('result.uploadAnother')}
              </button>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Recommendations */}
      <motion.div
        className="space-y-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          {t('result.recommendations')}
          {isTranslating && (
            <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
          )}
        </h3>

        {/* Chemical Treatment */}
        <div className="card border-l-4 border-l-blue-500">
          <button
            onClick={() => toggleSection('chemical')}
            className="w-full flex items-center justify-between text-left"
          >
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                <Droplet className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h4 className="text-lg font-semibold text-gray-800">
                  {t('result.chemical')}
                </h4>
                <p className="text-sm text-gray-600">
                  {translatedData ? translatedData.recommendations.chemical.name : recommendations.chemical.name}
                </p>
              </div>
            </div>
            {expandedSection === 'chemical' ? 
              <ChevronUp className="w-6 h-6 text-gray-400" /> : 
              <ChevronDown className="w-6 h-6 text-gray-400" />
            }
          </button>

          {expandedSection === 'chemical' && (
            <motion.div
              className="mt-4 pt-4 border-t border-gray-200 space-y-3"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-1">
                  {t('result.description')}
                </p>
                <p className="text-sm text-gray-600">
                  {translatedData ? translatedData.recommendations.chemical.description : recommendations.chemical.description}
                </p>
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-1">
                  {t('result.application')}
                </p>
                <p className="text-sm text-gray-600">
                  {translatedData ? translatedData.recommendations.chemical.application_steps : recommendations.chemical.application_steps}
                </p>
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-1">
                  {t('result.buy')}
                </p>
                <p className="text-sm text-gray-600">
                  {recommendations.chemical.where_to_buy}
                </p>
              </div>
            </motion.div>
          )}
        </div>

        {/* Organic Treatment */}
        <div className="card border-l-4 border-l-green-500">
          <button
            onClick={() => toggleSection('organic')}
            className="w-full flex items-center justify-between text-left"
          >
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                <Leaf className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <h4 className="text-lg font-semibold text-gray-800">
                  {t('result.organic')}
                </h4>
                <p className="text-sm text-gray-600">
                  {translatedData ? translatedData.recommendations.organic.name : recommendations.organic.name}
                </p>
              </div>
            </div>
            {expandedSection === 'organic' ? 
              <ChevronUp className="w-6 h-6 text-gray-400" /> : 
              <ChevronDown className="w-6 h-6 text-gray-400" />
            }
          </button>

          {expandedSection === 'organic' && (
            <motion.div
              className="mt-4 pt-4 border-t border-gray-200 space-y-3"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-1">
                  {t('result.description')}
                </p>
                <p className="text-sm text-gray-600">
                  {translatedData ? translatedData.recommendations.organic.description : recommendations.organic.description}
                </p>
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-1">
                  {t('result.application')}
                </p>
                <p className="text-sm text-gray-600">
                  {translatedData ? translatedData.recommendations.organic.application_steps : recommendations.organic.application_steps}
                </p>
              </div>
              {recommendations.organic.where_to_buy && (
                <div>
                  <p className="text-sm font-semibold text-gray-700 mb-1">
                    {t('result.buy')}
                  </p>
                  <p className="text-sm text-gray-600">
                    {recommendations.organic.where_to_buy}
                  </p>
                </div>
              )}
            </motion.div>
          )}
        </div>

        {/* Preventive Measures */}
        {recommendations.preventive_measures && recommendations.preventive_measures.length > 0 && (
          <div className="card border-l-4 border-l-yellow-500">
            <button
              onClick={() => toggleSection('preventive')}
              className="w-full flex items-center justify-between text-left"
            >
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-yellow-600" />
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-gray-800">
                    Prevention Tips
                  </h4>
                  <p className="text-sm text-gray-600">
                    {recommendations.preventive_measures.length} tips to prevent future problems
                  </p>
                </div>
              </div>
              {expandedSection === 'preventive' ? 
                <ChevronUp className="w-6 h-6 text-gray-400" /> : 
                <ChevronDown className="w-6 h-6 text-gray-400" />
              }
            </button>

            {expandedSection === 'preventive' && (
              <motion.div
                className="mt-4 pt-4 border-t border-gray-200"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
              >
                <ul className="space-y-2">
                  {(translatedData ? translatedData.recommendations.preventive_measures : recommendations.preventive_measures).map((measure, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <span className="text-yellow-600 mt-1">✓</span>
                      <span className="text-sm text-gray-600">{measure}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            )}
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default PredictionScreen;
