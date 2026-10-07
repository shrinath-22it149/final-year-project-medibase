import os, sys
import warnings, os as _os
warnings.filterwarnings("ignore")
_os.environ["PYTHONWARNINGS"] = "ignore"
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

import streamlit as st
import pandas as pd

st.set_page_config(page_title="History | MediPlant AI", page_icon="📋", layout="wide")

st.markdown("""
<style>
.main{background:#FAFFFE;}
h1,h2,h3{color:#2E8B57!important;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a3a2a,#2E8B57);}
section[data-testid="stSidebar"] *{color:white!important;}
div.stButton>button{background:linear-gradient(135deg,#2E8B57,#3CB371);
  color:white;border:none;border-radius:8px;font-weight:bold;}
.pcard{background:white;border-radius:12px;padding:14px;
  box-shadow:0 2px 8px rgba(0,0,0,.1);border-top:4px solid #2E8B57;margin-bottom:10px;}
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
    st.page_link("pages/7_Profile.py",  label="👤 Profile / Login")

st.title("📋 My Identification History")
st.divider()

if not st.session_state.user:
    st.warning("⚠️ Please login to view your history.")
    st.page_link("pages/7_Profile.py", label="👤 Login / Register")
    st.stop()

from database.db_operations import get_user_predictions, get_saved_plants, remove_saved_plant

tab1, tab2 = st.tabs(["🔍 Identification History", "💾 Saved Collection"])

with tab1:
    preds = get_user_predictions(st.session_state.user["id"])
    if not preds:
        st.info("No identifications yet. Go identify a plant!")
        st.page_link("pages/1_Identify.py", label="🔍 Go to Identify Page")
    else:
        st.success(f"You have made **{len(preds)}** identifications total")

        df = pd.DataFrame(preds)
        show_cols = [c for c in ["plant_name","confidence","model_used","created_at"] if c in df.columns]
        df2 = df[show_cols].copy()
        if "confidence" in df2.columns:
            df2["confidence"] = df2["confidence"].apply(lambda x: f"{float(x)*100:.1f}%")
        if "created_at" in df2.columns:
            df2["created_at"] = df2["created_at"].apply(lambda x: str(x)[:16])
        df2.columns = [c.replace("_"," ").title() for c in df2.columns]
        st.dataframe(df2, use_container_width=True, hide_index=True)

        if len(preds) > 1:
            try:
                import plotly.express as px
                names  = [p["plant_name"] for p in preds]
                counts = pd.Series(names).value_counts().head(8)
                fig    = px.bar(x=counts.index, y=counts.values,
                                title="Your Most Identified Plants",
                                labels={"x":"Plant","y":"Count"},
                                color=counts.values,
                                color_continuous_scale="Greens")
                fig.update_layout(height=300, showlegend=False, plot_bgcolor="#fafffe")
                st.plotly_chart(fig, use_container_width=True)
            except Exception:
                pass

with tab2:
    saved = get_saved_plants(st.session_state.user["id"])
    if not saved:
        st.info("No saved plants yet. Save plants from the Identify page.")
    else:
        st.success(f"**{len(saved)}** plants in your collection")
        for s in saved:
            c1, c2 = st.columns([5, 1])
            with c1:
                notes_html = f"<br><small style='color:#666;'>{s['notes']}</small>" if s.get("notes") else ""
                st.markdown(f"""
                <div class="pcard">
                  <b>🌿 {s['plant_name']}</b>
                  <span style="color:#888;font-size:.82em;margin-left:10px;">
                    Saved: {str(s.get('saved_at',''))[:10]}
                  </span>{notes_html}
                </div>""", unsafe_allow_html=True)
            with c2:
                if st.button("🗑️", key=f"rem_{s['id']}", help="Remove from collection"):
                    remove_saved_plant(s["id"], st.session_state.user["id"])
                    st.rerun()
