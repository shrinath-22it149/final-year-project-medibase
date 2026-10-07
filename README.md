# 🌿 MediPlant AI (Medibase) — Final Year Project
### Smart Medicinal Plant Identification & Clinical Pharmacognosy Platform

---

## 📋 PROJECT OVERVIEW

**MediPlant AI** is a comprehensive, production-grade web application for identifying and classifying medicinal plants, diagnosing plant leaf diseases, and delivering evidence-backed clinical pharmacognosy guidance.

### 🌟 Key Features
- 🔍 **Dual Plant & Disease Diagnostics:** Upload or capture leaf photos for instant 50-species botanical classification and 8-class disease pathological diagnosis.
- 🌡️ **Grad-CAM & Attention Heatmaps:** Visual explainability showing exactly which leaf regions, venation patterns, and contours the AI focused on.
- 🌐 **Pl@ntNet API Integration:** Official botanical API client enabling real 100% accurate plant species identification from leaf photos.
- 🤖 **MediBot AI Assistant (Google Gemini):** Multi-modal GenAI chatbot powered by Google Gemini 2.5 Flash with offline Ayurvedic pharmacopoeia fallback.
- 📺 **50-Plant Video Library:** Curated educational video guides for all 50 plants in **Tamil (தமிழ்)**, English, and Hindi.
- 💊 **Real-Time Drug-Herb Interaction Checker:** Evaluates clinical risks between traditional herbs and pharmaceutical drugs (e.g. Warfarin, Metformin, Digoxin, Aspirin).
- 🧘 **Ayurvedic Dosha (Prakriti) Profiler:** 6-step diagnostic quiz assessing individual Vata, Pitta, and Kapha constitution, matching personalized balancing herbs.
- 🥣 **Classical Remedy & Formulation Builder:** Computes dynamic poly-herbal Ayurvedic formulations (Kwatha, Churna, Lepa, Ksheerapaka) with scaled ratios and preparation protocols.
- 🌱 **Herbal Geo-Habitability & Cultivation Guide:** Agronomic guidelines covering soil pH, sunlight, watering, and climate zone parameters for home and terrace gardening.
- 🔊 **Voice Audio Pronunciation & Reader:** Interactive HTML5 audio speech synthesis reading botanical details and medicinal indications aloud.
- 📄 **Digital Botanical Certification:** Downloadable PDF report with verification credentials, clinical warnings, and diagnostic summaries.
- 👤 **User Profiles & History:** SQLite database with encrypted authentication (`demo` / `demo123`) tracking past scans and saved bookmarks.

---

## 🗂️ PROJECT STRUCTURE

```
mediaplant/
├── app.py                          ← Main landing dashboard
├── requirements.txt                ← Pinned dependencies
├── run.bat                         ← One-click Windows runner (auto-activates venv)
├── README.md                       ← Project documentation
├── .env.example                    ← API keys configuration template
├── .streamlit/
│   └── config.toml                 ← Theme & server configuration (Port 8501)
├── pages/
│   ├── 1_Identify.py               ← Plant identification (Pl@ntNet + Gemini + Ensemble) & Disease detection
│   ├── 2_Database.py               ← 50-Plant Encyclopedia with filters & voice reader
│   ├── 3_Analytics.py              ← Model architecture metrics & evaluation charts
│   ├── 4_Compare.py                ← Side-by-side multi-plant comparison
│   ├── 5_Chatbot.py                ← MediBot AI (Gemini 2.5 Flash + Offline RAG)
│   ├── 6_History.py                ← SQLite scan history & saved favorites
│   ├── 7_Profile.py                ← User auth, registration & stats
│   ├── 8_Drug_Interactions.py      ← Real-time Drug-Herb Interaction & Safety Checker
│   ├── 9_Dosha_Quiz.py             ← Ayurvedic Dosha Profiler & Herb Matcher
│   ├── 10_Remedy_Builder.py        ← Custom Ayurvedic Formulation & Recipe Builder
│   ├── 11_Cultivation_Guide.py     ← Geo-Habitability, Soil & Home Gardening Guide
│   └── 12_Plant_Videos.py          ← 50-Plant Video Library (Tamil / English / Hindi)
├── model/
│   ├── predictor.py                ← Prediction engine (Deep Learning + Feature Vector)
│   ├── disease_predictor.py        ← 8-Class Leaf Pathological Diagnostic Engine
│   ├── gradcam.py                  ← Heatmap explainability visualizer
│   ├── train_model.py              ← Model training pipeline
│   ├── plots/                      ← Confusion matrices & training history plots
│   └── saved_model/                ← Trained weights & metrics
├── database/
│   ├── db_operations.py            ← SQLite ORM & operations
│   └── mediaplant.db               ← SQLite database
├── data/
│   ├── class_labels.json           ← 50 synchronized medicinal plant labels
│   ├── plants_info.json            ← Complete 50-plant pharmacopoeia dataset
│   ├── drug_interactions.json      ← Clinical drug-herb interaction rules
│   └── dataset/                    ← Image dataset repository
└── utils/
    ├── helpers.py                  ← UI helpers & CSS styling
    └── report_generator.py         ← Formatted PDF medical/botanical certificates
```

