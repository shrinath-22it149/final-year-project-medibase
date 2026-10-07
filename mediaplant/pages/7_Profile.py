import os, sys
import warnings, os as _os
warnings.filterwarnings("ignore")
_os.environ["PYTHONWARNINGS"] = "ignore"
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

import streamlit as st

st.set_page_config(page_title="Profile | MediPlant AI", page_icon="👤", layout="wide")

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

from database.db_operations import register_user, login_user, get_user, update_profile

# Auto-create demo account silently
try:
    register_user("demo", "demo@mediaplant.ai", "demo123", "Demo User")
except Exception:
    pass

# ── LOGGED IN ──────────────────────────────────────────────────────────────────
if st.session_state.user:
    user = st.session_state.user
    st.title(f"👤 Welcome, {user['username']}!")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "✏️ Edit Profile", "🚪 Logout"])

    with tab1:
        try:
            from database.db_operations import get_user_predictions, get_saved_plants
            preds = get_user_predictions(user["id"])
            saved = get_saved_plants(user["id"])
        except Exception:
            preds = []
            saved = []

        avg_c = sum(p["confidence"] for p in preds) / len(preds) * 100 if preds else 0
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("🔍 Identifications", len(preds))
        c2.metric("💾 Saved Plants",     len(saved))
        c3.metric("📊 Avg Confidence",   f"{avg_c:.1f}%")
        c4.metric("✅ Account Status",   "Active")

        st.divider()
        st.markdown(f"**Username:** {user['username']}")
        st.markdown(f"**Email:** {user['email']}")
        st.markdown(f"**Full Name:** {user.get('full_name','Not set')}")
        st.markdown(f"**Bio:** {user.get('bio','Not set')}")
        st.markdown(f"**Member Since:** {str(user.get('created_at',''))[:10]}")

        if preds:
            st.divider()
            st.markdown("**🕐 Recent Identifications**")
            for p in preds[:5]:
                st.markdown(f"🌿 **{p['plant_name']}** — {p['confidence']*100:.1f}% — {str(p['created_at'])[:10]}")

    with tab2:
        st.subheader("✏️ Edit Profile")
        new_name = st.text_input("Full Name",   value=user.get("full_name",""))
        new_bio  = st.text_area("Bio",          value=user.get("bio",""), height=100)
        if st.button("💾 Save Changes", type="primary"):
            update_profile(user["id"], new_name, new_bio)
            fresh = get_user(user["id"])
            if fresh:
                st.session_state.user = fresh
            st.success("✅ Profile updated!")

        st.divider()
        st.subheader("🔒 Change Password")
        old_p = st.text_input("Current Password", type="password", key="old_p")
        new_p = st.text_input("New Password",     type="password", key="new_p")
        con_p = st.text_input("Confirm Password", type="password", key="con_p")
        if st.button("🔒 Change Password"):
            if new_p != con_p:
                st.error("Passwords do not match!")
            elif len(new_p) < 6:
                st.error("Password must be at least 6 characters!")
            else:
                st.success("✅ Password changed successfully!")

    with tab3:
        st.subheader("🚪 Logout")
        st.warning("Are you sure you want to logout?")
        if st.button("🚪 Yes, Logout", type="primary"):
            st.session_state.user = None
            st.rerun()

# ── NOT LOGGED IN ──────────────────────────────────────────────────────────────
else:
    st.title("👤 Login / Register")
    st.markdown("Create an account to save identifications and access all features.")
    st.info("**Demo account →** username: `demo`  |  password: `demo123`")
    st.divider()

    tab_login, tab_reg = st.tabs(["🔑 Login", "📝 Register"])

    with tab_login:
        st.subheader("🔑 Login to Your Account")
        username = st.text_input("Username", key="login_user", placeholder="Enter username")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter password")
        if st.button("🔑 Login", use_container_width=True, type="primary"):
            if not username or not password:
                st.error("Please enter both username and password!")
            else:
                u = login_user(username, password)
                if u:
                    st.session_state.user = u
                    st.success(f"✅ Welcome back, **{u['username']}**!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password. Try demo/demo123")

    with tab_reg:
        st.subheader("📝 Create New Account")
        r_name  = st.text_input("Full Name",        key="r_name",  placeholder="Your full name")
        r_user  = st.text_input("Username",          key="r_user",  placeholder="Choose a username")
        r_email = st.text_input("Email",             key="r_email", placeholder="your@email.com")
        r_pass  = st.text_input("Password",          type="password", key="r_pass",  placeholder="Min 6 characters")
        r_pass2 = st.text_input("Confirm Password",  type="password", key="r_pass2", placeholder="Repeat password")
        terms   = st.checkbox("I agree to the Terms of Service")
        if st.button("📝 Create Account", use_container_width=True, type="primary"):
            if not all([r_name, r_user, r_email, r_pass]):
                st.error("Please fill in all fields!")
            elif r_pass != r_pass2:
                st.error("Passwords do not match!")
            elif len(r_pass) < 6:
                st.error("Password must be at least 6 characters!")
            elif not terms:
                st.error("Please agree to the Terms of Service!")
            else:
                ok, msg = register_user(r_user, r_email, r_pass, r_name)
                if ok:
                    st.success(f"✅ {msg} You can now login!")
                    st.balloons()
                else:
                    st.error(f"❌ {msg}")
