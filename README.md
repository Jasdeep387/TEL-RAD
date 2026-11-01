#### TEL-RAD: Telecom Evidence Logging, Reconstruction & Anomaly Detection Framework

An automated digital forensics and threat intelligence framework designed to ingest, process, and visualize Call Detail Records (CDRs) and Internet Protocol Detail Records (IPDRs) to reconstruct geographical suspect timelines and proactively surface network infrastructure anomalies. 

#### 📡 Operational Overview

In high-stakes digital forensics and critical infrastructure protection, law enforcement teams are overwhelmed by millions of rows of raw, unstructured telecom transactional metadata. TEL-RAD bridges this operational gap by parsing tabular logs, structuring permanent hardware identifiers, and running programmatic geospatial mathematical analysis to isolate malicious indicators of compromise (IOCs). 

#### 🚨 Core Analytical Detection Capabilities

1. **Velocity Anomaly (Impossible Travel):** Uses the Haversine formula to compute great-circle distances between consecutive cellular network interactions. If the calculated physical velocity required to traverse between cell sites exceeds commercial jet speed thresholds (900 KM/H), a critical alert is triggered.
2. **IMEI-SIM Swapping Tracker:** Monitors persistent hardware identities (IMEI) against temporary network identities (MSISDN/IMSI) to detect malicious cell-swapping tactics commonly used by threat actors to evade profiling.

#### 🛠️ System Architecture & Tech Stack

* **Operating Sandbox:** Kali Linux / VMware
* **Backend Processing Engine:** Python 3, Pandas, NumPy
* **Geospatial Mapping Layer:** Folium (OpenStreetMap CDN Integration via manual tile routing)
* **Frontend Tactical Web Workspace:** Streamlit

#### 🚀 Execution & Deployment Instructions

Follow these exact steps within a terminal environment to replicate the operational workspace and deploy the local forensic dashboard instance. 

#### 1. Environment Initialization & Repository Cloning

Clone or navigate to the root directory and initialize an isolated Python virtual environment to prevent package collision with base system utilities: 

bash

cd ~/Desktop/TEL_RAD
python3 -m venv telrad_env
source telrad_env/bin/activate

Use code with caution.

#### 2. Dependency Management

Install the core data structures and graphical interface dependencies inside the active virtual environment: 

bash

pip install pandas numpy folium streamlit streamlit-folium

Use code with caution.

#### 3. Evidentiary Data Synthesis (Day 1 Engine)

Execute the data-generation module to programmatically synthesize standardized mock Indian telecom logs (incorporating custom hidden velocity anomalies designed to validate the analytical engine): 

bash

python3 scripts/generate_mock_data.py

Use code with caution.

#### 4. Running Standalone Mathematical Tracking Scripts (Optional)

To verify calculations and compile standalone threat maps directly via terminal command lines, run: 

bash

python3 scripts/detection_engine.py
python3 scripts/generate_maps.py

Use code with caution.

#### 5. Launching the Tactical Web Dashboard Workspace

Deploy the centralized graphic UI application server natively: 

bash

streamlit run app.py

Use code with caution.

The server will bind locally, automatically launching a new tab inside your web browser pointing to: http://localhost:8501. 

#### 📁 Repository Structure

text

TEL_RAD/
├── telrad_env/               # Isolated Python Virtual Sandbox
├── data/
│   ├── raw_cdr_logs.csv      # Synthesized Telecom Evidence Inputs
│   ├── tower_catalog.csv     # Regional Cellular Mast Coordinate Map
│   └── suspect_map.html      # Compiled Offline Geospatial Flight Line Layer
├── scripts/
│   ├── generate_mock_data.py # Data Engine Synthesis Script
│   ├── detection_engine.py   # Algorithmic Anomaly Logic Backend
│   └── generate_maps.py      # Independent Vector Mapping Script
├── app.py                    # Main Centralized Streamlit Panel Front-End
└── README.md                 # Production Documentation Blueprint

Use code with caution.

#### 🔬 Academic Research & Defense Alignment

This project acts as an engineering proof-of-capability for graduate admissions streams focusing on Systems Security, Network Forensics, and Critical Infrastructure Defense. It showcases structural engineering maturity by separating algorithmic calculations from presentation rendering pipelines while adhering to local privacy and sovereign network constraint guidelines.

---

## ⚖️ License & Authorship
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Lead Developer & Researcher:**
* **Jasdeep Kaur** - *B.Tech Computer Science & Engineering (Cybersecurity & Digital Forensics)*
