import numpy as np
import pandas as pd
import streamlit as st
import re
from newspaper import Article

from app.config import DEFAULT_TEXT, EXAMPLES, MAX_HISTORY, MODEL_NAME
from app.model import build_sentiment_pipeline, predict_sentiment, decide_label, extract_article_from_url, split_into_sentences, analyze_article_sentences, summarize_article_results
from app.ui import SWISS_CSS, hero_html

st.set_page_config(
    page_title="Financial Sentiment Radar",
    page_icon="📈",
    layout="wide",
)

st.markdown(SWISS_CSS, unsafe_allow_html=True)
st.markdown(hero_html(), unsafe_allow_html=True)


@st.cache_resource
def load_model():
    return build_sentiment_pipeline()


def ensure_state():
    if "user_text" not in st.session_state:
        st.session_state.user_text = DEFAULT_TEXT
    if "history" not in st.session_state:
        st.session_state.history = []

def explain_result(final_label, all_scores, threshold):
    scores_dict = {item['label']: item['score'] for item in all_scores}
    sorted_scores = sorted(all_scores, key=lambda x: x['score'], reverse=True)
    top = sorted_scores[0]
    second = sorted_scores[1] if len(sorted_scores) > 1 else None

    if final_label == "uncertain":
        if top['score'] < threshold:
            return f"The model is uncertain because its top confidence ({top['score']:.2%}) is below the required threshold of {threshold:.2%}."
        elif second and (top['score'] - second['score']) < 0.1:
            return f"The model is uncertain because the gap between {top['label']} ({top['score']:.2%}) and {second['label']} ({second['score']:.2%}) is too narrow."

    if final_label == "positive":
        return f"The sentiment is clearly positive (driven by strong financial performance indicators or bullish language) with {top['score']:.2%} confidence."
    if final_label == "negative":
        return f"The sentiment is negative (suggesting bearish trends or financial risk) with {top['score']:.2%} confidence."
    if final_label == "neutral":
        return f"The sentiment is neutral (matter-of-fact reporting without strong directional bias) with {top['score']:.2%} confidence."

def sentiment_bar_chart(scores_list):
    df = pd.DataFrame(scores_list)
    df.set_index('label', inplace=True)
    st.bar_chart(df['score'], horizontal=True)


ensure_state()
sentiment_pipeline = load_model()

with st.sidebar:
    st.markdown("### Model Configuration")
    st.write(f"**Loaded:** {MODEL_NAME}")
    st.caption("Domain-specific transformer from Hugging Face")
    
    st.markdown("### Settings")
    confidence_threshold = st.slider(
        "Uncertainty Threshold", 
        min_value=0.0, max_value=1.0, value=0.4, step=0.05,
        help="If top prediction's confidence is below this, label is marked as 'uncertain'."
    )
    
    st.markdown("---")
    st.markdown("### Dataset Provenance 📚")
    st.caption("""
    **Training Data**: Financial PhraseBank (Malo et al., 2014)
    - 4,840 sentences from English-language financial news.
    - Annotated by 16 individuals with background in finance.
    - Goal: Determine sentiment from perspective of a retail investor.
    - Labels: Positive, Negative, Neutral.
    """)

tab1, tab2, tab3 = st.tabs(["Single Headline", "Batch Analysis", "Article URL"])

with tab1:
    left_col, right_col = st.columns([5, 7])

    with left_col:
        st.markdown("#### INPUT")
        with st.container(border=False):
            st.markdown('<div class="swiss-card">', unsafe_allow_html=True)

            st.session_state.user_text = st.text_area(
                "Paste a financial headline or short news snippet:",
                value=st.session_state.user_text,
                height=150,
                label_visibility="collapsed",
            )

            st.caption("Examples")
            example_cols = st.columns(len(EXAMPLES))
            for idx, example in enumerate(EXAMPLES):
                with example_cols[idx]:
                    if st.button(example, key=f"example_{idx}"):
                        st.session_state.user_text = example

            analyze = st.button("Analyze sentiment", type="primary")

            st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown("#### SENTIMENT")
        with st.container(border=False):
            st.markdown('<div class="swiss-card">', unsafe_allow_html=True)

            if analyze and st.session_state.user_text.strip():
                label, score, all_scores = predict_sentiment(
                    sentiment_pipeline, st.session_state.user_text
                )

                # Apply threshold
                display_label = label
                if score < confidence_threshold:
                    display_label = "uncertain"

                st.markdown(f"##### {display_label.upper()}")
                st.write(f"Confidence: {score:.2%}")
                
                # Show richer explanation
                st.info(explain_result(display_label, all_scores, confidence_threshold))

                # Render nice horizontal bar chart
                sentiment_bar_chart(all_scores)

                st.divider()
                st.markdown("##### Text")
                st.write(st.session_state.user_text)

                st.session_state.history.insert(
                    0,
                    {
                        "text": st.session_state.user_text,
                        "label": display_label,
                        "confidence": round(score, 4),
                    },
                )
                st.session_state.history = st.session_state.history[:MAX_HISTORY]
            else:
                st.write("Run an analysis to see model sentiment here.")

            st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("#### Recent Analyses")
        st.dataframe(st.session_state.history, use_container_width=True)

