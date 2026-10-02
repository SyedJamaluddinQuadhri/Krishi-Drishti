# Krishi Drishti — Detailed Project Description

## 1. Executive Summary

Krishi Drishti is an AI-powered agricultural advisory platform designed to help Indian farmers make better, faster, and more informed farming decisions. The platform combines farmer information, farm location, soil health data, weather conditions, crop information, historical agriculture data, and machine-learning-ready structures to provide personalized agricultural guidance.

The central idea behind Krishi Drishti is simple: agricultural advice should be based on the actual conditions of a farmer's land rather than being limited to generic recommendations.

Different farms have different soil nutrients, water availability, climate, crop history, land sizes, and economic conditions. A crop that performs well in one location may not be suitable for another. Krishi Drishti aims to analyze these differences and present practical recommendations in a simple and accessible format.

The application is designed as a full-stack platform with:

- A React frontend for farmer interaction.
- A FastAPI backend for business logic and APIs.
- PostgreSQL for persistent data storage.
- PostGIS for farm-location data.
- Twilio for phone OTP delivery.
- i18next for multilingual support.
- External weather and public agriculture data sources.
- Future machine-learning modules for crop yield and advisory prediction.

Krishi Drishti is suitable as an agritech product, Smart India Hackathon project, academic project, startup prototype, or foundation for a larger agricultural decision-support platform.

---

## 2. Background and Context

Agriculture is one of the most important sectors in India. A large number of farmers depend on agriculture for their livelihood, but many farming decisions are still made using traditional experience, incomplete information, or generalized advice.

Farmers may have access to soil health cards, weather information, government data, and crop statistics, but these sources are often disconnected. Even when the data is available, it may be difficult to understand or convert into daily farming actions.

For example, a farmer may know that the soil has low nitrogen, but may still need help answering questions such as:

- Which crop is suitable for this soil?
- Which fertilizer should be considered?
- How much irrigation is required?
- When should the next farming activity be performed?
- What yield can reasonably be expected?
- Will the additional input cost produce better profit?

Krishi Drishti is intended to act as a bridge between agricultural data and practical field-level decisions.

---

## 3. Problem Statement

Farmers commonly face the following challenges.

### 3.1 Lack of personalized advice

Many agricultural services provide broad recommendations for a district, crop, or season. However, a farmer's actual soil, land size, water availability, and crop history may be different from the regional average.

### 3.2 Difficulty understanding soil information

Soil health cards contain valuable measurements such as nitrogen, phosphorus, potassium, pH, and organic carbon. However, a farmer may not know how these values affect crop selection and fertilizer planning.

### 3.3 Weather uncertainty

Rainfall, temperature, humidity, wind, and extreme weather directly affect crop health. Farmers need timely information to plan sowing, irrigation, spraying, and harvesting activities.

### 3.4 Input-cost pressure

Seeds, fertilizers, pesticides, labour, irrigation, and machinery contribute to cultivation cost. Without planning, a farmer may spend more without receiving proportional yield or profit.

### 3.5 Language and accessibility barriers

Many digital agriculture tools are designed primarily for English-speaking users. Farmers may prefer local languages, simple language, audio explanations, or visual guidance.

### 3.6 Scattered data sources

Crop production, soil information, rainfall statistics, weather data, market information, and government schemes are often available through separate systems. Farmers may not have the time or technical ability to use all of these sources independently.

---

## 4. Proposed Solution

Krishi Drishti proposes a unified agricultural advisory platform that collects farm-specific information and converts it into useful recommendations.

The platform can combine:

- User profile information.
- Phone-based identity verification.
- Farm size and location.
- Soil type and soil nutrients.
- Soil health card information.
- Crop season.
- Water availability.
- Weather and forecast data.
- Historical crop-production data.
- Crop duration and input-cost data.
- Farmer preferences and constraints.

The platform can use these inputs to provide:

- Suitable crop recommendations.
- Crop suitability scores.
- Expected yield estimates.
- Irrigation recommendations.
- Fertilizer planning support.
- Soil improvement guidance.
- Pest and disease advisory structures.
- Yield and profit plans.
- Optimization actions.
- Weather-aware alerts.

The first version can use rule-based recommendation logic, while future versions can incorporate trained machine-learning models.

---

## 5. Vision

The vision of Krishi Drishti is to make reliable, personalized, and understandable agricultural intelligence accessible to every farmer through a mobile-friendly digital platform.