---

## 🚀 QUICK START GUIDE (Run on Localhost)

### 1. Launch via One-Click Runner (Windows)
Double-click `run.bat` in the `mediaplant` folder. It will automatically activate the virtual environment and start Streamlit:
```
Open: http://localhost:8501
```

### 2. Or Launch via Command Prompt / Terminal
```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Run the application
streamlit run app.py
```

### 3. Demo Login Credentials
* **Username:** `demo`
* **Password:** `demo123`

---

## 📊 50 MEDICINAL PLANTS COVERED

1. Tulsi (Ocimum tenuiflorum)
2. Neem (Azadirachta indica)
3. Aloe Vera (Aloe barbadensis miller)
4. Ginger (Zingiber officinale)
5. Turmeric (Curcuma longa)
6. Ashwagandha (Withania somnifera)
7. Brahmi (Bacopa monnieri)
8. Amla (Phyllanthus emblica)
9. Giloy (Tinospora cordifolia)
10. Moringa (Moringa oleifera)
11. Curry Leaf (Murraya koenigii)
12. Mint (Mentha piperita)
13. Lemongrass (Cymbopogon citratus)
14. Hibiscus (Hibiscus rosa-sinensis)
15. Fenugreek (Trigonella foenum-graecum)
16. Coriander (Coriandrum sativum)
17. Guduchi (Tinospora sinensis)
18. Shatavari (Asparagus racemosus)
19. Triphala (Terminalia chebula complex)
20. Arjuna (Terminalia arjuna)
21. Guggul (Commiphora mukul)
22. Shilajit (Asphaltum punjabianum)
23. Kalmegh (Andrographis paniculata)
24. Bael (Aegle marmelos)
25. Noni (Morinda citrifolia)
26. Papaya Leaf (Carica papaya)
27. Drumstick (Moringa oleifera Pods)
28. Rose (Rosa damascena)
29. Jasmine (Jasminum sambac)
30. Sandalwood (Santalum album)
31. Vasaka (Adhatoda vasica)
32. Manjistha (Rubia cordifolia)
33. Punarnava (Boerhavia diffusa)
34. Bhringraj (Eclipta alba)
35. Shankhpushpi (Convolvulus pluricaulis)
36. Haritaki (Terminalia chebula)
37. Bibhitaki (Terminalia bellirica)
38. Gotu Kola (Centella asiatica)
39. Cardamom (Elettaria cardamomum)
40. Clove (Syzygium aromaticum)
41. Cinnamon (Cinnamomum verum)
42. Licorice (Glycyrrhiza glabra)
43. Senna (Cassia angustifolia)
44. Gokshura (Tribulus terrestris)
45. Kutki (Picrorhiza kurroa)
46. Vacha (Acorus calamus)
47. Pippali (Piper longum)
48. Ajwain (Trachyspermum ammi)
49. Betel Leaf (Piper betle)
50. Castor Plant (Ricinus communis)
