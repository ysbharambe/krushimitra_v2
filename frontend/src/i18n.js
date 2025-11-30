import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      // Homepage
      "hero.title": "AI-Powered Plant Disease Detection",
      "hero.subtitle": "Upload a photo of your crop to detect diseases instantly",
      "upload.button": "Upload Photo",
      "upload.dragdrop": "Drag & drop your image here, or click to select",
      "upload.formats": "Supports: JPG, PNG (Max 10MB)",
      "upload.processing": "Analyzing image...",
      
      // Performance Section
      "performance.title": "AI-Powered Excellence",
      "performance.subtitle": "Trusted by thousands of farmers across India",
      "performance.accuracy": "Overall Detection Accuracy",
      "performance.precision": "precision",
      "performance.description": "Our advanced AI model delivers industry-leading accuracy, ensuring reliable disease detection for your crops.",
      "performance.trainingImages": "Training Images",
      "performance.diseaseClasses": "Disease Classes",
      "performance.languages": "Languages",
      "performance.productionReady": "Production Ready",
      "performance.fastAccurate": "Fast & Accurate",
      "performance.aiPowered": "AI-Powered",
      "performance.multilingual": "Multilingual",
      
      // About Section
      "about.title": "About KrushiMitra",
      "about.description": "KrushiMitra is an AI-powered plant disease detection system designed specifically for Indian farmers. Using advanced computer vision and Google's Gemini AI, we help farmers identify crop diseases quickly and get actionable treatment recommendations in their local language.",
      "about.mission.title": "Our Mission",
      "about.mission.description": "Make crop disease detection accessible to every farmer, regardless of literacy or language barriers.",
      "about.farmers.title": "For Farmers",
      "about.farmers.description": "Simple image upload, instant results, and easy-to-understand treatment steps in your language.",
      "about.multilingual.title": "10+ Languages",
      "about.multilingual.description": "Hindi, Marathi, Gujarati, Tamil, Telugu, Kannada, Bengali, Punjabi, Malayalam & more.",
      
      // Results
      "result.title": "Detection Results",
      "result.disease": "Detected Disease",
      "result.confidence": "Confidence",
      "result.recommendations": "Treatment Recommendations",
      "result.chemical": "Chemical Treatment",
      "result.organic": "Organic Treatment",
      "result.name": "Name",
      "result.description": "Description",
      "result.application": "Application Steps",
      "result.buy": "Where to Buy",
      "result.listen": "Listen to Result",
      "result.uploadAnother": "Upload Another Photo",
      
      // Language
      "language.select": "Select Language",
      
      // Admin
      "admin.title": "Admin Panel",
      "admin.retrain": "Retrain Model",
      "admin.status": "Model Status",
      "admin.history": "Retraining History",
      "admin.back": "Back to Home",
      
      // Common
      "loading": "Loading...",
      "error": "Error occurred",
      "success": "Success"
    }
  },
  hi: {
    translation: {
      "hero.title": "एआई-संचालित पौधों की बीमारी का पता लगाना",
      "hero.subtitle": "तुरंत बीमारियों का पता लगाने के लिए अपनी फसल की फोटो अपलोड करें",
      "upload.button": "फोटो अपलोड करें",
      "upload.dragdrop": "अपनी छवि यहाँ खींचें और छोड़ें, या चुनने के लिए क्लिक करें",
      "upload.formats": "समर्थित: JPG, PNG (अधिकतम 10MB)",
      "upload.processing": "छवि का विश्लेषण कर रहे हैं...",
      
      "performance.title": "एआई-संचालित उत्कृष्टता",
      "performance.subtitle": "भारत भर के हजारों किसानों द्वारा विश्वसनीय",
      "performance.accuracy": "समग्र पहचान सटीकता",
      "performance.precision": "सटीकता",
      "performance.description": "हमारा उन्नत एआई मॉडल उद्योग-अग्रणी सटीकता प्रदान करता है, आपकी फसलों के लिए विश्वसनीय रोग पहचान सुनिश्चित करता है।",
      "performance.trainingImages": "प्रशिक्षण छवियां",
      "performance.diseaseClasses": "रोग वर्ग",
      "performance.languages": "भाषाएं",
      "performance.productionReady": "उत्पादन तैयार",
      "performance.fastAccurate": "तेज और सटीक",
      "performance.aiPowered": "एआई-संचालित",
      "performance.multilingual": "बहुभाषी",
      
      "about.title": "कृषिमित्र के बारे में",
      "about.description": "कृषिमित्र भारतीय किसानों के लिए विशेष रूप से डिज़ाइन किया गया एक एआई-संचालित पौधे की बीमारी पहचान प्रणाली है। उन्नत कंप्यूटर विज़न और Google के Gemini AI का उपयोग करते हुए, हम किसानों को फसल रोगों की तुरंत पहचान करने और उनकी स्थानीय भाषा में कार्रवाई योग्य उपचार सिफारिशें प्राप्त करने में मदद करते हैं।",
      "about.mission.title": "हमारा मिशन",
      "about.mission.description": "साक्षरता या भाषा बाधाओं की परवाह किए बिना, हर किसान के लिए फसल रोग पहचान को सुलभ बनाना।",
      "about.farmers.title": "किसानों के लिए",
      "about.farmers.description": "सरल छवि अपलोड, तत्काल परिणाम, और आपकी भाषा में समझने में आसान उपचार कदम।",
      "about.multilingual.title": "10+ भाषाएं",
      "about.multilingual.description": "हिंदी, मराठी, गुजराती, तमिल, तेलुगु, कन्नड़, बंगाली, पंजाबी, मलयालम और अधिक।",
      
      "result.title": "पहचान परिणाम",
      "result.disease": "पहचानी गई बीमारी",
      "result.confidence": "विश्वास",
      "result.recommendations": "उपचार सिफारिशें",
      "result.chemical": "रासायनिक उपचार",
      "result.organic": "जैविक उपचार",
      "result.name": "नाम",
      "result.description": "विवरण",
      "result.application": "आवेदन के चरण",
      "result.buy": "कहाँ से खरीदें",
      "result.listen": "परिणाम सुनें",
      "result.uploadAnother": "दूसरी फोटो अपलोड करें",
      
      "language.select": "भाषा चुनें",
      
      "loading": "लोड हो रहा है...",
      "error": "त्रुटि हुई",
      "success": "सफलता"
    }
  },
  mr: {
    translation: {
      "hero.title": "एआय-आधारित वनस्पती रोग शोध",
      "hero.subtitle": "रोगांचा त्वरित शोध घेण्यासाठी आपल्या पिकाचा फोटो अपलोड करा",
      "upload.button": "फोटो अपलोड करा",
      "upload.dragdrop": "तुमची प्रतिमा येथे ड्रॅग आणि ड्रॉप करा, किंवा निवडण्यासाठी क्लिक करा",
      "upload.formats": "समर्थित: JPG, PNG (कमाल 10MB)",
      "upload.processing": "प्रतिमेचे विश्लेषण करत आहे...",
      
      "performance.title": "एआय-आधारित उत्कृष्टता",
      "performance.subtitle": "भारतातील हजारो शेतकऱ्यांचा विश्वास",
      "performance.accuracy": "एकूण शोध अचूकता",
      "performance.precision": "अचूकता",
      "performance.description": "आमचे प्रगत एआय मॉडेल उद्योग-अग्रणी अचूकता प्रदान करते, तुमच्या पिकांसाठी विश्वसनीय रोग शोध सुनिश्चित करते.",
      "performance.trainingImages": "प्रशिक्षण प्रतिमा",
      "performance.diseaseClasses": "रोग वर्ग",
      "performance.languages": "भाषा",
      "performance.productionReady": "उत्पादन तयार",
      "performance.fastAccurate": "जलद आणि अचूक",
      "performance.aiPowered": "एआय-आधारित",
      "performance.multilingual": "बहुभाषिक",
      
      "about.title": "कृषिमित्र बद्दल",
      "about.description": "कृषिमित्र ही भारतीय शेतकऱ्यांसाठी विशेषतः डिझाइन केलेली एआय-आधारित वनस्पती रोग शोध प्रणाली आहे. प्रगत संगणक दृष्टी आणि Google च्या Gemini AI चा वापर करून, आम्ही शेतकऱ्यांना पीक रोगांची त्वरित ओळख करण्यात आणि त्यांच्या स्थानिक भाषेत कार्यवाही योग्य उपचार शिफारसी मिळवण्यात मदत करतो.",
      "about.mission.title": "आमचे ध्येय",
      "about.mission.description": "साक्षरता किंवा भाषा अडथळ्यांची पर्वा न करता, प्रत्येक शेतकऱ्यासाठी पीक रोग शोध सुलभ करणे.",
      "about.farmers.title": "शेतकऱ्यांसाठी",
      "about.farmers.description": "सोपे प्रतिमा अपलोड, त्वरित निकाल, आणि तुमच्या भाषेत समजण्यास सोपे उपचार चरण.",
      "about.multilingual.title": "10+ भाषा",
      "about.multilingual.description": "हिंदी, मराठी, गुजराती, तमिळ, तेलुगु, कन्नड, बंगाली, पंजाबी, मल्याळम आणि अधिक.",
      
      "result.title": "शोध परिणाम",
      "result.disease": "ओळखला गेलेला रोग",
      "result.confidence": "विश्वास",
      "result.recommendations": "उपचार शिफारसी",
      "result.chemical": "रासायनिक उपचार",
      "result.organic": "सेंद्रिय उपचार",
      "result.name": "नाव",
      "result.description": "वर्णन",
      "result.application": "अर्ज चरण",
      "result.buy": "कुठे खरेदी करावे",
      "result.listen": "परिणाम ऐका",
      "result.uploadAnother": "दुसरा फोटो अपलोड करा",
      
      "language.select": "भाषा निवडा"
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
