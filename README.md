# Chemical Equipment Parameter Visualizer

A full-stack (Desktop + Web + Backend) data visualization system for analyzing chemical plant equipment parameters from CSV datasets.  
The project emphasizes **data validation, correctness, interpretability, and reproducibility**, aligned with **FOSSEE / IIT Bombay** software quality expectations.

---

## Problem Statement

Chemical plants generate structured CSV data describing equipment parameters such as:

- Equipment Name
- Flowrate
- Pressure
- Temperature

Manual analysis is error-prone and does not scale.  
This project provides a **validated, visual, and reproducible system** to:

- Analyze equipment parameters
- Group equipment by logical type
- Detect data quality issues
- Visualize results consistently across platforms

---

## System Components

### 1. Desktop Application (Primary Reference Implementation)

Built using **PyQt5 + Pandas + Matplotlib**, the desktop app is the **authoritative analytics engine**.

#### Features
- CSV upload with schema validation
- Equipment type extraction (`Pump-1 → Pump`)
- Summary statistics
- Pie & bar charts with synchronized colors
- Scrollable UI
- Export charts as images
- Last 5 upload history with reload
- **Data Quality Report**
  - Missing values
  - Outliers
- Reproducible, deterministic output

---

### 2. Backend (Django REST API)

The backend exposes the **same validated processing logic** as the desktop app via REST APIs.

#### Responsibilities
- CSV upload endpoint
- Schema validation
- Equipment grouping logic
- Summary computation
- Distribution generation
- Upload history persistence

#### Example Endpoints
- `POST /upload/`
- `GET /history/`

> The backend ensures **logic consistency** between desktop and web clients.

---

### 3. Web Frontend (React + Chart.js)

The web interface consumes the backend APIs to present visual analytics in a browser.

#### Features
- CSV upload
- Summary metrics
- Pie & bar charts
- Upload history
- Shared processing semantics with desktop app

> The desktop application remains the **reference implementation** for correctness.

---

## System Architecture

CSV File
↓
Backend / Desktop Validation
↓
Data Quality Checks
↓
Processing Layer
↓
Summary + Distribution
↓
Charts (Desktop / Web)



---

## CSV Schema Requirements

| Column Name    | Type    | Description                     |
|----------------|---------|---------------------------------|
| Equipment Name | String  | e.g., Pump-1, Reactor-2         |
| Flowrate       | Numeric | Flow rate value                 |
| Pressure       | Numeric | Pressure value                  |
| Temperature    | Numeric | Temperature value               |

Invalid schemas are rejected early.

---

## Data Quality Report

Generated per upload:

- Total rows & columns
- Missing values per column
- Outlier counts for numeric attributes

This prevents misleading visual interpretation.

---

## Technology Stack

### Desktop
- Python 3
- PyQt5
- Pandas
- Matplotlib

### Backend
- Python
- Django
- Django REST Framework

### Web
- React
- Chart.js
- react-chartjs-2

---

## Installation

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver



Desktop Application

```bash
cd desktop-app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py



Web Frontend

```bash
cd web-frontend
npm install
npm start



Project Structure

chemical-equipment-visualizer/
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── api/
│
├── desktop-app/
│   ├── main.py
│   ├── requirements.txt
│
├── web-frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── chartSetup.js
│
└── README.md


Design Principles

Validation before visualization
One source of truth for processing logic
Reproducible analytics
Scientific data integrity
Extendable architecture


Alignment with FOSSEE / IIT Bombay

Emphasis on data correctness
Clear validation pipeline
Modular design
Reproducible results
Educational and scientific value


Future Improvements

Database-backed persistence
Statistical distribution analysis
Anomaly detection
Automated report export (PDF)
Unit testing for data pipeline


Author

Isha
Undergraduate Student
Interests: Data Science, Scientific Computing, Visualization


License

Academic and educational use under open-source principles.