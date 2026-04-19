-- Krishi Drishti Database Initialization Script
-- PostgreSQL 14+ with PostGIS Extension

-- Enable PostGIS extension for geospatial data
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types
CREATE TYPE farm_size_unit AS ENUM ('acres', 'hectares', 'bighas');
CREATE TYPE crop_season AS ENUM ('kharif', 'rabi', 'zaid', 'perennial');
CREATE TYPE irrigation_type AS ENUM ('rainfed', 'drip', 'sprinkler', 'flood', 'none');

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(15) UNIQUE NOT NULL,
    country_code VARCHAR(5) DEFAULT '+91',
    name VARCHAR(100),
    preferred_language VARCHAR(5) DEFAULT 'en',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Create index on phone for faster lookups
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- OTP table for authentication
CREATE TABLE otp_verifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(15) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    attempts INT DEFAULT 0
);

CREATE INDEX idx_otp_phone ON otp_verifications(phone);
CREATE INDEX idx_otp_expires ON otp_verifications(expires_at);

-- OTP codes table (used by FastAPI auth router)
CREATE TABLE IF NOT EXISTS otp_codes (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) NOT NULL,
    country_code VARCHAR(5) DEFAULT '+91',
    otp_code VARCHAR(6) NOT NULL,
    purpose VARCHAR(20) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_otp_codes_phone ON otp_codes(phone);
CREATE INDEX idx_otp_codes_expires ON otp_codes(expires_at);

-- Farms table with geospatial support
CREATE TABLE farms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    farm_name VARCHAR(100),
    location GEOGRAPHY(POINT, 4326) NOT NULL, -- PostGIS geography type
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    size DECIMAL(10, 2) NOT NULL CHECK (size > 0),
    size_unit farm_size_unit DEFAULT 'acres',
    soil_type VARCHAR(50),
    irrigation_type irrigation_type,
    region VARCHAR(50),
    district VARCHAR(50),
    state VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_farms_user_id ON farms(user_id);
CREATE INDEX idx_farms_location ON farms USING GIST(location);
CREATE INDEX idx_farms_region ON farms(region, state);

-- Soil Health Cards table
CREATE TABLE soil_health_cards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    image_url TEXT,
    image_path TEXT,
    -- Primary nutrients (kg/ha or ppm)
    nitrogen DECIMAL(6, 2) CHECK (nitrogen >= 0),
    phosphorus DECIMAL(6, 2) CHECK (phosphorus >= 0),
    potassium DECIMAL(6, 2) CHECK (potassium >= 0),
    -- Soil properties
    ph_value DECIMAL(3, 2) CHECK (ph_value BETWEEN 0 AND 14),
    electrical_conductivity DECIMAL(5, 2) CHECK (electrical_conductivity >= 0), -- dS/m
    organic_carbon DECIMAL(4, 2) CHECK (organic_carbon >= 0), -- %
    -- Secondary nutrients and micronutrients (ppm)
    sulphur DECIMAL(6, 2) CHECK (sulphur >= 0),
    zinc DECIMAL(6, 2) CHECK (zinc >= 0),
    iron DECIMAL(6, 2) CHECK (iron >= 0),
    copper DECIMAL(6, 2) CHECK (copper >= 0),
    manganese DECIMAL(6, 2) CHECK (manganese >= 0),
    boron DECIMAL(6, 2) CHECK (boron >= 0),
    -- Metadata
    tested_date DATE,
    lab_name VARCHAR(200),
    is_verified BOOLEAN DEFAULT FALSE,
    ocr_confidence DECIMAL(4, 2), -- OCR confidence score
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_shc_farm_id ON soil_health_cards(farm_id);
CREATE INDEX idx_shc_created_at ON soil_health_cards(created_at DESC);

