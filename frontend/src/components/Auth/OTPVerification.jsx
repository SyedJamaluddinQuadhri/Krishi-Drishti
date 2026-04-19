import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import { authAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';
import './Auth.css';

const OTPVerification = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [loading, setLoading] = useState(false);
  const [resendTimer, setResendTimer] = useState(60);

  const phone = location.state?.phone;
  const countryCode = location.state?.countryCode || '+91';

  useEffect(() => {
    if (!phone) {
      navigate('/login');
      return;
    }

    const timer = setInterval(() => {
      setResendTimer((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);

    return () => clearInterval(timer);
  }, [phone, navigate]);

  const handleOtpChange = (index, value) => {
    if (value.length > 1) return;

    const newOtp = [...otp];
    newOtp[index] = value;
    setOtp(newOtp);

    // Auto-focus next input
    if (value && index < 5) {
      document.getElementById(`otp-${index + 1}`).focus();
    }
  };

  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      document.getElementById(`otp-${index - 1}`).focus();
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const otpCode = otp.join('');
    if (otpCode.length !== 6) {
      toast.error('Please enter complete OTP');
      return;
    }

    setLoading(true);

    try {
      const response = await authAPI.verifyOTP(phone, countryCode, otpCode, 'login');

      if (response.data.access_token) {
        login(
          response.data.access_token,
          response.data.refresh_token,
          response.data.user
        );
        toast.success(t('auth.loginSuccess'));
        navigate('/dashboard');
      }
    } catch (error) {
      console.error('OTP verification error:', error);
      setOtp(['', '', '', '', '', '']);
      document.getElementById('otp-0').focus();
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    if (resendTimer > 0) return;

    try {
      await authAPI.sendOTP(phone, countryCode);
      toast.success(t('auth.otpSent'));
      setResendTimer(60);
    } catch (error) {
      console.error('Resend OTP error:', error);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>{t('auth.verifyOTP')}</h1>
          <p>Enter the code sent to {countryCode} {phone}</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="otp-input-group">
            {otp.map((digit, index) => (
              <input
                key={index}
                id={`otp-${index}`}
                type="text"
                inputMode="numeric"
                maxLength="1"
                value={digit}
                onChange={(e) => handleOtpChange(index, e.target.value.replace(/\D/g, ''))}
                onKeyDown={(e) => handleKeyDown(index, e)}
                className="otp-input"
                autoFocus={index === 0}
              />
            ))}
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-full"
            disabled={loading || otp.join('').length !== 6}
          >
            {loading ? t('common.loading') : t('auth.verifyOTP')}
          </button>
        </form>

        <div className="resend-container">
          <button
            type="button"
            onClick={handleResend}
            disabled={resendTimer > 0}
            className="resend-btn"
          >
            {resendTimer > 0
              ? `${t('auth.resendOTP')} in ${resendTimer}s`
              : t('auth.resendOTP')}
          </button>
        </div>

        <button
          onClick={() => navigate('/login')}
          className="btn btn-outline btn-full"
          style={{ marginTop: '1rem' }}
        >
          {t('common.back')}
        </button>
      </div>
    </div>
  );
};

export default OTPVerification;
