# 🏸 Badminton Stringing Analysis Dashboard

## 🚀 Live App

[View the GitHub Pages dashboard](https://Brandonlee-2002.github.io/Stringing-Analysis/)

---

## 📌 Overview

This project analyzes badminton stringing data to uncover trends in racket usage, string preferences, and tension patterns. It turns raw stringing logs into an interactive dashboard that runs entirely in the browser.

---

## 🎯 Key Features

* 📊 Interactive browser-based dashboard hosted on GitHub Pages
* 🎾 Racket and string popularity analysis
* 📈 Tension distribution and trends over time
* 👥 Gender-based comparisons
* 🚨 Outlier detection using the IQR method
* 🔍 Dynamic filtering by gender, racket, and string
* 🔐 Privacy-safe data with names and internal notes excluded from the UI and downloads

---

## 🧠 Insights Generated

* Identification of the most popular rackets and strings
* Average and median string tension patterns
* Differences in tension preferences across player groups
* Detection of extreme stringing behaviors and outliers

---

## 🛠️ Tech Stack

* **HTML, CSS, and JavaScript**
* **SheetJS** for reading the workbook in-browser
* **Chart.js** for interactive visualizations
* **GitHub Pages + GitHub Actions** for static hosting

---

## 📂 Project Structure

```text
Stringing-Analysis/
├── index.html
├── app.js
├── styles.css
├── data/
│   └── stringing_data.csv
├── README.md
└── .github/
    └── workflows/
        └── deploy-pages.yml
```

---

## 🔒 Data Privacy

* Player names are removed from dashboard views and exports
* Internal notes are excluded from charts and the filtered CSV export
* The app is designed to avoid exposing sensitive customer data

---

## ⚙️ How to Run Locally

Serve the repository root with any local HTTP server, then open the app in a browser.

```bash
python3 -m http.server 8000
```

Then visit:
`http://localhost:8000/`

> The workbook is fetched by the browser, so opening `index.html` directly from disk is not supported.

---

## 🌐 Deployment on GitHub Pages

1. Push the repository to GitHub on the `main` branch.
2. Open the repository settings and select **Pages**.
3. Choose **GitHub Actions** as the deployment source.
4. The workflow in `.github/workflows/deploy-pages.yml` publishes the site automatically.

The current `data/stringing_data.csv` file is an Excel workbook saved with a `.csv` extension for compatibility with the existing dashboard URL. The browser reads the `String Log` worksheet directly with SheetJS.

---

## 💡 Future Improvements

* 🎯 Recommendation system for optimal string setup
* 🤖 Machine learning model for tension prediction
* 📊 Anonymized player-retention analytics
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
