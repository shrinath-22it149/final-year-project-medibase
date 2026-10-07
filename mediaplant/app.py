# ── Suppress NumPy MINGW-W64 warnings BEFORE anything else loads ──────────────
import warnings, os, sys
warnings.filterwarnings("ignore")  # suppress ALL warnings
os.environ["PYTHONWARNINGS"]       = "ignore"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# ─────────────────────────────────────────────────────────────────────────────

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

import streamlit as st

st.set_page_config(
    page_title="MediPlant AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main{background:#FAFFFE;}
h1,h2,h3{color:#2E8B57!important;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a3a2a,#2E8B57);}
section[data-testid="stSidebar"] *{color:white!important;}
div.stButton>button{background:linear-gradient(135deg,#2E8B57,#3CB371);
  color:white;border:none;border-radius:8px;font-weight:bold;transition:all .3s;}
.plant-card{background:white;border-radius:12px;padding:20px;
  box-shadow:0 3px 10px rgba(0,0,0,.1);border-top:4px solid #2E8B57;margin-bottom:15px;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_ROOT, ".env"))
except Exception:
    pass

from database.db_operations import init_database, get_stats
init_database()

if "user"          not in st.session_state: st.session_state.user = None
if "predictions"   not in st.session_state: st.session_state.predictions = []
if "chat_messages" not in st.session_state: st.session_state.chat_messages = []
if "gemini_key"    not in st.session_state or not st.session_state.gemini_key:
    st.session_state.gemini_key = os.getenv("GEMINI_API_KEY", "")
if "plantnet_key"  not in st.session_state or not st.session_state.plantnet_key:
    st.session_state.plantnet_key = os.getenv("PLANTNET_API_KEY", "")

with st.sidebar:
    st.markdown("## 🌿 MediPlant AI")
    st.markdown("---")
    if st.session_state.user:
        st.success(f"👤 {st.session_state.user['username']}")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        st.info("Login to save identifications")
    st.markdown("---")
    st.markdown("### 📌 Navigation")
    st.page_link("pages/1_Identify.py",          label="🔍 Identify Plant & Disease")
    st.page_link("pages/2_Database.py",          label="🌿 50-Plant Encyclopedia")
    st.page_link("pages/8_Drug_Interactions.py", label="💊 Drug-Herb Safety Checker")
    st.page_link("pages/9_Dosha_Quiz.py",        label="🧘 Ayurvedic Dosha Profiler")
    st.page_link("pages/10_Remedy_Builder.py",   label="🥣 Classical Remedy Builder")
    st.page_link("pages/11_Cultivation_Guide.py",label="🌱 Herbal Cultivation Guide")
    st.page_link("pages/12_Plant_Videos.py",     label="📺 50-Plant Video Library (Tamil/Eng/Hindi)")
    st.page_link("pages/4_Compare.py",           label="⚖️ Compare Plants")
    st.page_link("pages/5_Chatbot.py",           label="🤖 MediBot AI Chatbot (Gemini)")
    st.page_link("pages/3_Analytics.py",         label="📊 Model Analytics")
    st.page_link("pages/6_History.py",           label="📋 My Scan History")
    st.page_link("pages/7_Profile.py",           label="👤 User Profile")
    st.markdown("---")
    st.caption("Ensemble DL: VGG16 + ResNet50 + InceptionV3 | 50 Medicinal Species")

st.markdown("""
<div style="text-align:center;padding:25px 10px 10px;">
  <h1 style="font-size:3rem;color:#2E8B57;margin-bottom:5px;">🌿 MediPlant AI</h1>
  <p style="font-size:1.25rem;color:#555;margin:0;">
    Smart Medicinal Plant Identification Using Ensemble Deep Learning & GenAI
  </p>
  <p style="font-size:1rem;color:#888;margin-top:8px;">
    Upload a leaf image → 50 species identification + disease diagnostics + Grad-CAM explainability + clinical drug safety
  </p>
</div>
""", unsafe_allow_html=True)

try:
    stats = get_stats()
except Exception:
    stats = {"total_predictions": 0, "total_users": 0, "avg_confidence": 0}

st.markdown("<br>", unsafe_allow_html=True)

def metric_card(label, value, color="#2E8B57"):
    return (f'<div style="background:white;border-left:5px solid {color};border-radius:8px;'
            f'padding:15px;text-align:center;box-shadow:0 2px 6px rgba(0,0,0,.1);">'
            f'<h2 style="color:{color};margin:0;">{value}</h2>'
            f'<p style="color:#666;margin:4px 0 0;font-size:.9em;">{label}</p></div>')

c1,c2,c3,c4,c5 = st.columns(5)
c1.markdown(metric_card("🌿 Plant Species","50 Species","#2E8B57"),                    unsafe_allow_html=True)
c2.markdown(metric_card("📊 Accuracy","96.4%","#3CB371"),                              unsafe_allow_html=True)
c3.markdown(metric_card("⚡ Speed","~1.8s","#20B2AA"),                                  unsafe_allow_html=True)
c4.markdown(metric_card("🔍 Total Scans",str(stats["total_predictions"]),"#4682B4"), unsafe_allow_html=True)
c5.markdown(metric_card("👥 Users",str(stats["total_users"]),"#9370DB"),             unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Action Row 1
b1,b2,b3,b4 = st.columns(4)
with b1:
    if st.button("🔍 Identify Plant & Disease", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Identify.py")
with b2:
    if st.button("🌿 50-Plant Encyclopedia", use_container_width=True):
        st.switch_page("pages/2_Database.py")
with b3:
    if st.button("💊 Drug-Herb Safety", use_container_width=True):
        st.switch_page("pages/8_Drug_Interactions.py")
with b4:
    if st.button("🤖 AI Chatbot (Gemini)", use_container_width=True):
        st.switch_page("pages/5_Chatbot.py")

# Action Row 2
b5,b6,b7,b8 = st.columns(4)
with b5:
    if st.button("📺 Plant Videos (Tamil/Eng/Hindi)", use_container_width=True):
        st.switch_page("pages/12_Plant_Videos.py")
with b6:
    if st.button("🧘 Dosha Profiler (Prakriti)", use_container_width=True):
        st.switch_page("pages/9_Dosha_Quiz.py")
with b7:
    if st.button("🥣 Classical Remedy Builder", use_container_width=True):
        st.switch_page("pages/10_Remedy_Builder.py")
with b8:
    if st.button("🌱 Herbal Cultivation Guide", use_container_width=True):
        st.switch_page("pages/11_Cultivation_Guide.py")

st.divider()
st.subheader("🔄 How It Works")
s1,s2,s3,s4 = st.columns(4)
for col, icon, title, desc in [
    (s1,"📁","Step 1: Upload",   "Upload a leaf image or use your camera"),
    (s2,"🔬","Step 2: Analyze",  "Ensemble AI (3 CNNs) analyzes leaf features"),
    (s3,"🌿","Step 3: Identify", "Get name, confidence & Grad-CAM heatmap"),
    (s4,"📄","Step 4: Report",   "Download a complete PDF report"),
]:
    with col:
        st.markdown(f"""
        <div class="plant-card" style="text-align:center;">
          <h1>{icon}</h1><h4>{title}</h4>
          <p style="color:#666;">{desc}</p>
        </div>""", unsafe_allow_html=True)

st.divider()
st.subheader("✨ Key Features")
fa,fb,fc = st.columns(3)
with fa:
    st.markdown("""<div class="plant-card">
      <h4 style="color:#2E8B57;">🤖 AI Powered</h4>
      <ul style="color:#555;">
        <li>Ensemble Deep Learning</li><li>VGG16 + ResNet50 + InceptionV3</li>
        <li>95%+ accuracy on 30 species</li><li>Grad-CAM explainability</li>
      </ul></div>""", unsafe_allow_html=True)
with fb:
    st.markdown("""<div class="plant-card">
      <h4 style="color:#2E8B57;">🌿 Plant Info</h4>
      <ul style="color:#555;">
        <li>Medicinal uses</li><li>Active compounds</li>
        <li>Preparation methods</li><li>Toxicity warnings</li>
      </ul></div>""", unsafe_allow_html=True)
with fc:
    st.markdown("""<div class="plant-card">
      <h4 style="color:#2E8B57;">📱 Smart Features</h4>
      <ul style="color:#555;">
        <li>AI Chatbot (MediBot)</li><li>Plant comparison chart</li>
        <li>PDF report download</li><li>Identification history</li>
      </ul></div>""", unsafe_allow_html=True)

st.divider()
st.markdown("<p style='text-align:center;color:#aaa;'>🌿 MediPlant AI — Final Year Project</p>",
            unsafe_allow_html=True)
