import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import { authAPI } from '../../services/api';
import LanguageSelector from '../shared/LanguageSelector';
import './Auth.css';

const Login = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [phone, setPhone] = useState('');
  const [countryCode, setCountryCode] = useState('+91');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (phone.length < 10) {
      toast.error('Please enter a valid phone number');
      return;
    }

    setLoading(true);

    try {
      const response = await authAPI.sendOTP(phone, countryCode, 'login');
if (response.data.success) {
  navigate('/verify-otp', { state: { phone, countryCode, purpose: 'login' } });
}
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>🌾 {t('app.name')}</h1>
          <p>{t('app.tagline')}</p>
        </div>

        <div className="language-selector-container">
          <LanguageSelector />
        </div>

        <form onSubmit={handleSubmit}>
          <div className="input-group">
  <label>{t('auth.phone')}</label>
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
      placeholder={t('auth.enterPhone')}
      maxLength="10"
      required
    />
  </div>
</div>


          <button 
            type="submit" 
            className="btn btn-primary btn-full"
            disabled={loading}
          >
            {loading ? t('common.loading') : t('auth.sendOTP')}
          </button>
        </form>

        <div className="auth-footer">
          <p>By continuing, you agree to our Terms & Privacy Policy</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
