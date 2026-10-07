"""
MediPlant AI - Dataset Generator
Creates a realistic synthetic leaf image dataset for training.
Each plant gets 50 training + 15 test images with varied visual properties.
"""
import warnings, os
warnings.filterwarnings("ignore")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import json, random, math

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data", "dataset")

# Plant visual properties: (h_center, h_std, sat_mean, val_mean, edge_freq, aspect_range, yellow_comp, gray_green)
PLANT_VISUAL = {
    "Tulsi":       (0.30, 0.02, 0.55, 0.42, 6,  (0.9,1.2),  0.05, 0.00),
    "Neem":        (0.28, 0.02, 0.58, 0.35, 12, (1.5,2.2),  0.03, 0.00),
    "Aloe Vera":   (0.32, 0.01, 0.38, 0.58, 1,  (2.5,4.0),  0.06, 0.05),
    "Ginger":      (0.29, 0.02, 0.50, 0.46, 4,  (1.4,1.8),  0.10, 0.00),
    "Turmeric":    (0.15, 0.03, 0.70, 0.52, 3,  (1.2,1.6),  0.30, 0.00),
    "Ashwagandha": (0.30, 0.03, 0.32, 0.44, 5,  (1.0,1.3),  0.05, 0.25),
    "Brahmi":      (0.33, 0.02, 0.42, 0.60, 3,  (0.6,0.9),  0.04, 0.00),
    "Amla":        (0.28, 0.02, 0.59, 0.36, 14, (0.8,1.1),  0.03, 0.00),
    "Giloy":       (0.31, 0.02, 0.46, 0.50, 4,  (0.8,0.9),  0.04, 0.00),
    "Moringa":     (0.33, 0.02, 0.38, 0.58, 3,  (0.8,1.0),  0.05, 0.00),
    "Curry Leaf":  (0.27, 0.02, 0.60, 0.36, 7,  (1.3,1.7),  0.04, 0.00),
    "Mint":        (0.34, 0.02, 0.35, 0.65, 5,  (0.8,1.0),  0.03, 0.00),
    "Lemongrass":  (0.23, 0.02, 0.62, 0.58, 1,  (3.5,5.0),  0.22, 0.00),
    "Hibiscus":    (0.30, 0.03, 0.62, 0.40, 10, (0.7,1.0),  0.05, 0.00),
    "Fenugreek":   (0.32, 0.02, 0.36, 0.56, 4,  (0.6,0.8),  0.07, 0.00),
    "Coriander":   (0.33, 0.02, 0.40, 0.58, 12, (0.6,0.8),  0.04, 0.00),
    "Guduchi":     (0.31, 0.02, 0.44, 0.48, 4,  (0.8,1.0),  0.04, 0.00),
    "Shatavari":   (0.32, 0.02, 0.28, 0.52, 1,  (2.8,4.0),  0.05, 0.20),
    "Triphala":    (0.29, 0.02, 0.50, 0.42, 8,  (0.9,1.1),  0.06, 0.00),
    "Arjuna":      (0.29, 0.02, 0.54, 0.40, 7,  (1.4,1.8),  0.04, 0.00),
    "Guggul":      (0.28, 0.03, 0.55, 0.38, 6,  (0.7,1.0),  0.05, 0.00),
    "Shilajit":    (0.27, 0.03, 0.58, 0.34, 5,  (0.7,0.9),  0.04, 0.00),
    "Kalmegh":     (0.28, 0.02, 0.48, 0.38, 6,  (1.0,1.3),  0.04, 0.00),
    "Bael":        (0.29, 0.02, 0.50, 0.42, 5,  (0.7,0.9),  0.06, 0.00),
    "Noni":        (0.31, 0.02, 0.48, 0.48, 4,  (0.7,0.9),  0.05, 0.00),
    "Papaya Leaf": (0.30, 0.02, 0.50, 0.48, 15, (0.5,0.7),  0.08, 0.00),
    "Drumstick":   (0.33, 0.02, 0.40, 0.54, 3,  (0.8,1.0),  0.05, 0.00),
    "Rose":        (0.29, 0.02, 0.58, 0.40, 9,  (0.8,1.1),  0.04, 0.00),
    "Jasmine":     (0.31, 0.02, 0.46, 0.46, 4,  (0.8,1.0),  0.05, 0.00),
    "Sandalwood":  (0.29, 0.02, 0.54, 0.40, 5,  (1.2,1.6),  0.04, 0.00),
}

