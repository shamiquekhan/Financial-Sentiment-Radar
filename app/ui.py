from app.config import APP_SUBTITLE, APP_TITLE

SWISS_CSS = """
<style>
/* Vibrant Block / Maximalist Theme */
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Space+Grotesk:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
}

/* Base background: high contrast loud color */
.stApp {
    background-color: #FAFAFA !important;
    color: #000000 !important;
    background-image: radial-gradient(#000 1px, transparent 1px);
    background-size: 20px 20px;
}

.main > div {
    max-width: 1200px;
    margin: 0 auto;
}

/* Massive typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Archivo Black', sans-serif !important;
    color: #000000 !important;
    text-transform: uppercase;
    line-height: 1.1;
}

h1 {
    font-size: 4rem;
    letter-spacing: -2px;
    margin-bottom: 0.5rem;
    text-shadow: 4px 4px 0px #FF00FF, 8px 8px 0px #00FFFF;
}

/* Solid blocks with thick black borders */
.swiss-card {
    background-color: #FF00FF; /* Magenta for all cards to match the screenshot */
    border: 4px solid #000000;
    box-shadow: 8px 8px 0px #000000;
    padding: 1.5rem 1.75rem;
    margin-bottom: 2rem;
    border-radius: 0;
    transition: transform 0.1s, box-shadow 0.1s;
    color: #000000;
}

/* Ensure text inside cards is black */
.swiss-card h1, .swiss-card h2, .swiss-card h3, .swiss-card h4, .swiss-card h5, .swiss-card p, .swiss-card label {
    color: #000000 !important;
}

.swiss-subtitle {
    border-top: 4px solid #000000;
    padding-top: 1rem;
    margin-top: 0.5rem;
    font-size: 1.5rem;
    font-weight: 700;
    background-color: #FFFF00;
    display: inline-block;
    padding: 0.5rem 1rem;
    border: 4px solid #000;
    box-shadow: 4px 4px 0px #000;
    transform: rotate(-2deg);
}

/* Aggressive Buttons */
.stButton > button {
    background-color: #FFDD00 !important;
    border: 4px solid #000000 !important;
    border-radius: 0 !important;
    color: #000000 !important;
    font-family: 'Archivo Black', sans-serif;
    font-size: 1.2rem;
    text-transform: uppercase;
    padding: 0.75rem 1.5rem;
    box-shadow: 6px 6px 0px #000000;
    transition: all 0s !important; /* Instant snap */
}

.stButton > button:hover {
    background-color: #00FFFF !important;
    color: #000000 !important;
    transform: translate(6px, 6px);
    box-shadow: 0px 0px 0px #000000;
}

.stButton > button:active {
    background-color: #FF0055 !important;
}

/* Sidebar - pure RGB contrast */
section[data-testid="stSidebar"] {
    background-color: #FF00FF !important;
    border-right: 4px solid #000000;
}
section[data-testid="stSidebar"] * {
    color: #000000 !important;
    font-weight: 700;
}

/* Inputs / text area */
.stTextArea textarea, .stTextInput input {
    background-color: #FFFFFF !important;
    border: 4px solid #000000 !important;
    border-radius: 0 !important;
    color: #000000 !important;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    box-shadow: 4px 4px 0px #000000;
    transition: all 0s;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    box-shadow: 8px 8px 0px #FF0055;
    background-color: #FFFF99 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 4px solid #000000;
}
.stTabs [data-baseweb="tab"] {
    color: #000000 !important;
    background: #CCCCCC;
    border: 4px solid #000000;
    border-bottom: none;
    margin-right: 4px;
    font-family: 'Archivo Black', sans-serif;
    text-transform: uppercase;
    font-size: 1.2rem;
    padding: 0.5rem 1rem;
    transition: none;
}
.stTabs [aria-selected="true"] {
    background-color: #00FFFF !important;
    border-bottom-color: transparent !important;
    box-shadow: inset 0 4px 0 #FF00FF;
}

/* Dataframe & tables */
.stDataFrame {
    border: 4px solid #000000;
    background-color: #FFFFFF !important;
    box-shadow: 8px 8px 0px #000000;
}

/* Sidebar Slider */
.stSlider div[data-testid="stThumbValue"] {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-family: 'Archivo Black', sans-serif;
}
.stSlider div[role="slider"] {
    background-color: #00FF66 !important;
    border: 4px solid #000000 !important;
    border-radius: 0;
    box-shadow: 4px 4px 0px #000000;
}
.stSlider div[data-testid="stTickBar"] {
    background-color: #000000 !important;
}

/* Progress bars / charts overrides could be minimal, 
   but let's do our best with Streamlit's constraints */
.stAlert {
    border: 4px solid #000000 !important;
    border-radius: 0 !important;
    box-shadow: 6px 6px 0px #000000 !important;
    color: #000000 !important;
    font-weight: 700;
}
.stAlert[data-testid="stAlert"] {
   background-color: #00FFFF !important;
}
</style>
"""


def hero_html() -> str:
    return f"""
    <div class=\"swiss-hero\">
        <h1>{APP_TITLE}</h1>
        <div class=\"swiss-subtitle\">
            <p>{APP_SUBTITLE}</p>
        </div>
    </div>
    """