The long-term vision is to create a farmer-oriented decision-support system that does not merely display data, but explains what the data means and what action the farmer can consider next.

The platform should eventually answer questions such as:

- What should I grow this season?
- Is my soil suitable for this crop?
- What nutrient is missing from my soil?
- When should I irrigate?
- How can I reduce input cost?
- What yield and profit can I expect?
- What should I do if heavy rainfall is forecast?

---

## 6. Mission

The mission of Krishi Drishti is to improve agricultural decision-making by connecting farmers with localized, multilingual, and data-informed recommendations.

The project aims to:

1. Improve access to farm-specific advice.
2. Help farmers understand soil-health information.
3. Support more suitable crop selection.
4. Reduce unnecessary use of water and agricultural inputs.
5. Improve yield and profit planning.
6. Make digital agricultural services easier to use.
7. Support regional languages and low-literacy users.
8. Build a foundation for scalable agricultural AI services.

---

## 7. Target Users

### 7.1 Small and marginal farmers

The platform can support farmers who manage small landholdings and need simple, practical recommendations with limited resources.

### 7.2 Farmers with soil health cards

Farmers can use soil health card data to understand nutrient levels and receive more suitable crop and fertilizer guidance.

### 7.3 Farmers managing multiple farms

Users can maintain separate records for multiple plots with different locations, sizes, and soil conditions.

### 7.4 Agricultural extension workers

Extension officers can use the platform to organize farmer information and support advisory activities.

### 7.5 Farmer-producer organizations and cooperatives

Organizations can use aggregated data and recommendations to understand regional crop patterns and support their members.

### 7.6 Educational and research institutions

Agricultural colleges and research groups can use the platform as a base for experimentation with crop models, yield prediction, and regional analysis.

### 7.7 NGOs and rural-development programs

Organizations working with farming communities can use the system to improve digital access to agricultural information.

---

## 8. Detailed User Journey

### Step 1: Open the application

The farmer opens the Krishi Drishti web application on a computer or mobile device.

### Step 2: Select language

The farmer selects a preferred language. The interface updates through the shared language-selector component.

### Step 3: Register or log in

A new farmer selects registration. An existing farmer selects login.

### Step 4: Enter phone number

The farmer selects the country code and enters a phone number.

### Step 5: Request OTP

The frontend sends the phone details to the FastAPI backend. The backend generates a temporary OTP, stores it, and sends it through Twilio.

### Step 6: Verify OTP

The farmer enters the received OTP. The backend validates the OTP value, purpose, and expiry time.

### Step 7: Create or access account

For registration, a new user record is created. For login, the backend confirms that the user already exists and is verified.

### Step 8: Capture farm location

The farmer can allow location access. The application retrieves latitude and longitude through the browser geolocation API.

### Step 9: Enter farm details

The farmer enters the farm name, size, district, state, soil type, and water-related information.

### Step 10: Add soil information

The farmer can enter soil values manually or upload a soil health card for future OCR processing.

### Step 11: View crop recommendations

The platform evaluates farm conditions and presents suitable crops with supporting explanations.

### Step 12: View yield plan

The farmer can compare baseline and optimized plans, expected yield, cost, revenue, and profit.

### Step 13: Follow advisory actions

The dashboard presents prioritized actions such as irrigation, nutrient management, crop-care timing, or weather precautions.

---

## 9. Major Functional Modules

## 9.1 Authentication and user-management module

The authentication module provides passwordless phone-based registration and login.

### Registration flow

A new user sends:

```json
{
  "phone": "9876543210",
  "country_code": "+91",
  "purpose": "registration"
}
```

The backend generates an OTP, stores it in `otp_codes`, and sends it using the SMS service. After successful verification, the backend creates or updates the user record in `users`.

### Login flow

An existing user sends:

```json
{
  "phone": "9876543210",
  "country_code": "+91",
  "purpose": "login"
}
```

The backend sends a new OTP. After verification, it checks whether the user is already registered.

### Security requirements

A production version should include:

- OTP expiry.
- OTP rate limiting.
- Maximum verification attempts.
- Resend cooldown.
- Device/session control.
- JWT or secure session tokens.
- HTTPS.
- OTP hashing.

---

## 9.2 Multilingual interface module

The multilingual interface is implemented with `i18next` and `react-i18next`.

The interface can support:

- English.
- Hindi.
- Telugu.
- Tamil.
- Kannada.
- Marathi.
- Bengali.
- Gujarati.
- Punjabi.

