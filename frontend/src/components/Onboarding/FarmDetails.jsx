import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import { farmAPI } from '../../services/api';
import './Onboarding.css';

const FarmDetails = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();

  const [formData, setFormData] = useState({
    nitrogen: '',
    phosphorus: '',
    potassium: '',
    ph_value: '',
    electrical_conductivity: '',
    organic_carbon: '',
    sulphur: '',
    zinc: '',
    iron: '',
    copper: '',
    manganese: '',
    boron: '',
  });

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (location.state?.extractedData) {
      setFormData({
        ...formData,
        ...location.state.extractedData
      });
    }
  }, [location.state]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const shcId = localStorage.getItem('shcId');
      if (!shcId) {
        toast.error('SHC ID not found');
        return;
      }

      await farmAPI.verifySHC(shcId, formData);
      toast.success('Farm details saved successfully');
      navigate('/dashboard');
    } catch (error) {
      console.error('Save error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="onboarding-container">
      <div className="onboarding-card wide">
        <div className="onboarding-header">
          <h1>✏️ {t('onboarding.farmDetails')}</h1>
          <p>Verify and edit the extracted soil health data</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="input-group">
              <label>Nitrogen (N) kg/ha</label>
              <input
                type="number"
                step="0.01"
                name="nitrogen"
                value={formData.nitrogen}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Phosphorus (P) kg/ha</label>
              <input
                type="number"
                step="0.01"
                name="phosphorus"
                value={formData.phosphorus}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Potassium (K) kg/ha</label>
              <input
                type="number"
                step="0.01"
                name="potassium"
                value={formData.potassium}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>pH Value</label>
              <input
                type="number"
                step="0.01"
                name="ph_value"
                value={formData.ph_value}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>EC (dS/m)</label>
              <input
                type="number"
                step="0.01"
                name="electrical_conductivity"
                value={formData.electrical_conductivity}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Organic Carbon (%)</label>
              <input
                type="number"
                step="0.01"
                name="organic_carbon"
                value={formData.organic_carbon}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Sulphur (S) ppm</label>
              <input
                type="number"
                step="0.01"
                name="sulphur"
                value={formData.sulphur}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Zinc (Zn) ppm</label>
              <input
                type="number"
                step="0.01"
                name="zinc"
                value={formData.zinc}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Iron (Fe) ppm</label>
              <input
                type="number"
                step="0.01"
                name="iron"
                value={formData.iron}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Copper (Cu) ppm</label>
              <input
                type="number"
                step="0.01"
                name="copper"
                value={formData.copper}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Manganese (Mn) ppm</label>
              <input
                type="number"
                step="0.01"
                name="manganese"
                value={formData.manganese}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Boron (B) ppm</label>
              <input
                type="number"
                step="0.01"
                name="boron"
                value={formData.boron}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="onboarding-actions">
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="btn btn-outline"
            >
              {t('common.back')}
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? t('common.loading') : t('onboarding.save')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default FarmDetails;
