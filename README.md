# Financial Sentiment Radar 📈

**Fundamentals of AI and ML Evaluated Course Project — Bring Your Own Project (BYOP)**

### Student Details
- **Name:** Shamique Khan
- **Registration No:** 25bai10187
- **Institution:** VIT Bhopal
- **Branch/Program:** BTech CSE AIML

---

## 📌 Project Overview

**The Problem:** Financial markets are highly sensitive to news. Traders, retail investors, and financial analysts are constantly flooded with news articles, earning reports, and economic updates. Manually reading and interpreting the sentiment—whether news is bullish (positive), bearish (negative), or neutral—is time-consuming and subjective.

**The Solution:** The **Financial Sentiment Radar** is an AI-powered web application that automates the extraction and sentiment analysis of financial text. Built using **FinBERT** (a Transformer model specifically fine-tuned on financial data), the application can accurately evaluate the sentiment of single headlines, batch CSV datasets, and full live articles fetched via URL. 

This project demonstrates the practical application of NLP (Natural Language Processing), Machine Learning pipelines, and modern web application development to solve a real-world financial information-overload problem.

---

## 🔥 Key Features

1. **Single Headline Analysis:** Paste a snippet of financial text or select from predefined examples to get an instant sentiment prediction with detailed confidence scores.
2. **Batch Analysis via CSV:** Upload a `.csv` file containing hundreds of headlines to run bulk inference. The app aggregates the overall sentiment distribution and lets you download the results.
3. **Live Article URL Extraction:** Enter a URL from sites like CNBC, Reuters, or Bloomberg. The app automatically scrapes the article, splits it into sentences, and provides a sentence-by-sentence NLP breakdown.
4. **Uncertainty Threshold:** A dynamic slider allows users to define how confident the model must be. If the model's confidence falls below the threshold, it smartly labels the text as "Uncertain."
5. **Maximalist UI Design:** Features a bold, high-contrast, Brutalist/Maximalist aesthetic (pure RGB colors, heavy borders, instant snap effects) powered by custom CSS over Streamlit.

---

## ⚙️ Technical Stack

- **AI/ML:** Hugging Face `transformers` (FinBERT), `scikit-learn`, `torch`, `sentencepiece`
- **Data Extractor & NLP:** `newspaper3k` (for web scraping), `lxml_html_clean`, `re` (regex)
- **Data Manipulation:** `pandas`, `numpy`
- **Frontend Framework:** `streamlit`

---

## 🚀 Setup & Installation

Follow these steps to run the application locally. Someone who has never seen this project should be able to run it flawlessly by following this guide.

### Prerequisites
- Python 3.9 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/shamiquekhan/Financial-Sentiment-Radar.git
cd Financial-Sentiment-Radar
```

### 2. Create and Activate a Virtual Environment
It is best practice to run this inside an isolated virtual environment.
**On Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(Note: If you are on Mac/Linux, run `source .venv/bin/activate` instead)*

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Launch the Streamlit web server:
```bash
streamlit run streamlit_app.py
```
The app will automatically open in your default web browser at `http://localhost:8501`.

---

## 📖 How to Use the App

The app is divided into three main tabs:
1. **Single Headline:** The default screen. Type or paste your text into the magenta input box and click **"Analyze sentiment"**. The panel on the right will display the dominant sentiment, confidence percentage, a horizontal chart of all class probabilities, and a human-readable explanation of why the model chose that label.
2. **Batch Analysis:** Switch to this tab to upload a structured CSV file. The app will auto-detect your text column, process every row, and generate a downloadable aggregated report alongside a visual distribution chart.
3. **Analyze Article by URL:** Paste a valid news URL. The web scraper will download the author data, publish date, and full text, break it down logically, and evaluate the sentiment bias sentence by sentence.

---

## 📁 Project Structure

```text
Financial-Sentiment-Radar/
│
├── app/
│   ├── __init__.py
│   ├── config.py       # Configuration variables (Model selection, App Titles)
│   ├── model.py        # Core ML logic, pipeline building, threshold math, scraping
│   └── ui.py           # Maximalist CSS injection
│
├── notebooks/
│   └── EDA_and_eval.ipynb # Jupyter notebook showcasing baseline model evaluations
│
├── report/
│   └── BYOP_report.md  # Detailed reflection report for the BYOP capstone
│
├── streamlit_app.py    # Main UI entrypoint for the Streamlit dashboard
├── requirements.txt    # Python package dependencies
└── README.md           # You are here!
```

---
*Developed for the AI and ML Fundamentals Course Project.*