The language selector changes the active language and can store the preference in browser local storage.

### Future language features

- Audio instructions.
- Voice search.
- Voice-based crop advisory.
- Local crop names.
- Regional units and terminology.
- Text simplification for low-literacy users.

---

## 9.3 Farm-management module

The farm-management module stores all information connected to agricultural land.

### Farm information

- Farm name.
- Farm location.
- Latitude.
- Longitude.
- Address.
- District.
- State.
- Pincode.
- Farm size.
- Size unit.
- Soil type.
- Water availability.
- Current crop.
- Previous crop.

### Multiple farms

One user may own or manage multiple farms. Each farm is stored as a separate database record linked to the user.

This design allows every farm to have different:

- Soil data.
- Coordinates.
- Crop recommendations.
- Yield plans.
- Weather conditions.

---

## 9.4 Geolocation module

The geolocation module captures a farm's coordinates through the browser geolocation API.

### Uses of location data

- Retrieve weather forecasts.
- Identify district or state.
- Filter agricultural datasets.
- Provide location-specific recommendations.
- Display a farm on a map.
- Compare regional crop performance.

The `useGeolocation` React hook manages:

- Current location.
- Loading state.
- Error state.
- Location request function.

Location should only be collected after the user provides permission.

---

## 9.5 Soil-health module

The soil-health module makes soil information available to recommendation logic.

### Supported soil values

- Nitrogen.
- Phosphorus.
- Potassium.
- pH value.
- Electrical conductivity.
- Organic carbon.
- Sulphur.
- Zinc.
- Iron.
- Copper.
- Manganese.
- Boron.

### Soil-health card support

The system can store:

- Soil health card number.
- Issue date.
- Uploaded image path.
- Nutrient values.
- Verification status.

### Future soil capabilities

- OCR extraction from uploaded cards.
- Automatic nutrient classification.
- Low, medium, and high nutrient labels.
- Fertilizer suggestions.
- Soil amendment recommendations.
- Longitudinal soil-health tracking.

---

## 9.6 Crop-recommendation module

The crop-recommendation module evaluates which crops may be appropriate for a farm.

### Possible inputs

- Soil pH.
- Nitrogen, phosphorus, and potassium.
- Organic carbon.
- Soil type.
- Water availability.
- Farm location.
- Current season.
- Crop duration.
- Expected market price.
- Average cost per acre.
- Historical crop production.

### Possible outputs

- Crop name.
- Suitability score.
- Recommendation rank.
- Expected yield.
- Water requirement.
- Growing season.
- Crop duration.
- Estimated cost.
- Explanation for recommendation.

### Recommendation approaches

The project can evolve through three stages:

#### Stage 1: Rule-based logic

Use thresholds and agriculture rules to provide initial recommendations.

#### Stage 2: Statistical scoring

Use historical performance, regional averages, and weighted scoring.

#### Stage 3: Machine-learning recommendation

Use trained models to predict crop suitability and expected yield.

Recommendations should be explainable so the farmer can understand why a crop was suggested.

---

## 9.7 Yield-planning module

The yield-planning module helps farmers compare existing practices with suggested improvements.

### Baseline plan

The baseline plan may use:

- Current crop.
- Current expected yield.
- Existing input cost.
- Existing revenue.
- Existing profit.

### Optimized plan

The optimized plan may include:

- Improved crop choice.
- Better sowing timing.
- Soil-specific fertilizer use.
- Improved irrigation scheduling.
- Pest-control planning.
- Weather-based actions.

### Calculated values

- Baseline yield.
- Optimized yield.
- Yield increase percentage.
- Baseline cost.
- Optimized cost.
- Revenue.
- Profit.
- Cost change percentage.
- ROI improvement.

---

## 9.8 Weather module

Weather information is important for daily farm decisions.

### Weather features

- Current temperature.
- Minimum and maximum temperature.
- Humidity.
- Rainfall.
- Wind speed.
- Forecast conditions.
- Severe-weather warnings.

### Advisory examples

- Delay irrigation when rainfall is expected.
- Avoid spraying before heavy rainfall.
- Protect sensitive crops during high winds.
- Adjust sowing schedules based on rainfall.
- Warn about heat or cold stress.

The `weather_cache` table can store recently retrieved responses and reduce unnecessary API calls.

---

## 9.9 Public agriculture-data module

Krishi Drishti can use open government datasets and public agricultural information.

