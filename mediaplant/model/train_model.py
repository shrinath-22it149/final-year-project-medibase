"""
MediPlant AI - Model Training Script
Ensemble: VGG16 + ResNet50 + InceptionV3
Compatible with TensorFlow 2.18+, Python 3.10-3.13

HOW TO RUN:
  1. Put dataset in data/dataset/train/<PlantName>/ and data/dataset/test/<PlantName>/
  2. cd mediaplant
  3. python model/train_model.py
"""

import os, sys, json, pickle
import numpy as np

# Suppress TF logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf
from tensorflow.keras.applications import VGG16, ResNet50, InceptionV3
from tensorflow.keras.layers import (Dense, GlobalAveragePooling2D,
    Dropout, Concatenate, Input, BatchNormalization, Reshape)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (EarlyStopping, ModelCheckpoint,
    ReduceLROnPlateau)
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

print(f"TensorFlow version: {tf.__version__}")
print(f"Python version: {sys.version}")

# ── CONFIG ─────────────────────────────────────────────────────────────────────
CFG = {
    "dataset_path"   : "data/dataset",
    "model_save_path": "model/saved_model",
    "image_size"     : 224,
    "batch_size"     : 32,
    "epochs"         : 50,
    "learning_rate"  : 0.0001,
    "dropout_rate"   : 0.5,
    "dense_units"    : 512,
}
os.makedirs(CFG["model_save_path"], exist_ok=True)
os.makedirs("model/plots",          exist_ok=True)

# ── DATA GENERATORS ────────────────────────────────────────────────────────────
def create_data_generators():
    print("\n📂 Loading dataset...")
    IMG = CFG["image_size"]

    train_gen_obj = ImageDataGenerator(
        rescale           = 1.0/255,
        rotation_range    = 40,
        width_shift_range = 0.2,
        height_shift_range= 0.2,
        shear_range       = 0.2,
        zoom_range        = 0.2,
        horizontal_flip   = True,
        vertical_flip     = True,
        brightness_range  = [0.8, 1.2],
        fill_mode         = "nearest",
        validation_split  = 0.2
    )
    test_gen_obj = ImageDataGenerator(rescale=1.0/255)

    train_gen = train_gen_obj.flow_from_directory(
        os.path.join(CFG["dataset_path"], "train"),
        target_size = (IMG, IMG), batch_size = CFG["batch_size"],
        class_mode  = "categorical", subset = "training", shuffle = True)

    val_gen = train_gen_obj.flow_from_directory(
        os.path.join(CFG["dataset_path"], "train"),
        target_size = (IMG, IMG), batch_size = CFG["batch_size"],
        class_mode  = "categorical", subset = "validation", shuffle = False)

    test_gen = test_gen_obj.flow_from_directory(
        os.path.join(CFG["dataset_path"], "test"),
        target_size = (IMG, IMG), batch_size = CFG["batch_size"],
        class_mode  = "categorical", shuffle = False)

    num_classes  = len(train_gen.class_indices)
    class_labels = list(train_gen.class_indices.keys())

    with open("data/class_labels.json", "w") as f:
        json.dump({"class_labels": class_labels, "num_classes": num_classes,
                   "image_size": IMG, "model_version": "1.0.0"}, f, indent=2)

    print(f"✅ Classes    : {num_classes}")
    print(f"✅ Train      : {train_gen.samples} images")
    print(f"✅ Validation : {val_gen.samples} images")
    print(f"✅ Test       : {test_gen.samples} images")
    return train_gen, val_gen, test_gen, num_classes, class_labels

# ── ENSEMBLE MODEL ─────────────────────────────────────────────────────────────
def build_ensemble(num_classes):
    print("\n🏗️  Building Ensemble Model...")
    IMG = (CFG["image_size"], CFG["image_size"], 3)

    def branch(base_fn, name, freeze_until):
        inp  = Input(shape=IMG, name=f"{name}_input")
        base = base_fn(weights="imagenet", include_top=False, input_tensor=inp)
        for layer in base.layers[:-freeze_until]:
            layer.trainable = False
        x = GlobalAveragePooling2D(name=f"{name}_gap")(base.output)
        x = Dense(256, activation="relu", name=f"{name}_dense")(x)
        x = BatchNormalization(name=f"{name}_bn")(x)
        x = Dropout(0.3, name=f"{name}_drop")(x)
        return inp, x

    vgg_in, vgg_out = branch(VGG16,       "vgg",  4)
    res_in, res_out = branch(ResNet50,    "res",  10)
    inc_in, inc_out = branch(InceptionV3, "inc",  15)

    merged = Concatenate(name="merge")([vgg_out, res_out, inc_out])
    x      = Dense(CFG["dense_units"], activation="relu", name="fc1")(merged)
    x      = BatchNormalization(name="fc1_bn")(x)
    x      = Dropout(CFG["dropout_rate"], name="fc1_drop")(x)
    x      = Dense(256, activation="relu", name="fc2")(x)
    x      = Dropout(0.3, name="fc2_drop")(x)
    out    = Dense(num_classes, activation="softmax", name="output")(x)

    model = Model(inputs=[vgg_in, res_in, inc_in], outputs=out, name="MediPlant_Ensemble")
    model.compile(optimizer=Adam(CFG["learning_rate"]),
                  loss="categorical_crossentropy", metrics=["accuracy"])
    print(f"✅ Ensemble model — {model.count_params():,} parameters")
    return model

