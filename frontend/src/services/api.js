import axios from 'axios';
import { toast } from 'react-toastify';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor - Add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      // Clear tokens and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
      
      toast.error('Session expired. Please login again.');
      return Promise.reject(error);
    }

    // Handle network errors
    if (!error.response) {
      toast.error('Network error. Please check your connection.');
      return Promise.reject(error);
    }

    // Handle other errors
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        'An error occurred';
    
    toast.error(errorMessage);
    return Promise.reject(error);
  }
);

// API Methods

export const authAPI = {
  sendOTP: (phone, countryCode, purpose = 'registration') =>
    api.post('/auth/send-otp', { phone, country_code: countryCode, purpose }),

  verifyOTP: (phone, countryCode, otp, purpose = 'registration') =>
    api.post('/auth/verify-otp', {
      phone,
      country_code: countryCode,
      otp_code: otp,
      purpose,
    }),
};

export const farmAPI = {
  createFarm: (farmData) => 
    api.post('/farm/create', farmData),
  
  getUserFarms: () => 
    api.get('/farm/farms'),
  
  uploadSHC: (farmId, file) => {
    const formData = new FormData();
    formData.append('farm_id', farmId);
    formData.append('file', file);
    
    return api.post('/farm/upload_shc', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  verifySHC: (shcId, shcData) => 
    api.put(`/farm/verify_shc/${shcId}`, shcData),
  
  getLatestSHC: (farmId) => 
    api.get(`/farm/shc/${farmId}`),
};

export const recommendAPI = {
  getCropRecommendations: (farmId, topN = 10) => 
    api.get(`/recommend/crops?farm_id=${farmId}&top_n=${topN}`),
};

export const planAPI = {
  getYieldPlan: (cropName, farmId) => 
    api.get(`/plan/${cropName}?farm_id=${farmId}`),
};

export const weatherAPI = {
  getWeather: (lat, lon) => 
    api.get(`/weather/${lat}/${lon}`),
};

export default api;
