import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import { farmAPI } from '../../services/api';
import './Onboarding.css';

const SHCUpload = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [extractedData, setExtractedData] = useState(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      toast.error('Please select an image file');
      return;
    }

    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('File size should be less than 5MB');
      return;
    }

    setSelectedFile(file);

    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      toast.error('Please select an image first');
      return;
    }

    // Get farm location from previous step
    const locationData = localStorage.getItem('farmLocation');
    if (!locationData) {
      toast.error('Location data not found. Please go back.');
      return;
    }

    setUploading(true);

    try {
      // First, create a farm
      const location = JSON.parse(locationData);
      const farmResponse = await farmAPI.createFarm({
        latitude: location.latitude,
        longitude: location.longitude,
        size: 1, // Temporary, will be updated later
        size_unit: 'acres'
      });

      const farmId = farmResponse.data.id;
      localStorage.setItem('currentFarmId', farmId);

      // Upload SHC image
      const uploadResponse = await farmAPI.uploadSHC(farmId, selectedFile);

      if (uploadResponse.data.success) {
        setExtractedData(uploadResponse.data.extracted_data);
        localStorage.setItem('shcId', uploadResponse.data.shc_id);
        toast.success('Soil Health Card uploaded successfully');
        
        // Navigate to farm details after 2 seconds
        setTimeout(() => {
          navigate('/onboarding/farm-details', { 
            state: { 
              extractedData: uploadResponse.data.extracted_data,
              shcId: uploadResponse.data.shc_id
            } 
          });
        }, 2000);
      }
    } catch (error) {
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="onboarding-container">
      <div className="onboarding-card">
        <div className="onboarding-header">
          <h1>📄 {t('onboarding.uploadSHC')}</h1>
          <p>{t('onboarding.shcDesc')}</p>
        </div>

        <div className="upload-section">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />

          {!preview ? (
            <div 
              className="upload-area"
              onClick={() => fileInputRef.current.click()}
            >
              <div className="upload-icon">📷</div>
              <p>{t('onboarding.selectImage')}</p>
              <span className="upload-hint">Click to select or drag and drop</span>
            </div>
          ) : (
            <div className="image-preview">
              <img src={preview} alt="SHC Preview" />
              <button
                onClick={() => {
                  setSelectedFile(null);
                  setPreview(null);
                  setExtractedData(null);
                }}
                className="change-image-btn"
              >
                Change Image
              </button>
            </div>
          )}
        </div>

        {extractedData && (
          <div className="extracted-data-preview">
            <h3>Extracted Data Preview:</h3>
            <div className="data-grid">
              {Object.entries(extractedData).map(([key, value]) => (
                value && (
                  <div key={key} className="data-item">
                    <span className="data-label">{key}:</span>
                    <span className="data-value">{value}</span>
                  </div>
                )
              ))}
            </div>
          </div>
        )}

        <div className="onboarding-actions">
          <button
            onClick={() => navigate(-1)}
            className="btn btn-outline"
          >
            {t('common.back')}
          </button>
          <button
            onClick={handleUpload}
            className="btn btn-primary"
            disabled={!selectedFile || uploading}
          >
            {uploading ? t('common.loading') : t('onboarding.upload')}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SHCUpload;
