"""
MediPlant AI - Helper Utilities
"""

import json
import os
import sys
import streamlit as st
from PIL import Image
import numpy as np
import io

# Always resolve root correctly
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_plants_data():
    """Load plant database from JSON - with multiple path fallbacks."""
    paths = [
        os.path.join(ROOT, "data", "plants_info.json"),
        os.path.join(os.getcwd(), "data", "plants_info.json"),
        "data/plants_info.json",
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    return json.load(f)["plants"]
            except Exception:
                continue
    return []


def get_plant_by_name(name):
    """Find a plant by common name (case-insensitive partial match)."""
    plants = load_plants_data()
    if not name:
        return None
    name_l = name.lower().strip()
    for p in plants:
        pname = p.get("common_name","").lower()
        if pname == name_l or name_l in pname or pname in name_l:
            return p
    return None


def confidence_color(conf):
    if conf >= 0.90: return "#2E8B57"
    elif conf >= 0.75: return "#FFA500"
    return "#CC0000"


def confidence_label(conf):
    if conf >= 0.90: return "✅ HIGH CONFIDENCE"
    elif conf >= 0.75: return "⚠️ MEDIUM CONFIDENCE"
    return "❌ LOW CONFIDENCE — Please verify manually"


def toxicity_badge(level):
    colours = {
        "Very Low": ("#d4edda","#155724"),
        "Low"     : ("#d4edda","#155724"),
        "Medium"  : ("#fff3cd","#856404"),
        "High"    : ("#f8d7da","#721c24"),
    }
    bg, fg = colours.get(level, ("#e2e3e5","#383d41"))
    return (f'<span style="background:{bg};color:{fg};padding:3px 10px;'
            f'border-radius:12px;font-weight:bold;">{level}</span>')


def resize_image(image, max_size=400):
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    w, h = image.size
    if max(w, h) > max_size:
        ratio = max_size / max(w, h)
        image = image.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
    return image


def image_to_bytes(image):
    buf = io.BytesIO()
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    image.save(buf, format="PNG")
    return buf.getvalue()


def render_metric_card(label, value, delta=None, color="#2E8B57"):
    delta_html = f'<p style="color:green;margin:0;font-size:.85em;">{delta}</p>' if delta else ""
    return f"""
    <div style="background:white;border-left:5px solid {color};border-radius:8px;
         padding:15px 20px;box-shadow:0 2px 6px rgba(0,0,0,.1);text-align:center;">
        <h2 style="color:{color};margin:0;">{value}</h2>
        <p style="color:#666;margin:4px 0 0;font-size:.9em;">{label}</p>
        {delta_html}
    </div>"""


def inject_css():
    st.markdown("""
    <style>
    .main{background-color:#FAFFFE;}
    h1{color:#2E8B57!important;}
    h2{color:#1a5c38!important;}
    h3{color:#2E8B57!important;}
    section[data-testid="stSidebar"]{
        background:linear-gradient(180deg,#1a3a2a 0%,#2E8B57 100%);}
    section[data-testid="stSidebar"] *{color:white!important;}
    div.stButton>button{
        background:linear-gradient(135deg,#2E8B57,#3CB371);
        color:white;border:none;border-radius:8px;font-weight:bold;
        transition:all .3s ease;}
    div.stButton>button:hover{
        background:linear-gradient(135deg,#1a5c38,#2E8B57);
        transform:translateY(-1px);box-shadow:0 4px 12px rgba(46,139,87,.4);}
    .plant-card{background:white;border-radius:12px;padding:20px;
        box-shadow:0 3px 10px rgba(0,0,0,.1);border-top:4px solid #2E8B57;margin-bottom:15px;}
    .result-banner{background:linear-gradient(135deg,#f0fff4,#e6ffe6);
        border:2px solid #2E8B57;border-radius:12px;padding:20px;text-align:center;margin:10px 0;}
    .warning-box{background:#fff3cd;border-left:5px solid #ffc107;
        border-radius:8px;padding:12px 16px;margin:8px 0;}
    .danger-box{background:#f8d7da;border-left:5px solid #dc3545;
        border-radius:8px;padding:12px 16px;margin:8px 0;}
    .success-box{background:#d4edda;border-left:5px solid #28a745;
        border-radius:8px;padding:12px 16px;margin:8px 0;}
    #MainMenu{visibility:hidden;}footer{visibility:hidden;}
    </style>
    """, unsafe_allow_html=True)