-- Crop master data
CREATE TABLE crops (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_name VARCHAR(100) UNIQUE NOT NULL,
    scientific_name VARCHAR(150),
    season crop_season,
    duration_days INT, -- Growing period in days
    water_requirement VARCHAR(20), -- low, medium, high
    -- Optimal soil requirements
    optimal_ph_min DECIMAL(3, 2),
    optimal_ph_max DECIMAL(3, 2),
    optimal_temp_min INT, -- Celsius
    optimal_temp_max INT,
    -- Market data
    avg_price_per_quintal DECIMAL(10, 2),
    avg_cost_per_acre DECIMAL(10, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_crops_season ON crops(season);
CREATE INDEX idx_crops_name ON crops(crop_name);

-- Crop recommendations
CREATE TABLE crop_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    shc_id UUID REFERENCES soil_health_cards(id),
    crop_id UUID NOT NULL REFERENCES crops(id),
    crop_name VARCHAR(100) NOT NULL,
    suitability_score DECIMAL(5, 2) CHECK (suitability_score BETWEEN 0 AND 100),
    rank INT,
    model_version VARCHAR(20),
    weather_data JSONB, -- Store weather snapshot
    recommendations_text TEXT,
    -- Feature contributions for explainability
    feature_importance JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_crop_rec_farm_id ON crop_recommendations(farm_id);
CREATE INDEX idx_crop_rec_score ON crop_recommendations(suitability_score DESC);
CREATE INDEX idx_crop_rec_created_at ON crop_recommendations(created_at DESC);

-- Yield predictions
CREATE TABLE yield_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    shc_id UUID REFERENCES soil_health_cards(id),
    crop_id UUID NOT NULL REFERENCES crops(id),
    crop_name VARCHAR(100) NOT NULL,
    -- Baseline prediction
    baseline_yield DECIMAL(10, 2) NOT NULL, -- quintals/acre
    baseline_cost DECIMAL(10, 2),
    baseline_revenue DECIMAL(10, 2),
    baseline_profit DECIMAL(10, 2),
    -- Optimized prediction
    optimized_yield DECIMAL(10, 2),
    optimized_cost DECIMAL(10, 2),
    optimized_revenue DECIMAL(10, 2),
    optimized_profit DECIMAL(10, 2),
    yield_increase_percent DECIMAL(5, 2),
    cost_increase_percent DECIMAL(5, 2),
    roi_improvement DECIMAL(5, 2),
    -- Model metadata
    model_version VARCHAR(20),
    prediction_confidence DECIMAL(5, 2),
    weather_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_yield_pred_farm_id ON yield_predictions(farm_id);
CREATE INDEX idx_yield_pred_crop_id ON yield_predictions(crop_id);

-- Optimization recommendations
CREATE TABLE optimization_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    yield_prediction_id UUID NOT NULL REFERENCES yield_predictions(id) ON DELETE CASCADE,
    recommendation_type VARCHAR(50), -- fertilizer, irrigation, pesticide, timing
    priority INT CHECK (priority BETWEEN 1 AND 10),
    action_description TEXT NOT NULL,
    expected_impact TEXT,
    cost_impact DECIMAL(10, 2),
    yield_impact DECIMAL(5, 2), -- percentage increase
    timing VARCHAR(50), -- when to implement
    resources_needed TEXT,
    implementation_difficulty VARCHAR(20), -- easy, medium, hard
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_opt_rec_yield_pred_id ON optimization_recommendations(yield_prediction_id);
CREATE INDEX idx_opt_rec_priority ON optimization_recommendations(priority);

-- Weather cache table
CREATE TABLE weather_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    weather_data JSONB NOT NULL,
    forecast_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX idx_weather_location ON weather_cache(latitude, longitude);
CREATE INDEX idx_weather_expires ON weather_cache(expires_at);

-- Audit log table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(50),
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_created_at ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_action ON audit_logs(action);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_farms_updated_at BEFORE UPDATE ON farms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_shc_updated_at BEFORE UPDATE ON soil_health_cards
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to clean expired OTPs
CREATE OR REPLACE FUNCTION clean_expired_otps()
RETURNS void AS $$
BEGIN
    DELETE FROM otp_verifications WHERE expires_at < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate farm size in hectares (for standardization)
CREATE OR REPLACE FUNCTION get_farm_size_in_hectares(
    size_value DECIMAL,
    unit farm_size_unit
)
RETURNS DECIMAL AS $$
BEGIN
    RETURN CASE unit
        WHEN 'hectares' THEN size_value
        WHEN 'acres' THEN size_value * 0.404686
        WHEN 'bighas' THEN size_value * 0.25 -- Approximate, varies by region
        ELSE size_value
    END;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Create views for common queries

-- Active farms with latest soil health data
CREATE VIEW farms_with_latest_shc AS
SELECT 
    f.*,
    shc.id as shc_id,
    shc.nitrogen, shc.phosphorus, shc.potassium,
    shc.ph_value, shc.electrical_conductivity, shc.organic_carbon,
    shc.sulphur, shc.zinc, shc.iron, shc.copper, shc.manganese, shc.boron,
    shc.tested_date, shc.is_verified
FROM farms f
LEFT JOIN LATERAL (
    SELECT * FROM soil_health_cards 
    WHERE farm_id = f.id 
    ORDER BY created_at DESC 
    LIMIT 1
) shc ON true;

-- User dashboard summary
CREATE VIEW user_dashboard_summary AS
SELECT 
    u.id as user_id,
    u.phone,
    u.name,
    COUNT(DISTINCT f.id) as total_farms,
    COUNT(DISTINCT cr.id) as total_recommendations,
    COUNT(DISTINCT yp.id) as total_predictions,
    MAX(cr.created_at) as last_recommendation_date
FROM users u
LEFT JOIN farms f ON u.id = f.user_id
LEFT JOIN crop_recommendations cr ON f.id = cr.farm_id
LEFT JOIN yield_predictions yp ON f.id = yp.farm_id
GROUP BY u.id, u.phone, u.name;

-- Grant permissions (adjust based on your user setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO krishi_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO krishi_user;

COMMENT ON DATABASE krishi_drishti IS 'Krishi Drishti - AI-Powered Crop Advisory Platform';
