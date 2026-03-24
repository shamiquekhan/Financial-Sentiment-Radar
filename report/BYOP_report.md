# Build Your Own Project (BYOP): Financial Sentiment Radar
## AI/ML Section Report

### 1. Problem Framing
The project addresses **3-class sentiment classification** for financial news text. Retail investors and trading systems often struggle to quickly interpret the sheer volume of market news. By automating sentiment detection, we can classify short news snippets or headlines into `positive`, `neutral`, or `negative` from an investor's perspective (i.e., whether the news is likely to drive asset prices up, have no effect, or drive them down).

### 2. Data and Annotations
For baseline evaluation and validation, we utilize the **FinancialPhraseBank (FPB)** dataset.
- **Source**: `takala/financial_phrasebank` (available on Hugging Face Datasets).
- **Scale and Quality**: It contains ~4.8k English sentences selected from financial news. We used the `sentences_75agree` configuration (~3.4k sentences), ensuring high-quality labels where at least 75% of the 16 finance expert annotators agreed on the sentiment.
- **Label Mapping**: The classes naturally map to: `0: negative`, `1: neutral`, and `2: positive`.

### 3. Baseline Model (Machine Learning)
To establish a performance floor, we developed a classical NLP pipeline using Scikit-Learn.
- **Features**: Term Frequency-Inverse Document Frequency (TF-IDF) vectorization, extracting unigrams and bigrams (`ngram_range=(1, 2)`).
- **Classifier**: Logistic Regression with an increased iteration limit (`max_iter=1000`) to ensure convergence.
- **Role**: This baseline gave us a foundational accuracy score and proved that while traditional keyword-based heuristics can identify obvious sentiment patterns, they often lack the contextual awareness needed for nuanced financial terminology.

### 4. Transformer Model: FinBERT
To improve on the baseline, the project relies on **FinBERT**, a domain-specific variant of the BERT architecture.
- **Model Selected**: `ProsusAI/finbert` (or `kdave/FineTuned_Finbert`). FinBERT was heavily pre-trained on large internal financial corpora and fine-tuned specifically for the FinancialPhraseBank dataset.
- **Why Transformer?**: Financial language is heavily context-dependent (e.g., "shortfall" or "cut" might be disastrous in one context but an expected policy adjustment in another). FinBERT's attention mechanisms capture these domain-specific semantic relationships perfectly.
- **Serving Configuration**: The model is executed with `top_k=None` (formerly `return_all_scores=True`) to return the probability distribution across all three classes, allowing the UI to display confidence bars rather than just a hard classification.

### 5. Serving Architecture
The application bridges the ML inference code with a fast, interactive user interface using **Streamlit**.
- **Caching**: Transformers can be extremely slow to load from disk. We use Streamlit's `@st.cache_resource` decorator on the `build_sentiment_pipeline()` function. This ensures the 400MB+ PyTorch model is loaded into memory only once upon startup.
- **Backend Wrapper**: The inference engine is neatly decoupled in `app/model.py`. The function `predict_sentiment()` takes the cached pipeline and raw text, performs the forward pass, and standardizes the label mapping before returning the normalized scores to the frontend.
- **Latency Handling**: The initial model loading introduces a 15-30s cold-start delay, but subsequent asynchronous inferences (via Streamlit's reactive reruns) execute in milliseconds.

### 6. Challenges, Limitations & Future Work
- **Domain Shift Constraints**: The base datasets like FPB are heavily leaning towards Western financial systems (e.g., Finnish or US markets). When applying this to specific localized markets (e.g., Indian RBI news context), slight sentiment mismatches can occur without localized fine-tuning.
- **Snippet Length Limitations**: BERT models strictly truncate input sequences (usually capping at 128 or 512 tokens). Passing full, lengthy articles requires a chunking/sliding-window aggregation architecture, which was not solved in this MVP.
- **Future Enhancements**: We plan to implement batch-processing allowing users to upload a `.csv` of headlines to retrieve average overarching market sentiment percentages.
