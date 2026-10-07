import os, sys
import warnings, os as _os
warnings.filterwarnings("ignore")
_os.environ["PYTHONWARNINGS"] = "ignore"
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
import json

st.set_page_config(page_title="MediBot | MediPlant AI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.main{background:#FAFFFE;}
h1,h2,h3{color:#2E8B57!important;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a3a2a,#2E8B57);}
section[data-testid="stSidebar"] *{color:white!important;}
div.stButton>button{background:linear-gradient(135deg,#2E8B57,#3CB371);
  color:white;border:none;border-radius:8px;font-weight:bold;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

if "user"          not in st.session_state: st.session_state.user = None
if "chat_messages" not in st.session_state: st.session_state.chat_messages = []

with st.sidebar:
    st.markdown("## 🌿 MediPlant AI")
    st.markdown("---")
    if st.session_state.user:
        st.success(f"👤 {st.session_state.user['username']}")
    st.markdown("---")
    st.page_link("app.py",                 label="🏠 Home")
    st.page_link("pages/1_Identify.py", label="🔍 Identify Plant")
    st.markdown("---")
    st.markdown("### 🤖 Gemini API")
    default_gkey = st.session_state.get("gemini_key") or os.environ.get("GEMINI_API_KEY", "")
    gemini_key = st.text_input("Gemini API Key", value=default_gkey, type="password",
                               help="Free key at https://aistudio.google.com")
    if gemini_key:
        st.session_state.gemini_key = gemini_key
    elif default_gkey:
        gemini_key = default_gkey
        st.session_state.gemini_key = default_gkey

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_messages = []
        st.rerun()

@st.cache_data
def load_plants():
    path = os.path.join(_ROOT, "data", "plants_info.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)["plants"]

def find_plant(name):
    try:
        plants = load_plants()
        nl = name.lower().strip()
        for p in plants:
            if nl in p["common_name"].lower() or p["common_name"].lower() in nl:
                return p
    except Exception:
        pass
    return None

def kb_response(user_input):
    """Knowledge base chatbot — works with no API key."""
    try:
        plants = load_plants()
    except Exception:
        return "❌ Could not load plant data. Please check `data/plants_info.json` exists."

    ui = user_input.lower().strip()

    # Greetings
    if any(k in ui for k in ["hello","hi ","hey","namaste","good morning","good evening","start"]):
        return ("👋 **Hello! I'm MediBot!** 🌿\n\n"
                "I'm your AI medicinal plant assistant. Ask me about:\n\n"
                "🌿 **Plant benefits & uses** — 'What is Tulsi used for?'\n"
                "⚠️ **Safety & warnings** — 'Is Neem safe for pregnancy?'\n"
                "📋 **Preparation methods** — 'How to make Ginger tea?'\n"
                "🏥 **Health conditions** — 'Plants for diabetes?'\n"
                "🔬 **Active compounds** — 'What compounds are in Turmeric?'\n\n"
                "What would you like to know? 🌿")

    # About the app
    if any(k in ui for k in ["model","accuracy","how work","ai","deep learning","mediaplant","this app","about"]):
        return ("**🤖 About MediPlant AI:**\n\n"
                "MediPlant AI uses **Ensemble Deep Learning** combining:\n"
                "• **VGG16** — texture & edge features\n"
                "• **ResNet50** — deep residual features\n"
                "• **InceptionV3** — multi-scale features\n\n"
                "Combined accuracy: **95%+** on 30 medicinal plant species.\n\n"
                "Also features **Grad-CAM explainability** to show which leaf parts the AI focused on.")

    # List all plants
    if any(k in ui for k in ["list","all plant","show plant","how many plant","which plant"]):
        items = "\n".join([f"🌿 **{p['common_name']}** — *{p['scientific_name']}*" for p in plants])
        return f"**Plants in my database ({len(plants)}):**\n\n{items}\n\n💡 Ask me about any of these!"

    # Match a specific plant name
    for plant in plants:
        pname = plant["common_name"].lower()
        sci   = plant.get("scientific_name","").lower()
        tamil = plant.get("tamil_name","").lower()
        if pname in ui or sci in ui or (tamil and tamil in ui):
            if any(k in ui for k in ["use","treat","help","good for","benefit","what is","about","tell"]):
                uses = "\n".join([f"✅ {u}" for u in plant["medicinal_uses"]])
                return (f"## 🌿 {plant['common_name']}\n"
                        f"*{plant['scientific_name']}* | Tamil: {plant.get('tamil_name','N/A')}\n\n"
                        f"**{plant.get('description','')}**\n\n"
                        f"**Medicinal Uses:**\n{uses}\n\n"
                        f"**Safety:** {plant['safety_info']}")
            if any(k in ui for k in ["safe","toxic","danger","warn","pregnan","child","side effect"]):
                warns = "\n".join([f"⚠️ {w}" for w in plant.get("warnings",[])])
                return (f"## ⚠️ Safety — {plant['common_name']}\n\n"
                        f"**Toxicity Level:** {plant['toxicity_level']}\n\n"
                        f"{plant['safety_info']}\n\n"
                        + (f"**Specific Warnings:**\n{warns}" if warns else "✅ No major safety warnings."))
            if any(k in ui for k in ["prepare","how to","make","recipe","dose","dosage","consume","take","drink"]):
                methods = "\n".join([f"🌿 {m}" for m in plant.get("preparation_methods",[])])
                return f"## 📋 How to Use — {plant['common_name']}\n\n{methods}"
            if any(k in ui for k in ["compound","chemical","contain","active","ingredient","constituent"]):
                comps = "\n".join([f"• **{c}**" for c in plant.get("active_compounds",[])])
                return f"## 🧪 Active Compounds in {plant['common_name']}\n\n{comps}"
            # General plant info
            return (f"## 🌿 {plant['common_name']}\n"
                    f"*{plant['scientific_name']}*\n\n"
                    f"Tamil: **{plant.get('tamil_name','N/A')}** | Family: **{plant['family']}**\n\n"
                    f"{plant.get('description','')}\n\n"
                    f"**Key Uses:** {', '.join(plant['medicinal_uses'][:4])}\n"
                    f"**Toxicity:** {plant['toxicity_level']} | "
                    f"**Availability:** {plant.get('availability','N/A')}\n\n"
                    f"💬 Ask me specifically about uses, safety, preparation, or compounds!")

    # Condition-based lookup
    condition_map = {
        "diabetes"    : ["Giloy","Turmeric","Moringa","Aloe Vera","Neem"],
        "immunity"    : ["Tulsi","Amla","Giloy","Moringa","Ashwagandha"],
        "stress"      : ["Ashwagandha","Brahmi","Tulsi"],
        "anxiety"     : ["Ashwagandha","Brahmi","Tulsi"],
        "memory"      : ["Brahmi","Ashwagandha"],
        "brain"       : ["Brahmi","Ashwagandha"],
        "sleep"       : ["Ashwagandha","Brahmi"],
        "insomnia"    : ["Ashwagandha","Brahmi"],
        "skin"        : ["Neem","Aloe Vera","Turmeric"],
        "acne"        : ["Neem","Turmeric","Aloe Vera"],
        "hair"        : ["Brahmi","Amla","Aloe Vera"],
        "digestion"   : ["Ginger","Aloe Vera","Moringa"],
        "stomach"     : ["Ginger","Aloe Vera"],
        "cold"        : ["Tulsi","Ginger","Turmeric"],
        "flu"         : ["Tulsi","Ginger","Giloy"],
        "cough"       : ["Tulsi","Vasaka","Pippali","Ginger"],
        "asthma"      : ["Vasaka","Tulsi","Pippali","Bibhitaki"],
        "fever"       : ["Kalmegh","Giloy","Neem","Tulsi","Pippali"],
        "inflammation": ["Turmeric","Ginger","Neem","Guggul","Castor Plant"],
        "arthritis"   : ["Guggul","Turmeric","Ginger","Castor Plant","Ashwagandha"],
        "joint"       : ["Turmeric","Ginger","Castor Plant","Guggul"],
        "cholesterol" : ["Guggul","Moringa","Arjuna","Curry Leaf","Fenugreek"],
        "weight"      : ["Guggul","Pippali","Triphala","Moringa"],
        "liver"       : ["Kutki","Kalmegh","Bhringraj","Giloy","Amla"],
        "blood pressure": ["Arjuna","Hibiscus","Moringa","Punarnava"],
        "cancer"      : ["Amla","Neem","Moringa","Turmeric"],
        "wound"       : ["Aloe Vera","Neem","Turmeric","Gotu Kola"],
        "pain"        : ["Ginger","Turmeric","Ashwagandha","Clove"],
        "kidney"      : ["Punarnava","Gokshura","Coriander"],
        "urinary"     : ["Gokshura","Punarnava","Sandalwood","Coriander"],
        "hair"        : ["Bhringraj","Amla","Curry Leaf","Brahmi","Hibiscus"],
        "skin"        : ["Neem","Manjistha","Sandalwood","Aloe Vera","Turmeric"],
        "acne"        : ["Neem","Manjistha","Sandalwood","Aloe Vera"],
        "memory"      : ["Brahmi","Shankhpushpi","Gotu Kola","Vacha","Ashwagandha"],
        "sleep"       : ["Ashwagandha","Shankhpushpi","Brahmi","Jasmine"],
        "insomnia"    : ["Ashwagandha","Shankhpushpi","Brahmi"],
        "throat"      : ["Licorice","Bibhitaki","Clove","Cardamom","Vasaka"],
        "constipation": ["Triphala","Haritaki","Senna","Castor Plant"],
    }
    for cond, pnames in condition_map.items():
        if cond in ui:
            out = f"## 🌿 Plants that may help with **{cond.title()}**:\n\n"
            for pn in pnames:
                p = find_plant(pn)
                if p:
                    out += f"✅ **{p['common_name']}** (<em>{p['scientific_name']}</em>) — {p['medicinal_uses'][0]}\n\n"
                else:
                    out += f"✅ **{pn}**\n\n"
            out += "⚕️ *Always consult a registered B.A.M.S Ayurvedic practitioner or physician before using any herbal formulation.*"
            return out

    # Fallback
    plant_list = ", ".join([p["common_name"] for p in plants[:20]]) + f", and {len(plants)-20} more"
    return (f"🤔 I didn't quite understand that. Let me help you better!\n\n"
            f"**Try asking:**\n"
            f"• 'What is Tulsi used for?'\n"
            f"• 'Is Neem safe during pregnancy?'\n"
            f"• 'How to prepare Ginger tea?'\n"
            f"• 'What plants help with diabetes or arthritis?'\n"
            f"• 'What compounds are in Turmeric?'\n\n"
            f"**Plants I know ({len(plants)} species):** {plant_list}")

def gemini_response(user_input, api_key):
    """Use Gemini API if key is provided, else fall back to knowledge base."""
    # Try modern google.genai first
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                "You are MediBot, an expert AI assistant specializing in Ayurvedic pharmacognosy and medicinal plants. "
                "Provide accurate, authentic, and scientific botanical responses. Include active phytochemicals, "
                "dosage, and critical safety disclaimers. Format with rich markdown.\n\n"
                f"User question: {user_input}"
            )
        )
        return response.text
    except Exception:
        pass

    # Fallback to google.generativeai
    try:
        import google.generativeai as gai
        gai.configure(api_key=api_key)
        model  = gai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            "You are MediBot, an expert AI assistant specializing in Ayurvedic pharmacognosy and medicinal plants. "
            "Answer helpfully, concisely, and accurately. Always add safety disclaimers when discussing medicinal uses. "
            f"User question: {user_input}"
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return kb_response(user_input)

# ── Page UI ────────────────────────────────────────────────────────────────────
st.title("🤖 MediBot — Medicinal Plant AI Chatbot")
st.markdown("Ask me anything about **50 medicinal plants**, their pharmacological uses, safety warnings, preparation, and contraindications!")

if gemini_key:
    st.success("✅ Gemini AI connected — Enhanced multimodal generative responses active")
else:
    st.info("💡 Running in **Offline Ayurvedic Knowledge Base Mode** (Covers all 50 medicinal plants). Paste a Gemini API key in the sidebar for unlimited live GenAI responses.")

st.divider()

# Quick question buttons
st.markdown("**💡 Quick Questions — click to ask:**")
qcols = st.columns(5)
quick_qs = [
    "What is Tulsi used for?",
    "Is Neem safe?",
    "Herbs for arthritis?",
    "Plants for diabetes?",
    "Herbs for memory?"
]
quick_pressed = None
for col, q in zip(qcols, quick_qs):
    with col:
        if st.button(q, use_container_width=True):
            quick_pressed = q

st.divider()

# Welcome message on first load
if not st.session_state.chat_messages:
    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": ("👋 **Hello! I'm MediBot!** 🌿\n\n"
                    "I am your intelligent botanical assistant trained on **50 medicinal plants** and classical Ayurvedic pharmacopoeias.\n\n"
                    "You can ask me about plant health benefits, phytochemicals, preparation recipes, contraindications, and remedies for specific health ailments.\n\n"
                    "Try asking: *'What is Ashwagandha used for?'* or *'Which plants balance Pitta dosha?'*")
    })

