# Project Report & Technical Documentation: Financial Sentiment Radar

**Course:** Fundamentals of AI and ML
**Student Name:** Shamique Khan
**Registration No:** 25bai10187
**Institution:** VIT Bhopal
**Branch/Program:** BTech CSE AIML

---

## 1. Introduction & Problem Statement

### 1.1 The Problem
In the modern financial ecosystem, raw data and news articles are generated at an unprecedented velocity. Retail investors, day traders, and financial analysts are constantly bombarded by headlines, earning reports, and macro-economic metrics. Identifying the underlying sentiment of this information—understanding whether an event is bullish (positive), bearish (negative), or neutral—is critical. However, manual sentiment analysis is slow, subjective, and practically impossible to scale across hundreds of daily news sources. 

### 1.2 Why It Matters
A delay in parsing financial news translates directly to missed market opportunities or unmitigated risks. Furthermore, standard language models (like general-purpose sentiment classifiers) frequently fail when applied to finance. For example, the phrase *"Company X cuts its debt by 20%"* contains a traditionally negative word ("cuts debt") but is undeniably a positive signal in a financial context. Solving this problem requires a **domain-specific AI model** integrated into a high-speed, user-friendly interface.

---

## 2. Our Approach: The Solution Architecture

To solve this, I developed the **Financial Sentiment Radar**, a full-stack AI/ML web application capable of classifying the sentiment of financial news in real-time.

### 2.1 The Machine Learning Pipeline
Instead of relying on basic keyword algorithms (like TF-IDF + Logistic Regression, which was used purely as an experimental baseline in our EDA), we transitioned to **Transformers**. 
- **Model Choice:** We utilized **FinBERT** (`ProsusAI/finbert`), a BERT-based language model fine-tuned entirely on a large financial corpus (Financial PhraseBank).
- **Classification Logic:** The pipeline analyzes raw text and returns probabilities across three absolute classes: **Positive, Negative, and Neutral**. 
- **Uncertainty Mapping:** A custom `decide_label` algorithm was engineered to handle edge cases. If the model's highest probability falls below a user-defined slider (e.g., `< 40%`) or if the gap between the top two probabilities is razor-thin, the system correctly overrides the prediction and labels it **"Uncertain"**, drastically reducing false positives in trading scenarios.

### 2.2 Data Scraping & Extraction Engine (`newspaper3k`)
A major hurdle was passing entire sprawling news articles into the FinBERT model, which has strict token limits (`max_length=512`). 
To overcome this:
1. We integrated **newspaper3k** to fetch the DOM, bypass clutter, and extract the raw body and metadata of any news URL.
2. We built an NLP token splitter (`split_into_sentences` via `re`) to divide the article logically into constituent sentences. 
3. The model iterates over each sentence, predicts its sentiment individually, and aggregates a macro-sentiment distribution for the article as a whole.

### 2.3 The Web Application (Streamlit)
To make the AI accessible, we wrapped the inference engine in a **Streamlit** dashboard. 
- **Caching (`@st.cache_resource`):** Injects the heavy ~400MB PyTorch model into global memory strictly once at startup, eliminating cold-start delays for subsequent inferences.
- **Batch Processing (`pandas`):** Allows users to upload a `.csv` file with hundreds of rows, iterating through them simultaneously to produce an aggregate analytical `.csv` report.

---

## 3. User Interface & Aesthetic Design

A vital part of the project was ensuring the interface did not look like a generic academic template. I implemented a custom **Maximalist / Neo-Brutalist API (Vibrant Block Design)** using injected CSS logic. 

**Design Decisions:**
- **Pure RGB High-Contrast Palette:** Featuring stark Magento (`#FF00FF`), Neon Greens (`#00FF66`), and Yellows (`#FFFF00`). 
- **Typography:** Heavyweight, oversized headers using *Archivo Black* coupled with *Space Grotesk* for technical data.
- **Tactile Inputs:** Hard borders (`4px solid #000`), aggressive black drop-shadows with zero blur, and no smooth transition times. Interacting with the buttons provides an instant, snappy layout shift reminiscent of vintage terminal blocks.

---

## 4. Key Decisions & Challenges Faced

### 4.1 Tokenizer and Pipeline Format Errors
**Challenge:** While executing `top_k=None` in modern Hugging Face pipelines to retrieve all three class probabilities simultaneously, the API started returning a nested list structure (`[[{label, score}]]`) instead of a flat list, crashing the dictionary mappings with `TypeError: string indices must be integers`.
**Decision:** We wrote defensive unpacking routines inside `app/model.py` (`predict_sentiment()`) that aggressively check variable instances (`isinstance(outputs, list)`) to flatten and catch raw outputs before formatting them for the UI.

### 4.2 Handling Overwhelming Context Limits
**Challenge:** FinBERT cannot digest a 2,000-word Bloomberg article in one pass due to a 512-token dimension limit. Passing the raw string directly resulted in index overflow errors.
**Decision:** Our custom web scraper solves this by splitting text logically using regex `r'(?<=[.!?]) +'`. Sentences under 10 characters are discarded as noise, and the remainder are processed sequentially. 

### 4.3 Environment & Dependency Handling
**Challenge:** Installing `newspaper3k` frequently throws dependency problems with modern `lxml` parsers on Windows. Model weights took too long to download on every execution.
**Decision:** Handled via `.venv` virtualization and locking the parser with `lxml_html_clean`. The model fallback strategy gracefully fails over if the primary model is unreachable.

---

## 5. What Was Learned

Through this Bring Your Own Project (BYOP), several pivotal concepts transitioned from theory into practice:
1. **Transformer Capabilities:** The leap in contextual understanding between standard ML (TF-IDF baselines) and Transformer models (attention mechanisms) in domain-specific tasks is monumental. Words that seem negative to classic ML algorithms are smoothly understood by FinBERT in a quantitative context.
2. **ML in Production:** Deploying a model is much more complex than evaluating it in a Jupyter Notebook. Managing memory caching, thread-safe asynchronous prediction in Streamlit, error handling for corrupted CSV text strings, and layout optimization are massive parts of a usable AI product.
3. **Data Provenance matters:** Implementing an explicit uncertainty threshold was critical because AI is never 100% precise; gracefully admitting uncertainty is an important system design pattern for financial software. 
4. **CSS-in-Python:** How to securely inject and force styling variables (`unsafe_allow_html`) across a standard Python abstraction layer to achieve aggressive UI aesthetics. 

---

## 6. Conclusion
The **Financial Sentiment Radar** successfully applies Natural Language Processing to alleviate information overload in the financial sector. The final product seamlessly extracts unstructured data from the web, leverages highly contextual machine learning inference, and packages the result into an aggressive, intuitive web interface—fully realizing the objectives set out in the Fundamental AI/ML course.