import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load the dataset with weather data
input_file = "C:\\Users\\sasha\\Traffic_Accident_Analysis_Project\\Traffic_Accident\\data\\latest_dataset.xlsx"
df = pd.read_excel(input_file)

# Set Dubai coordinates to center the map
dubai_coordinates = [25.276987, 55.296249]  # Latitude and Longitude for Dubai

# Create a base map centered around Dubai
accident_map = folium.Map(location=dubai_coordinates, zoom_start=12)

# Create a marker cluster
marker_cluster = MarkerCluster().add_to(accident_map)

# Function to create a popup with weather details
def create_popup(row):
    return f"""
    <b>Accident ID:</b> {row['acci_id']}<br>
    <b>Date:</b> {row['acci_date']}<br>
    <b>Time:</b> {row['acci_time']}<br>
    <b>Temperature:</b> {row['temp_c']}°C<br>
    <b>Condition:</b> {row['condition']}<br>
    """

# Add accident locations to the marker cluster
for _, row in df.iterrows():
    folium.Marker(
        location=[row["acci_x"], row["acci_y"]],  # Ensure coordinates are in the correct order (lat, long)
        popup=create_popup(row),  # Show weather details when clicked
        tooltip=f"Accident ID: {row['acci_id']}",  # Hover text
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(marker_cluster)

# Save the map as an HTML file
map_output = "C:\\Users\\sasha\\Traffic_Accident_Analysis_Project\\Traffic_Accident\\data\\accident_weather_map.html"
accident_map.save(map_output)

print(f"Map saved successfully! Open: {map_output}")
