"""
Builds complete 50-plant database, class labels, drug-herb interactions,
dosha matching profiles, and classical remedy formulations for MediPlant AI.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

PLANTS_50 = [
    {
        "id": 1, "common_name": "Tulsi", "scientific_name": "Ocimum tenuiflorum",
        "tamil_name": "துளசி (Thulasi)", "hindi_name": "तुलसी", "family": "Lamiaceae",
        "category": "Herb", "region": "India, Southeast Asia", "availability": "Very High", "rating": 4.9,
        "description": "Revered as the 'Queen of Herbs' in Ayurveda, Tulsi is an adaptogenic powerhouse that enhances immunity, alleviates respiratory infections, and reduces physical and emotional stress.",
        "medicinal_uses": ["Relieves cough, bronchitis, asthma and fever", "Antimicrobial & immunomodulator", "Reduces stress and cortisol levels", "Natural adaptogen & cellular protector", "Topical antiseptic for skin infections"],
        "active_compounds": ["Eugenol", "Rosmarinic acid", "Ursolic acid", "Linalool", "Beta-caryophyllene"],
        "preparation_methods": ["Herbal Infusion: Steep 10 fresh leaves in boiling water for 5 mins", "Fresh Juice: Extract 10ml juice, mix with honey on empty stomach", "Steam Inhalation: Boil leaves with camphor for congested sinuses"],
        "toxicity_level": "Low", "safety_info": "Generally safe. Mild anticoagulant properties; monitor if on blood thinners.",
        "warnings": ["May interact with blood thinning medications", "Hypoglycemic effect; monitor if taking insulin"],
        "dosha": {"vata": "Balances", "pitta": "Neutral", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Fertile, loamy, well-draining", "sunlight": "Direct sunlight (6+ hrs)", "water": "Daily light watering", "climate": "Tropical and subtropical"}
    },
    {
        "id": 2, "common_name": "Neem", "scientific_name": "Azadirachta indica",
        "tamil_name": "வேம்பு (Vembu)", "hindi_name": "नीम", "family": "Meliaceae",
        "category": "Tree", "region": "Indian Subcontinent, Tropical Africa", "availability": "High", "rating": 4.8,
        "description": "Known as the 'Village Pharmacy', every part of the Neem tree possesses potent antibacterial, antiviral, antifungal, and blood-purifying capabilities.",
        "medicinal_uses": ["Treats stubborn skin diseases, eczema, and acne", "Natural pesticide and oral hygiene protector", "Purifies blood and detoxifies liver", "Helps balance blood glucose in diabetes", "Fights fungal infections & dandruff"],
        "active_compounds": ["Azadirachtin", "Nimbin", "Nimbidin", "Quercetin", "Gedunin"],
        "preparation_methods": ["Leaf Paste: Grind fresh leaves for skin lesions", "Decoction: Boil 10 leaves to wash infected skin", "Neem Seed Oil: Dilute in coconut oil for hair/scalp application"],
        "toxicity_level": "Moderate (Internal)", "safety_info": "Safe topically. Oral consumption must be limited. Strictly prohibited for infants and pregnant women.",
        "warnings": ["Not safe for pregnant or lactating mothers", "Can be toxic to infants if oil is ingested", "May cause hypoglycemia in high doses"],
        "dosha": {"vata": "Aggravates in excess", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Sandy, clay, or rocky well-drained soil", "sunlight": "Full direct sunlight", "water": "Low, drought-resistant", "climate": "Warm arid & semi-arid"}
    },
    {
        "id": 3, "common_name": "Aloe Vera", "scientific_name": "Aloe barbadensis miller",
        "tamil_name": "கற்றாழை (Katrazhai)", "hindi_name": "घृतकुमारी", "family": "Asphodelaceae",
        "category": "Succulent", "region": "Arid & Tropical Worldwide", "availability": "Very High", "rating": 4.9,
        "description": "A succulent plant yielding clear polysaccharidic gel celebrated for dermal rejuvenation, cooling gastrointestinal inflammation, and accelerated tissue healing.",
        "medicinal_uses": ["Cools and heals burns, radiation dermatitis & sunburns", "Deeply moisturizes dermal tissue", "Relieves gastritis, acid reflux, and constipation", "Promotes oral wound healing & reduces plaque", "Regulates sebum production"],
        "active_compounds": ["Acemannan", "Aloin", "Barbaloin", "Aloe-emodin", "Vitamins A, C, E"],
        "preparation_methods": ["Raw Gel: Fillet fresh leaf, wash yellow resin, apply directly", "Digestive Juice: Blend 30ml pure gel with water and cumin", "Cooling Mask: Combine gel with cucumber puree for skin irritation"],
        "toxicity_level": "Low (Gel) / High (Latex)", "safety_info": "Transparent inner gel is benign. The yellow aloin latex beneath the skin is a harsh purgative.",
        "warnings": ["Avoid yellow latex during pregnancy", "Excessive internal consumption can cause potassium loss"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Sandy, porous cactus potting mix", "sunlight": "Bright indirect to direct sun", "water": "Allow soil to dry between waterings", "climate": "Dry, warm, frost-sensitive"}
    },
    {
        "id": 4, "common_name": "Ginger", "scientific_name": "Zingiber officinale",
        "tamil_name": "இஞ்சி (Inji)", "hindi_name": "अदरक", "family": "Zingiberaceae",
        "category": "Rhizome", "region": "Tropical Asia", "availability": "Very High", "rating": 4.9,
        "description": "A pungent aromatic rhizome that stokes the digestive fire (Agni), suppresses nausea, relieves musculoskeletal inflammation, and clears respiratory catarrh.",
        "medicinal_uses": ["Relieves nausea, motion sickness & morning sickness", "Eases osteoarthritis and muscular soreness", "Stimulates gastric digestion and eliminates flatulence", "Combats cold viruses & eases sore throat", "Antiplatelet cardioprotection"],
        "active_compounds": ["Gingerol", "Shogaol", "Zingiberene", "Paradol", "Zingerone"],
        "preparation_methods": ["Ginger Decoction: Simmer crushed fresh root with black pepper", "Digestive Appetizer: Chew thin slice with rock salt before meals", "Dry Ginger Powder (Sunthi): 1g with warm milk for joint pain"],
        "toxicity_level": "Very Low", "safety_info": "Extremely safe in dietary use. High concentrated doses may trigger mild heartburn.",
        "warnings": ["Use caution with gallstones due to bile stimulation", "Mild antiplatelet effect; caution with warfarin"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Aggravates in excess", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Rich, moist, organic loam", "sunlight": "Partial shade to filtered light", "water": "High; keep soil constantly moist", "climate": "Humid, warm tropical"}
    },
    {
        "id": 5, "common_name": "Turmeric", "scientific_name": "Curcuma longa",
        "tamil_name": "மஞ்சள் (Manjal)", "hindi_name": "हल्दी", "family": "Zingiberaceae",
        "category": "Rhizome", "region": "India, Southeast Asia", "availability": "Very High", "rating": 5.0,
        "description": "Ayurveda's golden panacea containing curcuminoids that provide systemic anti-inflammatory, antioxidant, neuroprotective, and hepatic shielding benefits.",
        "medicinal_uses": ["Potent systemic anti-inflammatory", "Accelerates wound healing and clears skin", "Supports hepatic detoxification", "Protects cognitive function and neuroplasticity", "Cardiovascular endothelial protection"],
        "active_compounds": ["Curcumin", "Demethoxycurcumin", "Bisdemethoxycurcumin", "Turmerone", "Atlantone"],
        "preparation_methods": ["Golden Milk: 1/2 tsp powder in warm milk with black pepper and ghee", "Antiseptic Lepa: Paste applied on cuts, scrapes, and bruises", "Morning Tonic: 1/4 tsp in warm water with raw honey"],
        "toxicity_level": "Very Low", "safety_info": "Safe culinary herb. Enhances absorption when taken with piperine (black pepper) and dietary fats.",
        "warnings": ["Avoid massive doses if suffering from bile duct blockage", "Stop 14 days before surgical procedures"],
        "dosha": {"vata": "Balances", "pitta": "Balances in moderation", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Well-drained, loose, organic loamy soil", "sunlight": "Full sun to partial dappled shade", "water": "Moderate to high watering", "climate": "Warm, humid tropical"}
    },
    {
        "id": 6, "common_name": "Ashwagandha", "scientific_name": "Withania somnifera",
        "tamil_name": "அமுக்கிரா (Amukkara)", "hindi_name": "अश्वगंधा", "family": "Solanaceae",
        "category": "Shrub", "region": "India, Middle East, Africa", "availability": "High", "rating": 4.9,
        "description": "Known as 'Indian Ginseng', Ashwagandha is an elite Rasayana adaptogen that rejuvenates neuromuscular vitality, calms anxiety, and optimizes endocrine resilience.",
        "medicinal_uses": ["Reduces stress, nervous exhaustion, and cortisol", "Enhances stamina, muscle mass, and physical endurance", "Supports male reproductive health and testosterone", "Promotes restorative sleep and treats insomnia", "Neuroprotective memory support"],
        "active_compounds": ["Withaferin A", "Withanolide D", "Sominone", "Anaferine", "Withanosides"],
        "preparation_methods": ["Night Rejuvenator: 3g root powder in warm milk with nutmeg and honey", "Decoction: Simmer crushed root in water for 15 minutes", "Medicated Ghee: Infuse in pure A2 cow ghee for vitality"],
        "toxicity_level": "Low", "safety_info": "Safe for long-term adaptogenic use. May increase thyroid hormone synthesis.",
        "warnings": ["Avoid during pregnancy due to potential abortifacient risk in high doses", "Potentiates sedative and thyroid medications"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Aggravates in excess heat", "kapha": "Balances"},
        "cultivation": {"soil": "Sandy loam or light red soil with pH 7.5-8.0", "sunlight": "Full hot sun", "water": "Low; drought-tolerant", "climate": "Dry subtropical"}
    },
    {
        "id": 7, "common_name": "Brahmi", "scientific_name": "Bacopa monnieri",
        "tamil_name": "வல்லாரை (Brahmi / Neerbrahmi)", "hindi_name": "ब्राह्मी", "family": "Plantaginaceae",
        "category": "Aquatic Herb", "region": "Wetlands of India, Asia", "availability": "High", "rating": 4.8,
        "description": "A premier Medhya Rasayana (nootropic herb) that sharpens synaptic transmission, memory retention, mental calm, and cognitive endurance.",
        "medicinal_uses": ["Enhances memory consolidation and cognitive recall", "Calms hyperactivity, anxiety, and ADHD symptoms", "Protects neurons from oxidative free-radical damage", "Improves cerebral blood flow and sleep architecture", "Soothes neuroinflammation"],
        "active_compounds": ["Bacoside A", "Bacoside B", "Bacolopaside", "Luteolin", "Apigenin"],
        "preparation_methods": ["Brain Tonic: 1/2 tsp powder in warm milk or ghee", "Fresh Juice: 5-10ml fresh herb juice with rock candy", "Medicated Oil: Brahmi taila massaged onto scalp for deep sleep"],
        "toxicity_level": "Very Low", "safety_info": "Very safe. Best taken with fat (ghee/milk) to maximize bacoside absorption and prevent mild gastrointestinal cramps.",
        "warnings": ["May cause mild nausea if taken on an empty stomach", "May mildly slow heart rate; caution with bradycardia"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Wet, marshy, clay-rich waterlogged soil", "sunlight": "Partial shade to morning sun", "water": "High; loves boggy moisture", "climate": "Warm, humid tropical"}
    },
    {
        "id": 8, "common_name": "Amla", "scientific_name": "Phyllanthus emblica",
        "tamil_name": "நெல்லிக்காய் (Nellikai)", "hindi_name": "आंवला", "family": "Phyllanthaceae",
        "category": "Tree", "region": "India, Southeast Asia", "availability": "Very High", "rating": 5.0,
        "description": "The Indian Gooseberry is nature's richest source of bio-stable Vitamin C and polyphenols. It balances all three doshas and serves as the cornerstone of Chyawanprash.",
        "medicinal_uses": ["Immune fortification and cellular anti-aging", "Enhances hair follicle strength and stops premature graying", "Improves eyesight and retinal microcirculation", "Improves digestive assimilation and eases hyperacidity", "Cardioprotective lipid balancer"],
        "active_compounds": ["Ascorbic acid", "Emblicanin A & B", "Punigluconin", "Ellagic acid", "Gallic acid"],
        "preparation_methods": ["Fresh Juice: 20ml fresh juice with 1 tsp honey every morning", "Churna (Powder): 3g dried fruit powder in warm water", "Hair Wash: Simmer dried amla in water and rinse scalp"],
        "toxicity_level": "None", "safety_info": "Exceptionally safe food-medicine. Can be taken continuously by people of all ages.",
        "warnings": ["Mild antiplatelet effect; caution before surgery", "High doses may loosen bowels in sensitive individuals"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Light loamy to deep clay soil", "sunlight": "Full sun", "water": "Moderate watering when young; drought-hardy when grown", "climate": "Tropical and subtropical"}
    },
    {
        "id": 9, "common_name": "Giloy", "scientific_name": "Tinospora cordifolia",
        "tamil_name": "சீந்தில் (Seenthil)", "hindi_name": "गिलोय / गुडुची", "family": "Menispermaceae",
        "category": "Climber", "region": "India, Myanmar, Sri Lanka", "availability": "High", "rating": 4.9,
        "description": "Known as 'Amrita' (Nectar of Immortality), Giloy is a bitter tonic climber celebrated for breaking recurrent fevers, rejuvenating hepatocytes, and modulating immunity.",
        "medicinal_uses": ["Breaks recurrent fevers, dengue, and viral infections", "Potent immunomodulator activating macrophages", "Lowers blood glucose levels in diabetes mellitus", "Liver protective against hepatotoxins and drugs", "Relieves gout and rheumatoid arthritis inflammation"],
        "active_compounds": ["Tinosporide", "Cordifolioside A", "Berberine", "Palmatine", "Giloin"],
        "preparation_methods": ["Stem Decoction (Kwath): Boil 2-inch fresh crushed stem in 2 cups water until reduced to half", "Giloy Satva: Water-extracted starch powder, 500mg with honey", "Fresh Juice: 15ml stem juice diluted in warm water"],
        "toxicity_level": "Very Low", "safety_info": "Safe herb. Should be used cautiously in autoimmune disorders because of strong immune activation.",
        "warnings": ["May trigger hypoglycemia when paired with diabetes drugs", "May over-stimulate immune system in lupus or rheumatoid flare-ups"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Medium loamy, organic soil", "sunlight": "Partial to full sunlight; needs support tree/trellis", "water": "Moderate watering", "climate": "Warm tropical"}
    },
    {
        "id": 10, "common_name": "Moringa", "scientific_name": "Moringa oleifera",
        "tamil_name": "முருங்கை (Murungai)", "hindi_name": "सहजन", "family": "Moringaceae",
        "category": "Tree", "region": "Indian Subcontinent", "availability": "Very High", "rating": 4.9,
        "description": "The 'Miracle Tree' is a nutritional powerhouse bursting with plant proteins, iron, calcium, antioxidants, and anti-inflammatory isothiocyanates.",
        "medicinal_uses": ["Treats nutritional anemia and iron deficiency", "Controls hypertension and arterial stiffness", "Reduces systemic inflammation and joint swelling", "Balances blood sugar and cholesterol", "Enhances lactation in nursing mothers"],
        "active_compounds": ["Moringine", "Isothiocyanates", "Quercetin", "Chlorogenic acid", "Beta-carotene"],
        "preparation_methods": ["Leaf Powder: 1 tsp mixed into smoothies, soups, or warm water", "Fresh Leaf Porridge: Cook leaves with lentils and garlic", "Bark/Seed Decoction: Traditional detox tea"],
        "toxicity_level": "Low (Leaves) / Caution (Root bark)", "safety_info": "Leaves and pods are highly nourishing and safe. The roots and root bark contain alkaloids that can induce uterine contractions.",
        "warnings": ["Root bark and flowers must be avoided in pregnancy", "Can lower blood pressure; monitor if taking antihypertensives"],
        "dosha": {"vata": "Balances", "pitta": "Aggravates in excess heat", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Sandy or loamy well-drained soil", "sunlight": "Full intense sun", "water": "Low; highly drought-resistant", "climate": "Arid, semi-arid and tropical"}
    },
    {
        "id": 11, "common_name": "Curry Leaf", "scientific_name": "Murraya koenigii",
        "tamil_name": "கறிவேப்பிலை (Kariveppilai)", "hindi_name": "कढ़ी पत्ता", "family": "Rutaceae",
        "category": "Shrub", "region": "India, Sri Lanka", "availability": "Very High", "rating": 4.7,
        "description": "A dark green aromatic culinary and medicinal shrub whose carbazole alkaloids promote hair melanogenesis, protect beta-cells in diabetes, and aid digestion.",
        "medicinal_uses": ["Stimulates hair growth and halts premature graying", "Aids digestion and prevents morning diarrhea", "Reduces LDL cholesterol and protects liver tissue", "Antidiabetic carbohydrate-blocking activity", "Antimicrobial & oral freshener"],
        "active_compounds": ["Mahanimbine", "Koenimbine", "Girinimbine", "Lutein", "Beta-carotene"],
        "preparation_methods": ["Hair Oil: Simmer fresh leaves in pure coconut oil until dark, massage scalp", "Daily Chutney: Fresh leaves ground with cumin and black salt", "Chewed Raw: 8-10 fresh leaves chewed on an empty stomach"],
        "toxicity_level": "Very Low", "safety_info": "Safe culinary herb eaten daily by millions.",
        "warnings": ["No significant toxicity noted in leaves"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Rich, moist, well-draining garden soil", "sunlight": "Full sun to partial sun", "water": "Regular moderate watering", "climate": "Subtropical and tropical"}
    },
    {
        "id": 12, "common_name": "Mint", "scientific_name": "Mentha piperita",
        "tamil_name": "புதினா (Pudhina)", "hindi_name": "पुदीना", "family": "Lamiaceae",
        "category": "Herb", "region": "Temperate & Subtropical Worldwide", "availability": "Very High", "rating": 4.8,
        "description": "A fragrant cooling herb loaded with menthol that relaxes gastrointestinal smooth muscles, clears sinus airways, and cools excessive bodily heat.",
        "medicinal_uses": ["Relieves IBS, abdominal cramps, and flatulence", "Clears respiratory congestion and opens bronchial passages", "Cooling fever reducer and headache soother", "Freshens breath and combats oral pathogens", "Topical cooling for itchy rashes"],
        "active_compounds": ["Menthol", "Menthone", "Menthyl acetate", "Limonene", "Rosmarinic acid"],
        "preparation_methods": ["Mint Tea: Steep fresh sprigs in hot water with a dash of lime", "Cooling Sherbet: Blend leaves with roasted cumin and rock salt", "Topical Paste: Crushed leaves applied to temples for tension headaches"],
        "toxicity_level": "Very Low", "safety_info": "Safe for regular use. May relax esophageal sphincter in severe GERD.",
        "warnings": ["May aggravate severe gastroesophageal acid reflux (GERD) in sensitive individuals"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Moist, rich, fertile loam", "sunlight": "Partial shade to morning sun", "water": "High; loves moist conditions", "climate": "Wide range"}
    },
    {
        "id": 13, "common_name": "Lemongrass", "scientific_name": "Cymbopogon citratus",
        "tamil_name": "எலுமிச்சை புல் (Elumichai Pul)", "hindi_name": "नींबू घास", "family": "Poaceae",
        "category": "Grass", "region": "Tropical Asia, India", "availability": "High", "rating": 4.6,
        "description": "A tall perennial aromatic grass packed with citral that provides antimicrobial, diaphoretic fever-breaking, and anxiety-relieving benefits.",
        "medicinal_uses": ["Induces sweating to break mild fevers", "Calms nervousness and induces sleep", "Mild diuretic clearing metabolic edema", "Antifungal and antibacterial agent", "Eases digestive bloating and stomach cramps"],
        "active_compounds": ["Citral", "Myrcene", "Geraniol", "Limonene", "Citronellal"],
        "preparation_methods": ["Lemongrass Infusion: Simmer fresh bruised blades with ginger and cardamom", "Essential Oil: Diluted in sesame oil for arthritic joint massage", "Culinary Broth: Bruised stalk simmered in herbal soups"],
        "toxicity_level": "Very Low", "safety_info": "Safe as tea. High essential oil concentrations should not be consumed internally.",
        "warnings": ["Avoid concentrated essential oil during pregnancy"],
        "dosha": {"vata": "Balances", "pitta": "Balances in moderation", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Sandy, loamy well-drained soil", "sunlight": "Full direct sun", "water": "Moderate; tolerates dry spells once established", "climate": "Tropical and subtropical"}
    },
    {
        "id": 14, "common_name": "Hibiscus", "scientific_name": "Hibiscus rosa-sinensis",
        "tamil_name": "செம்பருத்தி (Sembaruthi)", "hindi_name": "गुड़हल", "family": "Malvaceae",
        "category": "Shrub", "region": "Tropical & Subtropical Globally", "availability": "High", "rating": 4.8,
        "description": "A radiant tropical shrub whose flowers and mucilaginous leaves act as a cardiac tonic, blood pressure balancer, and scalp regenerator.",
        "medicinal_uses": ["Reduces systolic and diastolic blood pressure", "Rejuvenates hair roots and treats split ends", "Cooling demulcent for urinary tract irritation", "Regulates menstrual cycle and balances estrogen", "Cardiovascular antioxidant shielding LDL"],
        "active_compounds": ["Anthocyanins", "Hibiscic acid", "Cyanidin-3-glucoside", "Flavonoids", "Mucilage"],
        "preparation_methods": ["Ruby Tea: Steep 4-5 fresh or dried petals in hot water with honey", "Herbal Hair Pack: Grind flowers and leaves into a slimy paste, apply to scalp", "Flower Juice: Macerated petals strained with lime and rock sugar"],
        "toxicity_level": "Very Low", "safety_info": "Safe herbal tonic. May cause mild uterine stimulation in high concentrated doses.",
        "warnings": ["Avoid large doses in early pregnancy", "May interact with antihypertensive medications by compounding BP drop"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Rich, porous, moist potting soil", "sunlight": "Full bright sun (6 hrs)", "water": "Moderate regular watering", "climate": "Warm tropical"}
    },
    {
        "id": 15, "common_name": "Fenugreek", "scientific_name": "Trigonella foenum-graecum",
        "tamil_name": "வெந்தயம் (Vendhayam)", "hindi_name": "मेथी", "family": "Fabaceae",
        "category": "Herb", "region": "India, Mediterranean, North Africa", "availability": "Very High", "rating": 4.8,
        "description": "A bitter clover-like herb whose seeds and leaves contain galactomannan fibers and 4-hydroxyisoleucine, renowned for glycemic regulation and breastmilk enrichment.",
        "medicinal_uses": ["Controls postprandial glucose surges in diabetes", "Enhances breastmilk production in lactating mothers", "Reduces total cholesterol and triglycerides", "Soothes acid reflux and gastritis mucosal lining", "Stimulates hair follicles and eliminates dandruff"],
        "active_compounds": ["4-Hydroxyisoleucine", "Trigonelline", "Diosgenin", "Galactomannan", "Saponins"],
        "preparation_methods": ["Overnight Seed Water: Soak 1 tsp seeds overnight, drink water and chew seeds", "Sprouted Seeds: Eaten in salads for glycemic control", "Hair Mask: Ground soaked seed paste applied to hair for 30 minutes"],
        "toxicity_level": "Very Low", "safety_info": "Safe culinary staple. High intake may impart a sweet maple scent to sweat and urine.",
        "warnings": ["May stimulate uterine contractions; avoid high medicinal doses in pregnancy", "Enhances hypoglycemic effect of insulin"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Aggravates in excess", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Rich, well-draining loam with neutral pH", "sunlight": "Full sun to partial shade", "water": "Moderate watering", "climate": "Cool to moderate tropical"}
    },
    {
        "id": 16, "common_name": "Coriander", "scientific_name": "Coriandrum sativum",
        "tamil_name": "கொத்தமல்லி (Kothamalli)", "hindi_name": "धनिया", "family": "Apiaceae",
        "category": "Herb", "region": "Worldwide, Native to Southern Europe & Asia", "availability": "Very High", "rating": 4.7,
        "description": "Both fresh cilantro leaves and dry seeds act as a master digestive, chelating heavy metals, balancing Pitta fire, and acting as a gentle diuretic.",
        "medicinal_uses": ["Cools burning sensation in stomach and urinary tract", "Binds and facilitates excretion of heavy metals", "Relieves bloating, intestinal spasms, and gas", "Balances blood lipids and cholesterol", "Clears conjunctival eye strain when used as cold wash"],
        "active_compounds": ["Linalool", "Pinene", "Geraniol", "Quercetin", "Terpinene"],
        "preparation_methods": ["Coriander Seed Tea: Boil 1 tbsp crushed seeds in water for 10 minutes", "Fresh Juice: Blend leaves with cucumber and cumin", "Cooling Wash: Filtered sterile decoction for tired eyes"],
        "toxicity_level": "Very Low", "safety_info": "Exceptionally safe culinary herb with virtually no toxicity.",
        "warnings": ["Rare contact allergies in hypersensitive individuals"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Well-drained fertile loam", "sunlight": "Full sun to partial dappled shade", "water": "Consistent moderate watering", "climate": "Cool weather preferred"}
    },
    {
        "id": 17, "common_name": "Guduchi", "scientific_name": "Tinospora sinensis",
        "tamil_name": "சீந்தில் கொடி (Seenthil Kodi)", "hindi_name": "गुडुची / अमृता", "family": "Menispermaceae",
        "category": "Climber", "region": "India, Southeast Asia", "availability": "High", "rating": 4.8,
        "description": "A close relative of Tinospora cordifolia with fleshy heart-shaped leaves, renowned for deep tissue detoxification, uric acid reduction, and immune stamina.",
        "medicinal_uses": ["Eliminates accumulated uric acid in gout", "Balances hyperactive inflammatory cascades", "Protects cellular DNA from free radical damage", "Alleviates chronic allergic rhinitis and asthma", "Detoxifies kidneys and spleen"],
        "active_compounds": ["Tinosporide", "Columbin", "Palmatine", "Magnoflorine", "Berberine"],
        "preparation_methods": ["Stem Decoction: 20g fresh crushed climber simmered in water", "Medicated Ghee: Prepared with cow ghee for neurological calm", "Powder (Churna): 2g twice daily with warm water"],
        "toxicity_level": "Very Low", "safety_info": "Safe herbal adaptogen. Caution in autoimmune conditions.",
        "warnings": ["May lower blood sugar; adjust diabetic medication accordingly"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Loamy soil rich in organic matter", "sunlight": "Bright sunlight", "water": "Moderate watering", "climate": "Warm tropical"}
    },
    {
        "id": 18, "common_name": "Shatavari", "scientific_name": "Asparagus racemosus",
        "tamil_name": "தண்ணீர்விட்டான் கிழங்கு (Thaneervittan)", "hindi_name": "शतावरी", "family": "Asparagaceae",
        "category": "Climber", "region": "India, Sri Lanka, Himalayas", "availability": "High", "rating": 4.9,
        "description": "Known as 'She who possesses 100 husbands', Shatavari is the premier female reproductive rejuvenator, hormonal harmonizer, and gastric mucosal demulcent.",
        "medicinal_uses": ["Balances female estrogenic hormones and eases PMS/menopause", "Enhances lactation and breastmilk quality", "Heals peptic ulcers and gastric hyperacidity", "Deeply hydrates depleted Vata tissues", "Boosts reproductive vitality and libido in both sexes"],
        "active_compounds": ["Shatavarin I-IV", "Sarsasapogenin", "Diosgenin", "Isoflavones", "Mucilage"],
        "preparation_methods": ["Root Powder: 3-5g cooked in warm whole milk with ghee and cardamom", "Shatavari Ghruta: Medicated ghee taken before meals for ulcers", "Decoction: Simmer dried roots in water for 20 minutes"],
        "toxicity_level": "Very Low", "safety_info": "Very safe. Contains phytoestrogens; use clinical discretion in hormone-sensitive cancers.",
        "warnings": ["Caution in estrogen-dependent oncological conditions", "Avoid in acute severe pulmonary congestion (excess Kapha)"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Balances (Best)", "kapha": "Aggravates in excess"},
        "cultivation": {"soil": "Sandy, loose, well-draining soil for tuber development", "sunlight": "Full sun to partial shade", "water": "Moderate watering", "climate": "Subtropical to tropical"}
    },
    {
        "id": 19, "common_name": "Triphala", "scientific_name": "Terminalia chebula complex",
        "tamil_name": "திரிபலா (Thiriphala)", "hindi_name": "त्रिफला", "family": "Combretaceae / Phyllanthaceae",
        "category": "Compound Formulation", "region": "India", "availability": "Very High", "rating": 5.0,
        "description": "The classical tripartite combination of Haritaki, Bibhitaki, and Amalaki. It serves as a gentle bowel regulator, systemic detoxifier, and potent ocular Rasayana.",
        "medicinal_uses": ["Regulates healthy peristalsis without dependency", "Detoxifies the colon and gastrointestinal tract", "Strengthens visual acuity and ocular wellness", "Antioxidant cellular protection and weight management", "Balances oral microbiome and fights cavities"],
        "active_compounds": ["Chebulic acid", "Chebulagic acid", "Ellagic acid", "Gallic acid", "Ascorbic acid"],
        "preparation_methods": ["Bedtime Tonic: 1 tsp powder in warm water or milk at bedtime", "Eye Wash: Strain triphala tea through double sterile cloth, bathe eyes", "Mouth Rinse: Swish warm decoction for healthy gums"],
        "toxicity_level": "None", "safety_info": "Safe for ongoing, lifelong wellness regimens.",
        "warnings": ["May cause loose stools if initial dose is too high; titrate gradually", "Avoid during acute dehydrating diarrhea"],
        "dosha": {"vata": "Balances", "pitta": "Balances", "kapha": "Balances (Tridoshic)"},
        "cultivation": {"soil": "Forest loams", "sunlight": "Full forest canopy to sun", "water": "Natural rainfall", "climate": "Tropical forests"}
    },
    {
        "id": 20, "common_name": "Arjuna", "scientific_name": "Terminalia arjuna",
        "tamil_name": "மருத மரம் (Marutha Maram)", "hindi_name": "अर्जुन", "family": "Combretaceae",
        "category": "Tree", "region": "Riverbanks of Indian Subcontinent", "availability": "High", "rating": 4.9,
        "description": "The legendary Ayurvedic cardio-tonic tree bark that strengthens myocardium contractions, prevents ischemic damage, and tones vascular endothelium.",
        "medicinal_uses": ["Strengthens heart muscle in congestive heart failure", "Normalizes blood pressure and reduces angina episodes", "Accelerates bone fracture healing (Asthisandhaniya)", "Reduces arterial plaque and lipid peroxidation", "Antioxidant protector of cardiac mitochondria"],
        "active_compounds": ["Arjunic acid", "Arjunetin", "Arjungenin", "Terminic acid", "Flavonoids"],
        "preparation_methods": ["Arjuna Ksheerapaka: Simmer 5g bark powder in 1 cup milk + 1 cup water until water evaporates", "Decoction: 10g bark boiled in water down to 1/4th volume", "Bark Churna: 3g with honey or warm water"],
        "toxicity_level": "Very Low", "safety_info": "Very safe cardiovascular botanical. Does not cause sudden dangerous inotropic spikes.",
        "warnings": ["Monitor blood pressure and pulse if already on prescription beta-blockers or digoxin"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Moist, fertile, alluvial riverside soil", "sunlight": "Full sun", "water": "High; loves proximity to river water", "climate": "Subtropical to tropical"}
    },
    {
        "id": 21, "common_name": "Guggul", "scientific_name": "Commiphora mukul",
        "tamil_name": "குக்குலு (Guggulu)", "hindi_name": "गुग्गुल", "family": "Burseraceae",
        "category": "Shrub", "region": "Arid regions of India, Pakistan", "availability": "Medium", "rating": 4.8,
        "description": "An oleo-gum-resin tapped from arid shrubs that acts as a profound fat-clearing, anti-atherosclerotic, and arthritic anti-inflammatory agent.",
        "medicinal_uses": ["Reduces elevated cholesterol, LDL, and triglycerides", "Clears arterial plaque and sluggish circulation", "Relieves osteoarthritis, rheumatoid stiffness, and gout", "Stimulates thyroid metabolism to aid weight loss", "Purifies lymphatic and skin stagnation"],
        "active_compounds": ["Guggulsterone E", "Guggulsterone Z", "Muklic acid", "Cembrene", "Myrcene"],
        "preparation_methods": ["Purified Resin: 500mg-1g purified guggul with warm water after meals", "Yogaraj Guggulu / Kaishore Guggulu: Classical herbal tablets", "Herbal Poultice: Applied over swollen arthritic joints"],
        "toxicity_level": "Low (Purified) / Moderate (Raw)", "safety_info": "Must undergo traditional Ayurvedic shodhana (purification) in Triphala decoction before clinical use.",
        "warnings": ["Avoid during pregnancy due to uterine stimulating action", "May interact with liver-metabolized statins and blood thinners"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Aggravates in excess", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Rocky, sandy, calciferous dry soil", "sunlight": "Intense desert sun", "water": "Minimal; extreme drought-survivor", "climate": "Arid desert"}
    },
    {
        "id": 22, "common_name": "Shilajit", "scientific_name": "Asphaltum punjabianum",
        "tamil_name": "சிலாஜித் (Shilajit)", "hindi_name": "शिलाजीत", "family": "Mineral-Herbal Exudate",
        "category": "Herbo-Mineral", "region": "High Altitude Himalayas (10,000+ ft)", "availability": "Medium", "rating": 5.0,
        "description": "A dark phytogenic mineral pitch exuding from Himalayan rock fractures, rich in fulvic acid, delivering 84+ ionic trace minerals and mitochondrial ATP recharging.",
        "medicinal_uses": ["Enhances cellular mitochondrial ATP bioenergetics", "Rejuvenates physical stamina, libido, and endurance", "Fulvic acid facilitates deep cellular nutrient transport", "Sharpens cognitive memory and prevents tau aggregates", "Counters altitude sickness and hypoxic stress"],
        "active_compounds": ["Fulvic acid", "Humic acid", "Dibenzo-alpha-pyrones", "84+ Ionic trace minerals"],
        "preparation_methods": ["Resin Bead: Dissolve a pea-sized piece (250-500mg) in warm milk, green tea, or warm water", "Morning Elixir: Take with raw honey on empty stomach"],
        "toxicity_level": "None (Purified) / High (Unpurified raw rock)", "safety_info": "Raw resin contains fungal toxins and heavy metals. Use ONLY laboratory-purified (Shodhita) resin.",
        "warnings": ["Contraindicated in active gout (can increase uric acid excretion spikes)", "Ensure laboratory certificates for lead, mercury, and arsenic purity"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Aggravates in excess heat", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "High altitude rocky crags", "sunlight": "High UV mountain sunlight", "water": "Glacial seepage", "climate": "Alpine Himalayan"}
    },
    {
        "id": 23, "common_name": "Kalmegh", "scientific_name": "Andrographis paniculata",
        "tamil_name": "நிலவேம்பு (Nilavembu)", "hindi_name": "कालमेघ", "family": "Acanthaceae",
        "category": "Herb", "region": "India, Sri Lanka", "availability": "High", "rating": 4.9,
        "description": "Known as the 'King of Bitters', Kalmegh possesses fierce antiviral, hepatoprotective, and antipyretic qualities, serving as the main active in Nilavembu Kudineer.",
        "medicinal_uses": ["Combats viral fevers like dengue, chikungunya, and influenza", "Shields hepatocytes against toxins, alcohol, and viruses", "Eliminates intestinal worms and parasites", "Suppresses chronic upper respiratory tract infections", "Stimulates appetite and digestive bile flow"],
        "active_compounds": ["Andrographolide", "Neoandrographolide", "Deoxyandrographolide", "Flavonoids"],
        "preparation_methods": ["Nilavembu Kudineer: 15-30ml decoction twice daily during viral epidemics", "Churna (Powder): 1-2g with warm water after meals", "Cold Infusion: Soaked in water overnight to extract bitters"],
        "toxicity_level": "Low", "safety_info": "Safe at recommended dosages. Extremely bitter taste; take with warm water or honey.",
        "warnings": ["Avoid during pregnancy due to possible anti-fertility effects", "May lower blood pressure and glucose"],
        "dosha": {"vata": "Aggravates in excess", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Sandy, loamy well-drained soil", "sunlight": "Full sun to partial shade", "water": "Moderate watering", "climate": "Warm tropical"}
    },
    {
        "id": 24, "common_name": "Bael", "scientific_name": "Aegle marmelos",
        "tamil_name": "வில்வம் (Vilvam)", "hindi_name": "बेल", "family": "Rutaceae",
        "category": "Tree", "region": "India, Nepal, Southeast Asia", "availability": "High", "rating": 4.8,
        "description": "A sacred tree revered by Lord Shiva. Its leaves and woody fruits are unmatched in curing chronic colitis, bacillary dysentery, and irritable bowel diarrhea.",
        "medicinal_uses": ["Heals chronic dysentery, IBS, and watery diarrhea", "Restores mucosal lining in ulcerative colitis", "Leaves lower blood sugar in diabetes", "Cardioprotective and anti-ulcer properties", "Leaves treat respiratory wheezing and coughs"],
        "active_compounds": ["Marmelosin", "Imperatorin", "Aegeline", "Luvangetin", "Pectin"],
        "preparation_methods": ["Bael Fruit Sharbat: Pulp blended with water, strained, and sweetened lightly", "Leaf Juice: 10ml fresh Vilvam leaf juice for glycemic control", "Unripe Fruit Powder: 3g with buttermilk for diarrhea"],
        "toxicity_level": "Very Low", "safety_info": "Very safe fruit medicine. Unripe fruit cures diarrhea; ripe fruit acts as a mild laxative.",
        "warnings": ["Excessive consumption of ripe fruit can cause flatulence and bloating"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Tolerates poor, stony, alkaline soil", "sunlight": "Full sun", "water": "Low once established; drought-hardy", "climate": "Subtropical to tropical"}
    },
    {
        "id": 25, "common_name": "Noni", "scientific_name": "Morinda citrifolia",
        "tamil_name": "நோனி (Noni / Manjanathi)", "hindi_name": "नोनी", "family": "Rubiaceae",
        "category": "Shrub", "region": "Coastal India, Pacific Islands", "availability": "Medium", "rating": 4.6,
        "description": "The Indian Mulberry, rich in proxeronine, scopoletin, and polysaccharides that stimulate cellular repair, activate T-cells, and ease systemic inflammation.",
        "medicinal_uses": ["Activates immune T-cell and macrophage responses", "Relieves arthritis and chronic joint pain", "Regulates blood pressure via scopoletin vasodilation", "Protects cellular DNA against mutagenic damage", "Boosts physical energy and counters fatigue"],
        "active_compounds": ["Proxeronine", "Scopoletin", "Damnacanthal", "Anthraquinones", "Polysaccharides"],
        "preparation_methods": ["Fermented Juice: 30ml pure organic juice in half a glass of warm water on empty stomach", "Leaf Compress: Warmed leaves bound over arthritic joints"],
        "toxicity_level": "Low", "safety_info": "Safe in healthy individuals. High in potassium; caution in advanced chronic kidney disease.",
        "warnings": ["Contraindicated in severe renal failure due to high potassium content", "Rare reports of liver sensitivity with contaminated brands"],
        "dosha": {"vata": "Balances", "pitta": "Balances in moderation", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Sandy, saline, coastal soil", "sunlight": "Full tropical sun", "water": "Moderate; tolerates brackish water", "climate": "Humid coastal tropical"}
    },
    {
        "id": 26, "common_name": "Papaya Leaf", "scientific_name": "Carica papaya",
        "tamil_name": "பப்பாளி இலை (Pappali Ilai)", "hindi_name": "पपीते का पत्ता", "family": "Caricaceae",
        "category": "Small Tree", "region": "Tropical America, Cultivated Worldwide", "availability": "Very High", "rating": 4.9,
        "description": "Fresh papaya leaves are celebrated worldwide for their clinically proven ability to rapidly boost blood platelet (thrombocyte) count during dengue viral infections.",
        "medicinal_uses": ["Rapidly increases blood platelet count in dengue fever", "Papain enzyme breaks down stubborn dietary proteins", "Fights intestinal worms, pinworms, and amoeba", "Purifies blood and supports hepatic recovery", "Topical application speeds wound sloughing"],
        "active_compounds": ["Papain", "Chymopapain", "Carpaine", "Pseudocarpaine", "Flavonoids"],
        "preparation_methods": ["Fresh Leaf Juice: Crush clean leaves (remove bitter stems), squeeze through cloth: 15-20ml twice daily", "Herbal Tea: Dried leaf flakes steeped in boiling water for 8 mins"],
        "toxicity_level": "Low", "safety_info": "Safe at therapeutic doses. Very bitter taste.",
        "warnings": ["Avoid during pregnancy due to potential uterine stimulating carpaine alkaloids", "Do not boil leaves excessively for platelet therapy; fresh extract works best"],
        "dosha": {"vata": "Balances", "pitta": "Balances", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Rich, porous, well-draining loam; hates standing water", "sunlight": "Full sun", "water": "Moderate watering", "climate": "Warm tropical"}
    },
    {
        "id": 27, "common_name": "Drumstick", "scientific_name": "Moringa oleifera (Pods)",
        "tamil_name": "முருங்கைக்காய் (Murungaikkai)", "hindi_name": "सहजन फली", "family": "Moringaceae",
        "category": "Tree", "region": "Indian Subcontinent", "availability": "Very High", "rating": 4.8,
        "description": "The green ribbed seed pods of the Moringa tree are dense with zinc, sulfur amino acids, and minerals that boost bone density, male reproductive vitality, and digestion.",
        "medicinal_uses": ["Strengthens bone density and supplies bioavailable calcium", "Purifies blood and lowers elevated blood sugar", "Enhances male semen parameters and stamina", "Stimulates healthy gallbladder bile flow", "Antimicrobial protection against gut pathogens"],
        "active_compounds": ["Oleic acid", "Moringine", "Glucosinolates", "Zeatin", "Zinc"],
        "preparation_methods": ["Nutritious Soup: Simmer chopped pods with garlic, onions, and black pepper", "Cooked Curry: Stewed in lentil sambar or vegetable broths", "Seed Decoction: Simmer crushed seeds for joint inflammation"],
        "toxicity_level": "None", "safety_info": "Completely safe nutritious vegetable-medicine.",
        "warnings": ["No adverse toxicity when consumed as dietary food"],
        "dosha": {"vata": "Balances", "pitta": "Neutral", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Loose sandy loam", "sunlight": "Full direct sunlight", "water": "Low to moderate", "climate": "Tropical and subtropical"}
    },
    {
        "id": 28, "common_name": "Rose", "scientific_name": "Rosa damascena",
        "tamil_name": "ரோஜா (Roja)", "hindi_name": "गुलाब", "family": "Rosaceae",
        "category": "Shrub", "region": "Mediterranean, Persia, India", "availability": "High", "rating": 4.9,
        "description": "Damask Rose petals are a sweet, astringent, and deeply cooling cardiac tonic that pacifies aggravated Pitta fire, soothes inflamed skin, and lifts depressed moods.",
        "medicinal_uses": ["Cools excessive heat, burning sensations, and acidity", "Soothes emotional grief, heart palpitations, and stress", "Tones facial skin, minimizes pores, and heals acne", "Relieves menstrual cramps and heavy bleeding", "Gentle laxative in the form of Gulkand"],
        "active_compounds": ["Geraniol", "Citronellol", "Phenylethyl alcohol", "Nerol", "Gallic acid"],
        "preparation_methods": ["Gulkand (Rose Jam): Layer petals with rock sugar and sun-cure for 3 weeks", "Rose Water: Pure steam distillate used as eye drops and skin mist", "Petal Infusion: Steep fragrant dried petals in warm water with cardamom"],
        "toxicity_level": "None", "safety_info": "Exceptionally safe, gentle, and pleasing tonic.",
        "warnings": ["Avoid chemically sprayed ornamental florist roses; use certified organic edible Damask roses"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Rich, well-draining loamy garden soil with manure", "sunlight": "Direct sun (5-6 hours)", "water": "Regular deep watering", "climate": "Temperate to subtropical"}
    },
    {
        "id": 29, "common_name": "Jasmine", "scientific_name": "Jasminum sambac",
        "tamil_name": "மல்லிகை (Malligai)", "hindi_name": "मोगरा / चमेली", "family": "Oleaceae",
        "category": "Climbing Shrub", "region": "South & Southeast Asia", "availability": "High", "rating": 4.7,
        "description": "An intensely fragrant white flower known for neuro-calming properties, relieving breast engorgement, healing mouth ulcers, and cooling inflammatory dermatoses.",
        "medicinal_uses": ["Relieves tension headaches, nervous anxiety, and insomnia", "Topical leaf/flower paste heals aphthous mouth ulcers", "Cools hot inflamed skin rashes and eye burning", "Topical breast compress reduces lactation engorgement", "Aromatherapeutic mood elevation"],
        "active_compounds": ["Benzyl acetate", "Linalool", "Jasmone", "Indole", "Methyl anthranilate"],
        "preparation_methods": ["Fragrant Tea: Infuse dry blossoms with green tea leaves", "Cooling Paste: Grind fresh petals with rose water for skin redness", "Aromatic Floral Water: Spritz on face and pillow before sleep"],
        "toxicity_level": "Very Low", "safety_info": "Safe. Aromatherapy should be mild for asthmatic patients sensitive to strong floral scents.",
        "warnings": ["May suppress breast milk production when applied topically to breasts"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Well-draining, rich loamy soil", "sunlight": "Full morning sun", "water": "Regular watering; avoid waterlogging", "climate": "Warm tropical"}
    },
    {
        "id": 30, "common_name": "Sandalwood", "scientific_name": "Santalum album",
        "tamil_name": "சந்தனம் (Chandanam)", "hindi_name": "चंदन", "family": "Santalaceae",
        "category": "Tree", "region": "Southern India (Karnataka, Tamil Nadu)", "availability": "Medium", "rating": 5.0,
        "description": "One of the most sacred woods in Ayurveda, white sandalwood heartwood cools internal visceral heat, clears cystic acne, and elevates spiritual meditation.",
        "medicinal_uses": ["Cools burning sensations, prickly heat, and sun damage", "Eliminates inflammatory acne, scars, and blemishes", "Soothes cystitis and urinary tract burning", "Astringent cardiac and nervous relaxant", "Enhances mental clarity and meditation depth"],
        "active_compounds": ["Alpha-santalol", "Beta-santalol", "Santene", "Santalene", "Teresantalic acid"],
        "preparation_methods": ["Chandan Lepa: Rub sandalwood heartwood stick on stone with rose water to create paste", "Chandanadi Taila: Medicated cooling oil for head and skin", "Internal Infusion: 1g purified powder with water for urinary burning"],
        "toxicity_level": "Very Low", "safety_info": "Safe topically and in culinary medicine. Beware of cheap synthetic fragrance adulterants.",
        "warnings": ["Do not ingest synthetic sandalwood aroma oils", "Caution in advanced chronic kidney disease with large internal doses"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Sandy, clay, red rocky soil; hemiparasitic (requires host tree like Neem or Casuarina)", "sunlight": "Full sun", "water": "Low to moderate", "climate": "Tropical dry deciduous"}
    },
    {
        "id": 31, "common_name": "Vasaka", "scientific_name": "Adhatoda vasica",
        "tamil_name": "ஆடாதோடை (Adathodai)", "hindi_name": "वासा / अडूसा", "family": "Acanthaceae",
        "category": "Shrub", "region": "Himalayan foothills, Plains of India", "availability": "High", "rating": 4.9,
        "description": "Known as Malabar Nut, Vasaka is the supreme Ayurvedic respiratory herb. It yields vasicine, a potent bronchodilator and mucolytic that thins phlegm and stops wheezing.",
        "medicinal_uses": ["Relieves asthma, chronic bronchitis, and severe coughs", "Thins viscous bronchial mucus and aids expectoration", "Stops bleeding in hemoptysis, nosebleeds, and piles", "Reduces inflammatory throat swelling and hoarseness", "Antimicrobial against respiratory pathogens"],
        "active_compounds": ["Vasicine", "Vasicinone", "Adhatodine", "Vasicol", "Anisotine"],
        "preparation_methods": ["Vasaka Syrup: Simmer leaves in water with honey, long pepper, and ginger", "Fresh Leaf Juice: 10ml juice with raw honey twice daily", "Decoction: 15g dried leaf boiled in 200ml water down to 50ml"],
        "toxicity_level": "Low", "safety_info": "Safe expectorant. Stimulates uterine contractions in high doses; avoid during pregnancy.",
        "warnings": ["Contraindicated in pregnancy due to uterotonic action (induces uterine contractions)"],
        "dosha": {"vata": "Aggravates in excess", "pitta": "Balances (Best)", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Poor to fertile loamy soil", "sunlight": "Full sun to partial shade", "water": "Low to moderate; hardy", "climate": "Subtropical to tropical"}
    },
    {
        "id": 32, "common_name": "Manjistha", "scientific_name": "Rubia cordifolia",
        "tamil_name": "மஞ்சட்டி (Manjistha)", "hindi_name": "मंजीष्ठा", "family": "Rubiaceae",
        "category": "Climbing Herb", "region": "Hilly regions of India, Himalayas", "availability": "High", "rating": 4.8,
        "description": "The premier Ayurvedic lymph-clearing and blood-purifying root. Its red anthraquinones dissolve metabolic sludge (Ama), clear cystic acne, and tone the microcirculation.",
        "medicinal_uses": ["Clears sluggish lymphatic circulation and swollen nodes", "Dramatically improves stubborn cystic acne and hyperpigmentation", "Dissolves blood stagnation and promotes regular menses", "Protects kidney nephrons and supports urinary detox", "Accelerates chronic wound healing"],
        "active_compounds": ["Purpurin", "Munjistin", "Alizarin", "Rubiadin", "Nordamnacanthal"],
        "preparation_methods": ["Root Powder: 2-3g with warm water after meals", "Complexion Lepa: Mix powder with honey and sandalwood for dark spots", "Decoction: Simmer crushed root in water down to 1/4th volume"],
        "toxicity_level": "Low", "safety_info": "Safe herbal detoxifier. May temporarily tint urine and stool a harmless reddish-orange shade.",
        "warnings": ["Avoid during pregnancy due to emmenagogue action"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Rich, moist, loamy soil", "sunlight": "Partial shade", "water": "Regular watering", "climate": "Montane subtropical"}
    },
    {
        "id": 33, "common_name": "Punarnava", "scientific_name": "Boerhavia diffusa",
        "tamil_name": "மூக்கிரட்டை (Mookirattai)", "hindi_name": "पुनर्नवा", "family": "Nyctaginaceae",
        "category": "Spreading Herb", "region": "Throughout India and Warm Climates", "availability": "High", "rating": 4.8,
        "description": "Meaning 'That which renews the body', Punarnava is a renowned rejuvenating diuretic that regenerates nephrons, drains water retention, and heals congestive hepatic tissue.",
        "medicinal_uses": ["Flushes kidney gravel, excess uric acid, and metabolic waste", "Reduces generalized edema, ankle swelling, and ascites", "Regenerates kidney and liver tissues", "Combats urinary tract infections and cystitis", "Cardioprotective by relieving fluid overload"],
        "active_compounds": ["Punarnavine", "Boeravinones A-F", "Rotenoids", "Sitosterol", "Liriodendrin"],
        "preparation_methods": ["Whole Herb Decoction: 20g fresh herb boiled in water to 1/4th volume", "Root Powder: 3g with warm water or honey twice daily", "Cooked Greens: Fresh tender leaves cooked with lentils"],
        "toxicity_level": "Very Low", "safety_info": "Very safe, non-potassium-wasting natural diuretic.",
        "warnings": ["May compound effect of synthetic prescription diuretics; monitor hydration"],
        "dosha": {"vata": "Balances", "pitta": "Balances", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Sandy loam, dry wastelands", "sunlight": "Full sun", "water": "Low; very drought-tolerant", "climate": "Warm tropical"}
    },
    {
        "id": 34, "common_name": "Bhringraj", "scientific_name": "Eclipta alba",
        "tamil_name": "கரிசலாங்கண்ணி (Karisalanganni)", "hindi_name": "भृंगराज", "family": "Asteraceae",
        "category": "Herb", "region": "Moist Tropical Regions Worldwide", "availability": "High", "rating": 4.9,
        "description": "Known as the 'Ruler of Hair', Bhringraj revitalizes dormant hair follicles, reverses premature graying, calms liver fire, and sharpens visual acuity.",
        "medicinal_uses": ["Prevents male/female pattern hair thinning and regrows hair", "Reverses premature graying and darkens hair naturally", "Potent hepatoprotective agent clearing fatty liver", "Cools eye burning, strain, and conjunctival redness", "Promotes restful sleep when massaged onto scalp"],
        "active_compounds": ["Wedelolactone", "Demethylwedelolactone", "Ecliptine", "Stigmasterol", "Luteolin"],
        "preparation_methods": ["Bhringraj Taila: Leaves infused into sesame or coconut oil for scalp", "Fresh Leaf Juice: 10ml juice with honey for liver support", "Karisalanganni Soup: Leaves stewed with shallots and cumin"],
        "toxicity_level": "Very Low", "safety_info": "Safe for regular topical and oral wellness use.",
        "warnings": ["Cooling potency; individuals prone to recurrent chest colds should take with ginger"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Moist, water-retentive clay loam", "sunlight": "Full sun to partial shade", "water": "High; loves moist ditch banks", "climate": "Warm humid tropical"}
    },
    {
        "id": 35, "common_name": "Shankhpushpi", "scientific_name": "Convolvulus pluricaulis",
        "tamil_name": "சங்குபுஷ்பி (Shankhpushpi)", "hindi_name": "शंखपुष्पी", "family": "Convolvulaceae",
        "category": "Herb", "region": "Dry plains of India", "availability": "High", "rating": 4.8,
        "description": "An elite Ayurvedic brain tonic with morning-glory-shaped white flowers that calms nervous exhaustion, treats anxiety, balances thyroid, and enhances intellect.",
        "medicinal_uses": ["Sharpens focus, concentration, and exam stamina in students", "Relieves nervous anxiety, restlessness, and panic episodes", "Induces deep restful sleep in chronic insomnia", "Reduces elevated stress-related blood pressure", "Balances hyperthyroidism symptoms"],
        "active_compounds": ["Convolvine", "Convolamine", "Scopoletin", "Shankhpushpine", "Beta-sitosterol"],
        "preparation_methods": ["Nootropic Milk: 3g powder stirred into warm milk with 1/2 tsp ghee and honey", "Fresh Syrup: 15ml syrup with water before sleep", "Herbal Tea: Steep whole dried herb in hot water"],
        "toxicity_level": "Very Low", "safety_info": "Safe, non-sedating, non-addictive brain tonic.",
        "warnings": ["May slightly lower blood pressure; monitor if naturally hypotensive"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Sandy, gravelly dry wasteland soil", "sunlight": "Full direct sun", "water": "Low watering", "climate": "Subtropical arid"}
    },
    {
        "id": 36, "common_name": "Haritaki", "scientific_name": "Terminalia chebula",
        "tamil_name": "கடுக்காய் (Kadukkai)", "hindi_name": "हरड़", "family": "Combretaceae",
        "category": "Tree", "region": "Deciduous forests of India, Nepal", "availability": "High", "rating": 4.9,
        "description": "Revered as the 'Mother of Medicines', Haritaki gently scrapes visceral toxins from the intestinal villi, stimulates intelligence, and restores tridoshic balance.",
        "medicinal_uses": ["Gentle colon regulator clearing chronic constipation", "Accelerates wound healing and mouth ulcer recovery", "Protects gastric mucosa from ulceration", "Enhances longevity, metabolic longevity, and digestion", "Lowers elevated blood sugar"],
        "active_compounds": ["Chebulic acid", "Chebulagic acid", "Corilagin", "Tannins", "Gallic acid"],
        "preparation_methods": ["Kadukkai Water: 1/2 tsp powder in warm water at bedtime", "Mouthwash: Decoction for spongy bleeding gums and loose teeth", "Wound Powder: Applied dry on weepy ulcers"],
        "toxicity_level": "Very Low", "safety_info": "Safe everyday digestive herb. Possesses all tastes except salty.",
        "warnings": ["Contraindicated in severe dehydration, acute exhaustion, and pregnancy"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Balances", "kapha": "Balances"},
        "cultivation": {"soil": "Forest loam", "sunlight": "Full sun", "water": "Moderate", "climate": "Subtropical"}
    },
    {
        "id": 37, "common_name": "Bibhitaki", "scientific_name": "Terminalia bellirica",
        "tamil_name": "தான்றிக்காய் (Thandrikkai)", "hindi_name": "बहेड़ा", "family": "Combretaceae",
        "category": "Tree", "region": "Plains and lower hills of Southeast Asia", "availability": "High", "rating": 4.7,
        "description": "Meaning 'That which makes one fearless of disease', Bibhitaki is the prime Kapha-pacifying fruit of Triphala, specialized for clearing mucus, throat hoarseness, and eyes.",
        "medicinal_uses": ["Dissolves stubborn bronchial mucus, cough, and laryngitis", "Strengthens vocal cords (popular with singers)", "Reduces visceral fat and supports liver metabolism", "Nourishes hair roots and prevents premature shedding", "Astringent protector against diarrhea"],
        "active_compounds": ["Belliricanin", "Belleric acid", "Chebulagic acid", "Ellagic acid", "Gallic acid"],
        "preparation_methods": ["Throat Lozenge: Suckle small fruit piece with honey for persistent cough", "Powder: 2g with warm water after meals", "Decoction: Gargle warm decoction for sore throat"],
        "toxicity_level": "Very Low", "safety_info": "Safe, astringent fruit medicine.",
        "warnings": ["Dry astringency may aggravate Vata if taken in huge quantities without ghee or oil"],
        "dosha": {"vata": "Aggravates in excess", "pitta": "Balances", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Clayey, sandy loam", "sunlight": "Full sun", "water": "Moderate", "climate": "Tropical deciduous"}
    },
    {
        "id": 38, "common_name": "Gotu Kola", "scientific_name": "Centella asiatica",
        "tamil_name": "வல்லாரை (Vallarai)", "hindi_name": "मंडूकपर्णी", "family": "Apiaceae",
        "category": "Creeping Herb", "region": "Wetlands of Tropical Asia, Madagascar", "availability": "High", "rating": 4.9,
        "description": "The fan-shaped 'Herb of Longevity' that stimulates type-I collagen synthesis, repairs micro-capillaries, boosts neurogenesis, and elevates IQ and mental calm.",
        "medicinal_uses": ["Stimulates collagen synthesis and heals deep scar tissue", "Strengthens venous wall integrity in varicose veins", "Nootropic memory sharpener and anxiety reducer", "Enhances dendritic branching in brain neurons", "Cools chronic inflammatory skin conditions"],
        "active_compounds": ["Asiaticoside", "Madecassoside", "Asiatic acid", "Madecassic acid", "Centelloside"],
        "preparation_methods": ["Fresh Salad / Chutney: Fresh leaves ground with shredded coconut and shallots", "Infusion: 1 tsp dried leaf in hot water with honey", "Topical Cream: Madecassoside extract applied to surgical scars"],
        "toxicity_level": "Very Low", "safety_info": "Extremely safe food-herb eaten as culinary greens across Asia.",
        "warnings": ["Very high concentrated doses may cause mild dizziness or drowsiness"],
        "dosha": {"vata": "Balances", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Damp, rich, muddy soil", "sunlight": "Partial shade to morning sun", "water": "High; loves constant moisture", "climate": "Tropical wetlands"}
    },
    {
        "id": 39, "common_name": "Cardamom", "scientific_name": "Elettaria cardamomum",
        "tamil_name": "ஏலக்காய் (Elakkai)", "hindi_name": "इलायची", "family": "Zingiberaceae",
        "category": "Perennial Herb", "region": "Western Ghats of India (Cardamom Hills)", "availability": "High", "rating": 4.9,
        "description": "The 'Queen of Spices', green cardamom pods possess an exquisite aroma of terpinyl acetate that neutralizes acidity, clears halitosis, and relieves nausea.",
        "medicinal_uses": ["Neutralizes stomach acid, gas, and indigestion cramps", "Freshens breath and combats oral microbes", "Relieves nausea, vomiting, and acid regurgitation", "Clears bronchial mucus and calms asthma wheezing", "Mild diuretic helping eliminate urinary toxins"],
        "active_compounds": ["1,8-Cineole", "Alpha-terpinyl acetate", "Limonene", "Linalool", "Sabinene"],
        "preparation_methods": ["Cardamom Pod Chew: Lightly crush pod and chew after meals", "Digestive Tea: Boil crushed seeds with ginger and mint", "Flavoring Powder: 1/4 tsp in milk or herbal porridges"],
        "toxicity_level": "None", "safety_info": "Exceptionally safe, cherished culinary spice.",
        "warnings": ["Use caution with large gallstones due to mild bile duct contraction"],
        "dosha": {"vata": "Balances", "pitta": "Balances in moderation", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Rich, loamy forest soil with humus", "sunlight": "Dappled canopy shade", "water": "High humidity and continuous rain", "climate": "Highland tropical rain forests"}
    },
    {
        "id": 40, "common_name": "Clove", "scientific_name": "Syzygium aromaticum",
        "tamil_name": "கிராம்பு (Kirambu)", "hindi_name": "लौंग", "family": "Myrtaceae",
        "category": "Tree", "region": "Maluku Islands, India, Madagascar", "availability": "High", "rating": 4.9,
        "description": "Dried unopened flower buds containing the highest natural concentration of eugenol, providing unmatched local dental anesthesia, antibacterial, and digestive benefits.",
        "medicinal_uses": ["Instant local numbing relief for toothaches and dental pain", "Powerful antibacterial against food-borne pathogens", "Relieves bloating, flatulence, and nausea", "Clears throat irritation and coughing fits", "Inhibits blood clotting and reduces inflammation"],
        "active_compounds": ["Eugenol", "Eugenyl acetate", "Beta-caryophyllene", "Vanillin", "Gallic acid"],
        "preparation_methods": ["Clove Oil: 1 drop on cotton ball pressed onto aching tooth", "Clove Tea: Steep 3-4 crushed cloves in boiling water", "Whole Bud Suckle: Keep one bud in mouth for throat tickle"],
        "toxicity_level": "Low (Buds) / Moderate (Undiluted Essential Oil)", "safety_info": "Whole cloves are very safe. Pure essential oil can cause mucous membrane burns if not diluted.",
        "warnings": ["Never apply undiluted clove essential oil directly to infant gums", "Mild anticoagulant action; caution with blood thinners"],
        "dosha": {"vata": "Balances", "pitta": "Aggravates in excess heat", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Rich red loamy soil with good drainage", "sunlight": "Warm coastal sunshine with sea breeze", "water": "High; regular rainfall", "climate": "Humid maritime tropical"}
    },
    {
        "id": 41, "common_name": "Cinnamon", "scientific_name": "Cinnamomum verum",
        "tamil_name": "இலவங்கப்பட்டை (Lavangapattai)", "hindi_name": "दालचीनी", "family": "Lauraceae",
        "category": "Tree", "region": "Sri Lanka, Southern India", "availability": "High", "rating": 4.8,
        "description": "True Ceylon cinnamon inner bark acts as a natural insulin mimetic, boosting cellular glucose uptake, suppressing fungal candida, and warming cold extremities.",
        "medicinal_uses": ["Improves insulin sensitivity and lowers fasting blood sugar", "Potent antifungal combating Candida albicans", "Improves peripheral blood circulation to cold hands/feet", "Antimicrobial against respiratory and gut infections", "Reduces menstrual cramping pain"],
        "active_compounds": ["Cinnamaldehyde", "Eugenol", "Cinnamyl acetate", "Proanthocyanidins", "Coumarin (Trace in True Ceylon)"],
        "preparation_methods": ["Cinnamon Bark Tea: Boil 1 stick in water for 10 minutes", "Ground Powder: 1/2 tsp over morning oatmeal or in warm water with honey", "Tincture: Alcohol extract for fungal infections"],
        "toxicity_level": "Very Low (True Ceylon) / Moderate (Cassia due to high coumarin)", "safety_info": "Always prefer True Ceylon Cinnamon (Cinnamomum verum) over cheap Cassia to avoid coumarin liver load.",
        "warnings": ["Cassia cinnamon contains high coumarin which can stress liver; use true Ceylon cinnamon", "May compound hypoglycemia if taking insulin"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Aggravates in excess", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Sandy, loamy soil with high organic matter", "sunlight": "Full sun to light shade", "water": "High rainfall", "climate": "Warm, humid tropical"}
    },
    {
        "id": 42, "common_name": "Licorice", "scientific_name": "Glycyrrhiza glabra",
        "tamil_name": "அதிமதுரம் (Athimadhuram)", "hindi_name": "मुलेठी", "family": "Fabaceae",
        "category": "Perennial Herb", "region": "Mediterranean, Central Asia, Northern India", "availability": "High", "rating": 4.9,
        "description": "Known as Yashtimadhu, its sweet root contains glycyrrhizin, providing profound demulcent, anti-ulcer, adrenal cortisol-sparing, and throat-soothing relief.",
        "medicinal_uses": ["Heals peptic and duodenal ulcers by stimulating mucous barrier", "Instant relief for sore throat, hoarseness, and laryngitis", "Supports depleted adrenals by sparing natural cortisol", "Soothes acid reflux and gastritis burning", "Expectorant clearing chest catarrh"],
        "active_compounds": ["Glycyrrhizin", "Glycyrrhetinic acid", "Glabridin", "Liquiritin", "Isoliquiritin"],
        "preparation_methods": ["Licorice Tea: Simmer 1 tsp crushed root in water for 10 minutes", "Root Suckle: Chew a small root stick for sore throat", "Churna: 2g powder with warm milk and ghee for ulcers"],
        "toxicity_level": "Moderate (Prolonged high doses)", "safety_info": "Safe for short-to-medium term use (4-6 weeks). High chronic doses can cause sodium retention and potassium loss.",
        "warnings": ["Contraindicated in high blood pressure (hypertension) and congestive heart failure", "Do not take with potassium-wasting diuretics (Furosemide)"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Balances (Best)", "kapha": "Aggravates in excess"},
        "cultivation": {"soil": "Deep, rich, sandy loam with adequate drainage", "sunlight": "Full sun", "water": "Moderate", "climate": "Subtropical to temperate"}
    },
    {
        "id": 43, "common_name": "Senna", "scientific_name": "Cassia angustifolia",
        "tamil_name": "நிலவாகை (Nilavagai)", "hindi_name": "सनाय", "family": "Fabaceae",
        "category": "Small Shrub", "region": "Southern India (Tirunelveli Senna), Arabia", "availability": "High", "rating": 4.5,
        "description": "A potent anthraquinone stimulant laxative whose sennosides irritate bowel motility to clear acute stubborn constipation and prep bowels for clinical imaging.",
        "medicinal_uses": ["Fast reliable relief for acute severe constipation", "Pre-operative bowel evacuation", "Clears downward metabolic stagnation (Apana Vata)", "Helps treat anal fissures by softening impacted stools"],
        "active_compounds": ["Sennoside A", "Sennoside B", "Sennoside C", "Chrysophanol", "Aloe-emodin"],
        "preparation_methods": ["Senna Infusion: Steep 1-2g leaves in cold water for 12 hours (cold extraction reduces griping cramps)", "Bedtime Tablet / Churna: 500mg with ginger and rock salt"],
        "toxicity_level": "Moderate (Habit-forming if abused)", "safety_info": "Short-term use only (maximum 7 consecutive days). Overuse causes electrolyte loss and bowel dependency.",
        "warnings": ["Contraindicated in intestinal obstruction, Crohn's, and ulcerative colitis", "Do not use during pregnancy or breastfeeding", "Never use chronically for weight loss"],
        "dosha": {"vata": "Aggravates if overused", "pitta": "Balances", "kapha": "Balances"},
        "cultivation": {"soil": "Dry, sandy, marginal wasteland soil", "sunlight": "Full hot sun", "water": "Low; drought-hardy", "climate": "Semi-arid tropical"}
    },
    {
        "id": 44, "common_name": "Gokshura", "scientific_name": "Tribulus terrestris",
        "tamil_name": "நெருஞ்சி (Nerunji)", "hindi_name": "गोखरू", "family": "Zygophyllaceae",
        "category": "Sprawling Herb", "region": "Arid & warm regions worldwide", "availability": "High", "rating": 4.8,
        "description": "A sharp-burred ground creeper celebrated as a master genitourinary tonic, dissolving kidney stones, optimizing testosterone receptors, and easing dysuria.",
        "medicinal_uses": ["Dissolves calcium oxalate kidney stones (Ashmari)", "Relieves burning urination, dysuria, and UTI flare-ups", "Enhances male testosterone bioavailability, sperm count, and vigor", "Tones prostate health and eases BPH urinary hesitation", "Cardioprotective and mild diuretic reducing edema"],
        "active_compounds": ["Protodioscin", "Tribulosin", "Dioscin", "Terrestrosides", "Harmine"],
        "preparation_methods": ["Gokshura Decoction: Boil 10g crushed burrs in water down to half", "Gokshuradi Guggulu: Classical tablet for urinary and joint health", "Fruit Powder: 3g with milk and honey twice daily"],
        "toxicity_level": "Very Low", "safety_info": "Safe, non-irritating restorative tonic for the urinary system.",
        "warnings": ["Monitor blood pressure if taking antihypertensive medications", "Avoid during pregnancy"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Balances (Best)", "kapha": "Balances"},
        "cultivation": {"soil": "Sandy, rocky, dry poor soil", "sunlight": "Intense direct sunlight", "water": "Very low", "climate": "Arid to warm temperate"}
    },
    {
        "id": 45, "common_name": "Kutki", "scientific_name": "Picrorhiza kurroa",
        "tamil_name": "கடுகுரோகிணி (Kadugurohini)", "hindi_name": "कुटकी", "family": "Plantaginaceae",
        "category": "Alpine Herb", "region": "Himalayan Alpine Slopes (9,000-15,000 ft)", "availability": "Medium", "rating": 4.9,
        "description": "An endangered high-altitude Himalayan bitter rhizome whose kutkin iridoid glycosides protect liver cells against viral hepatitis, clear bile stagnation, and break fevers.",
        "medicinal_uses": ["Superior liver protection in viral hepatitis, jaundice, and cirrhosis", "Lowers elevated liver enzymes (SGOT, SGPT, Bilirubin)", "Breaks chronic fever and clears deep visceral inflammation", "Stimulates healthy gallbladder bile flow and digestive fire", "Suppresses asthmatic allergic hypersensitivity"],
        "active_compounds": ["Picroside I", "Picroside II", "Kutkoside", "Apocynin", "Androsin"],
        "preparation_methods": ["Churna: 500mg-1g root powder mixed with honey or warm water", "Decoction: 3g simmered in water for deep hepatic detoxification", "Arogyavardhini Vati: Classical Ayurvedic liver formulation"],
        "toxicity_level": "Low", "safety_info": "Potent medicine. High doses act as a purgative.",
        "warnings": ["Avoid large doses in chronic diarrhea or severe dehydration", "Sourced responsibly from sustainable Himalayan cultivations"],
        "dosha": {"vata": "Aggravates in excess", "pitta": "Balances (Best)", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Rocky, glacial alpine scree with high organic humus", "sunlight": "High altitude UV sunlight", "water": "Cold snowmelt", "climate": "Sub-alpine to alpine Himalayas"}
    },
    {
        "id": 46, "common_name": "Vacha", "scientific_name": "Acorus calamus",
        "tamil_name": "வசம்பு (Vasambu)", "hindi_name": "वच", "family": "Acoraceae",
        "category": "Marsh Herb", "region": "Wetlands of Northern & Eastern India", "availability": "High", "rating": 4.7,
        "description": "Known as 'Sweet Flag', its aromatic rhizome sharpens vocal speech, clears brain fog, protects against childhood colic, and counters neurotoxins.",
        "medicinal_uses": ["Sharpens speech clarity, articulation, and vocal stammering", "Clears cerebral phlegm, sluggish memory, and brain fog", "Relieves acute infant colic and abdominal bloating (used as burned ash paste)", "Induces therapeutic vomiting (Vamana) in toxin ingestion", "Repels moths, lice, and household insects"],
        "active_compounds": ["Alpha-asarone", "Beta-asarone", "Calamene", "Acorenone", "Camphene"],
        "preparation_methods": ["Vasambu Bhasma: Burn dry root on flame, rub ash with mother's milk/honey for infant colic", "Micro-dose Powder: 100-250mg with honey for speech and memory", "External Paste: Applied over forehead for sinus headaches"],
        "toxicity_level": "Moderate (Internal at high doses)", "safety_info": "Safe in micro-doses. High chronic oral doses of beta-asarone may cause nausea. Indian calamus varieties must be used responsibly.",
        "warnings": ["Strictly avoid large oral doses; acts as a strong emetic (vomiting inducer)", "Avoid during pregnancy"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Aggravates in excess heat", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Marshy, waterlogged, rich organic silt", "sunlight": "Full sun to partial shade", "water": "High; requires wetland standing water", "climate": "Temperate to subtropical"}
    },
    {
        "id": 47, "common_name": "Pippali", "scientific_name": "Piper longum",
        "tamil_name": "திப்பிலி (Thippili)", "hindi_name": "पिप्पली", "family": "Piperaceae",
        "category": "Climbing Vine", "region": "Tropical rainforests of India", "availability": "High", "rating": 4.8,
        "description": "Indian Long Pepper is an extraordinary bio-enhancer (Yogavahi) and lung rejuvenator that activates macrophage phagocytosis, clears asthma, and ignites metabolism.",
        "medicinal_uses": ["Rejuvenates lung tissue in chronic asthma, bronchitis, and cough", "Enhances bioavailability of other herbs and nutrients", "Destroys cold, wet Kapha toxins in the gastrointestinal tract", "Aids in spleen and liver enlargement recovery", "Stimulates metabolic rate and burns visceral fat"],
        "active_compounds": ["Piperine", "Piplartine", "Piperlongumine", "Piperundecalidine", "Essential oils"],
        "preparation_methods": ["Pippali Rasayana: Take 1-2 crushed peppers boiled in milk with honey", "Trikatu Churna: Equal parts Pippali, Black Pepper, and Ginger for sluggish digestion", "Honey Paste: 500mg powder mixed with honey for acute wet cough"],
        "toxicity_level": "Low", "safety_info": "Safe when taken with milk or honey to moderate its heating intensity.",
        "warnings": ["Do not use continuously in high doses without a carrier like milk or ghee", "Caution with active gastric ulcers"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Aggravates in excess heat", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Rich, moist, loamy forest soil with leaf mold", "sunlight": "Partial dappled shade; requires support trees", "water": "High rainfall and humidity", "climate": "Warm humid tropical"}
    },
    {
        "id": 48, "common_name": "Ajwain", "scientific_name": "Trachyspermum ammi",
        "tamil_name": "ஓமம் (Omam)", "hindi_name": "अजवाइन", "family": "Apiaceae",
        "category": "Herb", "region": "India, Iran, Middle East", "availability": "Very High", "rating": 4.9,
        "description": "A seed-like fruit loaded with natural thymol that provides instantaneous relief for severe flatulence, spasmodic stomach cramps, infant colic, and sinus blockage.",
        "medicinal_uses": ["Instant relief for indigestion, gas, and acute bloating", "Relieves intestinal spasms and acute colic cramps", "Thymol vapors open clogged sinuses and asthmatic wheezing", "Kills gut parasites and bacterial food poisoning pathogens", "Relieves toothache when gargled with warm water"],
        "active_compounds": ["Thymol", "Para-cymene", "Gamma-terpinene", "Beta-pinene", "Carvacrol"],
        "preparation_methods": ["Omam Water (Ajwain Ark): Boil 1 tsp seeds in 2 cups water until reduced to half", "Dry Heat Potli: Roast seeds in pan, wrap in cloth, inhale vapors for cold", "Digestive Chew: 1/2 tsp roasted seeds with a pinch of black salt"],
        "toxicity_level": "Very Low", "safety_info": "Exceptionally safe, rapid-acting household herbal remedy.",
        "warnings": ["Very heating; avoid huge amounts in active bleeding ulcers or hyperacidity"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Aggravates in excess heat", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Sandy, loamy well-drained soil", "sunlight": "Full bright sun", "water": "Moderate watering", "climate": "Arid to semi-arid subtropical"}
    },
    {
        "id": 49, "common_name": "Betel Leaf", "scientific_name": "Piper betle",
        "tamil_name": "வெற்றிலை (Vettilai)", "hindi_name": "पान का पत्ता", "family": "Piperaceae",
        "category": "Climber", "region": "South and Southeast Asia", "availability": "Very High", "rating": 4.8,
        "description": "Glossy heart-shaped leaves chewed as Paan since antiquity. It stimulates salivary amylase, destroys bad breath bacteria, clears chest congestion, and heals cuts.",
        "medicinal_uses": ["Stimulates saliva and digestive enzymes immediately after meals", "Freshens breath and destroys oral pathogens causing gum decay", "Warmed leaves smeared with castor oil relieve pediatric chest phlegm", "Topical antiseptic for cuts, boils, and fungal infections", "Relieves headache when crushed leaf is applied to temples"],
        "active_compounds": ["Chavibetol", "Eugenol", "Chavicol", "Caryophyllene", "Hydroxychavicol"],
        "preparation_methods": ["Post-meal Chew: Chew 1 fresh leaf with a clove and cardamom (NO tobacco or slaked lime)", "Chest Compress: Coat leaf with warm mustard/castor oil, place on chest for cough", "Leaf Juice: 5ml fresh juice with honey for pediatric cough"],
        "toxicity_level": "Very Low (Leaf alone)", "safety_info": "The pure betel leaf is highly beneficial and non-carcinogenic. (The health risks of commercial Paan come from tobacco, areca nut, and slaked lime additives).",
        "warnings": ["Never combine with tobacco or excessive slaked lime (chuna)"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Balances in moderation", "kapha": "Balances (Best)"},
        "cultivation": {"soil": "Rich, sandy, well-draining loam with high organic compost", "sunlight": "Partial shade under protective thatch", "water": "High; regular moistening", "climate": "Warm humid tropical"}
    },
    {
        "id": 50, "common_name": "Castor Plant", "scientific_name": "Ricinus communis",
        "tamil_name": "ஆமணக்கு (Amanakku)", "hindi_name": "अरंडी", "family": "Euphorbiaceae",
        "category": "Shrub / Small Tree", "region": "Tropical Africa, India, Worldwide", "availability": "High", "rating": 4.8,
        "description": "Revered as Eranda in Ayurveda, castor is the premier Vata-destroying herb. Cold-pressed castor oil penetrates deeply to relieve arthritic pain, lubricate dry joints, and purge bowels.",
        "medicinal_uses": ["Superior transdermal anti-inflammatory for arthritis and swollen joints", "Deeply clears chronic constipation via ricinoleic acid activation", "Stimulates eyebrow, eyelash, and scalp hair follicle growth", "External castor oil packs dissolve ovarian cysts and hepatic stagnation", "Soothes dry irritated eyes when pharmaceutical-grade oil is used"],
        "active_compounds": ["Ricinoleic acid", "Oleic acid", "Linoleic acid", "Ricin (IN RAW SEEDS ONLY - OIL IS RICIN-FREE)"],
        "preparation_methods": ["Castor Oil Pack: Saturate wool flannel with cold-pressed oil, apply over abdomen with heating pad", "Night Purgative: 1-2 tsp food-grade cold-pressed oil in warm milk or ginger tea", "Scalp Massage: Mixed 50/50 with coconut oil for hair growth"],
        "toxicity_level": "Low (Cold-pressed Oil) / Deadly (RAW CRUSHED SEEDS)", "safety_info": "Cold-pressed pure castor oil is totally safe because toxic ricin remains in the seed pulp during oil extraction. NEVER ingest raw whole castor seeds.",
        "warnings": ["CRITICAL: Raw castor seeds contain ricin and are lethally toxic. Never chew seeds.", "Contraindicated internally during pregnancy (can trigger labor contractions)", "Do not use internally in appendicitis or intestinal obstruction"],
        "dosha": {"vata": "Balances (Best)", "pitta": "Neutral", "kapha": "Balances"},
        "cultivation": {"soil": "Adaptable to sandy, clay, or poor rocky soils", "sunlight": "Full direct sun", "water": "Low to moderate; highly drought-resilient", "climate": "Subtropical to tropical"}
    }
]

# Write plants_info.json
plants_info_path = os.path.join(DATA_DIR, "plants_info.json")
with open(plants_info_path, "w", encoding="utf-8") as f:
    json.dump({"plants": PLANTS_50}, f, indent=2, ensure_ascii=False)
print(f"Generated {len(PLANTS_50)} plants in {plants_info_path}")

# Write class_labels.json
class_names = [p["common_name"] for p in PLANTS_50]
class_labels_path = os.path.join(DATA_DIR, "class_labels.json")
with open(class_labels_path, "w", encoding="utf-8") as f:
    json.dump({
        "class_labels": class_names,
        "num_classes": len(class_names),
        "image_size": 224,
        "model_version": "2.0.0"
    }, f, indent=2, ensure_ascii=False)
print(f"Generated {len(class_names)} class labels in {class_labels_path}")

# Drug-Herb Interactions Data
DRUG_INTERACTIONS = [
    {
        "herb": "Tulsi",
        "drug": "Warfarin / Aspirin / Clopidogrel",
        "category": "Blood Thinners / Anticoagulants",
        "severity": "Moderate",
        "severity_color": "#fd7e14",
        "mechanism": "Tulsi contains eugenol, which exhibits natural anti-platelet and mild antithrombotic properties. Combining with pharmaceutical blood thinners may increase bleeding time or bruising.",
        "recommendation": "Monitor INR / clotting time closely. Avoid high therapeutic doses of Tulsi extracts 2 weeks prior to surgical procedures."
    },
    {
        "herb": "Tulsi",
        "drug": "Metformin / Glimepiride / Insulin",
        "category": "Antidiabetic Medications",
        "severity": "Moderate",
        "severity_color": "#fd7e14",
        "mechanism": "Tulsi stimulates pancreatic beta-cell insulin secretion. Taking it alongside prescription hypoglycemics may lead to synergistic blood sugar drops.",
        "recommendation": "Monitor capillary blood glucose frequently. Adjust prescription medication under physician supervision if hypoglycemia symptoms occur."
    },
    {
        "herb": "Neem",
        "drug": "Metformin / Glipizide",
        "category": "Antidiabetic Medications",
        "severity": "High",
        "severity_color": "#dc3545",
        "mechanism": "Neem extracts exhibit potent insulin-mimetic and glucose-lowering activity. Simultaneous intake with antidiabetics can cause severe hypoglycemia.",
        "recommendation": "Strict blood glucose monitoring required. Dose reduction of pharmaceuticals may be needed under medical supervision."
    },
    {
        "herb": "Neem",
        "drug": "Cyclosporine / Tacrolimus",
        "category": "Immunosuppressive Drugs",
        "severity": "High",
        "severity_color": "#dc3545",
        "mechanism": "Neem possesses robust immunostimulatory properties that stimulate T-cell activity, potentially counteracting the therapeutic goal of organ-transplant immunosuppressants.",
        "recommendation": "Strictly contraindicated for post-transplant patients taking immunosuppressants."
    },
    {
        "herb": "Aloe Vera (Oral Latex)",
        "drug": "Digoxin",
        "category": "Cardiac Glycosides",
        "severity": "Critical",
        "severity_color": "#721c24",
        "mechanism": "Aloin in Aloe latex acts as a strong laxative that depletes serum potassium (hypokalemia). Hypokalemia dramatically magnifies digoxin cardiac toxicity, risking severe arrhythmias.",
        "recommendation": "Avoid internal aloe latex when on digoxin. Pure de-aloinized inner gel is acceptable in moderation."
    },
    {
        "herb": "Ginger",
        "drug": "Warfarin / Heparin / NSAIDs",
        "category": "Anticoagulants & Antiplatelets",
        "severity": "Moderate",
        "severity_color": "#fd7e14",
        "mechanism": "Gingerols inhibit thromboxane synthetase and platelet aggregation, compounding the anticoagulant activity of prescription blood thinners.",
        "recommendation": "Dietary culinary quantities are safe. High supplemental doses (>4g dry extract) should be avoided without physician approval."
    },
    {
        "herb": "Turmeric / Curcumin",
        "drug": "Aspirin / Warfarin",
        "category": "Blood Thinners",
        "severity": "Moderate",
        "severity_color": "#fd7e14",
        "mechanism": "Curcumin demonstrates anti-platelet and fibrinolytic properties that can enhance bleeding risk when paired with prescription anti-thrombotics.",
        "recommendation": "Culinary amounts in food are safe. High-dose liposomal curcumin supplements should be discontinued before elective surgeries."
    },
    {
        "herb": "Turmeric / Curcumin",
        "drug": "Omeprazole / Pantoprazole / Ranitidine",
        "category": "Antacids & Proton Pump Inhibitors (PPIs)",
        "severity": "Low",
        "severity_color": "#ffc107",
        "mechanism": "Turmeric stimulates gastric acid production (cholagogue/stomachic effect), which may partially counteract the acid-suppressing action of PPIs.",
        "recommendation": "Take turmeric at least 2 hours apart from acid-suppressing pharmaceuticals."
    },
    {
        "herb": "Ashwagandha",
        "drug": "Zolpidem / Alprazolam / Diazepam",
        "category": "Sedatives & Benzodiazepines",
        "severity": "High",
        "severity_color": "#dc3545",
        "mechanism": "Ashwagandha withanolides modulate GABA-A receptors, leading to additive central nervous system depression, extreme drowsiness, and slowed motor reflexes.",
        "recommendation": "Do not combine with sedative hypnotics or alcohol. Exercise caution when driving."
    },
    {
        "herb": "Ashwagandha",
        "drug": "Levothyroxine / Synthroid",
        "category": "Thyroid Hormone Replacements",
        "severity": "Moderate",
        "severity_color": "#fd7e14",
        "mechanism": "Ashwagandha stimulates endogenous T3 and T4 synthesis. In patients taking exogenous thyroid hormone, this can result in thyrotoxicosis symptoms.",
        "recommendation": "Monitor thyroid panel (TSH, free T3/T4) every 6-8 weeks if using Ashwagandha."
    },
    {
        "herb": "Licorice (Mulethi)",
        "drug": "Amlodipine / Losartan / Telmisartan",
        "category": "Antihypertensive Medications",
        "severity": "Critical",
        "severity_color": "#721c24",
        "mechanism": "Glycyrrhizin inhibits 11-beta-HSD2, preventing cortisol breakdown and causing pseudoaldosteronism (sodium/water retention and potassium excretion), elevating BP.",
        "recommendation": "Strictly avoid regular licorice root consumption if diagnosed with hypertension or taking BP medications."
    },
    {
        "herb": "Licorice (Mulethi)",
        "drug": "Furosemide / Hydrochlorothiazide",
        "category": "Diuretics",
        "severity": "Critical",
        "severity_color": "#721c24",
        "mechanism": "Both licorice and loop/thiazide diuretics induce renal potassium wasting. Combined intake can cause dangerous severe hypokalemia, muscle paralysis, and arrhythmias.",
        "recommendation": "Strictly contraindicated. Use DGL (Deglycyrrhizinated Licorice) instead for ulcer healing."
    },
    {
        "herb": "Senna",
        "drug": "Furosemide (Lasix)",
        "category": "Loop Diuretics",
        "severity": "High",
        "severity_color": "#dc3545",
        "mechanism": "Additive potassium excretion via both intestinal purging and renal diuresis, predisposing to hypokalemia.",
        "recommendation": "Do not use stimulant laxatives concurrently with potassium-wasting diuretics."
    },
    {
        "herb": "Guggul",
        "drug": "Atorvastatin / Rosuvastatin",
        "category": "HMG-CoA Reductase Inhibitors (Statins)",
        "severity": "Moderate",
        "severity_color": "#fd7e14",
        "mechanism": "Guggul induces CYP3A4 enzymes and hepatic bile acid receptors, potentially modifying circulating statin bioavailability.",
        "recommendation": "Monitor lipid profile and liver enzymes. Separate administration times by 3-4 hours."
    },
    {
        "herb": "Kalmegh (Nilavembu)",
        "drug": "Paracetamol / Acetaminophen",
        "category": "Antipyretics / Analgesics",
        "severity": "Low (Beneficial)",
        "severity_color": "#28a745",
        "mechanism": "Andrographolide demonstrates hepatoprotective properties that may mitigate paracetamol-induced oxidative liver stress during acute viral fever therapy.",
        "recommendation": "Generally safe. Maintain standard clinical dosages of both."
    },
    {
        "herb": "Castor Oil",
        "drug": "Oral Contraceptives / Antibiotics",
        "category": "Oral Medications",
        "severity": "Moderate",
        "severity_color": "#fd7e14",
        "mechanism": "Castor oil triggers intense peristaltic purging, drastically shortening intestinal transit time and causing incomplete absorption of co-administered oral tablets.",
        "recommendation": "Take prescription medications at least 4 hours before or after taking castor oil."
    }
]

drug_interactions_path = os.path.join(DATA_DIR, "drug_interactions.json")
with open(drug_interactions_path, "w", encoding="utf-8") as f:
    json.dump({"interactions": DRUG_INTERACTIONS}, f, indent=2, ensure_ascii=False)
print(f"Generated {len(DRUG_INTERACTIONS)} drug-herb interaction rules in {drug_interactions_path}")

print("All data artifacts successfully built!")
