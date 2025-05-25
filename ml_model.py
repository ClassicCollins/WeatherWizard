# -*- coding: utf-8 -*-


import joblib
import requests
import numpy as np
import pandas as pd
from time import sleep
from datetime import datetime, date
from xgboost import XGBRegressor
from geopy.geocoders import Nominatim
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from IPython.display import display
from datetime import datetime, date
from ipywidgets import interact_manual, Text, DatePicker

import warnings
warnings.filterwarnings("ignore")

def fetch_weather_data(cities, start_date, end_date):
    """
    Fetch weather data (historical or forecast) for given cities and dates.

    Args:
        cities (list): List of city names as strings.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: Combined DataFrame of weather data for all cities.
    """
    geolocator = Nominatim(user_agent="weather_app")
    hourly_params = [
        'temperature_2m',
        'relative_humidity_2m',
        'surface_pressure',
        'windspeed_10m',
        'winddirection_10m',
        'windgusts_10m',
        'precipitation',
        'cloudcover',
        'shortwave_radiation'
    ]

    all_data = []

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    today = datetime.today().date()

    for city in cities:
        try:
            location = geolocator.geocode(city)
            if not location:
                print(f"Geocoding failed for {city}")
                continue

            # Decide endpoint: archive or forecast
            if end_date_obj < today:
                base_url = "https://archive-api.open-meteo.com/v1/archive"
            else:
                base_url = "https://api.open-meteo.com/v1/forecast"

            params = {
                'latitude': location.latitude,
                'longitude': location.longitude,
                'start_date': start_date,
                'end_date': end_date,
                'hourly': ','.join(hourly_params),
                'timezone': 'auto'
            }

            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'hourly' not in data or 'time' not in data['hourly']:
                print(f"No valid hourly data for {city}")
                continue

            df_city = pd.DataFrame(data['hourly'])
            df_city['datetime'] = pd.to_datetime(df_city['time'])
            df_city['city'] = city

            df_city = df_city[['datetime'] + hourly_params + ['city']]
            all_data.append(df_city)

            sleep(1)  # Rate limiting

        except Exception as e:
            print(f"Error processing {city}: {e}")

    if all_data:
        weather_df = pd.concat(all_data, ignore_index=True)
        weather_df.rename(columns={
            'datetime': 'Datetime',
            'temperature_2m': 'Temperature (°C)',
            'relative_humidity_2m': 'Humidity (%)',
            'surface_pressure': 'Pressure (hPa)',
            'windspeed_10m': 'Wind Speed (m/s)',
            'winddirection_10m': 'Wind Direction (°)',
            'windgusts_10m': 'Wind Gusts (m/s)',
            'precipitation': 'Precipitation (mm)',
            'cloudcover': 'Cloud Cover (%)',
            'shortwave_radiation': 'Solar Radiation (W/m²)',
            'city': 'City'
        }, inplace=True)
        return weather_df

    return pd.DataFrame()

def train_temperature_model(cities, start_date, end_date, model_output_path='xgb_temperature_model.joblib'):
    """
    Train a temperature prediction model and save it to disk.
    Works with XGBoost 3.x.
    """

    df = fetch_weather_data(cities, start_date, end_date)

    # Daily aggregation
    df['Date'] = pd.to_datetime(df['Datetime']).dt.date
    daily_df = df.groupby(['Date', 'City']).agg({
        'Temperature (°C)': 'mean',
        'Humidity (%)': 'mean',
        'Pressure (hPa)': 'mean',
        'Wind Speed (m/s)': 'mean',
        'Precipitation (mm)': 'sum',
        'Cloud Cover (%)': 'mean',
        'Solar Radiation (W/m²)': 'mean'
    }).reset_index()

    daily_df.sort_values(['City', 'Date'], inplace=True)

    # Lag features
    for lag in range(1, 4):
        daily_df[f'temp_lag_{lag}'] = daily_df.groupby('City')['Temperature (°C)'].shift(lag)

    # Target = next day
    daily_df['target_temp'] = daily_df.groupby('City')['Temperature (°C)'].shift(-1)
    daily_df.dropna(inplace=True)

    # Encode City
    le = LabelEncoder()
    daily_df['City_Code'] = le.fit_transform(daily_df['City'])

    features = [
        'Humidity (%)', 'Pressure (hPa)', 'Wind Speed (m/s)',
        'Precipitation (mm)', 'Cloud Cover (%)', 'Solar Radiation (W/m²)',
        'temp_lag_1', 'temp_lag_2', 'temp_lag_3', 'City_Code'
    ]
    target = 'target_temp'

    # Train/val split
    train_df, val_df = train_test_split(daily_df, test_size=0.2, shuffle=False)
    X_train = train_df[features].values
    y_train = train_df[target].values
    X_val = val_df[features].values
    y_val = val_df[target].values

    # Fix: enable_categorical=False restores classic interface
    model = XGBRegressor(
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        enable_categorical=False
    )


    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],


        verbose=False
    )

    # Eval
    preds = model.predict(X_val)
    rmse = np.sqrt(mean_squared_error(y_val, preds))
    mae = mean_absolute_error(y_val, preds)
    r2 = r2_score(y_val, preds)

    # Save model
    joblib.dump(model, model_output_path)

    results_df = val_df[['Date', 'City', 'target_temp']].copy()
    results_df['predicted_temp'] = preds

    return {
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'model_path': model_output_path,
        'results': results_df
    }

def predict_temperature(model_path, city, start_date, end_date):
    """
    Predict temperatures for a city and date range using a trained XGBoost model.
    """
    # Load the model
    model = joblib.load(model_path)

    # Fetch weather data
    df = fetch_weather_data([city], start_date, end_date)

    # Daily aggregation
    df['Date'] = pd.to_datetime(df['Datetime']).dt.date
    daily_df = df.groupby(['Date', 'City']).agg({
        'Temperature (°C)': 'mean',
        'Humidity (%)': 'mean',
        'Pressure (hPa)': 'mean',
        'Wind Speed (m/s)': 'mean',
        'Precipitation (mm)': 'sum',
        'Cloud Cover (%)': 'mean',
        'Solar Radiation (W/m²)': 'mean'
    }).reset_index()

    daily_df.sort_values(['City', 'Date'], inplace=True)

    # Create lag features
    for lag in range(1, 4):
        daily_df[f'temp_lag_{lag}'] = daily_df['Temperature (°C)'].shift(lag)

    daily_df.dropna(inplace=True)

    # Encode city
    le = LabelEncoder()
    le.fit([city])  # Assume only one city or same as training
    daily_df['City_Code'] = le.transform(daily_df['City'])

    features = [
        'Humidity (%)', 'Pressure (hPa)', 'Wind Speed (m/s)',
        'Precipitation (mm)', 'Cloud Cover (%)', 'Solar Radiation (W/m²)',
        'temp_lag_1', 'temp_lag_2', 'temp_lag_3', 'City_Code'
    ]

    X = daily_df[features].values
    predictions = model.predict(X)

    result = daily_df[['Date', 'City']].copy()
    result['predicted_temp'] = predictions

    return result
