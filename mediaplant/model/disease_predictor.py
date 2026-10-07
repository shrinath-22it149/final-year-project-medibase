"""
MediPlant AI - Plant Disease Detection Engine
Detects 8 types of plant diseases using color + texture analysis.
Works without trained model using visual feature analysis.
"""
import warnings, os
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import sys, numpy as np
from PIL import Image

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

_DCACHE = {"model": None}

# Disease database with full info
DISEASE_INFO = {
    "Healthy": {
        "icon": "✅", "severity": "None", "severity_color": "#28a745",
        "description": "The leaf appears healthy with no visible disease symptoms. Normal green coloration and leaf structure detected.",
        "symptoms": ["Normal green coloration", "Uniform leaf surface", "No spots or lesions", "Good leaf texture"],
        "causes": ["Optimal growing conditions", "Good soil nutrition", "Proper watering"],
        "treatment": ["Continue regular care", "Maintain watering schedule", "Apply balanced fertilizer monthly"],
        "prevention": ["Regular inspection", "Proper spacing between plants", "Good air circulation"],
        "severity_score": 0,
    },
    "Yellow Spots (Nutrient Deficiency)": {
        "icon": "🟡", "severity": "Moderate", "severity_color": "#ffc107",
        "description": "Yellow spots on leaves indicate nutrient deficiency, commonly nitrogen, iron or magnesium deficiency causing chlorosis.",
        "symptoms": ["Yellow/pale spots on leaf surface", "Yellowing between leaf veins", "Pale green or yellow patches", "Stunted growth"],
        "causes": ["Nitrogen deficiency", "Iron deficiency (chlorosis)", "Magnesium deficiency", "Poor soil pH", "Overwatering"],
        "treatment": ["Apply nitrogen-rich fertilizer", "Use iron chelate for iron deficiency", "Add Epsom salt for magnesium", "Test and adjust soil pH to 6.0-7.0"],
        "prevention": ["Regular soil testing", "Balanced fertilization schedule", "Proper watering — avoid overwatering", "Mulching to retain nutrients"],
        "severity_score": 35,
    },
    "Brown Edges (Leaf Scorch)": {
        "icon": "🟤", "severity": "Moderate", "severity_color": "#fd7e14",
        "description": "Brown edges or tips indicate leaf scorch caused by drought stress, salt buildup, or wind damage.",
        "symptoms": ["Brown/crispy leaf edges", "Leaf tip burn", "Browning progressing inward", "Dry leaf margins"],
        "causes": ["Drought stress / under-watering", "Excessive salt buildup in soil", "Hot dry winds", "Root damage", "Fluoride/chlorine in water"],
        "treatment": ["Increase watering frequency", "Flush soil with water to remove salt", "Move plant away from heat/wind", "Trim brown edges with clean scissors"],
        "prevention": ["Consistent watering schedule", "Use rainwater or filtered water", "Mulch to retain moisture", "Wind protection for sensitive plants"],
        "severity_score": 30,
    },
    "Dark Patches (Fungal Infection)": {
        "icon": "⚫", "severity": "High", "severity_color": "#dc3545",
        "description": "Dark brown/black patches indicate fungal infection such as anthracnose, black spot, or leaf blight.",
        "symptoms": ["Dark brown or black irregular patches", "Sunken lesions on leaf", "Water-soaked appearance", "Premature leaf drop"],
        "causes": ["Fungal pathogens (Alternaria, Colletotrichum)", "High humidity and poor air circulation", "Overhead watering", "Infected plant debris"],
        "treatment": ["Apply copper-based fungicide", "Remove and destroy infected leaves", "Improve air circulation", "Neem oil spray (organic option)"],
        "prevention": ["Avoid wetting leaves when watering", "Space plants for air flow", "Remove fallen leaves promptly", "Rotate crops annually"],
        "severity_score": 70,
    },
    "White Powder (Powdery Mildew)": {
        "icon": "⬜", "severity": "High", "severity_color": "#dc3545",
        "description": "White powdery coating on leaves is classic powdery mildew — a fungal disease that thrives in warm, dry conditions.",
        "symptoms": ["White powdery spots on upper leaf surface", "Gray or white dusty coating", "Leaf curling and distortion", "Stunted new growth"],
        "causes": ["Fungal pathogen Erysiphe or Podosphaera", "Warm days with cool nights", "High humidity with poor circulation", "Overcrowding of plants"],
        "treatment": ["Baking soda spray (1 tsp/litre)", "Potassium bicarbonate spray", "Neem oil solution", "Sulfur-based fungicide for severe cases"],
        "prevention": ["Plant resistant varieties", "Ensure good air circulation", "Avoid nitrogen over-fertilization", "Morning watering only"],
        "severity_score": 65,
    },
    "Rust Spots (Rust Disease)": {
        "icon": "🟠", "severity": "High", "severity_color": "#dc3545",
        "description": "Orange-brown rust-colored pustules on leaves indicate rust fungal disease, which spreads rapidly.",
        "symptoms": ["Orange/rust-colored spots or pustules", "Yellow halo around spots", "Powdery orange spores", "Premature defoliation"],
        "causes": ["Rust fungi (Puccinia, Uromyces species)", "Cool wet conditions", "Poor air circulation", "Infected plant material nearby"],
        "treatment": ["Remove infected leaves immediately", "Apply sulfur or copper fungicide", "Neem oil spray weekly", "Destroy heavily infected plants"],
        "prevention": ["Plant rust-resistant varieties", "Avoid overhead irrigation", "Inspect new plants before introduction", "Clean tools between plants"],
        "severity_score": 75,
    },
    "Wilting (Root Rot / Water Stress)": {
        "icon": "🥀", "severity": "Critical", "severity_color": "#721c24",
        "description": "Wilting and drooping with dark discoloration indicates root rot or severe water stress requiring immediate action.",
        "symptoms": ["Wilting despite moist soil", "Yellowing and browning of leaves", "Soft, mushy stem base", "Foul smell from roots"],
        "causes": ["Root rot (Phytophthora, Pythium fungi)", "Overwatering and poor drainage", "Soil compaction", "Severe drought followed by overwatering"],
        "treatment": ["Remove plant from pot, trim black roots", "Repot in fresh well-draining soil", "Apply fungicide to roots", "Reduce watering significantly"],
        "prevention": ["Ensure excellent drainage", "Water only when topsoil is dry", "Use raised beds or container with drainage holes", "Avoid compacted soil"],
        "severity_score": 85,
    },
    "Mosaic Pattern (Viral Infection)": {
        "icon": "🟩", "severity": "Critical", "severity_color": "#721c24",
        "description": "Mosaic or mottled yellow-green pattern on leaves indicates viral infection — often spread by insects and has no cure.",
        "symptoms": ["Yellow-green mosaic or mottled pattern", "Leaf distortion and curling", "Stunted plant growth", "Irregular light/dark green patches"],
        "causes": ["Tobacco mosaic virus (TMV)", "Cucumber mosaic virus (CMV)", "Spread by aphids, thrips, contaminated tools", "Infected seeds or transplants"],
        "treatment": ["No cure — remove and destroy infected plants", "Control insect vectors with insecticide", "Disinfect all tools with bleach solution", "Quarantine infected area"],
        "prevention": ["Use virus-free certified seeds", "Control aphid and thrip populations", "Wash hands before handling plants", "Use reflective mulch to deter insects"],
        "severity_score": 90,
    },
}

