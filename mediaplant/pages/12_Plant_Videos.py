import os, sys, json
import urllib.parse
import warnings
warnings.filterwarnings("ignore")

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

import streamlit as st

st.set_page_config(
    page_title="Plant Video Library | MediPlant AI",
    page_icon="📺",
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
.video-card{background:white;border-radius:14px;padding:20px;box-shadow:0 3px 12px rgba(0,0,0,.08);margin-bottom:15px;border-top:4px solid #2E8B57;}
.yt-button{background:#FF0000;color:white!important;padding:8px 18px;border-radius:20px;font-weight:bold;text-decoration:none;display:inline-block;margin-top:10px;}
.badge-lang{background:#e8f5e9;color:#2e7d32;padding:3px 12px;border-radius:12px;font-weight:bold;font-size:0.85em;}
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
    st.page_link("pages/11_Cultivation_Guide.py",label="🌱 Cultivation Guide")
    st.markdown("---")
    st.caption("Visual learning reinforces botanical identification. Watch field botanists and Ayurvedic Vaidyas demonstrate live identification in Tamil, English, and Hindi.")

st.title("📺 50 Medicinal Plants Video Library")
st.markdown("Watch high-definition educational videos and field identification guides for all **50 medicinal plants** in **Tamil (தமிழ்)**, **English**, or **Hindi (हिंदी)**.")
st.divider()

# Load 50 plants
plants_path = os.path.join(_ROOT, "data", "plants_info.json")
try:
    with open(plants_path, "r", encoding="utf-8") as f:
        plants = json.load(f)["plants"]
except Exception:
    plants = []

# Language & Plant selectors
c_lang, c_plant = st.columns([1, 2])
with c_lang:
    language = st.selectbox(
        "🌐 Choose Video Language:",
        ["Tamil (தமிழ்)", "English", "Hindi (हिंदी)"]
    )

with c_plant:
    plant_names = [p["common_name"] for p in plants]
    selected_name = st.selectbox("🌿 Select Plant to Watch:", plant_names, index=0)

selected_plant = next((p for p in plants if p["common_name"] == selected_name), None)

if selected_plant:
    tamil_n = selected_plant.get("tamil_name", "")
    hindi_n = selected_plant.get("hindi_name", "")
    sci_n   = selected_plant.get("scientific_name", "")

    # Construct targeted search query based on selected language
    if "Tamil" in language:
        lang_code = "Tamil"
        search_query = f"{selected_name} {tamil_n} plant identification medicinal uses in Tamil"
        yt_search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
        lang_desc = f"Watch native identification and traditional Siddha / Ayurvedic uses of **{tamil_n}** explained in Tamil."
    elif "Hindi" in language:
        lang_code = "Hindi"
        search_query = f"{selected_name} {hindi_n} plant identification ayurvedic benefits in Hindi"
        yt_search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
        lang_desc = f"Watch detailed botanical identification and Ayurvedic health benefits of **{hindi_n}** explained in Hindi."
    else:
        lang_code = "English"
        search_query = f"{selected_name} {sci_n} plant identification botanical characteristics"
        yt_search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
        lang_desc = f"Watch scientific botanical identification, leaf morphology, and clinical pharmacognosy of **{selected_name} ({sci_n})** in English."

    st.markdown(f"""
    <div class="video-card">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <h2 style="color:#2E8B57;margin:0;">🌿 {selected_plant['common_name']} — <em>{sci_n}</em></h2>
        <span class="badge-lang">{language}</span>
      </div>
      <p style="margin-top:8px;color:#555;">
        Tamil: <strong>{tamil_n}</strong> | Hindi: <strong>{hindi_n}</strong> | Family: <strong>{selected_plant.get('family','')}</strong>
      </p>
      <p style="color:#444;">{lang_desc}</p>
      <a href="{yt_search_url}" target="_blank" class="yt-button">
        ▶️ Watch {selected_name} Video Guide on YouTube ({lang_code})
      </a>
    </div>
    """, unsafe_allow_html=True)

    # Educational Video Topics Covered
    v1, v2 = st.columns([1, 1], gap="large")
    with v1:
        st.markdown(f"### 🌿 What You'll See in the {selected_name} Video:")
        st.markdown(f"""
        * 🔍 **Leaf & Margin Morphology:** How to distinguish real *{selected_name}* from lookalike weeds.
        * 🌸 **Flowers, Seeds & Bark:** Visual inspection of secondary botanical characteristics.
        * 🧪 **Phytochemical Constituents:** Active compounds including *{', '.join(selected_plant.get('active_compounds',[])[:3])}*.
        * 💊 **Traditional Preparations:** Authentic preparation methods (*{selected_plant.get('preparation_methods',[ 'Decoction' ])[0]}*).
        """)

    with v2:
        st.markdown("### ⚠️ Clinical & Identification Safety:")
        st.warning(f"**Safety Warning:** {selected_plant.get('safety_info','')}")
        for w in selected_plant.get("warnings", []):
            st.markdown(f"🔸 {w}")

st.divider()

# Quick Video Carousel for Top 10 Popular Herbs
st.subheader("🌟 Quick Access Video Guides (Top 10 Essential Herbs)")
top_10 = plants[:10]
cols = st.columns(5)
for i, p in enumerate(top_10):
    with cols[i % 5]:
        pname = p["common_name"]
        ptamil = p.get("tamil_name", "")
        q_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(f'{pname} {ptamil} plant identification in Tamil')}"
        st.markdown(f"""
        <div style="background:white;padding:12px;border-radius:10px;text-align:center;box-shadow:0 2px 6px rgba(0,0,0,.08);margin-bottom:10px;border-top:3px solid #2E8B57;">
          <h4 style="margin:4px 0;color:#2E8B57;">🌿 {pname}</h4>
          <p style="font-size:0.8em;color:#666;margin:0;">{ptamil}</p>
          <a href="{q_url}" target="_blank" style="color:#c4302b;font-weight:bold;font-size:0.85em;text-decoration:none;display:inline-block;margin-top:6px;">
            ▶️ Watch in Tamil
          </a>
        </div>
        """, unsafe_allow_html=True)
