# Smart-Traffic-Accident-Analysis-Using-Visualization-and-ML-AI
Machine learning system for predicting traffic accident severity by integrating weather and traffic data with real-time visualization dashboard

## Overview
Predictive analytics system designed for Dubai's traffic safety authorities to identify high-risk areas and times by combining weather conditions with traffic accident data.

## Dataset & Features
- **Traffic Data**: Accident records with location, time, and severity classifications
- **Weather Data**: Meteorological conditions (precipitation, humidity, wind speed, temperature)
- **Integration**: SMOTENC applied for balanced categorical feature handling
- **Target Classes**: Simple, Minor, Severe accident severity levels

## Methodology

### Data Preprocessing
- Merged accident-weather datasets by time and location
- Applied SMOTENC to address class imbalance in categorical features
- Feature engineering for temporal and environmental variables

### Machine Learning Models
- **XGBoost**: Best performing model (88% accuracy, 0.88 weighted F1-score)
- **Random Forest**: Strong ensemble performance with feature importance analysis
- **Logistic Regression**: Linear baseline model
- **LightGBM**: Gradient boosting alternative

### Key Performance Metrics
- **Accuracy**: 88% (XGBoost)
- **Cross-validation**: 5-fold stratified validation
- **Feature Importance**: Humidity, precipitation, wind speed, time of day

## Visualization Dashboard
Built with **Plotly Dash** featuring:
- **Exploratory Analysis**: Weather trends, accident patterns, correlation heatmaps
- **Interactive Maps**: Geographic accident distribution with severity indicators
- **Live Predictor**: Real-time severity prediction based on current conditions
- **Risk Forecasting**: Future accident probability zones

## Real-World Impact
- **Emergency Response**: Faster resource allocation to high-risk areas
- **Traffic Management**: Proactive route planning during adverse weather
- **Public Safety**: Driver warnings for dangerous road conditions
- **Policy Planning**: Data-driven infrastructure improvements

## Technologies
- Python, scikit-learn, XGBoost, LightGBM
- Plotly Dash for interactive dashboards
- Pandas, NumPy for data processing
- SMOTENC for imbalanced learning
