import pandas as pd
import folium
import os

print("[*] TEL-RAD Visualizer: Constructing High-Contrast Dark Map UI...")

# 1. Gather files (Forcing phone numbers to be read as strings)
cdr_df = pd.read_csv('data/raw_cdr_logs.csv', dtype={'Calling_Number': str, 'Receiving_Number': str})
tower_df = pd.read_csv('data/tower_catalog.csv')

# Parse timestamps and merge datasets
cdr_df['Timestamp'] = pd.to_datetime(cdr_df['Timestamp'])
merged_df = pd.merge(cdr_df, tower_df, on='Cell_ID', how='left')

# 2. Isolate Target Suspect data chronologically
suspect_id = "919876543210"
suspect_data = merged_df[merged_df['Calling_Number'] == suspect_id].sort_values(by='Timestamp').reset_index(drop=True)

if suspect_data.empty:
    print("[-] Error: No data logs found for target suspect.")
    exit()

# 3. Initialize Base Map using manual free CDN mapping
base_map = folium.Map(location=[22.9734, 78.6568], zoom_start=5, tiles=None)

# Inject dark mode tiles using an explicit string for attribution to satisfy the Folium constructor
folium.TileLayer(
    tiles="https://{s}://{z}/{x}/{y}{r}.png",
    attr="&copy; OpenStreetMap contributors &copy; CARTO",
    name="TEL-RAD Tactical Dark Mode",
    control=False
).add_to(base_map)

# Keep track of coordinates to draw historical travel routes
movement_points = []

# 4. Generate Interactive Markers on the map
for idx, row in suspect_data.iterrows():
    coord = [row['Latitude'], row['Longitude']]
    movement_points.append(coord)
    
    # Custom forensic data popup box for each pin
    popup_text = f"""
    <div style="color: black; font-family: Arial, sans-serif; width: 200px;">
    <h4 style="margin: 0 0 5px 0; color: #FF9900;">Incident #{idx+1}</h4>
    <b>Tower ID:</b> {row['Cell_ID']}<br>
    <b>Location:</b> {row['Location_Name']}<br>
    <b>Timestamp:</b> {row['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')}<br>
    <b>IMEI Used:</b> {row['IMEI']}
    </div>
    """
    
    # Mark the tower position
    folium.Marker(
        location=coord,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=f"Incident {idx+1}: {row['Location_Name']}",
        icon=folium.Icon(color="orange", icon="phone", prefix="fa")
    ).add_to(base_map)

# 5. Connect the path dots with lines
for i in range(len(movement_points) - 1):
    pt1 = movement_points[i]
    pt2 = movement_points[i+1]
    
    # Check if this specific leg corresponds to our anomalous leap (Delhi to Bangalore)
    if suspect_data.iloc[i]['Cell_ID'] == "TWR-DEL-01" and suspect_data.iloc[i+1]['Cell_ID'] == "TWR-BLR-04":
        line_color = "#FF3333" # Cyber Neon Red
        line_weight = 6
        line_dash = "6, 6" 
    else:
        line_color = "#00CCFF" # Cyber Neon Blue
        line_weight = 3
        line_dash = None

    folium.PolyLine(
        locations=[pt1, pt2],
        color=line_color,
        weight=line_weight,
        dash_array=line_dash,
        tooltip="Suspect Operational Vector Route"
    ).add_to(base_map)

# 6. Export output
output_path = 'data/suspect_map.html'
base_map.save(output_path)
print(f"[+] Clean, unrestricted dark-mode map generated successfully at: {output_path}")
