// src/components/Auth/VerifyOTP.jsx
import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import { authAPI } from '../../services/api';
import './Auth.css';

const VerifyOTP = () => {
  const { t } = useTranslation();
  const location = useLocation();
  const navigate = useNavigate();
  const { phone, countryCode, purpose } = location.state || {};

  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!phone || !countryCode) {
      navigate('/register');
    }
  }, [phone, countryCode, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (otp.length < 4) {
      toast.error(t('auth.enterOTP') || 'Enter valid OTP');
      return;
    }
    setLoading(true);
    try {
      const res = await authAPI.verifyOTP(phone, countryCode, otp, purpose || 'registration');
      if (res.data.success) {
        // Store JWT tokens for authenticated requests
        if (res.data.access_token) {
          localStorage.setItem('access_token', res.data.access_token);
        }
        if (res.data.refresh_token) {
          localStorage.setItem('refresh_token', res.data.refresh_token);
        }
        if (res.data.user) {
          localStorage.setItem('user', JSON.stringify(res.data.user));
        }

        toast.success(t('auth.loginSuccess') || 'Phone verified successfully');

        // Route based on purpose
        if (purpose === 'registration') {
          navigate('/onboarding/location');
        } else {
          navigate('/dashboard');
        }
      }
    } catch (err) {
      console.error(err);
      toast.error(err.response?.data?.detail || 'OTP verification failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>{t('auth.verifyOTP') || 'Verify OTP'}</h1>
          <p>{t('auth.enterOTP') || 'Enter the code sent to'} {countryCode} {phone}</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="otp-input-group">
            <input
              className="otp-input"
              type="text"
              inputMode="numeric"
              value={otp}
              onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
              maxLength={6}
              placeholder="Enter 6-digit OTP"
              autoFocus
            />
          </div>

          <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
            {loading ? (t('common.loading') || 'Verifying...') : (t('auth.verifyOTP') || 'Verify & Continue')}
          </button>
        </form>
      </div>
    </div>
  );
};

export default VerifyOTP;