def load_disease_model():
    """Load disease detection model or use visual analysis."""
    if _DCACHE["model"] is not None:
        return _DCACHE["model"]
    try:
        import tensorflow as tf
        tf.get_logger().setLevel("ERROR")
        path = os.path.join(_ROOT, "model", "saved_model", "disease_model.h5")
        if os.path.exists(path):
            _DCACHE["model"] = tf.keras.models.load_model(path)
            return _DCACHE["model"]
    except Exception:
        pass
    return None


def _extract_disease_features(img_pil):
    """Extract features relevant for disease detection."""
    arr = np.array(img_pil.resize((224,224)).convert("RGB"), dtype=np.float32) / 255.0
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

    v   = np.max(arr, axis=2)
    minc= np.min(arr, axis=2)
    s   = np.where(v>0.01, (v-minc)/v, 0.0)

    # Leaf mask
    lm = (v>0.12)&(v<0.93)&(s>0.07)
    if lm.sum()<200: lm = np.ones_like(v, dtype=bool)

    r_l=r[lm]; g_l=g[lm]; b_l=b[lm]; v_l=v[lm]; s_l=s[lm]

    # Key disease indicators
    # 1. Yellow fraction (nutrient def, mosaic)
    yellow_frac = float(np.mean((r_l>0.55)&(g_l>0.45)&(b_l<0.30)))

    # 2. Brown fraction (scorch, rust, fungal)
    brown_frac = float(np.mean((r_l>0.45)&(g_l>0.20)&(g_l<0.45)&(b_l<0.25)))

    # 3. White/bright fraction (powdery mildew)
    white_frac = float(np.mean((v_l>0.82)&(s_l<0.18)))

    # 4. Dark patch fraction (fungal black spots)
    dark_frac  = float(np.mean(v_l < 0.25))

    # 5. Orange fraction (rust disease)
    orange_frac = float(np.mean((r_l>0.60)&(g_l>0.28)&(g_l<0.48)&(b_l<0.20)))

    # 6. Healthy green fraction
    green_frac  = float(np.mean((g_l>r_l)&(g_l>b_l)&(s_l>0.15)&(v_l>0.25)&(v_l<0.82)))

    # 7. Mosaic: high variance in green channel (patchy)
    g_var = float(np.var(g_l))

    # 8. Texture uniformity (healthy = uniform)
    vc = v.copy()
    bs = 16
    H_i, W_i = vc.shape
    lv = []
    for ii in range(0,H_i-bs,bs):
        for jj in range(0,W_i-bs,bs):
            lv.append(float(np.var(vc[ii:ii+bs,jj:jj+bs])))
    texture_var = float(np.mean(lv)) if lv else 0.02

    # 9. Overall brightness drop (wilting)
    v_mean = float(np.mean(v_l))

    # 10. Color uniformity
    r_std = float(np.std(r_l)); g_std = float(np.std(g_l)); b_std = float(np.std(b_l))
    color_var = (r_std + g_std + b_std) / 3.0

    return {
        "yellow_frac": yellow_frac, "brown_frac": brown_frac,
        "white_frac":  white_frac,  "dark_frac":  dark_frac,
        "orange_frac": orange_frac, "green_frac": green_frac,
        "g_var":       g_var,       "texture_var": texture_var,
        "v_mean":      v_mean,      "color_var":  color_var,
    }


