# Financial Sentiment Radar 📈

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://financial-sentiment-radar.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/shamiquekhan/Financial-Sentiment-Radar)

**Bring Your Own Project (BYOP) — Evaluated Course Project**

### Academic Details
- **Course:** Fundamentals of AI and ML
- **Student Name:** Shamique Khan
- **Registration Number:** 25BAI10187
- **Faculty Mentor:** PRAKASH N.B Sir
- **Institution:** VIT Bhopal University
- **Branch/Program:** BTech CSE (AI & ML)
- **Live Deployment:** [Financial Sentiment Radar via Streamlit](https://financial-sentiment-radar.streamlit.app/)

---

## 1. 📌 Problem Context & Motivation

**The Problem:** Financial markets are highly sensitive to news. Retail investors and algorithmic trading systems are exposed to a continuous stream of market news, and manually interpreting the directional impact of this information is time-consuming and error-prone. 

**The Gap:** General-purpose sentiment models often misinterpret domain-specific phrases. For example, the phrase *"Company X cuts its debt by 20%"* includes words that look negative ("cuts", "debt") generically, but it is clearly a *positive* signal for financial health.

**The Solution:** A domain-aware AI system built with transformers, capable of classifying financial text into positive, neutral, or negative classes from an investor-centric perspective in real-time.

---

## 2. 🧠 Data & Model Architecture

### Dataset: FinancialPhraseBank
Baseline evaluation and validation employ the **FinancialPhraseBank (FPB)** dataset (`takala/financial_phrasebank`), utilizing the strictly vetted `sentences_75agree` configuration. This subset guarantees at least 75% agreement among multiple independent financial annotators, yielding ~3,400 high-quality training/testing examples.

### Machine Learning Journey
*   **Baseline Model (Classical ML):** Initially established using a **TF-IDF + Logistic Regression** pipeline (capped at `max_iter=1000` for high-dimensional convergence). While effective for basic keyword spotting, it failed to capture the nuanced, context-dependent expressions and long-range dependencies common in sophisticated financial writing.
*   **Transformer Model (FinBERT):** To overcome classical ML limitations, the project integrates **FinBERT (`ProsusAI/finbert`)**. Based on the intricate BERT architecture, FinBERT utilizes self-attention mechanisms to understand deep context, having been pre-trained on a massive financial corpus and fine-tuned specifically for three-class financial sentiment analysis.

---

## 3. 🔥 Key Features & Capabilities

Wrapped in a custom **Maximalist / Neo-Brutalist UI** (featuring high-contrast pure RGB layouts and tactile elements injected via CSS), the application offers three interaction modes:

1.  **Single-Snippet Mode:** Paste a financial headline to see the predicted sentiment, detailed class probabilities, and an automatically generated explanation. Features an **Uncertainty-Aware Decision Logic**, intelligently changing labels to *"Uncertain"* if model confidence drops below the user-defined threshold, preventing the system from overstating weak signals.
2.  **Analyze Article by URL:** Paste any live news URL (e.g., Bloomberg, CNBC). Utilizing the `newspaper3k` library, the app scrapes the DOM, isolates the core article body, logic-splits the text into individual sentences (mitigating FinBERT's strict 512-token limit), and maps a macro-sentiment distribution of the entire piece.
3.  **Batch CSV Inference:** Upload a `.csv` dataset of headlines. The system parses the rows, runs bulk inference, and provides downloadable aggregated statistical reports.

---

## 4. ⚙️ Technical Stack & Engineering Deployments

- **AI / NLP Pipeline:** Hugging Face `transformers` (FinBERT), `scikit-learn`, `torch`, `sentencepiece`
- **Web Scraping:** `newspaper3k`, `lxml_html_clean`, `re`
- **Frontend / Deployment:** `streamlit` with aggressive global UI caching (`@st.cache_resource`) to load the heavy 400MB+ models into memory exactly *once*, bypassing cold-start constraints.

**Key Engineering Challenges Overcome:**
*   **Pipeline Output Format Changes:** Handled nested dictionary APIs (`[[{label, score}]]` dynamically using defensive OOP programming (using `isinstance()` checks) to ensure the inference module would not break under Hugging Face version updates.
*   **Context Length Limitations:** Re-engineered the URL analysis engine into a sliding window chunking algorithm since deep learning Transformers throw runtime exceptions if fed raw text over `max_length`.

---

## 5. 🚀 Setup & Installation Guide

Someone who has never seen this project can easily run it by following these commands:

### Prerequisites
- Python 3.9+
- Git

### Installation Steps
```bash
# 1. Clone the Repository
git clone https://github.com/shamiquekhan/Financial-Sentiment-Radar.git
cd Financial-Sentiment-Radar

# 2. Create and Activate a Virtual Environment
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate.ps1
# Mac/Linux:
# source .venv/bin/activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Run the Application locally
streamlit run streamlit_app.py
```
The app will automatically launch in your browser at `http://localhost:8501`.

---

## 6. 💡 Lessons Learned

This project bridged the gap between theory and practical application:
1.  **Transformers vs Classical NLP:** Demonstrated precisely why Attention-based language models drastically outperform TF-IDF algorithms on domain-specific ambiguity.
2.  **Production Realities:** Highlighted the complexities of moving from a Jupyter Notebook to a deployed full-stack application—handling asynchronous UI rendering, hardware memory limits, dependency parsing, and inference caching.
3.  **Graceful Fallbacks:** Showcased the paramount importance of AI systems admitting uncertainty. In finance, designing a model that says *"I don't know"* is safer than confident hallucination.
4.  **UX/UI in Python:** Leveraged custom un-safe CSS injection natively inside Streamlit to build a visual aesthetic that stands out heavily from standard, template-driven dashboards.

---
*Developed for the VIT Bhopal BYOP Capstone. All code is fully open-source and academically cited.*