DISEASE_TYPES = [
    "healthy",
    "yellow_spots",    # nutrient deficiency
    "brown_edges",     # drought stress / leaf burn
    "dark_patches",    # fungal infection
    "white_powder",    # powdery mildew
    "rust_spots",      # rust disease
    "wilting",         # root rot / water stress
    "mosaic_pattern",  # viral infection
]

def hsv_to_rgb(h, s, v):
    if s == 0: return v, v, v
    i = int(h * 6) % 6
    f = h * 6 - int(h * 6)
    p, q, t = v*(1-s), v*(1-s*f), v*(1-s*(1-f))
    return [(v,t,p),(q,v,p),(p,v,t),(p,q,v),(t,p,v),(v,p,q)][i]

def make_leaf_image(plant_name, disease="healthy", img_size=224, seed=None):
    if seed is not None:
        random.seed(seed); np.random.seed(seed % (2**31))

    props = PLANT_VISUAL.get(plant_name, PLANT_VISUAL["Tulsi"])
    h_c, h_s, sat_m, val_m, edge_f, asp_r, yc, gg = props

    # Randomize within range
    asp = random.uniform(*asp_r)
    h   = np.clip(h_c + random.gauss(0, h_s), 0.08, 0.45)
    sat = np.clip(sat_m + random.gauss(0, 0.05), 0.15, 0.90)
    val = np.clip(val_m + random.gauss(0, 0.05), 0.20, 0.88)

    # Ashwagandha/Shatavari: desaturate toward gray-green
    if gg > 0.15:
        sat = np.clip(sat * 0.55, 0.12, 0.38)
        h   = 0.30 + random.gauss(0, 0.02)

    # Turmeric: shift toward yellow
    if yc > 0.20:
        h   = np.clip(h + random.gauss(0.02, 0.02), 0.10, 0.22)
        sat = np.clip(sat + 0.10, 0.55, 0.85)

    # Canvas
    W = img_size
    H = img_size
    canvas = np.ones((H, W, 3), dtype=np.float32) * 0.96  # near-white background

    # Leaf shape: ellipse with random rotation
    cx, cy = W//2, H//2
    leaf_w = int(W * 0.35 / max(asp**0.3, 0.5))
    leaf_h = int(H * 0.35 * min(asp**0.5, 2.2))
    angle  = random.uniform(-15, 15)
    cos_a, sin_a = math.cos(math.radians(angle)), math.sin(math.radians(angle))

    # Fill leaf
    for i in range(H):
        for j in range(W):
            dx, dy = j - cx, i - cy
            rx = dx*cos_a + dy*sin_a
            ry = -dx*sin_a + dy*cos_a
            if (rx/leaf_w)**2 + (ry/leaf_h)**2 <= 1.0:
                noise_h   = h + np.random.randn()*0.015
                noise_s   = np.clip(sat + np.random.randn()*0.04, 0.10, 0.95)
                noise_v   = np.clip(val + np.random.randn()*0.04, 0.15, 0.95)
                r, g, b   = hsv_to_rgb(noise_h % 1.0, noise_s, noise_v)
                canvas[i, j] = [r, g, b]

    # Mid-vein
    for i in range(max(0,cy-leaf_h), min(H,cy+leaf_h)):
        dy  = i - cy
        xv  = int(cx + dy * math.tan(math.radians(angle)) * 0.3)
        for jj in range(max(0,xv-1), min(W,xv+2)):
            if (jj-cx)**2/leaf_w**2 + (i-cy)**2/leaf_h**2 <= 0.85:
                canvas[i, jj] = [max(0,canvas[i,jj,0]-0.08),
                                   max(0,canvas[i,jj,1]-0.05),
                                   max(0,canvas[i,jj,2]-0.08)]

    # Edge serrations
    if edge_f > 3:
        for _ in range(edge_f * 3):
            angle2 = random.uniform(0, 2*math.pi)
            sr     = random.uniform(0.88, 1.02)
            sx     = int(cx + leaf_w*sr*math.cos(angle2))
            sy     = int(cy + leaf_h*sr*math.sin(angle2))
            for ii in range(max(0,sy-3),min(H,sy+3)):
                for jj in range(max(0,sx-3),min(W,sx+3)):
                    canvas[ii,jj] = [0.96, 0.96, 0.96]

    # ── Apply disease effects ──────────────────────────────────────────────
    if disease == "yellow_spots":
        for _ in range(random.randint(5, 15)):
            yi, xi = random.randint(cy-leaf_h//2, cy+leaf_h//2), random.randint(cx-leaf_w//2, cx+leaf_w//2)
            r_spot = random.randint(5, 18)
            for ii in range(max(0,yi-r_spot), min(H,yi+r_spot)):
                for jj in range(max(0,xi-r_spot), min(W,xi+r_spot)):
                    if (ii-yi)**2+(jj-xi)**2 < r_spot**2 and canvas[ii,jj,1]>0.35:
                        canvas[ii,jj] = [np.clip(canvas[ii,jj,0]+0.25,0,1),
                                          np.clip(canvas[ii,jj,1]+0.15,0,1),
                                          np.clip(canvas[ii,jj,2]-0.10,0,1)]

    elif disease == "brown_edges":
        for i in range(H):
            for j in range(W):
                dx,dy = j-cx, i-cy
                dist = math.sqrt((dx/leaf_w)**2 + (dy/leaf_h)**2)
                if 0.75 < dist < 1.02:
                    canvas[i,j] = [np.clip(0.55+random.gauss(0,0.05),0.3,0.75),
                                    np.clip(0.32+random.gauss(0,0.04),0.15,0.50),
                                    np.clip(0.12+random.gauss(0,0.03),0.05,0.25)]

    elif disease == "dark_patches":
        for _ in range(random.randint(3, 8)):
            yi = random.randint(cy-leaf_h//2, cy+leaf_h//2)
            xi = random.randint(cx-leaf_w//2, cx+leaf_w//2)
            r_p = random.randint(8, 22)
            for ii in range(max(0,yi-r_p), min(H,yi+r_p)):
                for jj in range(max(0,xi-r_p), min(W,xi+r_p)):
                    if (ii-yi)**2+(jj-xi)**2 < r_p**2 and canvas[ii,jj,1]>0.30:
                        f = random.uniform(0.40, 0.65)
                        canvas[ii,jj] = [canvas[ii,jj,0]*f, canvas[ii,jj,1]*f, canvas[ii,jj,2]*f]

    elif disease == "white_powder":
        for _ in range(random.randint(200, 600)):
            yi = random.randint(cy-leaf_h, cy+leaf_h)
            xi = random.randint(cx-leaf_w, cx+leaf_w)
            if 0 <= yi < H and 0 <= xi < W and canvas[yi,xi,1] > 0.30:
                r_p = random.randint(2, 6)
                for ii in range(max(0,yi-r_p), min(H,yi+r_p)):
                    for jj in range(max(0,xi-r_p), min(W,xi+r_p)):
                        if (ii-yi)**2+(jj-xi)**2 < r_p**2:
                            alpha = random.uniform(0.3, 0.7)
                            canvas[ii,jj] = [min(1,canvas[ii,jj,0]*alpha+0.95*(1-alpha))]*3

    elif disease == "rust_spots":
        for _ in range(random.randint(8, 20)):
            yi = random.randint(cy-leaf_h//2, cy+leaf_h//2)
            xi = random.randint(cx-leaf_w//2, cx+leaf_w//2)
            r_s = random.randint(4, 12)
            for ii in range(max(0,yi-r_s), min(H,yi+r_s)):
                for jj in range(max(0,xi-r_s), min(W,xi+r_s)):
                    if (ii-yi)**2+(jj-xi)**2 < r_s**2 and canvas[ii,jj,1]>0.30:
                        canvas[ii,jj] = [np.clip(0.72+random.gauss(0,0.05),0,1),
                                          np.clip(0.38+random.gauss(0,0.04),0,1),
                                          np.clip(0.08+random.gauss(0,0.02),0,1)]

    elif disease == "mosaic_pattern":
        block = 12
        for bi in range(cy-leaf_h, cy+leaf_h, block):
            for bj in range(cx-leaf_w, cx+leaf_w, block):
                if random.random() < 0.35:
                    yi_start = max(0, bi); yi_end = min(H, bi+block)
                    xi_start = max(0, bj); xi_end = min(W, bj+block)
                    for ii in range(yi_start, yi_end):
                        for jj in range(xi_start, xi_end):
                            if canvas[ii,jj,1] > 0.30:
                                canvas[ii,jj,1] = np.clip(canvas[ii,jj,1]*0.60+0.15, 0, 1)
                                canvas[ii,jj,0] = np.clip(canvas[ii,jj,0]+0.12, 0, 1)

    elif disease == "wilting":
        # Darker, slightly brown overall
        for i in range(H):
            for j in range(W):
                if canvas[i,j,1] > 0.35:
                    canvas[i,j] = [np.clip(canvas[i,j,0]+0.05,0,1),
                                    np.clip(canvas[i,j,1]*0.82,0,1),
                                    np.clip(canvas[i,j,2]*0.78,0,1)]

    # Slight gaussian blur for realism
    canvas = np.clip(canvas, 0, 1)
    img    = Image.fromarray((canvas * 255).astype(np.uint8))
    img    = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    # Random brightness variation
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(random.uniform(0.85, 1.15))
    return img

def create_dataset(train_per_class=50, test_per_class=15):
    plants = list(PLANT_VISUAL.keys())
    total  = len(plants) * (train_per_class + test_per_class)
    done   = 0

    print(f"\n  Creating dataset: {len(plants)} plants × {train_per_class+test_per_class} images")
    print(f"  Total: {total} images")
    print(f"  Location: {DATA_DIR}")
    print()

    # Also create disease dataset folders
    disease_train = os.path.join(DATA_DIR, "disease_train")
    disease_test  = os.path.join(DATA_DIR, "disease_test")

    for split, n_imgs in [("train", train_per_class), ("test", test_per_class)]:
        for plant in plants:
            folder = os.path.join(DATA_DIR, split, plant.replace(" ", "_"))
            os.makedirs(folder, exist_ok=True)
            for idx in range(n_imgs):
                # Mix healthy and diseased
                disease = "healthy" if idx < n_imgs * 0.65 else \
                          random.choice(["yellow_spots","brown_edges","dark_patches",
                                         "white_powder","rust_spots","wilting","mosaic_pattern"])
                img = make_leaf_image(plant, disease=disease, seed=hash(f"{plant}{split}{idx}") % 99999)
                fname = f"{plant.replace(' ','_')}_{split}_{idx:03d}.jpg"
                img.save(os.path.join(folder, fname), "JPEG", quality=92)
                done += 1
            print(f"  ✅  {split:5s} | {plant:15s} | {n_imgs} images")

    # Create disease-specific dataset
    print("\n  Creating disease detection dataset...")
    for split, n_imgs in [("disease_train", 30), ("disease_test", 10)]:
        for disease in DISEASE_TYPES:
            folder = os.path.join(DATA_DIR, split, disease)
            os.makedirs(folder, exist_ok=True)
            for idx in range(n_imgs):
                plant = random.choice(plants[:10])  # use first 10 plants
                img   = make_leaf_image(plant, disease=disease, seed=hash(f"dis{disease}{split}{idx}")%99999)
                fname = f"{disease}_{idx:03d}.jpg"
                img.save(os.path.join(folder, fname), "JPEG", quality=92)
        print(f"  ✅  {split} | {disease}")

    # Save metadata
    meta = {
        "plants": plants,
        "num_classes": len(plants),
        "diseases": DISEASE_TYPES,
        "num_diseases": len(DISEASE_TYPES),
        "train_per_class": train_per_class,
        "test_per_class": test_per_class,
        "image_size": 224,
        "created_by": "MediPlant AI Dataset Generator"
    }
    with open(os.path.join(DATA_DIR, "dataset_info.json"), "w") as f:
        json.dump(meta, f, indent=2)

    print(f"\n  ✅ Dataset created successfully!")
    print(f"  📁 {DATA_DIR}")
    print(f"  🌿 {len(plants)} plant species")
    print(f"  🦠 {len(DISEASE_TYPES)} disease types")
    print(f"  📷 {done} total images")

if __name__ == "__main__":
    create_dataset(train_per_class=50, test_per_class=15)
