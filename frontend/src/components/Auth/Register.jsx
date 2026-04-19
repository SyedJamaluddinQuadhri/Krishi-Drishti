// src/components/Auth/Register.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import LanguageSelector from '../shared/LanguageSelector';
import { authAPI } from '../../services/api';
import './Auth.css';

const Register = () => {
  const { t } = useTranslation();  // ✅ Add this
  const navigate = useNavigate();
  const [phone, setPhone] = useState('');
  const [countryCode, setCountryCode] = useState('+91');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (phone.length < 10) {
      toast.error(t('auth.invalidPhone') || 'Please enter a valid phone number');
      return;
    }
    setLoading(true);
    try {
      const res = await authAPI.sendOTP(phone, countryCode, 'registration');
      if (res.data.success) {
        toast.success(t('auth.otpSent') || 'OTP sent for registration');
        navigate('/verify-otp', { state: { phone, countryCode, purpose: 'registration' } });
      }
    } catch (err) {
      console.error(err);
      toast.error(err.response?.data?.detail || t('auth.otpFailed') || 'Failed to send OTP');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>{t('app.name') || 'Krishi Drishti'}</h1>
          <p>{t('app.tagline') || 'AI-Powered Crop Advisory'}</p>
        </div>

        <div className="language-selector-container">
          <LanguageSelector />
        </div>

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>{t('auth.phone') || 'Phone Number'}</label>
            <div className="phone-input-group">
              <div className="country-code-wrapper">
                <select
                  value={countryCode}
                  onChange={(e) => setCountryCode(e.target.value)}
                  className="country-code-select"
                >
                  <option value="+91">+91 (India)</option>
                  <option value="+1">+1 (USA)</option>
                  <option value="+44">+44 (UK)</option>
                </select>
              </div>
              <input
                type="tel"
                className="phone-number-input"
                value={phone}
                onChange={(e) => setPhone(e.target.value.replace(/\D/g, ''))}
                placeholder={t('auth.enterPhone') || 'Enter phone number'}
                maxLength={10}
                required
              />
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
            {loading ? (t('common.loading') || 'Sending...') : (t('auth.sendOTP') || 'Register & Send OTP')}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            { 'Already have an account?'}{' '}
            <a href="/login" onClick={(e) => { e.preventDefault(); navigate('/login'); }}>
              {'Login with OTP'}
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
