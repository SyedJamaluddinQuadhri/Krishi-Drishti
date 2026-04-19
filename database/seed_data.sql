-- Seed data for Krishi Drishti
-- Insert master crop data

INSERT INTO crops (crop_name, scientific_name, season, duration_days, water_requirement, 
                  optimal_ph_min, optimal_ph_max, optimal_temp_min, optimal_temp_max,
                  avg_price_per_quintal, avg_cost_per_acre) VALUES

-- Kharif crops (Monsoon season: June-October)
('Rice', 'Oryza sativa', 'kharif', 120, 'high', 5.5, 7.0, 20, 35, 1850, 25000),
('Cotton', 'Gossypium', 'kharif', 180, 'medium', 6.0, 7.5, 21, 30, 5500, 30000),
('Maize', 'Zea mays', 'kharif', 90, 'medium', 5.5, 7.5, 18, 27, 1650, 20000),
('Bajra', 'Pennisetum glaucum', 'kharif', 75, 'low', 6.5, 8.0, 25, 35, 1400, 15000),
('Jowar', 'Sorghum bicolor', 'kharif', 110, 'low', 6.0, 7.5, 26, 34, 2200, 18000),
('Groundnut', 'Arachis hypogaea', 'kharif', 120, 'medium', 6.0, 7.0, 20, 30, 5000, 28000),
('Soybean', 'Glycine max', 'kharif', 95, 'medium', 6.0, 7.5, 20, 30, 3800, 22000),
('Sugarcane', 'Saccharum officinarum', 'perennial', 365, 'high', 6.0, 7.5, 20, 35, 3200, 75000),
('Turmeric', 'Curcuma longa', 'kharif', 240, 'medium', 4.5, 7.5, 20, 30, 7500, 45000),

-- Rabi crops (Winter season: October-March)
('Wheat', 'Triticum aestivum', 'rabi', 120, 'medium', 6.0, 7.5, 10, 25, 1975, 22000),
('Mustard', 'Brassica juncea', 'rabi', 110, 'low', 6.0, 7.5, 10, 25, 4500, 18000),
('Chickpea', 'Cicer arietinum', 'rabi', 120, 'low', 6.0, 7.5, 20, 30, 4800, 20000),
('Barley', 'Hordeum vulgare', 'rabi', 110, 'low', 6.5, 7.8, 12, 22, 1500, 16000),
('Lentil', 'Lens culinaris', 'rabi', 110, 'low', 6.0, 7.5, 18, 30, 5500, 19000),
('Peas', 'Pisum sativum', 'rabi', 90, 'medium', 6.0, 7.5, 10, 20, 3000, 25000),
('Potato', 'Solanum tuberosum', 'rabi', 90, 'medium', 5.0, 6.5, 15, 20, 800, 40000),
('Onion', 'Allium cepa', 'rabi', 120, 'medium', 6.0, 7.0, 13, 24, 1200, 35000),
('Tomato', 'Solanum lycopersicum', 'rabi', 90, 'medium', 6.0, 7.0, 18, 27, 1500, 45000),

-- Zaid crops (Summer season: March-June)
('Watermelon', 'Citrullus lanatus', 'zaid', 90, 'medium', 6.0, 7.0, 24, 30, 800, 30000),
('Muskmelon', 'Cucumis melo', 'zaid', 85, 'medium', 6.0, 7.0, 18, 30, 1200, 28000),
('Cucumber', 'Cucumis sativus', 'zaid', 60, 'medium', 5.5, 7.0, 18, 24, 1000, 35000),
('Bitter Gourd', 'Momordica charantia', 'zaid', 70, 'medium', 6.0, 7.0, 24, 30, 2500, 40000),

-- Perennial/Multiple season crops
('Banana', 'Musa', 'perennial', 365, 'high', 6.0, 7.5, 20, 35, 800, 120000),
('Papaya', 'Carica papaya', 'perennial', 300, 'medium', 6.0, 7.0, 22, 26, 1500, 80000),
('Mango', 'Mangifera indica', 'perennial', 1095, 'medium', 5.5, 7.5, 24, 30, 3500, 50000);

-- Insert sample test users (for development only)
INSERT INTO users (phone, country_code, name, preferred_language) VALUES
('+919876543210', '+91', 'Test Farmer 1', 'en'),
('+919876543211', '+91', 'परीक्षण किसान', 'hi'),
('+919876543212', '+91', 'పరీక్ష రైతు', 'te');

-- Insert sample farms (using test user IDs)
DO $$
DECLARE
    user1_id UUID;
    user2_id UUID;
    farm1_id UUID;
    farm2_id UUID;