def detect_disease(image):
    """
    Detect plant disease from leaf image.
    Returns disease name, confidence, severity, and full info.
    """
    warnings.filterwarnings("ignore")
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    img_pil = image.convert("RGB").resize((224,224))
    f = _extract_disease_features(img_pil)

    # Try trained model first
    model = load_disease_model()
    disease_names = list(DISEASE_INFO.keys())

    if model:
        try:
            arr = np.array(img_pil, dtype=np.float32)/255.0
            inp = np.expand_dims(arr, 0)
            probs = model.predict(inp, verbose=0)[0]
            top_idx = int(np.argmax(probs))
            d_name  = disease_names[top_idx] if top_idx < len(disease_names) else "Healthy"
            conf    = float(probs[top_idx])
            return _build_disease_result(d_name, conf, f, probs, disease_names)
        except Exception:
            pass

    # Rule-based disease scoring
    scores = _score_diseases(f)
    probs  = np.array([scores[d] for d in disease_names], dtype=np.float64)
    probs  = np.exp(probs * 4.0) / np.exp(probs * 4.0).sum()
    top_idx = int(np.argmax(probs))
    d_name  = disease_names[top_idx]
    conf    = float(probs[top_idx])
    return _build_disease_result(d_name, conf, f, probs, disease_names)


def _score_diseases(f):
    yf = f["yellow_frac"]; bf = f["brown_frac"]; wf = f["white_frac"]
    df = f["dark_frac"];   of = f["orange_frac"]; gf = f["green_frac"]
    gv = f["g_var"];       tv = f["texture_var"]; vm = f["v_mean"]
    cv = f["color_var"]

    scores = {
        "Healthy":
            gf * 6.0 + (1-yf*8) + (1-bf*8) + (1-df*10) + (1-wf*6) + (vm>0.35)*2.0,

        "Yellow Spots (Nutrient Deficiency)":
            yf * 12.0 + gv * 8.0 + (1-gf)*3.0,

        "Brown Edges (Leaf Scorch)":
            bf * 10.0 + (1-vm)*3.0 + (cv>0.12)*3.0,

        "Dark Patches (Fungal Infection)":
            df * 12.0 + bf * 4.0 + tv * 15.0,

        "White Powder (Powdery Mildew)":
            wf * 15.0 + (1-gf)*4.0 + (cv<0.12)*2.0,

        "Rust Spots (Rust Disease)":
            of * 14.0 + bf * 5.0 + yf * 3.0,

        "Wilting (Root Rot / Water Stress)":
            (1-vm)*6.0 + (1-gf)*4.0 + bf*4.0 + df*3.0,

        "Mosaic Pattern (Viral Infection)":
            gv * 10.0 + yf * 5.0 + cv * 6.0,
    }
    # Ensure all positive
    return {k: max(0.001, v) for k, v in scores.items()}


def _build_disease_result(d_name, conf, feat, probs, disease_names):
    info = DISEASE_INFO.get(d_name, DISEASE_INFO["Healthy"])
    top3 = np.argsort(probs)[-3:][::-1]
    return {
        "disease_name":    d_name,
        "confidence":      conf,
        "icon":            info["icon"],
        "severity":        info["severity"],
        "severity_color":  info["severity_color"],
        "severity_score":  info["severity_score"],
        "description":     info["description"],
        "symptoms":        info["symptoms"],
        "causes":          info["causes"],
        "treatment":       info["treatment"],
        "prevention":      info["prevention"],
        "top3": [{"name": disease_names[i], "confidence": float(probs[i]),
                  "icon": DISEASE_INFO.get(disease_names[i],{}).get("icon","🌿")}
                 for i in top3],
        "features": {
            "Yellow Frac":  round(feat["yellow_frac"]*100,1),
            "Brown Frac":   round(feat["brown_frac"]*100,1),
            "White Frac":   round(feat["white_frac"]*100,1),
            "Dark Frac":    round(feat["dark_frac"]*100,1),
            "Green Health": round(feat["green_frac"]*100,1),
        },
    }
