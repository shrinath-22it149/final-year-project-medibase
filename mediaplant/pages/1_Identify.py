import warnings, os as _os
warnings.filterwarnings("ignore")
_os.environ["PYTHONWARNINGS"] = "ignore"
_os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_ROOT, ".env"))
except Exception:
    pass

import streamlit as st
import numpy as np
from PIL import Image
import json
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Identify Plant | MediPlant AI",
    page_icon="🔍", layout="wide"
)

st.markdown("""
<style>
.main{background:#FAFFFE;}
h1,h2,h3{color:#2E8B57!important;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a3a2a,#2E8B57);}
section[data-testid="stSidebar"] *{color:white!important;}
div.stButton>button{background:linear-gradient(135deg,#2E8B57,#3CB371);
  color:white;border:none;border-radius:8px;font-weight:bold;padding:10px 20px;}
div.stButton>button:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(46,139,87,.4);}
.result-card{background:linear-gradient(135deg,#f0fff4,#e6ffe6);border:2px solid #2E8B57;
  border-radius:16px;padding:20px;text-align:center;margin:8px 0;}
.disease-card{border-radius:14px;padding:18px;margin:8px 0;border-left:5px solid;}
.healthy-card{background:#d4edda;border-color:#28a745;}
.warning-card{background:#fff3cd;border-color:#ffc107;}
.danger-card {background:#f8d7da;border-color:#dc3545;}
.critical-card{background:#f5c6cb;border-color:#721c24;}
.feature-pill{background:#2E8B57;color:white;border-radius:20px;
  padding:3px 12px;font-size:.80em;font-weight:bold;margin:3px;display:inline-block;}
.disease-pill{border-radius:20px;padding:3px 14px;font-size:.80em;font-weight:bold;
  margin:3px;display:inline-block;}
.upload-zone{background:#f0fff4;border:2px dashed #2E8B57;border-radius:12px;
  padding:20px;text-align:center;margin:8px 0;}
.tab-header{background:linear-gradient(135deg,#2E8B57,#3CB371);color:white!important;
  padding:8px 16px;border-radius:8px;font-weight:bold;}
.severity-bar{height:12px;border-radius:6px;margin:4px 0;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for key, val in [("user",None),("plant_result",None),("disease_result",None),
                 ("plant_image",None),("disease_image",None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 MediPlant AI")
    st.divider()
    if st.session_state.user:
        st.success(f"👤 {st.session_state.user['username']}")
    else:
        st.info("Login to save results")
    st.divider()
    st.page_link("app.py",                 label="🏠 Home")
    st.page_link("pages/2_Database.py", label="🌿 Plant Database")
    st.page_link("pages/5_Chatbot.py",  label="🤖 AI Chatbot")
    st.page_link("pages/6_History.py",  label="📋 My History")
    st.divider()
    st.markdown("### 📸 Photo Tips")
    st.info(
        "✅ Single clear leaf\n\n"
        "✅ Good natural lighting\n\n"
        "✅ Leaf fills the frame\n\n"
        "✅ Clean background\n\n"
        "❌ Avoid blurry shots"
    )
    st.divider()
    st.markdown("### 🔬 AI Methods Used")
    st.markdown("""
    **Plant ID:**
    - HSV Color Analysis
    - Texture Classification
    - Shape/Aspect Detection
    - Edge Density Analysis
    
    **Disease Detection:**
    - Pixel Color Distribution
    - Lesion Pattern Analysis
    - Spectral Feature Extraction
    - Severity Scoring Algorithm
    """)

# ── Imports ────────────────────────────────────────────────────────────────────
from model.predictor import load_models, predict_plant
from model.disease_predictor import detect_disease, DISEASE_INFO

@st.cache_data
def load_plant_db():
    path = os.path.join(_ROOT, "data", "plants_info.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)["plants"]

def get_plant_info(name):
    try:
        plants = load_plant_db()
        nl = name.lower().strip()
        for p in plants:
            if nl in p["common_name"].lower() or p["common_name"].lower() in nl:
                return p
    except Exception:
        pass
    return None

def conf_color(c):
    if c >= 0.80: return "#2E8B57"
    if c >= 0.60: return "#FFA500"
    return "#CC0000"

def conf_label(c):
    if c >= 0.80: return "✅ HIGH CONFIDENCE"
    if c >= 0.60: return "⚠️ MEDIUM CONFIDENCE"
    return "❌ LOW CONFIDENCE"

def make_heatmap(image):
    """Generate attention heatmap highlighting leaf regions."""
    try:
        arr = np.array(image.resize((224,224)).convert("RGB"), dtype=np.float32)/255.0
        r,g,b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        v = np.max(arr, axis=2)
        minc = np.min(arr, axis=2)
        s = np.where(v>0.01,(v-minc)/v,0.0)
        greenness = np.clip(g - 0.5*(r+b),0,1)*3
        lm = (v>0.12)&(v<0.93)&(s>0.07)
        attn = 0.7*greenness + 0.3*lm.astype(float)
        from PIL import ImageFilter
        attn_img = Image.fromarray((np.clip(attn,0,1)*255).astype(np.uint8),'L')
        attn_img = attn_img.filter(ImageFilter.GaussianBlur(radius=8))
        attn = np.array(attn_img, dtype=np.float32)/255.0
        def jet(v_):
            r_=(np.clip(1.5-abs(4*v_-3),0,1))
            g_=(np.clip(1.5-abs(4*v_-2),0,1))
            b_=(np.clip(1.5-abs(4*v_-1),0,1))
            return r_,g_,b_
        rh,gh,bh = jet(attn)
        heat = np.stack([rh,gh,bh],axis=2)
        orig = arr.copy()
        overlay = np.clip(0.55*orig + 0.45*heat, 0, 1)
        return Image.fromarray((orig*255).astype(np.uint8)), \
               Image.fromarray((overlay*255).astype(np.uint8))
    except Exception:
        return image.resize((224,224)), None

def severity_card_class(severity):
    m = {"None":"healthy-card","Moderate":"warning-card",
         "High":"danger-card","Critical":"critical-card"}
    return m.get(severity, "warning-card")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.title("🔍 Plant Identification & Disease Detection")
st.markdown("Upload leaf images for **AI-powered plant identification** and **disease diagnosis** — both powered by Smart Visual Analysis algorithms.")
st.divider()

models, labels = load_models()

# ═══════════════════════════════════════════════════════════════════════════════
# TWO COLUMN LAYOUT: Left = Plant ID | Right = Disease Detection
# ═══════════════════════════════════════════════════════════════════════════════
col_plant, col_disease = st.columns(2, gap="large")

# ─────────────────────────────────────────────────────────────────────────────
# LEFT COLUMN — PLANT IDENTIFICATION
# ─────────────────────────────────────────────────────────────────────────────
with col_plant:
    st.markdown("## 🌿 Plant Identification")
    st.markdown('<div class="upload-zone">📁 Upload a leaf image to identify the medicinal plant species</div>',
                unsafe_allow_html=True)

    p_method = st.radio("Input:", ["📁 Upload File","📷 Camera"], horizontal=True, key="p_method")
    plant_img_file = None
    if p_method == "📁 Upload File":
        plant_img_file = st.file_uploader("Choose leaf image",
            type=["jpg","jpeg","png","webp","bmp"], key="plant_upload",
            help="Upload a clear leaf photo for plant identification")
    else:
        cam = st.camera_input("Take a leaf photo", key="plant_cam")
        if cam: plant_img_file = cam

    p_engine = st.selectbox(
        "🧠 Identification Engine:",
        [
            "🌐 Pl@ntNet API (100% Real Online Botanical API)",
            "🤖 Google Gemini Vision AI (Multimodal GenAI)",
            "⚡ Offline Ensemble Model (No API Key Required)"
        ],
        key="p_engine"
    )

    if "Pl@ntNet" in p_engine:
        default_pn_key = st.session_state.get("plantnet_key") or os.environ.get("PLANTNET_API_KEY", "")
        plantnet_api_key = st.text_input(
            "🔑 Pl@ntNet API Key:",
            value=default_pn_key,
            type="password",
            help="Free key from https://my-api.plantnet.org/"
        )
        if plantnet_api_key:
            st.session_state.plantnet_key = plantnet_api_key
        st.caption("🌐 Connects to official Pl@ntNet global flora API with 300,000+ species.")
    elif "Gemini" in p_engine:
        default_gemini_key = st.session_state.get("gemini_key") or os.environ.get("GEMINI_API_KEY", "")
        gemini_vision_key = st.text_input(
            "🔑 Gemini API Key:",
            value=default_gemini_key,
            type="password",
            help="Free key from https://aistudio.google.com"
        )
        if gemini_vision_key:
            st.session_state.gemini_key = gemini_vision_key
        st.caption("🤖 Uses Google Gemini Vision for zero-shot leaf recognition.")
    else:
        p_model = st.selectbox("🤖 Model:", ["ensemble","hybrid"], key="p_model")

    show_heatmap = st.checkbox("🌡️ Show Attention Heatmap", value=True, key="p_heatmap")

    if plant_img_file:
        p_image = Image.open(plant_img_file).convert("RGB")
        st.session_state.plant_image = p_image
        st.image(p_image, caption=f"📷 {p_image.size[0]}×{p_image.size[1]}px", use_container_width=True)

        if st.button("🔍 IDENTIFY PLANT", type="primary", use_container_width=True, key="btn_identify"):
            if "Pl@ntNet" in p_engine:
                pkey = st.session_state.get("plantnet_key") or os.environ.get("PLANTNET_API_KEY", "")
                if not pkey:
                    st.warning("⚠️ Please paste your Pl@ntNet API Key above, or switch to 'Offline Ensemble Model'. Get a free key at https://my-api.plantnet.org/")
                    st.stop()
                with st.spinner("🌐 Querying Pl@ntNet Global Flora API (100% real live recognition)..."):
                    from utils.plantnet_client import identify_with_plantnet
                    pn_res = identify_with_plantnet(p_image, pkey)
                    if pn_res.get("success"):
                        result = pn_res
                    else:
                        st.error(f"❌ Pl@ntNet API Error: {pn_res.get('error')}. Falling back to offline model...")
                        result = predict_plant(p_image, models, labels, "ensemble")
            elif "Gemini" in p_engine:
                gkey = st.session_state.get("gemini_key") or os.environ.get("GEMINI_API_KEY", "")
                if not gkey:
                    st.warning("⚠️ Please paste your Gemini API Key above, or switch to 'Offline Ensemble Model'. Get a free key at https://aistudio.google.com")
                    st.stop()
                with st.spinner("🤖 Analyzing with Google Gemini Vision AI..."):
                    from utils.plantnet_client import identify_with_gemini_vision
                    gm_res = identify_with_gemini_vision(p_image, gkey)
                    if gm_res.get("success"):
                        result = gm_res
                    else:
                        st.error(f"❌ Gemini Vision Error: {gm_res.get('error')}. Falling back to offline model...")
                        result = predict_plant(p_image, models, labels, "ensemble")
            else:
                with st.spinner("🤖 Analyzing leaf features with Ensemble Model..."):
                    result = predict_plant(p_image, models, labels, p_model)

            plant_info = get_plant_info(result.get("plant_name", ""))
            if not plant_info and result.get("scientific_name"):
                plant_info = get_plant_info(result["scientific_name"])
            st.session_state.plant_result = result
            try:
                if st.session_state.user:
                    from database.db_operations import save_prediction
                    save_prediction(st.session_state.user["id"],
                                    result["plant_name"], result["confidence"], p_engine)
            except Exception:
                pass
            st.success(f"✅ Plant identified successfully via {result.get('engine', result.get('method', 'AI Engine'))}!")

    # Show plant result
    if st.session_state.plant_result:
        result = st.session_state.plant_result
        conf   = result["confidence"]
        color  = conf_color(conf)

        st.markdown(f"""
        <div class="result-card">
          <div style="font-size:2.2rem;font-weight:bold;color:#2E8B57;">🌿 {result['plant_name']}</div>
          <div style="font-size:1.1rem;color:{color};font-weight:bold;margin:6px 0;">{conf_label(conf)}</div>
          <div style="font-size:1.4rem;color:#333;font-weight:bold;">{conf*100:.1f}% Confidence</div>
          <span class="feature-pill">🤖 {result.get('method','Smart Visual Analysis')}</span>
        </div>""", unsafe_allow_html=True)

        st.progress(conf)

        # Metrics row
        m1,m2,m3 = st.columns(3)
        m1.metric("🎯 Confidence", f"{conf*100:.1f}%")
        m2.metric("🌿 Plant", result["plant_name"])
        m3.metric("📊 Method", "AI Analysis")

        # Heatmap
        if show_heatmap and st.session_state.plant_image:
            orig224, overlay = make_heatmap(st.session_state.plant_image)
            h1,h2 = st.columns(2)
            with h1: st.image(orig224, caption="Original", use_container_width=True)
            with h2:
                if overlay: st.image(overlay, caption="🌡️ AI Attention", use_container_width=True)

        # Features detected
        if result.get("features_used"):
            st.markdown("**🔬 Visual Features Detected:**")
            feat = result["features_used"]
            fc1,fc2 = st.columns(2)
            items = list(feat.items())
            for i,(k,v) in enumerate(items[:4]):
                (fc1 if i%2==0 else fc2).metric(k, str(v))

        # Top 5 chart
        if result.get("top5"):
            top5 = result["top5"]
            names_t = [p["name"] for p in top5]
            vals_t  = [p["confidence"]*100 for p in top5]
            bar_colors = ["#2E8B57" if i==0 else "#90EE90" for i in range(len(names_t))]
            fig = go.Figure(go.Bar(x=vals_t, y=names_t, orientation="h",
                marker_color=bar_colors,
                text=[f"{v:.1f}%" for v in vals_t], textposition="outside"))
            fig.update_layout(height=220, margin=dict(l=10,r=60,t=8,b=8),
                xaxis_title="Confidence (%)", plot_bgcolor="#fafffe", paper_bgcolor="white",
                xaxis=dict(range=[0,max(vals_t)*1.25]))
            st.plotly_chart(fig, use_container_width=True)

        # Plant info accordion
        plant_info = get_plant_info(result["plant_name"])
        if plant_info:
            with st.expander("📋 Full Plant Information", expanded=True):
                t1,t2,t3 = st.tabs(["💊 Medicinal Uses","📋 Preparation","⚠️ Safety"])
                with t1:
                    i1,i2 = st.columns(2)
                    with i1:
                        st.markdown(f"**🔬 Scientific:** *{plant_info.get('scientific_name','N/A')}*")
                        st.markdown(f"**🌏 Tamil:** {plant_info.get('tamil_name','N/A')}")
                        st.markdown(f"**🌱 Family:** {plant_info.get('family','N/A')}")
                    with i2:
                        st.markdown(f"**📍 Region:** {plant_info.get('region','N/A')}")
                        st.markdown(f"**⭐ Rating:** {plant_info.get('rating','N/A')}/5")
                        st.markdown(f"**🛒 Availability:** {plant_info.get('availability','N/A')}")
                    st.markdown(f"**Description:** {plant_info.get('description','')}")
                    st.markdown("**Medicinal Uses:**")
                    uc1,uc2 = st.columns(2)
                    for i,use in enumerate(plant_info.get("medicinal_uses",[])):
                        (uc1 if i%2==0 else uc2).markdown(f"✅ {use}")
                with t2:
                    for m in plant_info.get("preparation_methods",[]):
                        st.info(f"🌿 {m}")
                with t3:
                    st.markdown(f"**Toxicity:** {plant_info.get('toxicity_level','N/A')}")
                    st.markdown(f"**Safety:** {plant_info.get('safety_info','')}")
                    for w in plant_info.get("warnings",[]):
                        st.warning(f"⚠️ {w}")
                    st.error("🏥 Always consult a qualified Ayurvedic doctor before use.")

        # Speech synthesis for identified plant
        speech_text = f"Identified plant: {result['plant_name']}. Confidence: {int(conf*100)} percent. "
        if plant_info:
            speech_text += f"Scientific name: {plant_info.get('scientific_name','')}. Key medicinal uses: {', '.join(plant_info.get('medicinal_uses',[])[:3])}."
        clean_speech = speech_text.replace('"', '&quot;').replace("'", "\\'")

        st.components.v1.html(f"""
        <div style="margin: 8px 0;">
          <button onclick="window.speechSynthesis.cancel(); let u = new SpeechSynthesisUtterance('{clean_speech}'); u.rate = 0.95; window.speechSynthesis.speak(u);"
                  style="background:linear-gradient(135deg,#2E8B57,#3CB371);color:white;border:none;border-radius:20px;padding:6px 14px;cursor:pointer;font-weight:bold;font-size:0.85em;">
            🔊 Listen to Voice Identification
          </button>
          <button onclick="window.speechSynthesis.cancel();"
                  style="background:#f1f3f4;color:#555;border:1px solid #ccc;border-radius:20px;padding:6px 10px;cursor:pointer;font-size:0.85em;margin-left:5px;">
            ⏹️ Stop
          </button>
        </div>
        """, height=40)

        # Action buttons
        st.markdown("**📥 Actions & Clinical Safety:**")
        a1,a2,a3,a4 = st.columns(4)
        with a1:
            try:
                from utils.report_generator import generate_pdf_report
                uname = st.session_state.user["username"] if st.session_state.user else "Guest"
                pdf = generate_pdf_report(result, get_plant_info(result["plant_name"]), uname)
                st.download_button("📄 PDF Report", pdf,
                    f"{result['plant_name'].replace(' ','_')}_report.pdf",
                    mime="application/pdf", use_container_width=True)
            except Exception:
                pass
        with a2:
            if st.session_state.plant_image:
                import io
                buf = io.BytesIO()
                st.session_state.plant_image.save(buf, "PNG")
                st.download_button("🖼️ Image", buf.getvalue(),
                    f"{result['plant_name'].replace(' ','_')}.png",
                    mime="image/png", use_container_width=True)
        with a3:
            if st.button("💊 Drug Safety", key="check_drug_safety", use_container_width=True):
                st.switch_page("pages/8_Drug_Interactions.py")
        with a4:
            if st.button("🔄 Reset", key="reset_plant", use_container_width=True):
                st.session_state.plant_result = None
                st.session_state.plant_image  = None
                st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# RIGHT COLUMN — DISEASE DETECTION
# ─────────────────────────────────────────────────────────────────────────────
with col_disease:
    st.markdown("## 🦠 Disease Detection")
    st.markdown('<div class="upload-zone">🔬 Upload a leaf image to detect diseases, infections and deficiencies</div>',
                unsafe_allow_html=True)

    d_method = st.radio("Input:", ["📁 Upload File","📷 Camera"], horizontal=True, key="d_method")
    disease_img_file = None
    if d_method == "📁 Upload File":
        disease_img_file = st.file_uploader("Choose leaf image for disease detection",
            type=["jpg","jpeg","png","webp","bmp"], key="disease_upload",
            help="Upload a leaf photo to check for diseases")
    else:
        dcam = st.camera_input("Take a leaf photo", key="disease_cam")
        if dcam: disease_img_file = dcam

    show_d_features = st.checkbox("📊 Show Color Analysis", value=True, key="d_features")
    show_d_chart    = st.checkbox("📈 Show Disease Probability Chart", value=True, key="d_chart")

    if disease_img_file:
        d_image = Image.open(disease_img_file).convert("RGB")
        st.session_state.disease_image = d_image
        st.image(d_image, caption=f"📷 {d_image.size[0]}×{d_image.size[1]}px", use_container_width=True)

        if st.button("🦠 DETECT DISEASE", type="primary", use_container_width=True, key="btn_disease"):
            with st.spinner("🔬 Analyzing disease patterns..."):
                d_result = detect_disease(d_image)
                st.session_state.disease_result = d_result
            st.success("✅ Analysis complete!")

    # Show disease result
    if st.session_state.disease_result:
        dr     = st.session_state.disease_result
        sev    = dr["severity"]
        scolor = dr["severity_color"]
        sev_score = dr["severity_score"]
        card_class = severity_card_class(sev)

        # Main disease banner
        st.markdown(f"""
        <div class="disease-card {card_class}">
          <div style="font-size:2rem;font-weight:bold;">{dr['icon']} {dr['disease_name']}</div>
          <div style="margin:8px 0;">
            <span class="disease-pill" style="background:{scolor};color:white;">
              ⚠️ Severity: {sev}
            </span>
          </div>
          <div style="font-size:.95em;color:#333;margin-top:8px;">{dr['description']}</div>
        </div>""", unsafe_allow_html=True)

        # Severity progress bar
        st.markdown(f"**Disease Severity: {sev_score}%**")
        bar_color = scolor
        st.markdown(f"""
        <div style="background:#e9ecef;border-radius:6px;height:14px;margin:4px 0;">
          <div style="background:{bar_color};width:{sev_score}%;height:14px;
            border-radius:6px;transition:width .3s;"></div>
        </div>""", unsafe_allow_html=True)

        # Confidence
        dc = dr["confidence"]
        dm1,dm2,dm3 = st.columns(3)
        dm1.metric("🎯 Confidence", f"{dc*100:.1f}%")
        dm2.metric("🦠 Disease", dr["disease_name"][:18]+"..." if len(dr["disease_name"])>18 else dr["disease_name"])
        dm3.metric("⚠️ Severity", sev)

        # Color analysis features
        if show_d_features and dr.get("features"):
            st.markdown("**🎨 Color Pattern Analysis:**")
            feat = dr["features"]
            fc1,fc2 = st.columns(2)
            items = list(feat.items())
            for i,(k,v) in enumerate(items):
                (fc1 if i%2==0 else fc2).metric(k, f"{v}%")

        # Disease probability chart
        if show_d_chart and dr.get("top3"):
            top3 = dr["top3"]
            dnames = [f"{d['icon']} {d['name'][:25]}" for d in top3]
            dvals  = [d["confidence"]*100 for d in top3]
            d_colors = [scolor] + ["#6c757d"]*2
            fig2 = go.Figure(go.Bar(x=dvals[::-1], y=dnames[::-1], orientation="h",
                marker_color=d_colors[::-1],
                text=[f"{v:.1f}%" for v in dvals[::-1]], textposition="outside"))
            fig2.update_layout(height=180, margin=dict(l=10,r=70,t=8,b=8),
                xaxis_title="Probability (%)", plot_bgcolor="#fafffe", paper_bgcolor="white",
                xaxis=dict(range=[0, max(dvals)*1.3 if dvals else 100]))
            st.plotly_chart(fig2, use_container_width=True)

        # Detailed tabs
        with st.expander("🔍 Full Disease Analysis", expanded=True):
            dt1,dt2,dt3,dt4 = st.tabs(["🩺 Symptoms","💊 Treatment","🛡️ Prevention","⚗️ Causes"])
            with dt1:
                st.markdown("**Symptoms Detected:**")
                for sym in dr.get("symptoms",[]):
                    st.markdown(f"🔸 {sym}")
            with dt2:
                st.markdown("**Recommended Treatment:**")
                for i,t in enumerate(dr.get("treatment",[])):
                    st.markdown(f'<div style="background:#d4edda;border-left:4px solid #28a745;'
                                f'border-radius:6px;padding:8px;margin:4px 0;">💊 {t}</div>',
                                unsafe_allow_html=True)
            with dt3:
                st.markdown("**Prevention Measures:**")
                for p in dr.get("prevention",[]):
                    st.markdown(f'<div style="background:#cce5ff;border-left:4px solid #004085;'
                                f'border-radius:6px;padding:8px;margin:4px 0;">🛡️ {p}</div>',
                                unsafe_allow_html=True)
            with dt4:
                st.markdown("**Root Causes:**")
                for c in dr.get("causes",[]):
                    st.markdown(f"⚗️ {c}")

        # Disease gallery reference
        st.markdown("**🦠 Disease Reference Guide:**")
        diseases = list(DISEASE_INFO.items())
        dg1,dg2 = st.columns(2)
        for i,(dname,dinfo) in enumerate(diseases):
            col_ref = dg1 if i%2==0 else dg2
            is_current = (dname == dr["disease_name"])
            border = "3px solid #2E8B57" if is_current else "1px solid #dee2e6"
            bg = "#d4edda" if is_current else "#f8f9fa"
            col_ref.markdown(f"""
            <div style="background:{bg};border:{border};border-radius:8px;
              padding:8px;margin:3px 0;font-size:.85em;">
              <b>{dinfo['icon']} {dname[:28]}</b><br>
              <span style="color:{dinfo['severity_color']};font-size:.78em;">
                ● {dinfo['severity']} Severity</span>
            </div>""", unsafe_allow_html=True)

        # Action row
        st.markdown("**📥 Actions:**")
        da1,da2 = st.columns(2)
        with da1:
            import json as _json
            report_data = {k:v for k,v in dr.items() if k not in ["features"]}
            st.download_button("📄 Download Report",
                data=_json.dumps(dr, indent=2, default=str),
                file_name=f"disease_report_{dr['disease_name'][:20].replace(' ','_')}.json",
                mime="application/json", use_container_width=True)
        with da2:
            if st.button("🔄 Reset", key="reset_disease", use_container_width=True):
                st.session_state.disease_result = None
                st.session_state.disease_image  = None
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# COMBINED ANALYSIS SECTION (shown when both results available)
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.plant_result and st.session_state.disease_result:
    st.divider()
    st.markdown("## 📊 Combined Plant + Disease Analysis Report")

    pr = st.session_state.plant_result
    dr = st.session_state.disease_result

    ra1,ra2,ra3,ra4 = st.columns(4)
    ra1.metric("🌿 Plant Identified",   pr["plant_name"])
    ra2.metric("🎯 Plant Confidence",   f"{pr['confidence']*100:.1f}%")
    ra3.metric("🦠 Disease Detected",   dr["disease_name"][:20])
    ra4.metric("⚠️ Disease Severity",   dr["severity"])

    # Combined radar chart
    categories = ["Plant Conf.","Green Health","Disease Risk","Severity Inv.","AI Certainty"]
    plant_conf   = pr["confidence"] * 100
    green_health = pr.get("features_used",{}).get("Greenness (%)", 60.0)
    disease_risk = dr["severity_score"]
    sev_inv      = 100 - dr["severity_score"]
    ai_certainty = (pr["confidence"] + dr["confidence"]) / 2 * 100

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[plant_conf, green_health, disease_risk, sev_inv, ai_certainty],
        theta=categories, fill="toself", name="Analysis",
        line_color="#2E8B57", fillcolor="rgba(46,139,87,0.2)"
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,100])),
        showlegend=False, height=350,
        title="Plant Health Radar Analysis"
    )
    rc1, rc2 = st.columns([1,1])
    with rc1:
        st.plotly_chart(fig_radar, use_container_width=True)
    with rc2:
        st.markdown("### 📋 Health Summary")
        health_score = int((sev_inv * 0.6) + (plant_conf * 0.4))
        if health_score >= 80:
            st.success(f"🌿 **Overall Health Score: {health_score}/100** — Excellent")
        elif health_score >= 60:
            st.warning(f"🌿 **Overall Health Score: {health_score}/100** — Fair")
        else:
            st.error(f"🌿 **Overall Health Score: {health_score}/100** — Needs Attention")

        st.markdown(f"""
        | Metric | Value |
        |--------|-------|
        | 🌿 Plant Species | {pr['plant_name']} |
        | 🎯 ID Confidence | {pr['confidence']*100:.1f}% |
        | 🦠 Disease | {dr['disease_name'][:30]} |
        | ⚠️ Severity | {dr['severity']} ({dr['severity_score']}%) |
        | 🏥 Action Needed | {'Yes — See treatment' if dr['severity_score']>30 else 'No — Plant is healthy'} |
        """)

    # Quick combined recommendations
    st.markdown("### 💡 AI Recommendations")
    rec1, rec2 = st.columns(2)
    with rec1:
        st.markdown("**For the Plant:**")
        plant_info = get_plant_info(pr["plant_name"])
        if plant_info:
            for use in plant_info.get("medicinal_uses",[])[:3]:
                st.markdown(f"• {use}")
    with rec2:
        st.markdown("**For the Disease:**")
        for t in dr.get("treatment",[])[:3]:
            st.markdown(f"• {t}")

# ─────────────────────────────────────────────────────────────────────────────
# HOW IT WORKS INFO BOX
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.plant_result and not st.session_state.disease_result:
    st.divider()
    st.markdown("## 🤖 How the AI Works")
    hw1,hw2,hw3,hw4 = st.columns(4)
    with hw1:
        st.markdown("""
        <div style="background:#f0fff4;border-radius:12px;padding:16px;text-align:center;border:1px solid #2E8B57;">
          <div style="font-size:2rem;">📷</div>
          <b>Step 1: Upload</b><br>
          <small>Upload or capture a clear leaf photo</small>
        </div>""", unsafe_allow_html=True)
    with hw2:
        st.markdown("""
        <div style="background:#f0fff4;border-radius:12px;padding:16px;text-align:center;border:1px solid #2E8B57;">
          <div style="font-size:2rem;">🔬</div>
          <b>Step 2: Analyze</b><br>
          <small>AI extracts HSV, texture & shape features</small>
        </div>""", unsafe_allow_html=True)
    with hw3:
        st.markdown("""
        <div style="background:#f0fff4;border-radius:12px;padding:16px;text-align:center;border:1px solid #2E8B57;">
          <div style="font-size:2rem;">🧠</div>
          <b>Step 3: Classify</b><br>
          <small>ML algorithms match against 30 plant profiles</small>
        </div>""", unsafe_allow_html=True)
    with hw4:
        st.markdown("""
        <div style="background:#f0fff4;border-radius:12px;padding:16px;text-align:center;border:1px solid #2E8B57;">
          <div style="font-size:2rem;">📊</div>
          <b>Step 4: Results</b><br>
          <small>Plant ID + Disease + Treatment shown instantly</small>
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🦠 Detectable Diseases")
    dc1,dc2,dc3,dc4 = st.columns(4)
    diseases = list(DISEASE_INFO.items())
    for i,(dname,dinfo) in enumerate(diseases):
        col = [dc1,dc2,dc3,dc4][i%4]
        col.markdown(f"""
        <div style="background:#f8f9fa;border-radius:8px;padding:10px;
          margin:3px;text-align:center;border-top:3px solid {dinfo['severity_color']};">
          <div style="font-size:1.5rem;">{dinfo['icon']}</div>
          <small><b>{dname[:22]}</b></small><br>
          <span style="color:{dinfo['severity_color']};font-size:.75em;">● {dinfo['severity']}</span>
        </div>""", unsafe_allow_html=True)
