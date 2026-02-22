import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.set_page_config(
    page_title="Thunderstorm Predictor",
    page_icon="⛈️",
    layout="centered",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main > div { max-width: 800px; margin: auto; }

    .hero {
        text-align: center;
        padding: 2rem 1rem 1rem;
    }
    .hero h1 {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .hero p {
        color: #94a3b8;
        font-size: 1.05rem;
    }

    .section-label {
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #6366f1;
        margin-bottom: 0.6rem;
    }

    div.stButton > button {
        width: 100%;
        padding: 0.75rem 1.5rem;
        font-size: 1.05rem;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: #fff;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.35);
    }

    .result-card {
        border-radius: 16px;
        padding: 1.8rem;
        text-align: center;
        margin-top: 1.5rem;
    }
    .result-storm {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        border: 1px solid #fca5a5;
    }
    .result-clear {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 1px solid #86efac;
    }
    .result-icon { font-size: 3rem; margin-bottom: 0.5rem; }
    .result-label {
        font-size: 1.4rem;
        font-weight: 700;
    }
    .result-storm .result-label { color: #dc2626; }
    .result-clear .result-label { color: #16a34a; }
    .result-prob {
        font-size: 0.95rem;
        color: #64748b;
        margin-top: 0.3rem;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>⛈️ Thunderstorm Predictor</h1>
    <p>Enter atmospheric indices to predict thunderstorm occurrence</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

FIELDS = [
    ("SWEAT_index",                "SWEAT Index",                  "Severe Weather Threat index"),
    ("K_index",                    "K Index",                      "Thunderstorm potential index"),
    ("Totals_totals_index",        "Totals Totals Index",          "Vertical totals + cross totals"),
    ("Environmental_Stability",    "Environmental Stability",      "Atmospheric stability measure"),
    ("Moisture_Indices",           "Moisture Indices",             "Moisture availability measure"),
    ("Convective_Potential",       "Convective Potential",         "Convective energy estimate"),
    ("Temperature_Pressure",       "Temperature & Pressure",       "Temp-pressure interaction"),
    ("Moisture_Temperature_Profiles","Moisture-Temp Profiles",     "Combined moisture-temp profile"),
]

st.markdown('<p class="section-label">Atmospheric Parameters</p>', unsafe_allow_html=True)

values = {}
col1, col2 = st.columns(2, gap="large")
for i, (key, label, help_text) in enumerate(FIELDS):
    with (col1 if i % 2 == 0 else col2):
        values[key] = st.number_input(label, value=0.0, format="%.4f", help=help_text, key=key)

st.markdown("")
predict_clicked = st.button("Predict Thunderstorm")

if predict_clicked:
    with st.spinner("Analyzing atmospheric conditions..."):
        try:
            response = requests.post(API_URL, json=values, timeout=10)

            if response.status_code == 200:
                result = response.json()
                pred = result["prediction"]
                prob = result.get("probability")

                if pred == 1:
                    icon, label, css_class = "⛈️", "Thunderstorm Likely", "result-storm"
                else:
                    icon, label, css_class = "☀️", "No Thunderstorm", "result-clear"

                prob_text = f"{prob * 100:.1f}% probability" if prob is not None else ""

                st.markdown(f"""
                <div class="result-card {css_class}">
                    <div class="result-icon">{icon}</div>
                    <div class="result-label">{label}</div>
                    <div class="result-prob">{prob_text}</div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("View input summary"):
                    for key, label, _ in FIELDS:
                        st.markdown(f"**{label}:** `{values[key]}`")
            else:
                st.error(f"API returned status {response.status_code}. Make sure the FastAPI backend is running.")

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the API. Start the FastAPI backend first:\n\n`uvicorn api.main:app --reload`")
        except requests.exceptions.Timeout:
            st.error("Request timed out. The API server might be overloaded.")

st.markdown('<div class="footer">Thunderstorm Prediction ML &mdash; KNN Model</div>', unsafe_allow_html=True)
