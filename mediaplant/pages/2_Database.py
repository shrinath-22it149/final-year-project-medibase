import os, sys
import warnings, os as _os
warnings.filterwarnings("ignore")
_os.environ["PYTHONWARNINGS"] = "ignore"
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

import streamlit as st
import json

st.set_page_config(page_title="Plant Database | MediPlant AI", page_icon="🌿", layout="wide")

st.markdown("""
<style>
.main{background:#FAFFFE;}
h1,h2,h3{color:#2E8B57!important;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a3a2a,#2E8B57);}
section[data-testid="stSidebar"] *{color:white!important;}
div.stButton>button{background:linear-gradient(135deg,#2E8B57,#3CB371);
  color:white;border:none;border-radius:8px;font-weight:bold;}
.pcard{background:white;border-radius:12px;padding:16px;
  box-shadow:0 3px 10px rgba(0,0,0,.1);border-top:4px solid #2E8B57;margin-bottom:12px;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None

with st.sidebar:
    st.markdown("## 🌿 MediPlant AI")
    st.markdown("---")
    if st.session_state.user:
        st.success(f"👤 {st.session_state.user['username']}")
    st.markdown("---")
    st.page_link("app.py",                 label="🏠 Home")
    st.page_link("pages/1_Identify.py", label="🔍 Identify Plant")

@st.cache_data
def load_plants():
    path = os.path.join(_ROOT, "data", "plants_info.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)["plants"]

def tox_badge(level):
    colors = {
        "Very Low": ("#d4edda","#155724"),
        "Low":      ("#d4edda","#155724"),
        "Medium":   ("#fff3cd","#856404"),
        "High":     ("#f8d7da","#721c24"),
    }
    bg, fg = colors.get(level, ("#e2e3e5","#383d41"))
    return f'<span style="background:{bg};color:{fg};padding:2px 10px;border-radius:12px;font-weight:bold;font-size:.82em;">{level}</span>'

st.title("🌿 Medicinal Plant Database")
st.markdown("Browse our database of medicinal plants with detailed information.")
st.divider()

try:
    plants = load_plants()
except Exception as e:
    st.error(f"❌ Could not load plant data: {e}")
    st.info(f"Expected file at: {os.path.join(_ROOT, 'data', 'plants_info.json')}")
    st.stop()

# Search & Filter
sc1, sc2, sc3 = st.columns([3,2,2])
with sc1:
    search = st.text_input("🔍 Search plants...", placeholder="e.g. Tulsi, Neem, diabetes")
with sc2:
    categories = ["All"] + sorted(set(p.get("category","General") for p in plants))
    cat_filter = st.selectbox("📂 Category", categories)
with sc3:
    tox_opts = ["All"] + sorted(set(p.get("toxicity_level","Low") for p in plants))
    tox_filter = st.selectbox("⚠️ Toxicity Level", tox_opts)

# Apply filters
filtered = plants
if search:
    sl = search.lower()
    filtered = [p for p in filtered if
                sl in p["common_name"].lower() or
                sl in p.get("scientific_name","").lower() or
                sl in p.get("tamil_name","").lower() or
                any(sl in u.lower() for u in p.get("medicinal_uses",[]))]
if cat_filter != "All":
    filtered = [p for p in filtered if p.get("category") == cat_filter]
if tox_filter != "All":
    filtered = [p for p in filtered if p.get("toxicity_level") == tox_filter]

st.markdown(f"**Showing {len(filtered)} of {len(plants)} plants**")
st.divider()

if not filtered:
    st.warning("No plants match your search. Try different keywords.")
    st.stop()

# Display cards
for i in range(0, len(filtered), 2):
    row = filtered[i:i+2]
    cols = st.columns(len(row))
    for col, p in zip(cols, row):
        with col:
            st.markdown(f"""
            <div class="pcard">
              <h3 style="color:#2E8B57;margin-top:0;">🌿 {p['common_name']}</h3>
              <p style="color:#888;font-style:italic;margin:0;">{p.get('scientific_name','')}</p>
              <p style="color:#666;font-size:.85em;">
                Tamil: <b>{p.get('tamil_name','N/A')}</b> | Family: <b>{p.get('family','N/A')}</b>
              </p>
            </div>""", unsafe_allow_html=True)

            with st.expander(f"📖 View Details — {p['common_name']}"):
                # Audio Speech Reader (HTML5 Web Speech API)
                speech_text = f"{p['common_name']}. Botanical name: {p.get('scientific_name','')}. Tamil name: {p.get('tamil_name','')}. {p.get('description','')[:180]}. Key uses include: {', '.join(p.get('medicinal_uses',[])[:3])}."
                clean_speech = speech_text.replace('"', '&quot;').replace("'", "\\'")
                
                audio_button_html = f"""
                <div style="margin: 8px 0;">
                  <button onclick="window.speechSynthesis.cancel(); let u = new SpeechSynthesisUtterance('{clean_speech}'); u.rate = 0.95; window.speechSynthesis.speak(u);"
                          style="background:linear-gradient(135deg,#2E8B57,#3CB371);color:white;border:none;border-radius:20px;padding:6px 14px;cursor:pointer;font-weight:bold;font-size:0.82em;">
                    🔊 Listen to Voice Description
                  </button>
                  <button onclick="window.speechSynthesis.cancel();"
                          style="background:#f1f3f4;color:#555;border:1px solid #ccc;border-radius:20px;padding:6px 10px;cursor:pointer;font-size:0.82em;margin-left:5px;">
                    ⏹️ Stop Audio
                  </button>
                </div>
                """
                st.components.v1.html(audio_button_html, height=45)

                st.markdown(f"**Hindi Name:** {p.get('hindi_name','N/A')} | **Family:** {p.get('family','N/A')}")
                st.markdown(f"**Description:** {p.get('description','')}")
                st.markdown(f"**Toxicity:** {tox_badge(p.get('toxicity_level','Low'))}", unsafe_allow_html=True)
                st.markdown(f"**Availability:** {p.get('availability','N/A')} | **Region:** {p.get('region','N/A')}")
                st.markdown(f"⭐ Rating: {p.get('rating','N/A')}/5")

                tab1, tab2, tab3, tab4, tab5 = st.tabs(["💊 Uses","🧪 Compounds","📋 Preparation","⚠️ Safety", "🌱 Cultivation"])
                with tab1:
                    for u in p.get("medicinal_uses",[]):
                        st.markdown(f"✅ {u}")
                with tab2:
                    for c in p.get("active_compounds",[]):
                        st.markdown(f"🔬 **{c}**")
                with tab3:
                    for m in p.get("preparation_methods",[]):
                        st.info(f"🌿 {m}")
                with tab4:
                    st.markdown(p.get("safety_info",""))
                    for w in p.get("warnings",[]):
                        st.warning(f"⚠️ {w}")
                with tab5:
                    cult = p.get("cultivation", {})
                    st.markdown(f"**☀️ Sunlight:** {cult.get('sunlight', 'Full sun')}")
                    st.markdown(f"**💧 Watering:** {cult.get('water', 'Moderate')}")
                    st.markdown(f"**🌱 Soil:** {cult.get('soil', 'Loamy soil')}")
                    st.markdown(f"**🌡️ Climate:** {cult.get('climate', 'Tropical')}")

st.divider()
st.info("💡 Use the 🔍 **Identify Plant** page to identify plants from photos.")
