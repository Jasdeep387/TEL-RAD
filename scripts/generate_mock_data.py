import csv
import random
from datetime import datetime, timedelta

# Configurations
NUM_CDR_RECORDS = 1000
START_DATE = datetime(2026, 10, 25, 9, 0, 0) # Fixed timeline for consistency

# Indian Mobile Handset Data Simulation Pools
suspect_msisdn = "919876543210"
suspect_imei = "860432048765432"
suspect_imsi = "404451234567890"

normal_numbers = [f"91982345{i:04d}" for i in range(50)]
tower_pool = {
    "TWR-DEL-01": {"lat": 28.6139, "lon": 77.2090, "loc": "Connaught Place, Delhi"},
    "TWR-MUM-02": {"lat": 19.0760, "lon": 72.8777, "loc": "Andheri East, Mumbai"},
    "TWR-PUN-03": {"lat": 30.7333, "lon": 76.7794, "loc": "Sector 17, Chandigarh"},
    "TWR-BLR-04": {"lat": 12.9716, "lon": 77.5946, "loc": "MG Road, Bangalore"}
}

tower_ids = list(tower_pool.keys())

# Write Tower Database
with open('data/tower_catalog.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Cell_ID', 'Latitude', 'Longitude', 'Location_Name'])
    for tid, info in tower_pool.items():
        writer.writerow([tid, info['lat'], info['lon'], info['loc']])

# Generate CDR Records
with open('data/raw_cdr_logs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Calling_Number', 'Receiving_Number', 'Duration_Secs', 'IMEI', 'IMSI', 'Cell_ID'])
    
    current_time = START_DATE
    
    for i in range(NUM_CDR_RECORDS):
        current_time += timedelta(minutes=random.randint(1, 15))
        
        # Regular baseline generation
        if random.random() > 0.05:
            caller = random.choice(normal_numbers)
            receiver = random.choice(normal_numbers)
            while caller == receiver:
                receiver = random.choice(normal_numbers)
            
            writer.writerow([
                current_time.strftime('%Y-%m-%d %H:%M:%S'),
                caller, receiver, random.randint(10, 600),
                f"86011100{random.randint(1000000, 9999999)}",
                f"40445000{random.randint(1000000, 9999999)}",
                random.choice(tower_ids)
            ])
        else:
            # Inject Suspect Data Strategy
            writer.writerow([
                current_time.strftime('%Y-%m-%d %H:%M:%S'),
                suspect_msisdn, random.choice(normal_numbers), random.randint(30, 300),
                suspect_imei, suspect_imsi, "TWR-DEL-01"
            ])

    # CRITICAL INJECTION: Velocity Anomaly (Impossible Travel)
    # The suspect will make a call from Delhi and then instantly 2 minutes later from Bangalore
    anomaly_time_1 = START_DATE + timedelta(hours=5)
    anomaly_time_2 = anomaly_time_1 + timedelta(minutes=2)
    
    writer.writerow([anomaly_time_1.strftime('%Y-%m-%d %H:%M:%S'), suspect_msisdn, "919823450001", 45, suspect_imei, suspect_imsi, "TWR-DEL-01"])
    writer.writerow([anomaly_time_2.strftime('%Y-%m-%d %H:%M:%S'), suspect_msisdn, "919823450002", 120, suspect_imei, suspect_imsi, "TWR-BLR-04"])

print("[+] Mock dataset successfully generated inside data/ directory!")