with tab2:
    st.markdown("#### BATCH ANALYSIS")
    with st.container(border=False):
        st.markdown('<div class="swiss-card">', unsafe_allow_html=True)
        st.write("Upload a `.csv` file containing a `text` or `headline` column.")
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                # Find the text column creatively
                text_col = None
                for col in df.columns:
                    if col.lower() in ("text", "headline", "sentence", "news"):
                        text_col = col
                        break
                
                if text_col is None:
                    st.error("Could not find a valid text column. Ensure your CSV has a column named 'text' or 'headline'.")
                else:
                    st.success(f"Found text column: `{text_col}`. Found {len(df)} rows.")
                    
                    if st.button("Run Batch Inference", type="primary"):
                        with st.spinner("Analyzing sentiments..."):
                            preds = []
                            for txt in df[text_col].dropna().astype(str):
                                lbl, sc, _ = predict_sentiment(sentiment_pipeline, txt[:512]) # Truncate heavily to prevent context length errors
                                if sc < confidence_threshold:
                                    lbl = "uncertain"
                                preds.append({"text": txt, "label": lbl, "confidence": round(sc, 4)})
                            
                            results_df = pd.DataFrame(preds)
                            
                            # Summary Metrics
                            st.divider()
                            st.markdown("##### Aggregate Sentiment")
                            sentiment_counts = results_df["label"].value_counts()
                            st.bar_chart(sentiment_counts)
                            
                            st.markdown("##### Preview")
                            st.dataframe(results_df.head(20), use_container_width=True)
                            
                            # Download button
                            csv_data = results_df.to_csv(index=False).encode("utf-8")
                            st.download_button(
                                label="Download Results as CSV",
                                data=csv_data,
                                file_name="sentiment_results.csv",
                                mime="text/csv",
                            )
                        
            except Exception as e:
                st.error(f"Error reading or processing file: {e}")

with tab3:
    st.markdown("#### ANALYZE ARTICLE BY URL")
    with st.container(border=False):
        st.markdown('<div class="swiss-card">', unsafe_allow_html=True)
        
        url_input = st.text_input("Enter a valid news article URL (e.g. from CNBC, Reuters, Bloomberg):", key="article_url")
        if st.button("Fetch and Analyze Article", type="primary"):
            if url_input.strip():
                with st.spinner("Fetching article and running analysis..."):
                    title, text, authors, pub_date = extract_article_from_url(url_input)
                    
                    if not title and not text:
                        st.error("Could not fetch or parse the article. Please check the URL or try another source.")
                    else:
                        st.success(f"**Title:** {title} | **Date:** {pub_date}")
                        st.caption(f"Authors: {', '.join(authors) if authors else 'Unknown'}")
                        
                        sentences = split_into_sentences(text)
                        st.info(f"Extracted {len(sentences)} sentences for analysis.")
                        
                        results = analyze_article_sentences(sentiment_pipeline, sentences, confidence_threshold)
                        summary = summarize_article_results(results)
                        
                        # Display summary chart
                        st.markdown("##### Overall Sentiment Distribution")
                        st.bar_chart({
                            "Positive": [summary["positive"]],
                            "Neutral": [summary["neutral"]],
                            "Negative": [summary["negative"]],
                            "Uncertain": [summary["uncertain"]]
                        })
                        
                        st.markdown("##### Sentence-by-Sentence Breakdown")
                        for r in results:
                            color = "gray"
                            if r["label"] == "positive": color = "green"
                            elif r["label"] == "negative": color = "red"
                            elif r["label"] == "uncertain": color = "orange"
                            
                            st.markdown(f"**[{r['label'].upper()}]** ({r['confidence']:.2%}) - :{color}[{r['sentence']}]")

            else:
                st.warning("Please enter a URL to continue.")
                
        st.markdown("</div>", unsafe_allow_html=True)

