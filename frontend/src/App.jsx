import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';

// Direct imports (not lazy)
import Register from './components/Auth/Register';
import VerifyOTP from './components/Auth/VerifyOTP';

// Lazy load components for code splitting
const Login = lazy(() => import('./components/Auth/Login'));
const LocationCapture = lazy(() => import('./components/Onboarding/LocationCapture'));
const SHCUpload = lazy(() => import('./components/Onboarding/SHCUpload'));
const FarmDetails = lazy(() => import('./components/Onboarding/FarmDetails'));
const Dashboard = lazy(() => import('./components/Dashboard/Dashboard'));
const CropRecommendation = lazy(() => import('./components/Dashboard/CropRecommendation'));
const YieldPlan = lazy(() => import('./components/Dashboard/YieldPlan'));

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('access_token');
  return token ? children : <Navigate to="/login" replace />;
};

function App() {
  return (
    <Router>
      <Suspense fallback={<div className="loading-container"><div className="spinner"></div><p>Loading...</p></div>}>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Navigate to="/register" replace />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/verify-otp" element={<VerifyOTP />} />

          {/* Protected Routes - Onboarding */}
          <Route
            path="/onboarding/location"
            element={
              <ProtectedRoute>
                <LocationCapture />
              </ProtectedRoute>
            }
          />
          <Route
            path="/onboarding/shc-upload"
            element={
              <ProtectedRoute>
                <SHCUpload />
              </ProtectedRoute>
            }
          />
          <Route
            path="/onboarding/farm-details"
            element={
              <ProtectedRoute>
                <FarmDetails />
              </ProtectedRoute>
            }
          />

          {/* Protected Routes - Dashboard */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard/crop-recommendation"
            element={
              <ProtectedRoute>
                <CropRecommendation />
              </ProtectedRoute>
            }
          />
          {/* Alias route for /recommendations (used by Dashboard navigation) */}
          <Route
            path="/recommendations"
            element={
              <ProtectedRoute>
                <CropRecommendation />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard/yield-plan"
            element={
              <ProtectedRoute>
                <YieldPlan />
              </ProtectedRoute>
            }
          />
          {/* Yield plan with crop name param (used by CropRecommendation) */}
          <Route
            path="/yield-plan/:cropName"
            element={
              <ProtectedRoute>
                <YieldPlan />
              </ProtectedRoute>
            }
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/register" replace />} />
        </Routes>

        {/* Toast notifications */}
        <ToastContainer
          position="top-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </Suspense>
    </Router>
  );
}

export default App;