BEGIN
    -- Get user IDs
    SELECT id INTO user1_id FROM users WHERE phone = '+919876543210';
    SELECT id INTO user2_id FROM users WHERE phone = '+919876543211';
    
    -- Insert farms for user 1
    INSERT INTO farms (user_id, farm_name, location, latitude, longitude, size, size_unit, soil_type, irrigation_type, region, district, state)
    VALUES (
        user1_id,
        'Green Valley Farm',
        ST_SetSRID(ST_MakePoint(77.5946, 12.9716), 4326)::geography,
        12.9716,
        77.5946,
        5.5,
        'acres',
        'Clay Loam',
        'drip',
        'Southern',
        'Bangalore Rural',
        'Karnataka'
    ) RETURNING id INTO farm1_id;
    
    -- Insert sample soil health card
    INSERT INTO soil_health_cards (
        farm_id, nitrogen, phosphorus, potassium, ph_value, electrical_conductivity,
        organic_carbon, sulphur, zinc, iron, copper, manganese, boron,
        tested_date, is_verified, ocr_confidence
    ) VALUES (
        farm1_id,
        245.0, 28.5, 185.0, 6.8, 0.45,
        0.75, 18.5, 1.2, 15.3, 0.8, 8.5, 0.6,
        CURRENT_DATE - INTERVAL '30 days',
        TRUE,
        95.5
    );
    
    -- Insert farm for user 2
    INSERT INTO farms (user_id, farm_name, location, latitude, longitude, size, size_unit, soil_type, irrigation_type, region, district, state)
    VALUES (
        user2_id,
        'Golden Fields',
        ST_SetSRID(ST_MakePoint(80.9462, 26.8467), 4326)::geography,
        26.8467,
        80.9462,
        10.0,
        'acres',
        'Alluvial',
        'flood',
        'Northern',
        'Lucknow',
        'Uttar Pradesh'
    ) RETURNING id INTO farm2_id;
    
    INSERT INTO soil_health_cards (
        farm_id, nitrogen, phosphorus, potassium, ph_value, electrical_conductivity,
        organic_carbon, sulphur, zinc, iron, copper, manganese, boron,
        tested_date, is_verified
    ) VALUES (
        farm2_id,
        280.0, 32.0, 210.0, 7.2, 0.38,
        0.85, 22.0, 1.5, 18.0, 1.0, 10.2, 0.8,
        CURRENT_DATE - INTERVAL '45 days',
        TRUE
    );
END $$;

-- Insert regional soil type reference data
CREATE TABLE IF NOT EXISTS regional_soil_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    state VARCHAR(50),
    district VARCHAR(50),
    soil_type VARCHAR(50),
    characteristics TEXT,
    common_crops TEXT[]
);

INSERT INTO regional_soil_types (state, district, soil_type, characteristics, common_crops) VALUES
('Karnataka', 'Bangalore Rural', 'Red Sandy Loam', 'Well-drained, low fertility', ARRAY['Ragi', 'Groundnut', 'Vegetables']),
('Karnataka', 'Mysuru', 'Clay Loam', 'Good water retention', ARRAY['Rice', 'Sugarcane', 'Cotton']),
('Uttar Pradesh', 'Lucknow', 'Alluvial', 'Highly fertile, rich in minerals', ARRAY['Wheat', 'Rice', 'Sugarcane']),
('Punjab', 'Ludhiana', 'Alluvial', 'Very fertile, suitable for cereals', ARRAY['Wheat', 'Rice', 'Maize']),
('Maharashtra', 'Pune', 'Black Cotton', 'Rich in calcium and magnesium', ARRAY['Cotton', 'Sorghum', 'Wheat']),
('Tamil Nadu', 'Coimbatore', 'Red Loam', 'Porous, well-drained', ARRAY['Cotton', 'Groundnut', 'Maize']),
('Telangana', 'Hyderabad', 'Red Sandy', 'Low water retention', ARRAY['Cotton', 'Rice', 'Maize']);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_regional_soil_state ON regional_soil_types(state);
CREATE INDEX IF NOT EXISTS idx_regional_soil_district ON regional_soil_types(district);

-- Insert weather station reference data (for offline fallback)
CREATE TABLE IF NOT EXISTS weather_stations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    station_name VARCHAR(100),
    location GEOGRAPHY(POINT, 4326),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    state VARCHAR(50),
    district VARCHAR(50)
);

-- Sample weather stations (major agricultural regions)
INSERT INTO weather_stations (station_name, location, latitude, longitude, state, district) VALUES
('Bangalore Agro Station', ST_SetSRID(ST_MakePoint(77.5946, 12.9716), 4326)::geography, 12.9716, 77.5946, 'Karnataka', 'Bangalore'),
('Lucknow Farm Station', ST_SetSRID(ST_MakePoint(80.9462, 26.8467), 4326)::geography, 26.8467, 80.9462, 'Uttar Pradesh', 'Lucknow'),
('Ludhiana Agri Center', ST_SetSRID(ST_MakePoint(75.8573, 30.9010), 4326)::geography, 30.9010, 75.8573, 'Punjab', 'Ludhiana'),
('Pune Weather Station', ST_SetSRID(ST_MakePoint(73.8567, 18.5204), 4326)::geography, 18.5204, 73.8567, 'Maharashtra', 'Pune');

ANALYZE; -- Update statistics for query optimizer
