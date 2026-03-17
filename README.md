# HealthyOrNot

## 💡Inspiration

People are an essential facet of our communities. However, it can often be difficult for people to know of any health issues and defects they suffer from, ranging from diabetes to cancer, to sometihng smaller like slightly high blood pressure.


HealthyOrNot aims to change that.

## 🔍 What it does

HealthyOrNot analyzes a user’s bloodwork results to determine whether key health indicators fall within healthy reference ranges. Using a supervised machine learning classification model, the system evaluates biomarkers (such as glucose levels, cholesterol, blood pressure indicators, etc) and predicts whether the results suggest a healthy or at risk status.

The application then processes the results to identify the most significant out of the ordinary markers. These markers are cleaned, categorized, and ranked based on severity and frequency of abnormality. 

This provides users with an accessible first step toward understanding their bloodwork before consulting a medical professional.

⚙️ How I built it
I built the frontend using React for dynamic UI rendering and Tailwind CSS featuring a dataset selector, a dynamic biomarker input form with a fill progress tracker, and a results panel that displays the prediction alongside a ranked feature for importance breakdown

The backend was built with Flask and uses two endpoints:
- `GET /datasets` — returns available datasets and their metadata
- `POST /predict` — runs inference and returns the prediction with per-feature importances

On startup, the backend trains and caches a best-fit model for each dataset by benchmarking multiple algorithms (linear models, decision trees, random forests, SVMs, KNN) using cross-validation and selecting the top performer. Models are persisted with **joblib** to avoid retraining on subsequent runs.

## ML Models evaluated per dataset

- Linear / Ridge / Lasso Regression
- Decision Tree
- Random Forest
- Support Vector Machine (SVC / SVR)
- K-Nearest Neighbors

## Running locally
```bash
# Backend
python api/app.py

# Frontend
npm install
npm run dev
```