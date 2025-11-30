import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Cloudinary configuration
const CLOUDINARY_UPLOAD_URL = process.env.REACT_APP_CLOUDINARY_UPLOAD_URL || 
  'https://api.cloudinary.com/v1_1/YOUR_CLOUD_NAME/image/upload';
const CLOUDINARY_UPLOAD_PRESET = process.env.REACT_APP_CLOUDINARY_UPLOAD_PRESET || 'krushimitra';

export const uploadToCloudinary = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('upload_preset', CLOUDINARY_UPLOAD_PRESET);
  formData.append('folder', 'krushimitra');

  try {
    const response = await axios.post(CLOUDINARY_UPLOAD_URL, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data.secure_url;
  } catch (error) {
    console.error('Cloudinary upload error:', error);
    throw new Error('Failed to upload image');
  }
};

export const predictDisease = async (imageUrl) => {
  try {
    const response = await api.post('/predict/', {
      image_url: imageUrl,
    });
    return response.data;
  } catch (error) {
    console.error('Prediction error:', error);
    throw error.response?.data || error;
  }
};

export const translateText = async (text, targetLanguage, sourceLanguage = 'en') => {
  try {
    const response = await api.post('/translate/', {
      text,
      target_language: targetLanguage,
      source_language: sourceLanguage,
    });
    return response.data.translated_text;
  } catch (error) {
    console.error('Translation error:', error);
    return text; // Return original text if translation fails
  }
};

export const translateBulk = async (texts, targetLanguage, sourceLanguage = 'en') => {
  try {
    const response = await api.post('/translate/bulk/', {
      texts,
      target_language: targetLanguage,
      source_language: sourceLanguage,
    });
    return response.data.translated_texts;
  } catch (error) {
    console.error('Bulk translation error:', error);
    return texts; // Return original texts if translation fails
  }
};

export const getSupportedLanguages = async () => {
  try {
    const response = await api.get('/languages/');
    return response.data.supported_languages;
  } catch (error) {
    console.error('Get languages error:', error);
    return {};
  }
};

export const triggerRetraining = async () => {
  try {
    const response = await api.post('/retrain/');
    return response.data;
  } catch (error) {
    console.error('Retraining error:', error);
    throw error.response?.data || error;
  }
};

export const getRetrainingStatus = async () => {
  try {
    const response = await api.get('/retrain/status/');
    return response.data;
  } catch (error) {
    console.error('Get retrain status error:', error);
    throw error.response?.data || error;
  }
};

export const getModelInfo = async () => {
  try {
    const response = await api.get('/model-info/');
    return response.data;
  } catch (error) {
    console.error('Get model info error:', error);
    throw error.response?.data || error;
  }
};

export default api;
