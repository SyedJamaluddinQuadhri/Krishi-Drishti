import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { planAPI } from '../../services/api';
import LoadingSpinner from '../shared/LoadingSpinner';
import './Dashboard.css';

const YieldPlan = () => {
  const { t } = useTranslation();
  const { cropName } = useParams();
  const navigate = useNavigate();
  
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchYieldPlan();
  }, [cropName]);

  const fetchYieldPlan = async () => {
    try {
      const farmId = localStorage.getItem('currentFarmId');
      
      if (!farmId) {
        setError('No farm selected');
        setLoading(false);
        return;
      }

      const response = await planAPI.getYieldPlan(cropName, farmId);
      setPlan(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch yield plan');
      console.error('Error fetching yield plan:', err);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority) => {
    if (priority <= 3) return '#ef4444';
    if (priority <= 6) return '#f59e0b';
    return '#10b981';
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      easy: '#10b981',
      medium: '#f59e0b',
      hard: '#ef4444'
    };
    return colors[difficulty?.toLowerCase()] || '#6b7280';
  };

  if (loading) {
    return <LoadingSpinner message="Generating yield plan and optimization strategies..." />;
  }

  if (error) {
    return (
      <div className="dashboard-page">
        <div className="container">
          <div className="error-state">
            <div className="error-icon">⚠️</div>
            <h3>Error Loading Yield Plan</h3>
            <p>{error}</p>
            <button onClick={() => navigate('/recommendations')} className="btn btn-primary">
              Back to Recommendations
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
            <button onClick={() => navigate('/recommendations')} className="back-btn">
              ← {t('common.back')}
            </button>
            <h1>{t('yieldPlan.title')}: {plan?.crop_name}</h1>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="container">
          <div className="yield-comparison">
            <div className="comparison-card baseline">
              <h3>📊 {t('yieldPlan.baseline')}</h3>
              <div className="comparison-stats">
                <div className="stat-item">
                  <span className="stat-label">{t('yieldPlan.yield')}</span>
                  <span className="stat-value">{plan?.baseline_yield?.toFixed(2)} quintals/acre</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">{t('yieldPlan.cost')}</span>
                  <span className="stat-value">₹{plan?.baseline_cost?.toFixed(0)}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">{t('yieldPlan.revenue')}</span>
                  <span className="stat-value">₹{plan?.baseline_revenue?.toFixed(0)}</span>
                </div>
                <div className="stat-item profit">
                  <span className="stat-label">{t('yieldPlan.profit')}</span>
                  <span className="stat-value">₹{plan?.baseline_profit?.toFixed(0)}</span>
                </div>
              </div>
            </div>

            <div className="comparison-arrow">→</div>

            <div className="comparison-card optimized">
              <h3>🚀 {t('yieldPlan.optimized')}</h3>
              <div className="comparison-stats">
                <div className="stat-item">
                  <span className="stat-label">{t('yieldPlan.yield')}</span>
                  <span className="stat-value">
                    {plan?.optimized_yield?.toFixed(2)} quintals/acre
                    <span className="increase-badge">+{plan?.yield_increase_percent?.toFixed(1)}%</span>
                  </span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">{t('yieldPlan.cost')}</span>
                  <span className="stat-value">
                    ₹{plan?.optimized_cost?.toFixed(0)}
                    <span className="increase-badge">+{plan?.cost_increase_percent?.toFixed(1)}%</span>
                  </span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">{t('yieldPlan.revenue')}</span>
                  <span className="stat-value">₹{plan?.optimized_revenue?.toFixed(0)}</span>
                </div>
                <div className="stat-item profit">
                  <span className="stat-label">{t('yieldPlan.profit')}</span>
                  <span className="stat-value">
                    ₹{plan?.optimized_profit?.toFixed(0)}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="roi-highlight">
            <div className="roi-icon">💰</div>
            <div className="roi-content">
              <h3>{t('yieldPlan.roi')}</h3>
              <p className="roi-value">+{plan?.roi_improvement?.toFixed(1)}%</p>
              <p className="roi-description">
                Additional profit of ₹{(plan?.optimized_profit - plan?.baseline_profit)?.toFixed(0)} 
                {' '}with recommended optimizations
              </p>
            </div>
          </div>

          <section className="recommendations-section">
            <h2>🎯 {t('yieldPlan.recommendations')}</h2>
            <p className="section-description">
              Follow these optimization strategies to achieve the projected yield increase:
            </p>

            <div className="recommendations-list">
              {plan?.optimization_recommendations?.map((rec, index) => (
                <div key={rec.id} className="optimization-card">
                  <div className="optimization-header">
                    <div className="optimization-number">{index + 1}</div>
                    <div className="optimization-title">
                      <h4>{rec.action_description}</h4>
                      <div className="optimization-badges">
                        <span 
                          className="priority-badge"
                          style={{ backgroundColor: getPriorityColor(rec.priority) }}
                        >
                          {t('yieldPlan.priority')} {rec.priority}
                        </span>
                        <span 
                          className="difficulty-badge"
                          style={{ backgroundColor: getDifficultyColor(rec.implementation_difficulty) }}
                        >
                          {rec.implementation_difficulty}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="optimization-details">
                    {rec.expected_impact && (
                      <div className="detail-row">
                        <span className="detail-icon">💡</span>
                        <div>
                          <strong>{t('yieldPlan.impact')}:</strong> {rec.expected_impact}
                        </div>
                      </div>
                    )}

                    {rec.yield_impact && (
                      <div className="detail-row">
                        <span className="detail-icon">📈</span>
                        <div>
                          <strong>Yield Impact:</strong> +{rec.yield_impact}%
                        </div>
                      </div>
                    )}

                    {rec.cost_impact && (
                      <div className="detail-row">
                        <span className="detail-icon">💵</span>
                        <div>
                          <strong>Cost:</strong> ₹{rec.cost_impact}
                        </div>
                      </div>
                    )}

                    {rec.timing && (
                      <div className="detail-row">
                        <span className="detail-icon">⏰</span>
                        <div>
                          <strong>{t('yieldPlan.timing')}:</strong> {rec.timing}
                        </div>
                      </div>
                    )}

                    {rec.resources_needed && (
                      <div className="detail-row">
                        <span className="detail-icon">🛠️</span>
                        <div>
                          <strong>{t('yieldPlan.resources')}:</strong> {rec.resources_needed}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>

          <div className="action-buttons">
            <button 
              onClick={() => window.print()}
              className="btn btn-outline"
            >
              🖨️ Print Plan
            </button>
            <button 
              onClick={() => navigate('/recommendations')}
              className="btn btn-primary"
            >
              View Other Crops
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default YieldPlan;
