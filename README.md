# Financial News Sentiment Radar

Minimal Streamlit app for financial sentiment classification using a pretrained Hugging Face FinBERT model.

## Features
- Sentiment prediction for a headline/snippet (`positive`, `neutral`, `negative`)
- Confidence bars for all classes
- Swiss-style minimal UI
- Session history for recent predictions

## Model
Default model in this project:
- `kdave/FineTuned_Finbert`

You can switch model by editing `MODEL_NAME` in `app/config.py`.

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
streamlit run streamlit_app.py
```

## Optional evaluation notebook
Use `notebooks/EDA_and_eval.ipynb` to:
- load FinancialPhraseBank
- run quick benchmark/evaluation
- inspect label distribution

## Project structure
```text
app/
  __init__.py
  config.py
  model.py
  ui.py
streamlit_app.py
notebooks/EDA_and_eval.ipynb
requirements.txt
README.md
```
