AI Multi-Disaster Prediction System
AI-Driven Multi-Disaster Prediction and Resilience System

Status: Deployment Ready | License: Academic/Research Use Only


PROJECT OVERVIEW

This repository hosts an end-to-end disaster intelligence platform designed to predict, monitor, and analyze multiple natural disasters in real time. The system integrates deep learning models, geospatial data analysis, and a responsive web dashboard to facilitate early warning systems, risk assessment, and data-driven decision-making.

By leveraging historical data and real-time environmental metrics, the platform addresses the critical need for predictive resilience in the face of complex, cascading climate crises.

---

DEPLOYMENT ACCESS
Link: https://ai-multi-disaster-predicition-system.onrender.com

---

TECHNICAL ARCHITECTURE

The system follows a service-oriented architecture. The frontend client communicates with a FastAPI backend, which orchestrates data ingestion, executes machine learning inference, and processes geospatial queries using external and internal datasets.

Flow Summary:
Frontend (React + TypeScript)
→ FastAPI Backend
→ ML Model Inference Services
→ Geospatial & Population Data
→ External Weather and Seismic APIs
→ JSON Responses to Frontend

---

CORE CAPABILITIES

1. Multi-Disaster Prediction

The platform provides predictive analytics for the following disaster categories:

• Earthquakes – Seismic activity monitoring and magnitude estimation
• Floods – Water level forecasting and flood inundation mapping
• Cyclones – Path tracking and intensity prediction
• Heatwaves – Temperature anomaly and duration detection
• Landslides – Terrain stability analysis and risk zoning

2. Machine Learning Implementation

• Algorithms include LSTM networks for time-series forecasting and U-Net CNNs for spatial segmentation
• Models are optimized and serialized for efficient production inference
• Modular loader architecture allows easy addition of new disaster models

3. Geospatial Intelligence

• Integration of GADM (Global Administrative Areas) datasets
• Risk zone classification and affected population estimation
• Interactive spatial layers and heatmap visualization

4. Real-Time Data Pipeline

• High-performance REST APIs built with FastAPI
• Asynchronous background schedulers for data ingestion
• Centralized alert generation and response logic

---

TECHNOLOGY STACK

Frontend
Framework: React 18
Language: TypeScript
Styling: Tailwind CSS
Build Tool: Vite

Backend
Framework: FastAPI
Runtime: Python 3.9+
Validation: Pydantic
Server: Uvicorn (ASGI)

Machine Learning & Data Science
Libraries: TensorFlow, Keras, Scikit-learn, NumPy, Pandas
Geospatial Processing: Shapefiles, GeoPandas

Infrastructure
Hosting: Render (Static Site + Web Service)
Containerization: Docker support included

---

PROJECT STRUCTURE

AI-Multi-Disaster-System
frontend/        – React frontend source
backend/         – FastAPI backend source
routers/       – API route definitions
services/      – Core business logic
models/        – ML model loaders and artifacts
database/      – Database utilities
data_pipeline/   – ETL and preprocessing scripts
ml_models/       – Trained model files (.h5, .pkl)
deployment/      – Deployment configuration
docker-compose.yml
requirements.txt

---

LOCAL DEVELOPMENT SETUP

Prerequisites
• Node.js v16+
• Python v3.9+
• Git

Repository Setup
Clone the repository and navigate into the project directory.

Backend Setup
Create and activate a virtual environment, install dependencies, and run the FastAPI server.
The backend will be available at [http://localhost:8000](http://localhost:8000)

Frontend Setup
Install frontend dependencies and start the development server.
The frontend will be available at [http://localhost:5173](http://localhost:5173)

---

CONFIGURATION

The backend requires environment variables for external APIs and model paths.
Create a .env file inside the backend directory with the following values:

WEATHER_API_KEY=your_api_key
MODEL_PATH=backend/models

---

CONTRIBUTORS

Diya Arora
Role: Frontend Engineering, Deployment, System Integration

Aman
Role: Backend Engineering, Machine Learning, Data Pipelines

---

LICENSE

This project is developed strictly for academic and research purposes.
Commercial usage is prohibited without explicit written permission from the authors.