Possible sources include:

- data.gov.in.
- State agriculture departments.
- Rainfall datasets.
- District crop-production data.
- Soil-health card statistics.
- Public market-price datasets.

### Uses of public data

- Historical model training.
- Regional benchmarking.
- Crop-production comparison.
- Yield-estimation support.
- District-level dashboards.
- Seasonal analysis.

Public data should be validated before it is used in recommendations.

---

## 10. Frontend Technical Description

The frontend is a React single-page application that communicates with the FastAPI backend through JSON APIs.

### Frontend responsibilities

- Display user interfaces.
- Handle routing.
- Validate form input.
- Send API requests.
- Display success and error messages.
- Manage OTP flow.
- Store temporary route state.
- Change languages.
- Capture geolocation.
- Display recommendation results.

### Frontend screens

#### Authentication screens

- Registration.
- Login.
- OTP verification.

#### Onboarding screens

- Location capture.
- Soil-health card upload.
- Farm details.

#### Dashboard screens

- Overview dashboard.
- Crop recommendations.
- Yield plan.
- Optimization recommendations.
- Weather summary.

### Frontend services

`api.js` centralizes HTTP requests, while `geolocation.js` isolates browser-location logic from UI components.

---

## 11. Backend Technical Description

The backend is a REST API built using FastAPI.

### Backend responsibilities

- Validate incoming requests.
- Generate OTPs.
- Store OTPs.
- Send SMS.
- Verify users.
- Manage farm records.
- Store soil information.
- Provide recommendations.
- Generate yield plans.
- Connect to external services.
- Return structured JSON responses.

### Backend layers

#### Main application layer

Creates and configures FastAPI.

#### Router layer

Defines URLs and endpoint handlers.

#### Schema layer

Validates request and response data using Pydantic.

#### Model layer

Represents database tables using SQLAlchemy.

#### Service layer

Contains reusable logic such as Twilio integration, weather retrieval, and recommendation processing.

#### Database layer

Creates SQLAlchemy sessions and manages PostgreSQL connections.

---

## 12. Database Technical Description

PostgreSQL provides relational persistence for all application data.

PostGIS extends PostgreSQL with geographic data types and indexes.

### Main relationships

```text
User 1 ──────── * Farm
Farm 1 ──────── * SoilHealthCard
Farm 1 ──────── * CropRecommendation
Farm 1 ──────── * YieldPlan
YieldPlan 1 ─── * OptimizationRecommendation
```

### Database design benefits

- Data consistency through foreign keys.
- Fast lookups through indexes.
- Clear separation between users, farms, recommendations, and plans.
- Spatial support for location-aware services.
- Future compatibility with analytics and machine learning.

---

## 13. Data Flow

### Registration and OTP data flow

```text
User enters phone number
          │
          ▼
React registration page
          │
          ▼
POST /auth/send-otp
          │
          ▼
FastAPI validates request
          │
          ▼
OTP generated and stored
          │
          ▼
Twilio sends SMS
          │
          ▼
User enters OTP
          │
          ▼
POST /auth/verify-otp
          │
          ▼
Backend validates OTP
          │
          ▼
User created or logged in
```

### Farm advisory data flow

```text
Farm details + Soil data + Location + Weather
                    │
                    ▼
              FastAPI API
                    │
                    ▼
       Recommendation and planning logic
                    │
                    ▼
            Crop and yield results
                    │
                    ▼
             React dashboard display
```

---

## 14. Expected Benefits

### Benefits for farmers

- Personalized agricultural guidance.
- Better crop selection.
- Improved understanding of soil values.
- More efficient water and fertilizer use.
- Better visibility into expected costs and revenue.
- Localized weather-aware recommendations.
- Access to information in preferred languages.

### Benefits for agricultural organizations

- Centralized farmer and farm information.
- Regional crop analysis.
- Better extension support.
- Digital advisory delivery.
- Easier collection of field-level information.

### Benefits for government programs

- Digital delivery of agricultural services.
- Better use of open agriculture datasets.
- Regional agricultural intelligence.
- Easier monitoring of farmer-support programs.

---

## 15. Innovation Potential

Krishi Drishti can become more innovative by combining multiple agricultural data sources into an explainable advisory engine.

Potential innovations include:

