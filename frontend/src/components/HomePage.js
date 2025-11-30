import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { Upload, Loader, Image as ImageIcon, Leaf, Info, Target, Users, Globe, Award, Zap, CheckCircle, ShieldCheck } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { uploadToCloudinary, predictDisease } from '../services/api';
import FeedbackForm from './FeedbackForm';

const HomePage = ({ onPredictionComplete }) => {
  const { t } = useTranslation();
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [preview, setPreview] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setError(null);
    
    // Create preview
    const reader = new FileReader();
    reader.onload = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(file);

    setUploading(true);

    try {
      // Upload to Cloudinary
      const imageUrl = await uploadToCloudinary(file);
      
      // Get prediction
      const prediction = await predictDisease(imageUrl);
      
      // Pass results to parent
      onPredictionComplete(prediction, imageUrl);
    } catch (err) {
      setError(err.detail || err.message || 'Failed to process image');
      setUploading(false);
    }
  }, [onPredictionComplete]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxSize: 10485760, // 10MB
    multiple: false,
    disabled: uploading
  });

  return (
    <div className="max-w-4xl mx-auto relative">
      {/* Animated Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
        <div className="absolute top-20 left-10 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      {/* Hero Section */}
      <motion.div
        className="text-center mb-12 relative"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <motion.div
          className="inline-block mb-6 relative"
          animate={{ 
            rotate: [0, 10, -10, 10, 0],
            scale: [1, 1.1, 1, 1.1, 1]
          }}
          transition={{ duration: 3, repeat: Infinity, repeatDelay: 2 }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-green-400 to-blue-500 rounded-full blur-2xl opacity-30 animate-pulse"></div>
          <Leaf className="w-20 h-20 text-primary-600 mx-auto relative z-10 drop-shadow-lg" />
        </motion.div>
        
        <motion.h2 
          className="text-4xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-green-600 via-blue-600 to-purple-600 bg-clip-text text-transparent"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          {t('hero.title')}
        </motion.h2>
        <motion.p 
          className="text-xl md:text-2xl text-gray-600 mb-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          {t('hero.subtitle')}
        </motion.p>
        
        {/* Decorative line */}
        <motion.div
          className="w-24 h-1 bg-gradient-to-r from-green-500 to-blue-500 mx-auto rounded-full"
          initial={{ width: 0 }}
          animate={{ width: 96 }}
          transition={{ delay: 0.6, duration: 0.8 }}
        ></motion.div>
      </motion.div>


      {/* Model Performance - Marketing Style */}
      <motion.div
        className="relative overflow-hidden bg-gradient-to-br from-green-50 via-blue-50 to-purple-50 rounded-2xl p-8 mt-8 border border-green-200 shadow-xl"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        {/* Background decoration */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-green-200 to-blue-200 rounded-full filter blur-3xl opacity-30 -mr-32 -mt-32"></div>
        
        <div className="relative">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
            <div className="flex items-center gap-3">
              <div className="w-14 h-14 bg-gradient-to-br from-green-500 to-blue-500 rounded-xl flex items-center justify-center shadow-lg">
                <Award className="w-8 h-8 text-white" />
              </div>
              <div>
                <h3 className="text-3xl font-bold bg-gradient-to-r from-green-700 to-blue-700 bg-clip-text text-transparent">
                  {t('performance.title')}
                </h3>
                <p className="text-sm text-gray-600">{t('performance.subtitle')}</p>
              </div>
            </div>
          </div>

          {/* Main accuracy display */}
          <div className="bg-white/80 backdrop-blur rounded-2xl p-8 mb-6 shadow-lg">
            <div className="grid md:grid-cols-2 gap-8 items-center">
              <div>
                <p className="text-sm text-gray-600 mb-2 uppercase tracking-wide font-semibold">{t('performance.accuracy')}</p>
                <div className="flex items-baseline gap-3 mb-4">
                  <span className="text-6xl md:text-7xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                    92.5%
                  </span>
                  <span className="text-2xl text-gray-500 font-medium">{t('performance.precision')}</span>
                </div>
                <p className="text-gray-600 text-sm">
                  {t('performance.description')}
                </p>
              </div>
              
              <div className="flex justify-center">
                <div className="w-48 h-48 relative">
                  <svg className="w-full h-full transform -rotate-90">
                    <circle
                      cx="96"
                      cy="96"
                      r="80"
                      stroke="#e5e7eb"
                      strokeWidth="12"
                      fill="none"
                    />
                    <circle
                      cx="96"
                      cy="96"
                      r="80"
                      stroke="url(#gradient)"
                      strokeWidth="12"
                      fill="none"
                      strokeDasharray="502.4"
                      strokeDashoffset={502.4 - (502.4 * 92.5) / 100}
                      strokeLinecap="round"
                      className="transition-all duration-1000"
                    />
                    <defs>
                      <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#10b981" />
                        <stop offset="100%" stopColor="#3b82f6" />
                      </linearGradient>
                    </defs>
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center flex-col">
                    <Zap className="w-12 h-12 text-yellow-500 mb-2" />
                    <span className="text-2xl font-bold text-gray-800">92.5%</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="mt-6 h-5 bg-gray-200 rounded-full overflow-hidden shadow-inner">
              <motion.div 
                className="h-full bg-gradient-to-r from-green-500 via-blue-500 to-purple-500 rounded-full shadow-lg relative overflow-hidden"
                initial={{ width: 0 }}
                animate={{ width: '92.5%' }}
                transition={{ duration: 2, delay: 0.7 }}
              >
                <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
              </motion.div>
            </div>
          </div>

          {/* Stats grid */}
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="bg-white/70 backdrop-blur rounded-xl p-6 text-center hover:bg-white/90 transition-all shadow-md hover:shadow-xl hover:scale-105 duration-300">
              <div className="text-4xl font-bold text-green-600 mb-2">1.5L+</div>
              <div className="text-sm text-gray-600 font-medium">{t('performance.trainingImages')}</div>
            </div>
            <div className="bg-white/70 backdrop-blur rounded-xl p-6 text-center hover:bg-white/90 transition-all shadow-md hover:shadow-xl hover:scale-105 duration-300">
              <div className="text-4xl font-bold text-blue-600 mb-2">38+</div>
              <div className="text-sm text-gray-600 font-medium">{t('performance.diseaseClasses')}</div>
            </div>
            <div className="bg-white/70 backdrop-blur rounded-xl p-6 text-center hover:bg-white/90 transition-all shadow-md hover:shadow-xl hover:scale-105 duration-300">
              <div className="text-4xl font-bold text-purple-600 mb-2">10+</div>
              <div className="text-sm text-gray-600 font-medium">{t('performance.languages')}</div>
            </div>
          </div>

          {/* Achievement badges */}
          <div className="flex flex-wrap gap-3 justify-center">
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-full text-sm font-semibold shadow-sm">
              <CheckCircle className="w-4 h-4" />
              {t('performance.productionReady')}
            </span>
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold shadow-sm">
              <Zap className="w-4 h-4" />
              {t('performance.fastAccurate')}
            </span>
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-semibold shadow-sm">
              <Award className="w-4 h-4" />
              {t('performance.aiPowered')}
            </span>
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-orange-100 text-orange-700 rounded-full text-sm font-semibold shadow-sm">
              <Globe className="w-4 h-4" />
              {t('performance.multilingual')}
            </span>
          </div>
        </div>
      </motion.div>

      {/* About Project Section */}
      <motion.div
        className="relative mt-12 overflow-hidden"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        {/* Gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-green-100 via-white to-blue-100 rounded-2xl opacity-50"></div>
        
        <div className="card relative border-2 border-green-200">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-blue-500 rounded-xl flex items-center justify-center shadow-lg animate-glow-pulse">
              <Info className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-3xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
              {t('about.title')}
            </h3>
          </div>
          
          <p className="text-gray-700 leading-relaxed mb-6 text-lg">
            {t('about.description')}
          </p>
          
          <div className="grid md:grid-cols-3 gap-6">
            <motion.div 
              className="group relative overflow-hidden bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border-2 border-green-200 hover:border-green-400 transition-all duration-300 hover:shadow-xl hover:scale-105"
              whileHover={{ y: -5 }}
            >
              <div className="absolute top-0 right-0 w-20 h-20 bg-green-200 rounded-full -mr-10 -mt-10 opacity-50"></div>
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center flex-shrink-0 mb-4 shadow-md">
                  <Target className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-bold text-gray-800 mb-2 text-lg">{t('about.mission.title')}</h4>
                <p className="text-sm text-gray-700">
                  {t('about.mission.description')}
                </p>
              </div>
            </motion.div>
            
            <motion.div 
              className="group relative overflow-hidden bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border-2 border-blue-200 hover:border-blue-400 transition-all duration-300 hover:shadow-xl hover:scale-105"
              whileHover={{ y: -5 }}
            >
              <div className="absolute top-0 right-0 w-20 h-20 bg-blue-200 rounded-full -mr-10 -mt-10 opacity-50"></div>
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center flex-shrink-0 mb-4 shadow-md">
                  <Users className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-bold text-gray-800 mb-2 text-lg">{t('about.farmers.title')}</h4>
                <p className="text-sm text-gray-700">
                  {t('about.farmers.description')}
                </p>
              </div>
            </motion.div>
            
            <motion.div 
              className="group relative overflow-hidden bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl border-2 border-purple-200 hover:border-purple-400 transition-all duration-300 hover:shadow-xl hover:scale-105"
              whileHover={{ y: -5 }}
            >
              <div className="absolute top-0 right-0 w-20 h-20 bg-purple-200 rounded-full -mr-10 -mt-10 opacity-50"></div>
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center flex-shrink-0 mb-4 shadow-md">
                  <Globe className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-bold text-gray-800 mb-2 text-lg">{t('about.multilingual.title')}</h4>
                <p className="text-sm text-gray-700">
                  {t('about.multilingual.description')}
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* Upload Section - Try It Now! */}
      <motion.div
        className="relative mt-12"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        {/* Glow effect behind card */}
        <div className="absolute -inset-1 bg-gradient-to-r from-green-500 via-blue-500 to-purple-500 rounded-2xl blur-lg opacity-30 group-hover:opacity-50 transition duration-300"></div>
        
        <div className="card relative bg-white">
          <div
            {...getRootProps()}
            className={`
              border-3 border-dashed rounded-xl p-12 text-center cursor-pointer
              transition-all duration-300 relative overflow-hidden
              ${isDragActive ? 'border-primary-500 bg-gradient-to-br from-primary-50 to-blue-50 scale-105' : 'border-gray-300 hover:border-primary-400 hover:bg-gradient-to-br hover:from-gray-50 hover:to-green-50'}
              ${uploading ? 'opacity-50 cursor-not-allowed' : ''}
            `}
          >
            {/* Animated border on hover */}
            <div className="absolute inset-0 border-2 border-transparent hover:border-gradient rounded-xl"></div>
          <input {...getInputProps()} />
          
          {!preview && !uploading && (
            <>
              <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-lg font-semibold text-gray-700 mb-2">
                {isDragActive ? 'Drop the image here' : t('upload.button')}
              </p>
              <p className="text-sm text-gray-500 mb-4">
                {t('upload.dragdrop')}
              </p>
              <p className="text-xs text-gray-400">
                {t('upload.formats')}
              </p>
            </>
          )}

          {preview && !uploading && (
            <div className="space-y-4">
              <img 
                src={preview} 
                alt="Preview" 
                className="max-h-64 mx-auto rounded-lg shadow-md"
              />
              <p className="text-sm text-gray-600">
                Click to upload a different image
              </p>
            </div>
          )}

          {uploading && (
            <div className="space-y-4">
              {preview && (
                <img 
                  src={preview} 
                  alt="Preview" 
                  className="max-h-64 mx-auto rounded-lg shadow-md opacity-50"
                />
              )}
              <div className="flex items-center justify-center gap-3">
                <Loader className="w-8 h-8 text-primary-600 animate-spin" />
                <p className="text-lg font-semibold text-primary-600">
                  {t('upload.processing')}
                </p>
              </div>
            </div>
          )}
          </div>
        </div>

        {error && (
          <motion.div
            className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <p className="text-red-700 text-sm">{error}</p>
          </motion.div>
        )}
      </motion.div>

      {/* Feedback Form */}
      <FeedbackForm />
    </div>
  );
};

export default HomePage;
