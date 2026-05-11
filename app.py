import streamlit as st
import pandas as pd
import joblib

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Student Performance System",
    page_icon="🎓",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "show_result" not in st.session_state:
    st.session_state.show_result = False

if "prediction" not in st.session_state:
    st.session_state.prediction = 0

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

html, body, [class*="css"] {
    background-color: #0B1120;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Main Container */
.block-container {
    padding-top: 0.8rem;
    padding-bottom: 1rem;
    max-width: 1200px;
}

/* Main Title */
.main-title {
    text-align: center;
    font-size: 34px;
    font-weight: 800;
    color: #00FFD1;
    margin-bottom: 6px;
}

/* Subtitle */
.sub-title {
    text-align: center;
    font-size: 15px;
    color: #94A3B8;
    margin-bottom: 20px;
}

/* Input Box */
.input-box {
    background: rgba(17, 24, 39, 0.9);
    padding: 22px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0px 0px 20px rgba(0,255,209,0.08);
}

/* Labels */
label {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: white !important;
    margin-bottom: 2px !important;
}

/* Compact Inputs */
.stSlider,
.stRadio,
.stSelectSlider {
    margin-bottom: 4px;
}

/* Radio Buttons */
div[role="radiogroup"] {
    background-color: #1E293B;
    padding: 5px 8px;
    border-radius: 10px;
    justify-content: space-around;
}

/* Columns */
div[data-testid="column"] {
    padding: 4px;
}

/* Predict Button */
.stButton > button {
    width: 100%;
    height: 55px;
    border: none;
    border-radius: 14px;
    background: linear-gradient(90deg, #00FFD1, #00BFFF);
    color: black;
    font-size: 20px;
    font-weight: bold;
    transition: 0.3s ease;
    margin-top: 12px;
}

.stButton > button:hover {
    transform: scale(1.02);
    color: white;
}

/* MODAL BACKGROUND */
.modal-container {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.6);
    z-index: 999;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* RESULT CARD */
.result-card {
    background: linear-gradient(135deg, #111827, #1E293B);
    width: 500px;
    padding: 35px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0px 0px 40px rgba(0,255,209,0.15);
    text-align: center;
}

/* Score */
.score-text {
    font-size: 75px;
    font-weight: 800;
    color: #00FFD1;
    margin-top: 10px;
    margin-bottom: 10px;
}

/* Recommendation */
.recommendation {
    margin-top: 20px;
    background-color: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 14px;
    color: #E2E8F0;
    line-height: 1.7;
    text-align: left;
}

/* Close Hint */
.close-text {
    margin-top: 15px;
    color: #94A3B8;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------

model = joblib.load("model.pkl")

# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">🎓 AI-Powered Student Performance System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Machine Learning Based Academic Performance Prediction</div>',
    unsafe_allow_html=True
)

# ---------------- INPUT SECTION ----------------

st.markdown("### 📚 Enter Student Details")

col1, col2 = st.columns(2)

# ---------------- LEFT COLUMN ----------------

with col1:

    hours = st.slider(
        "📖 Study Hours",
        1, 20, 5
    )

    attendance = st.slider(
        "🧾 Attendance Percentage",
        50, 100, 80
    )

    previous = st.slider(
        "📈 Previous Scores",
        40, 100, 70
    )

    tutoring = st.select_slider(
        "👨‍🏫 Tutoring Sessions",
        options=[0,1,2,3,4,5,6,7,8,9,10],
        value=2
    )

# ---------------- RIGHT COLUMN ----------------

with col2:

    resources = st.radio(
        "📚 Access to Resources",
        ["Low", "Medium", "High"],
        horizontal=True
    )

    parental = st.radio(
        "👨‍👩‍👧 Parental Involvement",
        ["Low", "Medium", "High"],
        horizontal=True
    )

    motivation = st.radio(
        "🔥 Motivation Level",
        ["Low", "Medium", "High"],
        horizontal=True
    )

    peer = st.radio(
        "🧑‍🤝‍🧑 Peer Influence",
        ["Low", "Medium", "High"],
        horizontal=True
    )

# ---------------- ENCODING ----------------

mapping = {
    "Low": 0,
    "Medium": 1,
    "High": 2
}

resources = mapping[resources]
parental = mapping[parental]
motivation = mapping[motivation]
peer = mapping[peer]

# ---------------- PREDICT BUTTON ----------------

if st.button("🚀 Predict Exam Score"):

    sample = pd.DataFrame([[
        hours,
        attendance,
        previous,
        tutoring,
        resources,
        parental,
        motivation,
        peer
    ]], columns=[
        'Hours_Studied',
        'Attendance',
        'Previous_Scores',
        'Tutoring_Sessions',
        'Access_to_Resources',
        'Parental_Involvement',
        'Motivation_Level',
        'Peer_Influence'
    ])

    prediction = model.predict(sample)[0]

    st.session_state.prediction = prediction
    st.session_state.show_result = True


# ---------------- RESULT POPUP ----------------

if st.session_state.show_result:

    prediction = st.session_state.prediction

    # STATUS + MESSAGE

    if prediction < 60:

        status = "⚠️ Below Average Performance"

        recommendation = """
- Increase study consistency

- Improve attendance

- Focus more on revision

- Reduce distractions
"""

        card_type = "error"

    elif prediction < 75:

        status = "📌 Average Performance"

        recommendation = """
- Practice regularly

- Improve weak subjects

- Maintain study routine

- Increase focus during study
"""

        card_type = "warning"

    else:

        status = "✅ Excellent Performance"

        recommendation = """
- Maintain your current routine

- Continue consistent practice

- Stay focused and disciplined

- Keep improving your academic skills
"""

        card_type = "success"

    # POPUP DIALOG

    @st.dialog("🎯 Prediction Result")

    def show_result():

        st.metric(
            label="Predicted Exam Score",
            value=f"{round(prediction)}"
        )

        if card_type == "error":
            st.error(status)

        elif card_type == "warning":
            st.warning(status)

        else:
            st.success(status)

        st.markdown("### 📋 Recommendations")

        st.markdown(recommendation)

        if st.button("Close"):

            st.session_state.show_result = False
            st.rerun()

    show_result()