- Hyperlocal crop suitability scoring.
- Soil-aware fertilizer recommendations.
- Weather-based irrigation alerts.
- Explainable recommendations.
- Regional-language voice guidance.
- Profit-aware crop selection.
- AI-based soil-health card interpretation.
- Low-bandwidth progressive web app.
- Offline data capture.
- Personalized farm history.
- Risk scoring for weather and crop disease.

---

## 16. Current Development Status

The current project foundation includes:

- React frontend.
- FastAPI backend.
- PostgreSQL integration.
- PostGIS support.
- OTP registration and login structure.
- Twilio integration.
- Language-selector component.
- Geolocation hook.
- Farm database design.
- Soil-health-card database design.
- Crop master data.
- Crop recommendation structures.
- Yield-plan structures.
- Weather-cache structure.

Additional implementation may be required for:

- Final JWT/session-token handling.
- Complete production-ready ML models.
- Advanced recommendation algorithms.
- Final dashboard visualizations.
- Automated tests.
- Production deployment.
- Database migrations.

---

## 17. Scalability Plan

### Phase 1: Local prototype

- Local React frontend.
- Local FastAPI backend.
- Local PostgreSQL.
- Manual SQL initialization.
- Development OTP logging or Twilio.

### Phase 2: Pilot deployment

- Cloud PostgreSQL.
- Hosted backend.
- Hosted frontend.
- Real SMS delivery.
- Initial crop recommendation model.
- Basic monitoring and logs.

### Phase 3: Production platform

- Dockerized services.
- Horizontal API scaling.
- Database backups.
- Background jobs.
- Redis or another cache.
- Monitoring and alerting.
- Machine-learning model versioning.
- Role-based access control.

### Phase 4: Large-scale ecosystem

- State-wise agriculture integration.
- Farmer-producer organizations.
- Agricultural departments.
- Market and mandi prices.
- Voice assistant.
- Native mobile application.
- Offline-first operation.

---

## 18. Success Metrics

### Technical metrics

- API response time.
- OTP delivery success rate.
- OTP verification success rate.
- System uptime.
- Recommendation response time.
- Database query performance.
- Error rate.

### User metrics

- Registration completion rate.
- Number of active farmers.
- Number of farms added.
- Number of soil records uploaded.
- Number of recommendations viewed.
- Number of yield plans created.
- Language usage.
- User retention.

### Agricultural metrics

- Crop recommendation accuracy.
- Yield-estimation accuracy.
- Reduction in unnecessary input cost.
- Improvement in water-use efficiency.
- Farmer satisfaction.
- Adoption of recommendations.
- Change in estimated profitability.

---

## 19. Security and Privacy

Krishi Drishti handles sensitive information such as phone numbers, farm locations, soil data, and agricultural plans.

A production version should:

- Use HTTPS.
- Encrypt sensitive data in transit.
- Protect environment variables.
- Hash OTP values.
- Apply request rate limiting.
- Limit OTP attempts.
- Avoid production OTP logging.
- Implement access control.
- Validate uploaded files.
- Restrict database permissions.
- Back up data securely.
- Provide a privacy policy.
- Allow users to delete their data where required.

The following must never be committed publicly:

- Database passwords.
- Twilio credentials.
- JWT secrets.
- Weather API keys.
- data.gov.in API keys.

---

## 20. Why Krishi Drishti Matters

Krishi Drishti is valuable because it focuses on practical decision-making rather than presenting agricultural data without context.

A farmer does not only need to know the nitrogen value of soil. The farmer needs to understand what that value means for crop choice, fertilizer use, cost, and expected result.

A farmer does not only need a weather forecast. The farmer needs to know whether to irrigate, spray, sow, harvest, or protect the crop from a forecasted condition.

A farmer does not only need a list of crops. The farmer needs to know which crop may be suitable for the specific soil, season, water availability, location, and economic situation.

Krishi Drishti is designed to convert this information into understandable and actionable advice.

---

## 21. Conclusion

Krishi Drishti is a comprehensive agricultural decision-support platform that combines modern web technologies with agricultural data and future AI capabilities.

The platform provides a strong foundation for:

- Phone-based farmer onboarding.
- Multilingual access.
- Farm and location management.
- Soil-health interpretation.
- Crop recommendation.
- Yield planning.
- Weather-aware advisory.
- Public agriculture-data integration.
- Future machine-learning models.

The project can start as a local full-stack application and evolve into a scalable platform used by farmers, agricultural organizations, extension workers, cooperatives, and government programs.

Its long-term purpose is to make agricultural information more personal, understandable, accessible, and useful for real-world farming decisions.
