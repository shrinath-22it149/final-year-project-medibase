import os, sys, json
import warnings
warnings.filterwarnings("ignore")

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

import streamlit as st

st.set_page_config(
    page_title="Remedy Builder | MediPlant AI",
    page_icon="🥣",
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
.recipe-card{background:white;border-radius:14px;padding:22px;box-shadow:0 3px 12px rgba(0,0,0,.08);
  border-top:5px solid #2E8B57;margin-bottom:15px;}
.step-item{background:#f3f9f4;padding:12px 16px;border-radius:10px;margin:8px 0;border-left:4px solid #2E8B57;}
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
    st.page_link("pages/9_Dosha_Quiz.py",  label="🧘 Dosha Profiler")
    st.markdown("---")
    st.caption("Ayurvedic formulation chemistry relies on synergy (Samyoga) and carrier mediums (Anupana) to transport active phyto-molecules to target cellular tissues.")

st.title("🥣 Classical Ayurvedic Remedy & Formulation Builder")
st.markdown("Select a health condition to dynamically formulate **authentic poly-herbal Ayurvedic preparations** with exact ingredient ratios, preparation steps, and optimal vehicle carriers (Anupana).")
st.divider()

REMEDIES = {
    "Respiratory & Cold / Cough": {
        "title": "Kasashwasahara Kwatha (Chest Cleansing Decoction)",
        "formulation_type": "Kwatha (Decoction)",
        "anupana": "Raw Honey (Madhu) - added only after cooling",
        "timing": "Morning and Evening after food",
        "ingredients": [
            {"herb": "Tulsi Leaves", "ratio": 3, "unit": "leaves or grams", "action": "Antiviral, immunomodulator, bronchodilator"},
            {"herb": "Fresh Ginger (Adrak)", "ratio": 2, "unit": "grams crushed", "action": "Burns metabolic mucus (Ama), relieves coughing fits"},
            {"herb": "Vasaka (Malabar Nut)", "ratio": 2, "unit": "grams dried or 4 fresh leaves", "action": "Vasicine liquefies viscous bronchial phlegm"},
            {"herb": "Cinnamon / Clove", "ratio": 1, "unit": "gram", "action": "Antimicrobial essential oils clearing throat irritation"}
        ],
        "instructions": [
            "Coarsely crush the fresh Tulsi, Ginger, Vasaka, and Cinnamon.",
            "Add 400 ml (2 cups) of clean water to a non-reactive stainless steel or clay pot.",
            "Simmer over low-medium heat until the liquid reduces to 100 ml (1/4th original volume).",
            "Strain the warm decoction through a fine sieve.",
            "Allow the decoction to cool until lukewarm, then stir in 1 teaspoon of raw honey (Never add honey to boiling liquid)."
        ]
    },
    "Hyperacidity, Gastritis & Heartburn": {
        "title": "Amlapitta Shaman Churna (Cooling Gastric Balancer)",
        "formulation_type": "Churna / Infusion",
        "anupana": "Lukewarm Water or Coconut Water",
        "timing": "Before lunch and dinner on empty stomach",
        "ingredients": [
            {"herb": "Coriander Seeds (Dhania)", "ratio": 2, "unit": "teaspoons", "action": "Cools gastric Pitta fire, relieves burning sensations"},
            {"herb": "Licorice Root (Yashtimadhu)", "ratio": 1, "unit": "teaspoon powder", "action": "Coats and heals duodenal mucosal ulcerations"},
            {"herb": "Amla (Indian Gooseberry)", "ratio": 1, "unit": "teaspoon powder", "action": "Bio-stable antioxidant balancing stomach acid"},
            {"herb": "Fennel / Cardamom Seeds", "ratio": 1, "unit": "teaspoon", "action": "Carminative easing upper abdominal spasm"}
        ],
        "instructions": [
            "Coarsely grind coriander seeds and fennel.",
            "Combine with Licorice and Amla powder in a clean glass bowl.",
            "For cold infusion (Hima): Soak 1 tablespoon of this blend in 1 glass of room-temperature water overnight.",
            "In the morning, gently strain through a clean muslin cloth and drink on an empty stomach."
        ]
    },
    "Insomnia, Nervous Stress & Mental Exhaustion": {
        "title": "Nidrajanak Ksheerapaka (Sleep & Neuro-Restorative Medicated Milk)",
        "formulation_type": "Ksheerapaka (Medicated Milk Decoction)",
        "anupana": "Pure A2 Cow Milk or Almond Milk",
        "timing": "30-45 minutes before bedtime",
        "ingredients": [
            {"herb": "Ashwagandha Root Powder", "ratio": 3, "unit": "grams", "action": "Reduces cortisol, sedates overactive autonomic nervous system"},
            {"herb": "Brahmi / Shankhpushpi", "ratio": 2, "unit": "grams", "action": "Calms mental chatter, protects acetylcholine synaptic transmission"},
            {"herb": "Cardamom Pods", "ratio": 1, "unit": "crushed pod", "action": "Eases digestion of whole milk proteins"},
            {"herb": "Nutmeg (Jaiphal)", "ratio": 0.5, "unit": "pinch", "action": "Classical Ayurvedic natural hypnotic easing sleep onset"}
        ],
        "instructions": [
            "In a saucepan, mix 150 ml of milk with 150 ml of water.",
            "Add Ashwagandha, Brahmi, and crushed cardamom.",
            "Simmer on low heat until the water completely evaporates and only 150 ml of medicated milk remains.",
            "Remove from heat, strain into a mug, stir in a tiny pinch of nutmeg and 1/2 teaspoon of pure ghee.",
            "Sip slowly while warm in a dim, tech-free environment."
        ]
    },
    "Joint Pain, Arthritis & Musculoskeletal Stiffness": {
        "title": "Sandhivata Shoola Haran Taila / Lepa (Transdermal Joint Oil & Paste)",
        "formulation_type": "Lepa (Topical Paste) / Oil Infusion",
        "anupana": "Warm Sesame Oil or Castor Oil",
        "timing": "Apply topically twice daily",
        "ingredients": [
            {"herb": "Turmeric Root Powder", "ratio": 2, "unit": "tablespoons", "action": "Curcumin suppresses inflammatory COX-2 and TNF-alpha"},
            {"herb": "Dry Ginger Powder (Sunthi)", "ratio": 1, "unit": "tablespoon", "action": "Promotes local blood circulation to stiff joints"},
            {"herb": "Castor Oil (Eranda Taila)", "ratio": 3, "unit": "tablespoons", "action": "Ricinoleic acid penetrates deep joint capsule to pacify Vata"},
            {"herb": "Rock Salt (Saindhava Lavana)", "ratio": 0.5, "unit": "teaspoon", "action": "Opens dermal pores to facilitate herbal absorption"}
        ],
        "instructions": [
            "Warm the Castor oil gently in a double boiler (do not overheat).",
            "Whisk in Turmeric, Dry Ginger powder, and fine rock salt to form a smooth golden paste.",
            "Gently massage the warm paste over aching knees, wrists, or spine in circular motions for 5 minutes.",
            "Cover with a warm dry towel or heating pad for 20 minutes to drive herbal constituents into tissue.",
            "Rinse off with warm water."
        ]
    },
    "Skin Detox, Acne & Blood Purification": {
        "title": "Raktashodhaka Lepa & Kashayam (Dermal Clarification Remedy)",
        "formulation_type": "Lepa (Facial Mask) & Internal Cleanser",
        "anupana": "Pure Rose Water (External) / Warm Water (Internal)",
        "timing": "Apply mask twice weekly; drink infusion in the morning",
        "ingredients": [
            {"herb": "Neem Leaf Powder", "ratio": 2, "unit": "teaspoons", "action": "Broad-spectrum antibacterial eradicating acne bacteria"},
            {"herb": "Manjistha (Indian Madder)", "ratio": 1, "unit": "teaspoon", "action": "Dissolves micro-vascular blood stagnation and pigment spots"},
            {"herb": "Sandalwood (Chandanam)", "ratio": 1, "unit": "teaspoon", "action": "Soothes burning inflammation and tightens pores"},
            {"herb": "Aloe Vera Gel", "ratio": 2, "unit": "tablespoons", "action": "Hydrating matrix that prevents skin dryness"}
        ],
        "instructions": [
            "In a small ceramic bowl, mix Neem, Manjistha, and Sandalwood powder.",
            "Blend with fresh transparent Aloe Vera gel and 1 teaspoon of pure rose water until a creamy paste forms.",
            "Cleanse the face with lukewarm water and apply an even layer, avoiding the delicate eye area.",
            "Leave on for 15-20 minutes until semi-dry (do not allow it to crack completely).",
            "Rinse gently with cool water and pat dry."
        ]
    }
}

c_cond, c_days = st.columns([2, 1])
with c_cond:
    chosen_condition = st.selectbox("🎯 Select Therapeutic Indication:", list(REMEDIES.keys()))
with c_days:
    days = st.slider("🗓️ Batch Duration (Days):", min_value=1, max_value=14, value=3)

rem = REMEDIES[chosen_condition]

st.markdown(f"""
<div class="recipe-card">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <h2 style="color:#2E8B57;margin:0;">🌿 {rem['title']}</h2>
    <span style="background:#2E8B57;color:white;padding:5px 14px;border-radius:12px;font-weight:bold;">
      {rem['formulation_type']}
    </span>
  </div>
  <p style="margin-top:10px;color:#555;"><strong>Optimal Anupana (Carrier Vehicle):</strong> {rem['anupana']} | <strong>Dosage Timing:</strong> {rem['timing']}</p>
</div>
""", unsafe_allow_html=True)

col_ing, col_steps = st.columns([1, 1], gap="large")

with col_ing:
    st.subheader(f"⚖️ Scaled Ingredient Formulation ({days} Day{'s' if days > 1 else ''})")
    for ing in rem["ingredients"]:
        scaled_qty = round(ing["ratio"] * days, 1)
        st.markdown(f"""
        <div style="background:white;padding:12px 16px;border-radius:10px;margin-bottom:8px;box-shadow:0 1px 4px rgba(0,0,0,.08);border-left:4px solid #3CB371;">
          <div style="display:flex;justify-content:space-between;">
            <strong>🌿 {ing['herb']}</strong>
            <span style="color:#2E8B57;font-weight:bold;">{scaled_qty} {ing['unit']}</span>
          </div>
          <span style="font-size:0.85em;color:#666;">Action: {ing['action']}</span>
        </div>
        """, unsafe_allow_html=True)

with col_steps:
    st.subheader("📋 Step-by-Step Preparation Protocol")
    for i, step in enumerate(rem["instructions"]):
        st.markdown(f"""
        <div class="step-item">
          <strong>Step {i+1}:</strong> {step}
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Printable prescription card
remedy_text = f"""==================================================
        MEDIPLANT AI - AYURVEDIC FORMULATION
==================================================
Condition: {chosen_condition}
Formulation: {rem['title']}
Type: {rem['formulation_type']}
Carrier (Anupana): {rem['anupana']}
Timing: {rem['timing']}
Batch Duration: {days} Days

INGREDIENTS:
"""
for ing in rem["ingredients"]:
    remedy_text += f"- {ing['herb']}: {round(ing['ratio'] * days, 1)} {ing['unit']} ({ing['action']})\n"

remedy_text += "\nPREPARATION PROTOCOL:\n"
for i, step in enumerate(rem["instructions"]):
    remedy_text += f"{i+1}. {step}\n"

remedy_text += "\n==================================================\nAlways consult a registered B.A.M.S Ayurvedic practitioner."

st.download_button(
    "📥 Download Ayurvedic Recipe Card (TXT)",
    data=remedy_text,
    file_name=f"{chosen_condition.replace(' ', '_')}_remedy_card.txt",
    mime="text/plain",
    use_container_width=True
)
