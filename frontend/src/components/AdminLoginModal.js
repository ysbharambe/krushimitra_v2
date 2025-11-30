import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Lock, Loader2, AlertCircle } from 'lucide-react';
import axios from 'axios';

const AdminLoginModal = ({ isOpen, onClose, onLoginSuccess }) => {
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
      const response = await axios.post(`${apiUrl}/admin/login/`, { password });

      if (response.data.success) {
        // Store token in localStorage
        localStorage.setItem('adminToken', response.data.token);
        onLoginSuccess();
        setPassword('');
        onClose();
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
        <motion.div
          className="bg-white rounded-lg shadow-xl max-w-md w-full p-6"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
        >
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              <Lock className="w-6 h-6 text-primary-600" />
              Admin Login
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Admin Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter admin password"
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                autoFocus
              />
            </div>

            {error && (
              <motion.div
                className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-center gap-2"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
                <p className="text-sm text-red-700">{error}</p>
              </motion.div>
            )}

            <button
              type="submit"
              disabled={loading || !password}
              className={`w-full btn-primary flex items-center justify-center gap-2 ${
                loading || !password ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Verifying...
                </>
              ) : (
                <>
                  <Lock className="w-5 h-5" />
                  Login
                </>
              )}
            </button>
          </form>

          <p className="text-xs text-gray-500 text-center mt-4">
            Admin access is protected. Contact the administrator if you need access.
          </p>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default AdminLoginModal;
