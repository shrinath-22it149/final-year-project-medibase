import os, sys, json
import warnings
warnings.filterwarnings("ignore")

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Drug-Herb Interactions | MediPlant AI",
    page_icon="💊",
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
.interaction-card{border-radius:14px;padding:22px;margin:15px 0;box-shadow:0 3px 12px rgba(0,0,0,.08);}
.safe-card{background:#d4edda;border-left:6px solid #28a745;}
.caution-card{background:#fff3cd;border-left:6px solid #ffc107;}
.warning-card{background:#ffeeba;border-left:6px solid #fd7e14;}
.critical-card{background:#f8d7da;border-left:6px solid #dc3545;}
.badge-pill{padding:4px 14px;border-radius:16px;font-weight:bold;font-size:0.85rem;color:white;display:inline-block;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🌿 MediPlant AI")
    st.markdown("---")
    st.page_link("app.py",                 label="🏠 Home")
    st.page_link("pages/1_Identify.py",    label="🔍 Identify Plant")
    st.page_link("pages/2_Database.py",    label="🌿 Plant Database")
    st.page_link("pages/5_Chatbot.py",     label="🤖 AI Chatbot")
    st.markdown("---")
    st.markdown("### ⚠️ Clinical Advisory")
    st.caption("This interaction engine cross-references Ayurvedic pharmacognosy with modern pharmacology. Always consult your prescribing physician before modifying medications.")

st.title("💊 Real-Time Drug-Herb Interaction & Safety Checker")
st.markdown("Check potential pharmacodynamic & pharmacokinetic interactions between **traditional medicinal herbs** and **prescription pharmaceuticals**.")
st.divider()

# Load interaction data
data_path = os.path.join(_ROOT, "data", "drug_interactions.json")
try:
    with open(data_path, "r", encoding="utf-8") as f:
        interactions_list = json.load(f)["interactions"]
except Exception:
    interactions_list = []

# Load plants
plants_path = os.path.join(_ROOT, "data", "plants_info.json")
try:
    with open(plants_path, "r", encoding="utf-8") as f:
        all_plants = [p["common_name"] for p in json.load(f)["plants"]]
except Exception:
    all_plants = ["Tulsi", "Neem", "Ginger", "Turmeric", "Ashwagandha", "Licorice", "Senna"]

c1, c2 = st.columns(2)
with c1:
    selected_herb = st.selectbox("🌿 Select Medicinal Herb:", sorted(all_plants), index=0)
with c2:
    med_options = [
        "All Medications (View Full Safety Profile)",
        "Warfarin / Aspirin / Clopidogrel (Blood Thinners)",
        "Metformin / Glimepiride / Insulin (Diabetes Medications)",
        "Digoxin (Heart Glycosides)",
        "Amlodipine / Telmisartan / Losartan (BP Medications)",
        "Furosemide / Hydrochlorothiazide (Diuretics)",
        "Omeprazole / Pantoprazole (Antacids / PPIs)",
        "Zolpidem / Alprazolam (Sedatives / Anxiolytics)",
        "Levothyroxine (Thyroid Medications)",
        "Cyclosporine / Tacrolimus (Immunosuppressants)",
        "Atorvastatin / Rosuvastatin (Cholesterol Statins)",
        "Paracetamol / Acetaminophen (Analgesics)",
        "Oral Contraceptives / Antibiotics"
    ]
    selected_med = st.selectbox("💊 Select Pharmaceutical Drug or Class:", med_options)

st.markdown("<br>", unsafe_allow_html=True)

# Find matching interactions
matched = []
for item in interactions_list:
    herb_match = item["herb"].lower() in selected_herb.lower() or selected_herb.lower() in item["herb"].lower()
    if not herb_match:
        continue
    
    if selected_med == "All Medications (View Full Safety Profile)":
        matched.append(item)
    else:
        med_key = selected_med.split(" (")[0].lower()
        if any(part.strip() in item["drug"].lower() or item["drug"].lower() in part.strip() for part in med_key.split("/")):
            matched.append(item)

if matched:
    st.subheader(f"⚠️ Clinical Safety Alerts for {selected_herb}")
    for item in matched:
        sev = item["severity"]
        scolor = item.get("severity_color", "#fd7e14")
        
        card_class = "caution-card"
        if sev.lower() in ["high"]: card_class = "warning-card"
        elif sev.lower() in ["critical"]: card_class = "critical-card"
        elif sev.lower() in ["low", "low (beneficial)"]: card_class = "safe-card"

        st.markdown(f"""
        <div class="interaction-card {card_class}">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <h3 style="margin:0;color:#222;">🌿 {item['herb']}  ⟷  💊 {item['drug']}</h3>
            <span class="badge-pill" style="background:{scolor};">{sev.upper()} RISK</span>
          </div>
          <p><strong>Clinical Category:</strong> {item['category']}</p>
          <hr style="border:0;border-top:1px solid rgba(0,0,0,0.1);margin:10px 0;">
          <p><strong>🔬 Pharmacological Mechanism:</strong><br>{item['mechanism']}</p>
          <p><strong>💡 Recommended Clinical Action:</strong><br>{item['recommendation']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.success(f"✅ **No documented severe contraindications** found between **{selected_herb}** and the selected medication.")
    st.info(f"🌿 **General Safety Note for {selected_herb}:** Culinary dietary amounts are generally safe. For therapeutic concentrated extracts, maintain at least a 2-hour interval between herbal intake and allopathic prescription doses.")

st.divider()

# Complete searchable matrix
st.subheader("📋 Comprehensive Drug-Herb Interaction Database")
with st.expander("🔍 View & Search Entire Interaction Matrix (All 16 Rules)", expanded=False):
    if interactions_list:
        df = pd.DataFrame(interactions_list)[["herb", "drug", "category", "severity", "mechanism", "recommendation"]]
        df.columns = ["Herb", "Pharmaceutical Drug", "Drug Class", "Risk Level", "Mechanism", "Action Guidance"]
        st.dataframe(df, use_container_width=True)
