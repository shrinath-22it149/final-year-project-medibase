import os, sys
import warnings, os as _os
warnings.filterwarnings("ignore")
_os.environ["PYTHONWARNINGS"] = "ignore"
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json

st.set_page_config(page_title="Compare Plants | MediPlant AI", page_icon="⚖️", layout="wide")

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
    st.page_link("pages/2_Database.py", label="🌿 Plant Database")

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

st.title("⚖️ Compare Medicinal Plants")
st.markdown("Select two or three plants to compare their properties side by side.")
st.divider()

try:
    plants = load_plants()
except Exception as e:
    st.error(f"Could not load plant data: {e}")
    st.stop()

plant_names = [p["common_name"] for p in plants]

c1, c2, c3 = st.columns(3)
with c1:
    p1 = st.selectbox("🌿 Plant 1", plant_names, index=0)
with c2:
    p2 = st.selectbox("🌿 Plant 2", plant_names, index=min(1, len(plant_names)-1))
with c3:
    p3 = st.selectbox("🌿 Plant 3 (optional)", ["None"] + plant_names)

if st.button("⚖️ Compare Now", type="primary", use_container_width=True):
    sel_names  = [p1, p2] + ([p3] if p3 != "None" else [])
    sel_plants = [next((p for p in plants if p["common_name"]==n), None) for n in sel_names]
    sel_plants = [p for p in sel_plants if p is not None]

    if len(sel_plants) < 2:
        st.error("Please select at least 2 different plants.")
    else:
        st.divider()
        st.subheader("📋 Side-by-Side Comparison")

        rows = ["Scientific Name","Tamil Name","Family","Category","Toxicity","Availability","Region","Rating"]
        keys = ["scientific_name","tamil_name","family","category","toxicity_level","availability","region","rating"]
        table = {"Property": rows}
        for p in sel_plants:
            table[p["common_name"]] = [str(p.get(k,"N/A")) for k in keys]
        df = pd.DataFrame(table).set_index("Property")
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.subheader("💊 Medicinal Uses")
        cols = st.columns(len(sel_plants))
        for i, p in enumerate(sel_plants):
            with cols[i]:
                st.markdown(f"**🌿 {p['common_name']}**")
                for u in p.get("medicinal_uses",[]):
                    st.markdown(f"✅ {u}")

        st.divider()
        st.subheader("🧪 Active Compounds")
        cols2 = st.columns(len(sel_plants))
        for i, p in enumerate(sel_plants):
            with cols2[i]:
                st.markdown(f"**🔬 {p['common_name']}**")
                for c in p.get("active_compounds",[]):
                    st.markdown(f"• {c}")

        st.divider()
        st.subheader("⚠️ Safety Comparison")
        cols3 = st.columns(len(sel_plants))
        for i, p in enumerate(sel_plants):
            with cols3[i]:
                tox = p.get("toxicity_level","Low")
                st.markdown(f"**{p['common_name']}**")
                st.markdown(tox_badge(tox), unsafe_allow_html=True)
                st.caption(p.get("safety_info",""))

        st.divider()
        st.subheader("📡 Radar Chart Comparison")

        tox_score  = {"Very Low":5,"Low":4,"Medium":3,"High":1}
        avail_score= {"Very High":5,"High":4,"Medium":3,"Low":2,"Very Low":1}
        categories = ["Safety","Availability","Uses Count","Compounds","Rating"]
        colors_list= ["#2E8B57","#FF6B35","#4682B4"]

        fig = go.Figure()
        for i, p in enumerate(sel_plants):
            scores = [
                tox_score.get(p.get("toxicity_level","Low"), 3),
                avail_score.get(p.get("availability","Medium"), 3),
                min(len(p.get("medicinal_uses",[])), 5),
                min(len(p.get("active_compounds",[])), 5),
                float(p.get("rating", 3)),
            ]
            scores_closed = scores + [scores[0]]
            cats_closed   = categories + [categories[0]]
            fig.add_trace(go.Scatterpolar(
                r=scores_closed,
                theta=cats_closed,
                fill="toself",
                name=p["common_name"],
                line=dict(color=colors_list[i % len(colors_list)])
            ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0,5])),
            height=450,
            paper_bgcolor="white",
            legend=dict(orientation="h")
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("📋 Preparation Methods")
        cols4 = st.columns(len(sel_plants))
        for i, p in enumerate(sel_plants):
            with cols4[i]:
                st.markdown(f"**🌿 {p['common_name']}**")
                for m in p.get("preparation_methods",[]):
                    st.info(m)
