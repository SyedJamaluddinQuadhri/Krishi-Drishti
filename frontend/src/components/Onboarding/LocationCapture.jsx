import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import { useGeolocation } from '../../hooks/useGeolocation';
import './Onboarding.css';

const LocationCapture = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { location, error, loading, getLocation } = useGeolocation();
  const [capturedLocation, setCapturedLocation] = useState(null);

  const handleCaptureLocation = async () => {
    try {
      const position = await getLocation();
      setCapturedLocation(position);
      toast.success('Location captured successfully');
    } catch (err) {
      toast.error(err.message);
    }
  };

  const handleNext = () => {
    if (!capturedLocation) {
      toast.error('Please capture your location first');
      return;
    }

    localStorage.setItem('farmLocation', JSON.stringify(capturedLocation));
    navigate('/onboarding/shc-upload');
  };

  return (
    <div className="onboarding-container">
      <div className="onboarding-card">
        <div className="onboarding-header">
          <h1>📍 {t('onboarding.location')}</h1>
          <p>{t('onboarding.locationDesc')}</p>
        </div>

        <div className="location-capture-section">
          <button
            onClick={handleCaptureLocation}
            className="btn btn-primary btn-large"
            disabled={loading}
          >
            {loading ? t('common.loading') : t('onboarding.getLocation')}
          </button>

          {error && (
            <div className="error-box">
              <p>{error}</p>
            </div>
          )}

          {capturedLocation && (
            <div className="location-details">
              <div className="location-item">
                <span className="label">{t('onboarding.latitude')}:</span>
                <span className="value">{capturedLocation.latitude.toFixed(6)}</span>
              </div>
              <div className="location-item">
                <span className="label">{t('onboarding.longitude')}:</span>
                <span className="value">{capturedLocation.longitude.toFixed(6)}</span>
              </div>
              <div className="location-item">
                <span className="label">{t('onboarding.accuracy')}:</span>
                <span className="value">{capturedLocation.accuracy.toFixed(2)} m</span>
              </div>
            </div>
          )}
        </div>

        <div className="onboarding-actions">
          <button
            onClick={handleNext}
            className="btn btn-primary btn-full"
            disabled={!capturedLocation}
          >
            {t('onboarding.next')}
          </button>
        </div>
      </div>
    </div>
  );
};

export default LocationCapture;
