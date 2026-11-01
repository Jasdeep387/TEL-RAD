# ==============================================================================
# PROJECT TEL-RAD: TELECOM EVIDENCE LOGGING, RECONSTRUCTION & ANOMALY DETECTION
# AUTHOR: JASDEEP KAUR
# DEGREE: B.TECH CSE (CYBERSECURITY & DIGITAL FORENSICS)
# COPYRIGHT (C) 2026 ALL RIGHTS RESERVED. LICENSED UNDER THE MIT LICENSE.
# ==============================================================================


import pandas as pd
import numpy as np

print("[*] TEL-RAD Core Engine Initiated. Analyzing telecom records...")

# 1. Load the data streams
cdr_df = pd.read_csv('data/raw_cdr_logs.csv')
tower_df = pd.read_csv('data/tower_catalog.csv')

# Convert text timestamps into actual processing datetimes
cdr_df['Timestamp'] = pd.to_datetime(cdr_df['Timestamp'])

# 2. Merge tower coordinates into the call records
merged_df = pd.merge(cdr_df, tower_df, on='Cell_ID', how='left')

# 3. Sort chronologically by player number and time
merged_df = merged_df.sort_values(by=['Calling_Number', 'Timestamp']).reset_index(drop=True)

# 4. Calculate shifts to compare current record with the NEXT record of the same person
merged_df['Next_Time'] = merged_df.groupby('Calling_Number')['Timestamp'].shift(-1)
merged_df['Next_Lat'] = merged_df.groupby('Calling_Number')['Latitude'].shift(-1)
merged_df['Next_Lon'] = merged_df.groupby('Calling_Number')['Longitude'].shift(-1)
merged_df['Next_Loc'] = merged_df.groupby('Calling_Number')['Location_Name'].shift(-1)

# Drop the last record of each person since they don't have a "next" record
analysis_df = merged_df.dropna(subset=['Next_Time']).copy()

# 5. Math Engine: Calculate distance using Haversine formula (Earth curvature)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

analysis_df['Distance_KM'] = calculate_distance(
    analysis_df['Latitude'], analysis_df['Longitude'],
    analysis_df['Next_Lat'], analysis_df['Next_Lon']
)

# Calculate temporal difference in hours
analysis_df['Time_Diff_Hours'] = (analysis_df['Next_Time'] - analysis_df['Timestamp']).dt.total_seconds() / 3600.0

# Calculate required speed (Speed = Distance / Time)
# Avoid division by zero if timestamps are identical
analysis_df['Required_Speed_KMPH'] = np.where(
    analysis_df['Time_Diff_Hours'] > 0,
    analysis_df['Distance_KM'] / analysis_df['Time_Diff_Hours'],
    0
)

# 6. Flag Phase: Anyone moving faster than 900 km/h (Commercial jet speed limit) is a anomaly
SPEED_THRESHOLD = 900.0
anomalies = analysis_df[analysis_df['Required_Speed_KMPH'] > SPEED_THRESHOLD]

print(f"\n[+] Analysis complete. Scanned {len(cdr_df)} entries.")
print(f"[🚨] CRITICAL ALERTS FOUND: {len(anomalies)}")

# Display the alerts cleanly
for idx, row in anomalies.iterrows():
    print(f"\n--- VELOCITY ANOMALY DETECTED ---")
    print(f"Target Suspect ID  : {row['Calling_Number']}")
    print(f"Origin Incident    : {row['Timestamp']} at {row['Location_Name']}")
    print(f"Destination Breach : {row['Next_Time']} at {row['Next_Loc']}")
    print(f"Calculated Shift   : {row['Distance_KM']:.2f} KM traversed in {row['Time_Diff_Hours']*60:.1f} minutes!")
    print(f"Required Velocity  : {row['Required_Speed_KMPH']:.2f} KM/H (IMPOSSIBLE TRAVEL)")
