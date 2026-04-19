import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { farmAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';
import LanguageSelector from '../shared/LanguageSelector';
import LoadingSpinner from '../shared/LoadingSpinner';
import './Dashboard.css';

const Dashboard = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFarm, setSelectedFarm] = useState(null);

  useEffect(() => {
    fetchFarms();
  }, []);

  const fetchFarms = async () => {
    try {
      const response = await farmAPI.getUserFarms();
      setFarms(response.data);
      
      if (response.data.length > 0) {
        setSelectedFarm(response.data[0]);
        localStorage.setItem('currentFarmId', response.data[0].id);
      }
    } catch (error) {
      console.error('Error fetching farms:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGetRecommendations = () => {
    if (!selectedFarm) {
      return;
    }
    navigate('/recommendations');
  };

  if (loading) {
    return <LoadingSpinner message="Loading your dashboard..." />;
  }

  return (
    <div className="dashboard-page">
      <header className="dashboard-header">
        <div className="container">
          <div className="header-content">
            <h1 className="dashboard-logo">🌾 {t('app.name')}</h1>
            <div className="header-actions">
              <LanguageSelector />
              <button onClick={logout} className="btn btn-outline btn-small">
                {t('common.logout')}
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="container">
          <div className="welcome-section">
            <h2>{t('dashboard.welcome')}, {user?.name || 'Farmer'}! 👋</h2>
            <p>Manage your farms and get AI-powered crop recommendations</p>
          </div>

          {farms.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🏞️</div>
              <h3>No farms added yet</h3>
              <p>Start by adding your first farm to get personalized crop recommendations</p>
              <button 
                onClick={() => navigate('/onboarding/location')}
                className="btn btn-primary"
              >
                Add Your First Farm
              </button>
            </div>
          ) : (
            <>
              <section className="farms-section">
                <h3>{t('dashboard.myFarms')}</h3>
                <div className="farms-grid">
                  {farms.map((farm) => (
                    <div 
                      key={farm.id}
                      className={`farm-card ${selectedFarm?.id === farm.id ? 'selected' : ''}`}
                      onClick={() => {
                        setSelectedFarm(farm);
                        localStorage.setItem('currentFarmId', farm.id);
                      }}
                    >
                      <div className="farm-icon">🌾</div>
                      <h4>{farm.farm_name || 'Farm'}</h4>
                      <div className="farm-details">
                        <p>📍 {farm.district}, {farm.state}</p>
                        <p>📏 {farm.size} {farm.size_unit}</p>
                        <p>🌱 {farm.soil_type || 'Soil type not specified'}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              <section className="actions-section">
                <div className="action-cards">
                  <div className="action-card primary-card">
                    <div className="action-icon">🎯</div>
                    <h3>{t('dashboard.recommendations')}</h3>
                    <p>Get AI-powered crop recommendations based on your soil health and weather conditions</p>
                    <button 
                      onClick={handleGetRecommendations}
                      className="btn btn-primary"
                      disabled={!selectedFarm}
                    >
                      Get Recommendations
                    </button>
                  </div>

                  <div className="action-card">
                    <div className="action-icon">📊</div>
                    <h3>Soil Health Analysis</h3>
                    <p>View detailed analysis of your soil health card data</p>
                    <button 
                      onClick={() => navigate('/soil-analysis')}
                      className="btn btn-outline"
                      disabled={!selectedFarm}
                    >
                      View Analysis
                    </button>
                  </div>

                  <div className="action-card">
                    <div className="action-icon">🌦️</div>
                    <h3>Weather Forecast</h3>
                    <p>Get 7-day weather forecast for your farm location</p>
                    <button 
                      onClick={() => navigate('/weather')}
                      className="btn btn-outline"
                      disabled={!selectedFarm}
                    >
                      View Weather
                    </button>
                  </div>
                </div>
              </section>

              <section className="info-section">
                <div className="info-card">
                  <h3>💡 How It Works</h3>
                  <ol>
                    <li>Our AI analyzes your soil health card data</li>
                    <li>We consider local weather patterns and climate</li>
                    <li>You get personalized crop recommendations with suitability scores</li>
                    <li>View yield predictions and optimization strategies</li>
                  </ol>
                </div>
              </section>
            </>
          )}
        </div>
      </main>

      <footer className="dashboard-footer">
        <div className="container">
          <p>&copy; 2025 Krishi Drishti. Built with ❤️ for Indian Farmers.</p>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