# ── HYBRID CNN-LSTM MODEL ──────────────────────────────────────────────────────
def build_hybrid(num_classes):
    print("\n🏗️  Building Hybrid CNN-LSTM Model...")
    from tensorflow.keras.layers import LSTM
    IMG = (CFG["image_size"], CFG["image_size"], 3)

    inp  = Input(shape=IMG)
    base = VGG16(weights="imagenet", include_top=False, input_tensor=inp)
    for layer in base.layers[:-4]:
        layer.trainable = False
    x = GlobalAveragePooling2D()(base.output)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.4)(x)
    x = Reshape((1, 256))(x)
    x = LSTM(128, return_sequences=True)(x)
    x = LSTM(64)(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.5)(x)
    out = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=inp, outputs=out, name="MediPlant_Hybrid")
    model.compile(optimizer=Adam(CFG["learning_rate"]),
                  loss="categorical_crossentropy", metrics=["accuracy"])
    print(f"✅ Hybrid model — {model.count_params():,} parameters")
    return model

# ── ENSEMBLE DATA WRAPPER ──────────────────────────────────────────────────────
class EnsembleGenerator(tf.keras.utils.Sequence):
    def __init__(self, generator):
        self.gen = generator
    def __len__(self):
        return len(self.gen)
    def __getitem__(self, idx):
        X, y = self.gen[idx]
        return [X, X, X], y

# ── TRAIN ──────────────────────────────────────────────────────────────────────
def train(model, train_gen, val_gen, name):
    print(f"\n🚀 Training {name}...")
    save_path = os.path.join(CFG["model_save_path"], f"{name}_model.h5")

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=10,
                      restore_best_weights=True, verbose=1),
        ModelCheckpoint(save_path, monitor="val_accuracy",
                        save_best_only=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5,
                          patience=5, min_lr=1e-7, verbose=1),
    ]

    tr = EnsembleGenerator(train_gen) if name == "ensemble" else train_gen
    vl = EnsembleGenerator(val_gen)   if name == "ensemble" else val_gen

    history = model.fit(tr, validation_data=vl,
                        epochs=CFG["epochs"], callbacks=callbacks, verbose=1)

    with open(os.path.join(CFG["model_save_path"], f"{name}_history.pkl"), "wb") as f:
        pickle.dump(history.history, f)

    print(f"✅ {name} saved → {save_path}")
    return history

# ── EVALUATE ───────────────────────────────────────────────────────────────────
def evaluate(model, test_gen, name, class_labels):
    print(f"\n📊 Evaluating {name}...")
    td   = EnsembleGenerator(test_gen) if name == "ensemble" else test_gen
    loss, acc = model.evaluate(td, verbose=0)
    print(f"   Loss    : {loss:.4f}")
    print(f"   Accuracy: {acc*100:.2f}%")

    preds  = model.predict(td, verbose=0)
    y_pred = np.argmax(preds, axis=1)
    y_true = test_gen.classes[:len(y_pred)]
    used_labels = class_labels[:len(set(y_true))]

    print(classification_report(y_true, y_pred, target_names=used_labels))

    metrics = {"model": name, "test_loss": float(loss), "test_accuracy": float(acc)}
    with open(os.path.join(CFG["model_save_path"], f"{name}_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(14, 11))
    sns.heatmap(cm, annot=False, fmt="d", cmap="Greens",
                xticklabels=used_labels, yticklabels=used_labels)
    plt.title(f"Confusion Matrix — {name}")
    plt.ylabel("True"); plt.xlabel("Predicted")
    plt.xticks(rotation=45, ha="right"); plt.tight_layout()
    plt.savefig(f"model/plots/{name}_confusion_matrix.png", dpi=100)
    plt.close()
    return metrics

# ── PLOT HISTORY ───────────────────────────────────────────────────────────────
def plot_history(history, name):
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    ax[0].plot(history.history["accuracy"],     label="Train", color="#2E8B57", lw=2)
    ax[0].plot(history.history["val_accuracy"], label="Val",   color="#FF6B35", lw=2, linestyle="--")
    ax[0].set_title(f"{name} — Accuracy"); ax[0].set_xlabel("Epoch")
    ax[0].legend(); ax[0].grid(alpha=0.3)

    ax[1].plot(history.history["loss"],     label="Train", color="#2E8B57", lw=2)
    ax[1].plot(history.history["val_loss"], label="Val",   color="#FF6B35", lw=2, linestyle="--")
    ax[1].set_title(f"{name} — Loss"); ax[1].set_xlabel("Epoch")
    ax[1].legend(); ax[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"model/plots/{name}_training_history.png", dpi=100)
    plt.close()

# ── MAIN ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  🌿  MediPlant AI — Model Training")
    print("=" * 60)

    train_gen, val_gen, test_gen, num_classes, class_labels = create_data_generators()

    # Ensemble
    ens  = build_ensemble(num_classes)
    h_e  = train(ens, train_gen, val_gen, "ensemble")
    plot_history(h_e, "ensemble")
    m_e  = evaluate(ens, test_gen, "ensemble", class_labels)

    # Hybrid
    hyb  = build_hybrid(num_classes)
    h_h  = train(hyb, train_gen, val_gen, "hybrid")
    plot_history(h_h, "hybrid")
    m_h  = evaluate(hyb, test_gen, "hybrid", class_labels)

    print("\n" + "=" * 60)
    print("  📊  FINAL RESULTS")
    print("=" * 60)
    print(f"  Ensemble Accuracy : {m_e['test_accuracy']*100:.2f}%")
    print(f"  Hybrid   Accuracy : {m_h['test_accuracy']*100:.2f}%")
    print("=" * 60)
    print("\n✅ Done! Models saved to model/saved_model/")
