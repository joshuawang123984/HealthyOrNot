# HealthyOrNot

## 💡Inspiration

People are an essential facet of our communities. However, it can often be difficult for people to know of any health issues and defects they suffer from, ranging from diabetes to cancer, to sometihng smaller like slightly high blood pressure.


HealthyOrNot aims to change that.

## 🔍 What it does

HealthyOrNot analyzes a user’s bloodwork results to determine whether key health indicators fall within healthy reference ranges. Using a supervised machine learning classification model, the system evaluates biomarkers (such as glucose levels, cholesterol, blood pressure indicators, etc) and predicts whether the results suggest a healthy or at risk status.

The application then processes the results to identify the most significant out of the ordinary markers. These markers are cleaned, categorized, and ranked based on severity and frequency of abnormality. The top five potential health concerns are displayed to the user.

This provides users with an accessible first step toward understanding their bloodwork before consulting a medical professional.

⚙️ How we built it
We built the frontend using React for dynamic UI rendering and Tailwind CSS and Bootstrap for responsive styling and layout.
The backend was developed using Flask, which handled API requests, processed user bloodwork input, and ran the machine learning model. The model was trained using supervised learning techniques to classify whether biomarkers fall within healthy reference ranges.

We implemented a preprocessing pipeline that:

-- Normalized numerical health indicators

-- Compared values against standard medical reference ranges

-- Identified out-of-range markers

-- Ranked abnormalities based on severity

The backend then returned structured health insights to the frontend, where results were displayed in an interactive and user-friendly format.

## 🚧 Challenges we ran into



## ✔️ Accomplishments that we're proud of


## 📚 What we learned


## 🔭 What's next for HealthyOrNot

HealthyOrNot would like to be able to produce graphs that display significant health indicators and the statistics of where one should lie. The graph should also include the individual persons own health indicator statistics.

