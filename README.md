# Gurgaon Real Estate Analytics & Prediction Platform

# 🚀 Live Demo
Check out the app here : [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gurgaon-real-estate-dashboard-34ntxe4grfdgprhj3uvbwv.streamlit.app/)


Welcome to the Gurgaon Real Estate Analytics Dashboard, a comprehensive, data-driven web application designed to provide deep insights into the Gurgaon property market. This project leverages machine learning and data analytics to offer tools for price prediction, market analysis, property recommendations, and interactive price estimation.

![Gurgaon Skyline](data/gurgaon_real_estate.jpeg) <!-- Make sure your image is in the data folder -->

---

## 🚀 Key Features

This application is composed of four powerful, interconnected modules:

### 1. 💲 Price Predictor
A robust machine learning model that predicts property prices with high accuracy. Users can input a wide range of property features—such as location, area, number of bedrooms, and luxury amenities—to receive an estimated market value.

### 2. 📈 Analysis Dashboard
An interactive dashboard providing a high-level visual analysis of the Gurgaon real estate market. It features charts and graphs on:
- Price distributions across different sectors.
- Property type concentrations (flats vs. houses).
- Trends in luxury and furnishing categories.

### 3. 🏡 Society Recommender System
A personalized recommendation engine to help users discover properties that match their specific needs. It uses a content-based filtering approach, allowing users to weigh the importance of:
- **Amenities & Facilities:** Similarity based on available top facilities.
- **Price & Configuration:** Similarity based on price range, area, and property type.
- **Location Advantages:** Similarity based on proximity to key landmarks.

### 4. 💡 Price Insights Module
An interactive tool that allows users to understand the financial impact of property features. Users can select a sector and dynamically adjust features like `built_up_area` or `bedRoom` count to see how these changes affect the estimated price relative to the sector's average.

---

## 🛠️ Tech Stack

- **Backend & ML:** Python, Pandas, NumPy, Scikit-learn
- **Web Framework:** Streamlit
- **Data Visualization:** Plotly, Matplotlib
- **Jupyter Notebook** for data cleaning, feature engineering, and model development.

---

## 📂 Project Structure

The project is organized for clarity and scalability:

├── data/                 # All data files (.csv, .pkl, .joblib)├── notebooks/            # Jupyter notebooks for analysis and modeling├── pages/                # Individual Streamlit pages for each module├── .gitignore            # Files to be ignored by Git├── Home.py               # The main landing page of the Streamlit app├── requirements.txt      # Python dependencies for the project└── README.md             # Project documentation
---

## ⚙️ Setup and Installation

To run this project locally, please follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
    cd YOUR_REPOSITORY
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run Home.py
    ```
    The application will open in your default web browser.

---

## 📊 Data & Notebooks

The `notebooks` directory contains the complete workflow of this project, from initial data exploration to final model training. The key stages include:
- **Data Cleaning:** Handling missing values, outliers, and inconsistencies.
- **Feature Engineering:** Creating advanced interaction features like `sector_avg_price` and `area_by_room` to improve model accuracy.
- **Model Development:** Training and evaluating multiple regression and recommendation models.
