"""
MediPlant AI - Dataset Setup Helper
Run this script to create the correct dataset folder structure
and optionally download a sample dataset for testing.

Usage: python setup_dataset.py
"""

import os
import shutil
import urllib.request
from pathlib import Path

PLANT_CLASSES = [
    "Tulsi", "Neem", "Aloe_Vera", "Ginger", "Turmeric",
    "Ashwagandha", "Brahmi", "Amla", "Giloy", "Moringa",
    "Curry_Leaf", "Mint", "Lemongrass", "Hibiscus", "Fenugreek",
    "Coriander", "Guduchi", "Shatavari", "Bael", "Moringa"
]


def create_dataset_structure():
    """Create the dataset folder structure."""
    print("📂 Creating dataset folder structure...")

    for split in ["train", "test"]:
        for plant in PLANT_CLASSES:
            path = Path(f"data/dataset/{split}/{plant}")
            path.mkdir(parents=True, exist_ok=True)

    print("✅ Dataset folders created!")
    print("\n📋 NEXT STEPS:")
    print("─" * 50)
    print("1. Download dataset from Kaggle:")
    print("   https://www.kaggle.com/datasets/warcoder/indian-medicinal-leaves-image-datasets")
    print()
    print("2. Extract the downloaded zip file")
    print()
    print("3. Copy your plant images to:")
    print("   data/dataset/train/PlantName/  (80% of images)")
    print("   data/dataset/test/PlantName/   (20% of images)")
    print()
    print("4. Run training:")
    print("   python model/train_model.py")
    print()
    print("5. Run the app:")
    print("   streamlit run app.py")
    print("─" * 50)


def create_sample_images():
    """Create placeholder images for quick testing (solid color images)."""
    try:
        from PIL import Image
        import random

        print("\n🖼️  Creating sample test images (for demo only)...")

        colors = [
            (34,139,34), (0,128,0), (50,205,50),
            (144,238,144), (0,100,0), (46,139,87),
            (60,179,113), (0,255,127), (0,250,154),
            (85,107,47)
        ]

        for split in ["train", "test"]:
            count = 60 if split == "train" else 15
            for idx, plant in enumerate(PLANT_CLASSES[:10]):
                folder = Path(f"data/dataset/{split}/{plant}")
                folder.mkdir(parents=True, exist_ok=True)
                for i in range(count):
                    # Create varied green leaf-like images
                    img = Image.new("RGB", (224, 224), colors[idx % len(colors)])
                    # Add variation
                    pixels = img.load()
                    for x in range(0, 224, 10):
                        for y in range(0, 224, 10):
                            r = random.randint(-20, 20)
                            base = colors[idx % len(colors)]
                            new_c = tuple(max(0, min(255, c + r)) for c in base)
                            for dx in range(min(10, 224-x)):
                                for dy in range(min(10, 224-y)):
                                    pixels[x+dx, y+dy] = new_c
                    img.save(folder / f"{plant}_{i+1:03d}.jpg")

        print(f"✅ Sample images created for {len(PLANT_CLASSES[:10])} plants")
        print("⚠️  These are placeholder images — use real plant images for actual training!")

    except ImportError:
        print("Install Pillow: pip install Pillow")


def check_dataset():
    """Check dataset structure and image counts."""
    print("\n📊 Checking dataset...")
    dataset_path = Path("data/dataset")

    if not dataset_path.exists():
        print("❌ Dataset folder not found. Run setup first.")
        return

    total_train = 0
    total_test  = 0

    print(f"\n{'Plant':<20} {'Train':>10} {'Test':>10} {'Status':>12}")
    print("─" * 55)

    for split_name, split_total in [("train", None), ("test", None)]:
        pass

    all_plants = set()
    for split in ["train", "test"]:
        split_path = dataset_path / split
        if split_path.exists():
            for plant_dir in sorted(split_path.iterdir()):
                if plant_dir.is_dir():
                    all_plants.add(plant_dir.name)

    for plant in sorted(all_plants):
        train_count = len(list((dataset_path / "train" / plant).glob("*.jpg"))) + \
                      len(list((dataset_path / "train" / plant).glob("*.png")))
        test_count  = len(list((dataset_path / "test"  / plant).glob("*.jpg"))) + \
                      len(list((dataset_path / "test"  / plant).glob("*.png")))
        status      = "✅ Good" if train_count >= 50 else ("⚠️ Low" if train_count > 0 else "❌ Empty")
        print(f"{plant:<20} {train_count:>10} {test_count:>10} {status:>12}")
        total_train += train_count
        total_test  += test_count

    print("─" * 55)
    print(f"{'TOTAL':<20} {total_train:>10} {total_test:>10}")
    print(f"\n✅ {len(all_plants)} plant classes found")
    print(f"✅ Total images: {total_train + total_test}")

    if total_train == 0:
        print("\n⚠️  No training images found!")
        print("   Download a dataset or run: python setup_dataset.py --sample")


if __name__ == "__main__":
    import sys

    create_dataset_structure()

    if "--sample" in sys.argv:
        create_sample_images()

    if "--check" in sys.argv:
        check_dataset()
    else:
        check_dataset()
