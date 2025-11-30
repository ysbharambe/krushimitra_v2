import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import HomePage from './components/HomePage';
import PredictionScreen from './components/PredictionScreen';
import AdminPanel from './components/AdminPanel';
import AdminLoginModal from './components/AdminLoginModal';
import LanguageSelector from './components/LanguageSelector';
import { Sprout, Shield } from 'lucide-react';

function App() {
  const [currentScreen, setCurrentScreen] = useState('home'); // 'home', 'prediction', 'admin'
  const [predictionData, setPredictionData] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [isAdminAuthenticated, setIsAdminAuthenticated] = useState(false);
  const [showAdminLogin, setShowAdminLogin] = useState(false);

  // Check if admin is already authenticated
  useEffect(() => {
    const token = localStorage.getItem('adminToken');
    if (token === 'admin_authenticated') {
      setIsAdminAuthenticated(true);
    }
  }, []);

  const handlePredictionComplete = (data, imgUrl) => {
    setPredictionData(data);
    setImageUrl(imgUrl);
    setCurrentScreen('prediction');
  };

  const handleReset = () => {
    setPredictionData(null);
    setImageUrl(null);
    setCurrentScreen('home');
  };

  const handleAdminLogin = () => {
    setShowAdminLogin(true);
  };

  const handleLoginSuccess = () => {
    setIsAdminAuthenticated(true);
    setCurrentScreen('admin');
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-md sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <motion.div 
            className="flex items-center gap-3 cursor-pointer"
            onClick={handleReset}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Sprout className="text-primary-600 w-8 h-8" />
            <h1 className="text-2xl font-bold text-primary-700">
              KrushiMitra
            </h1>
          </motion.div>
          
          <div className="flex items-center gap-4">
            <LanguageSelector />
            <motion.button
              onClick={handleAdminLogin}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Shield className="w-5 h-5 text-gray-600" />
              <span className="text-gray-600">Admin</span>
            </motion.button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <AnimatePresence mode="wait">
          {currentScreen === 'home' && (
            <motion.div
              key="home"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <HomePage onPredictionComplete={handlePredictionComplete} />
            </motion.div>
          )}

          {currentScreen === 'prediction' && predictionData && (
            <motion.div
              key="prediction"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <PredictionScreen 
                data={predictionData}
                imageUrl={imageUrl}
                onReset={handleReset}
              />
            </motion.div>
          )}

          {currentScreen === 'admin' && isAdminAuthenticated && (
            <motion.div
              key="admin"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <AdminPanel onBack={handleReset} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Admin Login Modal */}
        <AdminLoginModal 
          isOpen={showAdminLogin}
          onClose={() => setShowAdminLogin(false)}
          onLoginSuccess={handleLoginSuccess}
        />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="text-center md:text-left text-gray-600">
              <p className="text-sm">
                © 2025 KrushiMitra - Empowering Farmers with AI Technology
              </p>
              <p className="text-xs mt-1 text-gray-500">
                Made with ❤️ for Indian Farmers
              </p>
            </div>
            {!isAdminAuthenticated && currentScreen !== 'admin' && (
              <button
                onClick={handleAdminLogin}
                className="flex items-center gap-2 px-4 py-2 text-sm text-gray-600 hover:text-primary-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <Shield className="w-4 h-4" />
                Admin Login
              </button>
            )}
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
