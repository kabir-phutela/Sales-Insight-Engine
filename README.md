# 🛒 Product Stock Management System

An AI-powered data science project that predicts the number of product units a retailer should stock for a specific area and date. The system uses external factors such as weather conditions, holidays, death rate, festival craze, and online trends to generate accurate stock recommendations.

---

## 📁 Project Structure

stock_management_system/
├── data/
│ ├── raw/ # Raw input data (API + synthetic sales)
│ └── processed/ # Cleaned and merged dataset
├── pipeline/ # Data collection and feature pipeline scripts
├── model/ # Model training and saved model file
├── api/ # Flask backend API to serve predictions
├── frontend/ # Streamlit UI to input and view predictions
├── dashboard/ # Power BI or other analytics visualizations
├── utils/ # API keys and shared utility functions
├── generate_sales_data.py # Script to create synthetic internal sales
├── main_pipeline.py # Main data pipeline runner
├── requirements.txt # All dependencies
└── README.md 




---

## 🚀 Features

✅ Predicts product stock needed using ML  
✅ Considers real-world factors like weather, holidays, and trends  
✅ Synthetic sales generator for testing  
✅ Flask API for backend integration  
✅ Streamlit frontend for live interaction  
✅ Power BI dashboard for insights  

---

## 🔧 Technologies Used

- **Python 3.x**
- **Pandas, Scikit-learn, Joblib**
- **Requests, PyTrends**
- **Flask (API)**
- **Streamlit (Frontend)**
- **Power BI (Dashboard)**

---

