import os, sys, json
import warnings
warnings.filterwarnings("ignore")

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dosha Profiler | MediPlant AI",
    page_icon="🧘",
    layout="wide"
)

st.markdown("""
<style>
.main{background:#FAFFFE;}
h1,h2,h3{color:#2E8B57!important;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a3a2a,#2E8B57);}
section[data-testid="stSidebar"] *{color:white!important;}
div.stButton>button{background:linear-gradient(135deg,#2E8B57,#3CB371);
  color:white;border:none;border-radius:8px;font-weight:bold;}
.dosha-card{background:white;border-radius:14px;padding:20px;box-shadow:0 3px 10px rgba(0,0,0,.08);margin-bottom:15px;}
.vata-box{border-left:5px solid #4682B4;}
.pitta-box{border-left:5px solid #FF6B35;}
.kapha-box{border-left:5px solid #2E8B57;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🌿 MediPlant AI")
    st.markdown("---")
    st.page_link("app.py",                 label="🏠 Home")
    st.page_link("pages/1_Identify.py",    label="🔍 Identify Plant")
    st.page_link("pages/2_Database.py",    label="🌿 Plant Database")
    st.page_link("pages/8_Drug_Interactions.py", label="💊 Drug Interactions")
    st.markdown("---")
    st.caption("Ayurveda recognizes that each individual possesses a unique biological blueprint (Prakriti). Personalized herbal selection ensures harmony without aggravation.")

st.title("🧘 Ayurvedic Dosha (Prakriti) Diagnostic & Herb Matcher")
st.markdown("Discover your dominant biological constitution (**Vata**, **Pitta**, or **Kapha**) and find the exact medicinal plants tailored to restore your physiological equilibrium.")
st.divider()

# Load 50 plants
plants_path = os.path.join(_ROOT, "data", "plants_info.json")
try:
    with open(plants_path, "r", encoding="utf-8") as f:
        plants = json.load(f)["plants"]
except Exception:
    plants = []

# Questionnaire
st.subheader("📋 6-Step Ayurvedic Constitution Assessment")

q1 = st.radio("1. Physical Body Frame & Weight Tendency:", [
    "Vata: Slender, thin, light-boned, difficult to gain weight",
    "Pitta: Medium frame, athletic, proportionate, gains/loses weight easily",
    "Kapha: Broad, solid, sturdy frame, tends to gain weight easily and lose slowly"
], key="q1")

q2 = st.radio("2. Skin Texture & Temperature:", [
    "Vata: Dry, rough, thin, easily chilled hands and feet",
    "Pitta: Warm, sensitive, reddish, prone to freckles, acne or flushing",
    "Kapha: Smooth, soft, thick, cool, naturally oily and hydrated"
], key="q2")

q3 = st.radio("3. Appetite & Digestion (Agni):", [
    "Vata: Irregular; sometimes ravenous, sometimes forget to eat, prone to gas/bloating",
    "Pitta: Intense and strong; irritable if meals are skipped, prone to hyperacidity/heartburn",
    "Kapha: Steady and moderate; can easily skip meals, slow digestion, sluggishness after eating"
], key="q3")

q4 = st.radio("4. Emotional & Mental Disposition under Stress:", [
    "Vata: Mind races quickly, creative, easily anxious, restless, or fearful",
    "Pitta: Goal-oriented, sharp intelligence, easily irritated, frustrated, or impatient",
    "Kapha: Calm, forgiving, loyal, slow to react, prone to lethargy or stubbornness"
], key="q4")

q5 = st.radio("5. Sleep Quality:", [
    "Vata: Light, interrupted sleep; tendency to wake up between 2 AM - 4 AM",
    "Pitta: Moderate, sound sleep; wake up refreshed; intense, colorful dreams",
    "Kapha: Heavy, deep, prolonged sleep; difficulty waking up early morning"
], key="q5")

q6 = st.radio("6. Climate & Weather Preferences:", [
    "Vata: Dislikes cold, dry, windy weather; loves warmth and sunshine",
    "Pitta: Dislikes intense heat, direct summer sun, and humidity; thrives in cool breezes",
    "Kapha: Dislikes damp, cold, rainy weather; prefers dry warmth"
], key="q6")

if st.button("🔮 ANALYZE MY PRAKRITI & MATCH HERBS", type="primary", use_container_width=True):
    # Calculate scores
    answers = [q1, q2, q3, q4, q5, q6]
    v_score = sum(1 for a in answers if a.startswith("Vata"))
    p_score = sum(1 for a in answers if a.startswith("Pitta"))
    k_score = sum(1 for a in answers if a.startswith("Kapha"))
    total = len(answers)

    v_pct = round((v_score / total) * 100, 1)
    p_pct = round((p_score / total) * 100, 1)
    k_pct = round((k_score / total) * 100, 1)

    scores = {"Vata": v_score, "Pitta": p_score, "Kapha": k_score}
    dominant_dosha = max(scores, key=scores.get)

    st.success(f"✨ Assessment Complete! Your Dominant Constitution is **{dominant_dosha} ({max(v_pct, p_pct, k_pct)}%)**")

    # Chart & breakdown
    c_chart, c_desc = st.columns([1, 1])
    with c_chart:
        fig = go.Figure(data=[go.Pie(
            labels=["Vata (Air/Ether)", "Pitta (Fire/Water)", "Kapha (Earth/Water)"],
            values=[v_pct, p_pct, k_pct],
            hole=0.45,
            marker_colors=["#4682B4", "#FF6B35", "#2E8B57"]
        )])
        fig.update_layout(title="Your Prakriti Proportion", height=320, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with c_desc:
        if dominant_dosha == "Vata":
            st.markdown("""
            <div class="dosha-card vata-box">
              <h3>🌬️ Vata Dominance (Air + Space)</h3>
              <p><strong>Qualities:</strong> Cold, dry, light, subtle, mobile.</p>
              <p><strong>Goal:</strong> Nourish, warm, ground, and hydrate your nervous system and colon.</p>
              <p><strong>Key Balancing Herbs:</strong> Ashwagandha, Ginger, Shatavari, Licorice, Cardamom, Castor Oil.</p>
            </div>
            """, unsafe_allow_html=True)
        elif dominant_dosha == "Pitta":
            st.markdown("""
            <div class="dosha-card pitta-box">
              <h3>🔥 Pitta Dominance (Fire + Water)</h3>
              <p><strong>Qualities:</strong> Hot, sharp, light, oily, spreading.</p>
              <p><strong>Goal:</strong> Cool, pacify acidity, calm irritation, and support hepatic bile balance.</p>
              <p><strong>Key Balancing Herbs:</strong> Aloe Vera, Neem, Brahmi, Amla, Sandalwood, Rose, Shatavari, Manjistha.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="dosha-card kapha-box">
              <h3>🌱 Kapha Dominance (Earth + Water)</h3>
              <p><strong>Qualities:</strong> Heavy, slow, cool, oily, dense, stable.</p>
              <p><strong>Goal:</strong> Stimulate, warm, dry excess fluid, invigorate circulation, and stoke metabolic fire.</p>
              <p><strong>Key Balancing Herbs:</strong> Tulsi, Ginger, Turmeric, Pippali, Cinnamon, Kalmegh, Ajwain, Bibhitaki.</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.subheader(f"🌿 Curated 50-Plant Match for {dominant_dosha} Prakriti")

    # Filter herbs based on dosha
    d_key = dominant_dosha.lower()
    balancing_herbs = [p for p in plants if p.get("dosha", {}).get(d_key, "").startswith("Balances")]
    caution_herbs   = [p for p in plants if "Aggravates" in p.get("dosha", {}).get(d_key, "")]

    col_b, col_c = st.columns(2)
    with col_b:
        st.markdown(f"#### ✅ Best Herbs to Balance {dominant_dosha}")
        for p in balancing_herbs[:8]:
            st.markdown(f"""
            <div style="background:#eefbf0;padding:12px;border-radius:10px;margin-bottom:8px;border-left:4px solid #2E8B57;">
              <strong>🌿 {p['common_name']}</strong> (<em>{p['scientific_name']}</em>)<br>
              <span style="font-size:0.85em;color:#555;">{p.get('medicinal_uses', [''])[0]}</span>
            </div>
            """, unsafe_allow_html=True)

    with col_c:
        st.markdown(f"#### ⚠️ Herbs to Use with Caution in High Heat/Dose")
        if caution_herbs:
            for p in caution_herbs[:6]:
                st.markdown(f"""
                <div style="background:#fff6f3;padding:12px;border-radius:10px;margin-bottom:8px;border-left:4px solid #FF6B35;">
                  <strong>⚠️ {p['common_name']}</strong> (<em>{p['scientific_name']}</em>)<br>
                  <span style="font-size:0.85em;color:#555;">{p.get('warnings', ['Use in moderation'])[0]}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"Most general herbs are well-tolerated by {dominant_dosha} in moderate culinary and wellness doses.")
