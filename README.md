# 🏸 Badminton Stringing Analysis Dashboard

## 🚀 Live App

[View the Streamlit Dashboard](https://your-app-name.streamlit.app)

---

## 📌 Overview

This project analyzes badminton stringing data to uncover trends in racket usage, string preferences, and tension patterns. It transforms raw stringing logs into an interactive dashboard for data-driven decision-making.

---

## 🎯 Key Features

* 📊 Interactive Streamlit dashboard
* 🎾 Racket and string popularity analysis
* 📈 Tension distribution and trends over time
* 👥 Gender-based comparisons
* 🚨 Outlier detection using IQR
* 🔍 Dynamic filtering (racket, string, gender)
* 🔐 Privacy-safe data using anonymized Player IDs

---

## 🧠 Insights Generated

* Identification of most popular rackets and strings
* Average and median string tension patterns
* Differences in tension preferences across player groups
* Detection of extreme stringing behaviors (outliers)

---

## 🛠️ Tech Stack

* **Python**
* **Pandas** (data processing)
* **Plotly** (visualizations)
* **Streamlit** (dashboard UI)

---

## 📂 Project Structure

```
Stringing-Analysis/
├── app.py
├── requirements.txt
├── data/
│   └── stringing_data.csv
├── images/
└── README.md
```

---

## 🔒 Data Privacy

* Player names are removed and replaced with anonymized `Player_ID`
* Internal notes are excluded from all visualizations and exports
* Designed with real-world data privacy considerations in mind

---

## ⚙️ How to Run Locally

```
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌐 Deployment

This app is deployed using **Streamlit Community Cloud**.

To deploy your own version:

1. Push code to GitHub
2. Connect repo on Streamlit Cloud
3. Select `app.py` as entry point
4. Deploy 🚀

---

## 💡 Future Improvements

* 🎯 Recommendation system for optimal string setup
* 🤖 Machine learning model for tension prediction
* 📊 Player-level analytics dashboard
* ⏱️ String durability tracking

---

## 📈 Resume Impact

Built an end-to-end data analytics project with:

* Data cleaning and preprocessing
* Exploratory data analysis
* Interactive dashboard development
* Privacy-aware data handling

---

## 🙌 Acknowledgments

This project is based on real-world badminton stringing data and reflects practical experience in sports analytics.
