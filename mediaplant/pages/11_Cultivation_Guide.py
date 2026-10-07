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
    page_title="Cultivation Guide | MediPlant AI",
    page_icon="🌱",
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
.guide-card{background:white;border-radius:14px;padding:20px;box-shadow:0 3px 10px rgba(0,0,0,.08);margin-bottom:15px;border-top:4px solid #2E8B57;}
.tag-badge{background:#e8f5e9;color:#2e7d32;padding:3px 10px;border-radius:12px;font-size:0.85em;font-weight:bold;display:inline-block;margin-right:5px;}
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
    st.page_link("pages/10_Remedy_Builder.py",   label="🥣 Remedy Builder")
    st.markdown("---")
    st.caption("Growing your own medicinal herb garden promotes sustainable biodiversity conservation and guarantees organic, pesticide-free therapeutic yields.")

st.title("🌱 Herbal Geo-Habitability & Home Cultivation Guide")
st.markdown("Detailed agronomic profiles, propagation methods, and soil/sunlight requirements to successfully cultivate **medicinal plants in home gardens, terrace pots, and farms**.")
st.divider()

# Load plants
plants_path = os.path.join(_ROOT, "data", "plants_info.json")
try:
    with open(plants_path, "r", encoding="utf-8") as f:
        plants = json.load(f)["plants"]
except Exception:
    plants = []

# Garden tier tabs
tab_single, tab_catalog, tab_tips = st.tabs(["🔍 Plant Cultivation Profile", "🌿 50-Herb Agronomic Matrix", "🏡 Balcony & Kitchen Garden Blueprint"])

with tab_single:
    plant_names = [p["common_name"] for p in plants]
    selected_name = st.selectbox("🌿 Select Medicinal Plant to Cultivate:", plant_names, index=0)

    selected_plant = next((p for p in plants if p["common_name"] == selected_name), None)

    if selected_plant:
        cult = selected_plant.get("cultivation", {})
        
        st.markdown(f"""
        <div class="guide-card">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <h2>🌿 {selected_plant['common_name']} (<em>{selected_plant['scientific_name']}</em>)</h2>
            <span class="tag-badge">Category: {selected_plant.get('category','Herb')}</span>
          </div>
          <p style="color:#555;"><strong>Native Range:</strong> {selected_plant.get('region','India')} | <strong>Availability:</strong> {selected_plant.get('availability','High')}</p>
        </div>
        """, unsafe_allow_html=True)

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("☀️ Sunlight", cult.get("sunlight", "6+ hrs direct sun"))
        k2.metric("💧 Water Needs", cult.get("water", "Moderate"))
        k3.metric("🌱 Soil Type", cult.get("soil", "Well-draining loam")[:22] + "...")
        k4.metric("🌡️ Climate Zone", cult.get("climate", "Tropical / Subtropical"))

        st.markdown("### 📋 Agronomic Guidelines")
        g1, g2 = st.columns(2)
        with g1:
            st.markdown(f"""
            **🌱 Soil & Nutrients:**
            * {cult.get('soil', 'Rich, porous, well-draining garden soil with compost.')}
            * **Recommended pH:** 6.2 - 7.4 (Neutral to slightly alkaline)
            * **Compost:** Add decomposed cow dung manure or vermicompost every 45 days.

            **💧 Irrigation Protocol:**
            * {cult.get('water', 'Moderate; allow topsoil to dry between watering.')}
            * Avoid water stagnation to prevent fungal root rot (Pythium/Phytophthora).
            """)
        with g2:
            st.markdown(f"""
            **☀️ Sunlight & Climate:**
            * {cult.get('sunlight', 'Requires bright natural sunlight.')}
            * **Ideal Temperature:** 20°C - 38°C
            * Protect from winter frost and harsh desiccating summer winds.

            **✂️ Harvesting & Pruning:**
            * Harvest mature leaves in the morning after dew has dried.
            * Pinch off apical flowering shoots to encourage bushy lateral leaf growth.
            """)

with tab_catalog:
    st.subheader("📊 50 Medicinal Plants Agronomic Matrix")
    matrix_data = []
    for p in plants:
        c = p.get("cultivation", {})
        matrix_data.append({
            "Plant": p["common_name"],
            "Scientific Name": p["scientific_name"],
            "Category": p.get("category", "Herb"),
            "Sunlight": c.get("sunlight", "Full Sun"),
            "Watering": c.get("water", "Moderate"),
            "Soil": c.get("soil", "Loamy"),
            "Climate": c.get("climate", "Tropical")
        })
    df_matrix = pd.DataFrame(matrix_data)
    st.dataframe(df_matrix, use_container_width=True)

with tab_tips:
    st.subheader("🏡 Beginner's Guide: Setting Up an Urban Ayurvedic Balcony Garden")
    
    c_easy, c_soil = st.columns(2)
    with c_easy:
        st.markdown("""
        #### 🌟 Top 5 Easiest Herbs for Balcony Pots
        1. **Tulsi (Holy Basil):** Needs 8-10 inch pot, 5 hours sunlight, everyday water.
        2. **Mint (Pudhina):** Thrives in shallow wide planters; spreads rapidly via runners.
        3. **Aloe Vera:** Indestructible succulent; water only once weekly; bright indirect light.
        4. **Lemongrass:** Grows vigorously in 12-inch pots; repels mosquitoes naturally.
        5. **Gotu Kola / Brahmi:** Loves moist shallow trays on shady windowsills.
        """)

    with c_soil:
        st.markdown("""
        #### 🪴 Ideal Organic Potting Soil Mix Formula
        * **40%** Garden Loam / Red Soil
        * **30%** Organic Vermicompost / Well-aged Cow Dung Manure
        * **20%** Cocopeat (for moisture retention without compaction)
        * **10%** Perlite / Sand (for free drainage)
        * **Handful of Neem Cake Powder:** Prevents subterranean root nematodes and fungal rots.
        """)