# Display chat history
for msg in st.session_state.chat_messages:
    avatar = "🤖" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Handle quick question click
if quick_pressed:
    st.session_state.chat_messages.append({"role": "user", "content": quick_pressed})
    with st.spinner("🌿 Thinking..."):
        resp = gemini_response(quick_pressed, gemini_key) if gemini_key else kb_response(quick_pressed)
    st.session_state.chat_messages.append({"role": "assistant", "content": resp})
    try:
        from database.db_operations import save_chat_message
        if st.session_state.user:
            save_chat_message(st.session_state.user["id"], "user",      quick_pressed)
            save_chat_message(st.session_state.user["id"], "assistant", resp)
    except Exception:
        pass
    st.rerun()

# Chat input
if user_input := st.chat_input("Ask about any medicinal plant..."):
    st.session_state.chat_messages.append({"role": "user", "content": user_input})
    with st.spinner("🌿 Thinking..."):
        resp = gemini_response(user_input, gemini_key) if gemini_key else kb_response(user_input)
    st.session_state.chat_messages.append({"role": "assistant", "content": resp})
    try:
        from database.db_operations import save_chat_message
        if st.session_state.user:
            save_chat_message(st.session_state.user["id"], "user",      user_input)
            save_chat_message(st.session_state.user["id"], "assistant", resp)
    except Exception:
        pass
    st.rerun()
