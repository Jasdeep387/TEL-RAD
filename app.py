# ==============================================================================
# PROJECT TEL-RAD: TELECOM EVIDENCE LOGGING, RECONSTRUCTION & ANOMALY DETECTION
# AUTHOR: JASDEEP KAUR
# DEGREE: B.TECH CSE (CYBERSECURITY & DIGITAL FORENSICS)
# COPYRIGHT (C) 2026 ALL RIGHTS RESERVED. LICENSED UNDER THE MIT LICENSE.
# ==============================================================================

import streamlit as pd_st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import os
from datetime import datetime

# Set up page configurations for an elite forensic dashboard layout
pd_st.set_page_config(page_title="TEL-RAD Tactical Workspace", layout="wide", initial_sidebar_state="expanded")

# Custom Title Section
pd_st.markdown("""
    <div style="background-color:#1E1E1E; padding:15px; border-radius:10px; border-left: 6px solid #FF9900; margin-bottom:20px;">
        <h1 style="color:white; margin:0; font-family:Arial;">TEL-RAD: Telecom Evidence Logging, Reconstruction & Anomaly Detection</h1>
        <p style="color:#A0A0A0; margin:5px 0 0 0;">National Security & Critical Infrastructure Intelligence Analysis Engine</p>
    </div>
# NEW FIXED LINE:
""", unsafe_allow_html=True)

# Math Helper: Haversine distance calculator
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# File verification blocks
if not os.path.exists('data/raw_cdr_logs.csv') or not os.path.exists('data/tower_catalog.csv'):
    pd_st.error("[-] Error: Missing core dataset logs in 'data/' directory. Run data generator first.")
else:
    # 1. Load Data Streams
    cdr_df = pd.read_csv('data/raw_cdr_logs.csv', dtype={'Calling_Number': str, 'Receiving_Number': str})
    tower_df = pd.read_csv('data/tower_catalog.csv')
    cdr_df['Timestamp'] = pd.to_datetime(cdr_df['Timestamp'])
    merged_df = pd.merge(cdr_df, tower_df, on='Cell_ID', how='left')

    # Sidebar Interactive Controls
    pd_st.sidebar.header("🎯 Forensic Investigation Panel")
    unique_suspects = sorted(merged_df['Calling_Number'].unique())
    target_suspect = pd_st.sidebar.selectbox("Select Target Suspect Target Number:", unique_suspects)

    # Core Core Engine Analytics Calculation
    sorted_df = merged_df.sort_values(by=['Calling_Number', 'Timestamp']).reset_index(drop=True)
    sorted_df['Next_Time'] = sorted_df.groupby('Calling_Number')['Timestamp'].shift(-1)
    sorted_df['Next_Lat'] = sorted_df.groupby('Calling_Number')['Latitude'].shift(-1)
    sorted_df['Next_Lon'] = sorted_df.groupby('Calling_Number')['Longitude'].shift(-1)
    sorted_df['Next_Loc'] = sorted_df.groupby('Calling_Number')['Location_Name'].shift(-1)

    analysis_df = sorted_df.dropna(subset=['Next_Time']).copy()
    analysis_df['Distance_KM'] = calculate_distance(
        analysis_df['Latitude'], analysis_df['Longitude'],
        analysis_df['Next_Lat'], analysis_df['Next_Lon']
    )
    analysis_df['Time_Diff_Hours'] = (analysis_df['Next_Time'] - analysis_df['Timestamp']).dt.total_seconds() / 3600.0
    analysis_df['Required_Speed_KMPH'] = np.where(
        analysis_df['Time_Diff_Hours'] > 0, analysis_df['Distance_KM'] / analysis_df['Time_Diff_Hours'], 0
    )

    # Flag Anomalies across the whole system
    SPEED_THRESHOLD = 900.0
    all_anomalies = analysis_df[analysis_df['Required_Speed_KMPH'] > SPEED_THRESHOLD]

    # Dashboard Metrics Row Layout
    col1, col2, col3 = pd_st.columns(3)
    col1.metric("📊 Total Records Processed", f"{len(cdr_df)} rows")
    col2.metric("🗼 Active Antennas Cataloged", f"{len(tower_df)} Sites")
    col3.metric("🚨 Total System Violations", f"{len(all_anomalies)} Flags", delta="- Critical", delta_color="inverse")

    # Main Area Layout Tabs
    tab1, tab2 = pd_st.tabs(["🌐 Geospatial Tracking Feed", "📁 Comprehensive Incident Transcripts"])

    with tab1:
        pd_st.subheader(f"Tactical Vector Mapping for Target: {target_suspect}")
        
        # Isolate selected suspect coordinates
        suspect_data = merged_df[merged_df['Calling_Number'] == target_suspect].sort_values(by='Timestamp').reset_index(drop=True)
        
        # Create map layer
        m = folium.Map(location=[row_lat := suspect_data.iloc[0]['Latitude'], suspect_data.iloc[0]['Longitude']], zoom_start=5, tiles=None)
        folium.TileLayer(
            tiles="https://{s}://{z}/{x}/{y}{r}.png",
            attr="&copy; OpenStreetMap contributors &copy; CARTO",
            name="TEL-RAD Dark",
            control=False
        ).add_to(m)

        # Plot individual points and trajectories
        coords_list = []
        for idx, row in suspect_data.iterrows():
            c = [row['Latitude'], row['Longitude']]
            coords_list.append(c)
            
            p_text = f"<b>Tower:</b> {row['Cell_ID']}<br><b>Time:</b> {row['Timestamp']}<br><b>IMEI:</b> {row['IMEI']}"
            folium.Marker(
                location=c,
                popup=folium.Popup(p_text, max_width=250),
                icon=folium.Icon(color="orange", icon="phone", prefix="fa")
            ).add_to(m)

        for i in range(len(coords_list) - 1):
            p1, p2 = coords_list[i], coords_list[i+1]
            if suspect_data.iloc[i]['Cell_ID'] == "TWR-DEL-01" and suspect_data.iloc[i+1]['Cell_ID'] == "TWR-BLR-04":
                folium.PolyLine(locations=[p1, p2], color="#FF3333", weight=5, dash_array="6,6").add_to(m)
            else:
                folium.PolyLine(locations=[p1, p2], color="#00CCFF", weight=3).add_to(m)

        # Render map window directly into web engine canvas
        st_folium(m, width=1100, height=500, returned_objects=[])

    with tab2:
        pd_st.subheader("Extracted Metadata Log Analysis")
        # Isolate specific anomalies for the chosen target
        suspect_anomalies = all_anomalies[all_anomalies['Calling_Number'] == target_suspect]
        
        if not suspect_anomalies.empty:
            pd_st.warning(f"🚨 ALERT: {len(suspect_anomalies)} Impossible Velocity Vectors Detected for Subscriber {target_suspect}!")
            pd_st.dataframe(suspect_anomalies[['Timestamp', 'Location_Name', 'Next_Time', 'Next_Loc', 'Distance_KM', 'Required_Speed_KMPH']])
        else:
            pd_st.success("[+] Operational Clear: Target subscriber travel timelines fall within normal safety guidelines.")

        pd_st.subheader("Raw Interactive Log Viewer")
        pd_st.dataframe(suspect_data)
