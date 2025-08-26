import pandas as pd
import requests
import time
import random
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load dataset
dataset_path = "C:\\Users\\sasha\\Traffic_Accident_Analysis_Project\\Traffic_Accident\\data\\updated_target.xlsx"
output_file = "C:\\Users\\sasha\\Traffic_Accident_Analysis_Project\\Traffic_Accident\\data\\updated_target1.xlsx"

# Set up your WeatherAPI key (Replace with your actual key)
API_KEY = "cb8abdc4079f47ce878135604252103"
BASE_URL = "http://api.weatherapi.com/v1/history.json"

df = pd.read_excel(dataset_path)

# Convert date format to YYYY-MM-DD
df["acci_date"] = pd.to_datetime(df["acci_date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")

# Extract only the hour from time
df["acci_hour"] = pd.to_datetime(df["acci_time"], format="%H:%M:%S").dt.hour

# Weather parameters to fetch (Added 'condition')
weather_columns = ["temp_c", "humidity", "wind_kph", "precip_mm", "cloud", "pressure_mb", "condition"]

# Initialize new columns for weather data
for col in weather_columns:
    df[col] = None

# Function to fetch weather data from WeatherAPI
def get_weather_data(lat, lon, date, hour, retries=3):
    params = {
        "key": API_KEY,
        "q": f"{lat},{lon}",
        "dt": date
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Extract the correct hour's data
            hourly_data = data.get("forecast", {}).get("forecastday", [{}])[0].get("hour", [])
            for entry in hourly_data:
                if entry["time"] == f"{date} {hour:02d}:00":
                    return {
                        "temp_c": entry.get("temp_c"),
                        "humidity": entry.get("humidity"),
                        "wind_kph": entry.get("wind_kph"),
                        "precip_mm": entry.get("precip_mm"),
                        "cloud": entry.get("cloud"),
                        "pressure_mb": entry.get("pressure_mb"),
                        "condition": entry.get("condition", {}).get("text", "Unknown")  # Fetch condition
                    }
        except Exception as e:
            print(f"API error: {e} (Attempt {attempt+1}/{retries})")
            time.sleep(2)
    return None

# Function to process a batch in parallel
def process_batch(batch_df):
    results = {}
    with ThreadPoolExecutor(max_workers=5) as executor:  # Using 5 threads for faster processing
        future_to_index = {
            executor.submit(get_weather_data, row["acci_x"], row["acci_y"], row["acci_date"], row["acci_hour"]): index 
            for index, row in batch_df.iterrows()
        }

        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                weather_data = future.result()
                if weather_data:
                    results[index] = weather_data
            except Exception as e:
                print(f"Error processing row {index}: {e}")
    
    for index, weather_data in results.items():
        for key, value in weather_data.items():
            df.at[index, key] = value

# Batch processing
batch_size = 1000
save_interval = 10
start_row = 1  # Change if needed
start_batch = start_row // batch_size

print("\nFetching weather data...")

for i in tqdm(range(start_batch, len(df) // batch_size + (1 if len(df) % batch_size > 0 else 0)), desc="Processing", unit="batch"):
    batch_df = df.iloc[i * batch_size : (i + 1) * batch_size]
    print(f"Processing batch {i + 1}...")
    process_batch(batch_df)
    
    if (i // batch_size) % save_interval == 0:
        df.to_excel(output_file, index=False)
        print(f"Progress saved at batch {i // batch_size}")
    
    time.sleep(2)  # Reduce rate of API calls to prevent limits

# Final save
df.to_excel(output_file, index=False)
print("\nWeather data collection completed!")
print("Saved at:", output_file)
