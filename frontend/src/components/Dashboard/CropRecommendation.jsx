import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { recommendAPI } from '../../services/api';
import LoadingSpinner from '../shared/LoadingSpinner';
import './Dashboard.css';

const CropRecommendation = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      const farmId = localStorage.getItem('currentFarmId');
      
      if (!farmId) {
        setError('No farm selected. Please select a farm from dashboard.');
        setLoading(false);
        return;
      }

      const response = await recommendAPI.getCropRecommendations(farmId, 10);
      setRecommendations(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch recommendations');
      console.error('Error fetching recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSuitabilityColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
  };

  const getSuitabilityLabel = (score) => {
    if (score >= 80) return 'Highly Suitable';
    if (score >= 60) return 'Moderately Suitable';
    return 'Less Suitable';
  };

  if (loading) {
    return <LoadingSpinner message="Analyzing your soil and generating recommendations..." />;
  }

  if (error) {
    return (
      <div className="dashboard-page">
        <div className="container">
          <div className="error-state">
            <div className="error-icon">⚠️</div>
            <h3>Error Loading Recommendations</h3>
            <p>{error}</p>
            <button onClick={() => navigate('/dashboard')} className="btn btn-primary">
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <header className="dashboard-header">
        <div className="container">
          <div className="header-content">
            <button onClick={() => navigate('/dashboard')} className="back-btn">
              ← {t('common.back')}
            </button>
            <h1>{t('recommendations.title')}</h1>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="container">
          {recommendations.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🌾</div>
              <h3>{t('recommendations.noRecommendations')}</h3>
              <p>Please ensure your soil health card is uploaded and verified.</p>
            </div>
          ) : (
            <>
              <div className="recommendations-header">
                <p>Based on your soil health analysis and local weather conditions, here are the top crops recommended for your farm:</p>
              </div>

              <div className="recommendations-grid">
                {recommendations.map((rec) => (
                  <div key={rec.id} className="recommendation-card">
                    <div className="recommendation-header">
                      <div className="crop-info">
                        <h3>{rec.crop_name}</h3>
                        <span className="rank-badge">Rank #{rec.rank}</span>
                      </div>
                      <div 
                        className="suitability-score"
                        style={{ backgroundColor: getSuitabilityColor(rec.suitability_score) }}
                      >
                        <span className="score-value">{rec.suitability_score.toFixed(1)}</span>
                        <span className="score-label">Score</span>
                      </div>
                    </div>

                    <div className="suitability-bar-container">
                      <div 
                        className="suitability-bar"
                        style={{ 
                          width: `${rec.suitability_score}%`,
                          backgroundColor: getSuitabilityColor(rec.suitability_score)
                        }}
                      />
                    </div>
                    <p className="suitability-label">
                      {getSuitabilityLabel(rec.suitability_score)}
                    </p>

                    <div className="crop-details">
                      {rec.season && (
                        <div className="detail-item">
                          <span className="detail-icon">🌦️</span>
                          <span className="detail-label">{t('recommendations.season')}:</span>
                          <span className="detail-value">{rec.season}</span>
                        </div>
                      )}
                      
                      {rec.duration_days && (
                        <div className="detail-item">
                          <span className="detail-icon">⏱️</span>
                          <span className="detail-label">{t('recommendations.duration')}:</span>
                          <span className="detail-value">{rec.duration_days} {t('recommendations.days')}</span>
                        </div>
                      )}
                      
                      {rec.water_requirement && (
                        <div className="detail-item">
                          <span className="detail-icon">💧</span>
                          <span className="detail-label">{t('recommendations.waterReq')}:</span>
                          <span className="detail-value">{rec.water_requirement}</span>
                        </div>
                      )}
                    </div>

                    <div className="economic-info">
                      {rec.avg_price_per_quintal && (
                        <div className="economic-item">
                          <span className="economic-label">{t('recommendations.avgPrice')}</span>
                          <span className="economic-value">₹{rec.avg_price_per_quintal}/{t('recommendations.perQuintal')}</span>
                        </div>
                      )}
                      
                      {rec.avg_cost_per_acre && (
                        <div className="economic-item">
                          <span className="economic-label">{t('recommendations.avgCost')}</span>
                          <span className="economic-value">₹{rec.avg_cost_per_acre}/{t('recommendations.perAcre')}</span>
                        </div>
                      )}
                    </div>

                    {rec.recommendations_text && (
                      <div className="recommendation-text">
                        <p>{rec.recommendations_text}</p>
                      </div>
                    )}

                    <button 
                      onClick={() => navigate(`/yield-plan/${rec.crop_name}`)}
                      className="btn btn-primary btn-full"
                    >
                      {t('recommendations.viewPlan')}
                    </button>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
};

export default CropRecommendation;
