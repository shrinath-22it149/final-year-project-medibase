"""
Grad-CAM Explainability Module
Generates heatmaps showing which part of the leaf the AI focused on
"""

import numpy as np
import cv2
import tensorflow as tf
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io


def get_gradcam_heatmap(model, img_array, last_conv_layer_name=None):
    """
    Generate Grad-CAM heatmap for a given image and model.
    Works for both ensemble and single models.
    """
    try:
        # Find last conv layer automatically if not specified
        if last_conv_layer_name is None:
            for layer in reversed(model.layers):
                if isinstance(layer, tf.keras.layers.Conv2D):
                    last_conv_layer_name = layer.name
                    break

        if last_conv_layer_name is None:
            return None

        # Create gradient model
        grad_model = tf.keras.models.Model(
            inputs  = model.inputs,
            outputs = [model.get_layer(last_conv_layer_name).output, model.output]
        )

        with tf.GradientTape() as tape:
            if isinstance(img_array, list):
                conv_outputs, predictions = grad_model(img_array)
            else:
                conv_outputs, predictions = grad_model(np.array([img_array]))
            pred_index = tf.argmax(predictions[0])
            class_channel = predictions[:, pred_index]

        grads    = tape.gradient(class_channel, conv_outputs)
        pooled   = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_out = conv_outputs[0]
        heatmap  = conv_out @ pooled[..., tf.newaxis]
        heatmap  = tf.squeeze(heatmap)
        heatmap  = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
        return heatmap.numpy()

    except Exception:
        return None


def overlay_heatmap_on_image(original_image, heatmap, alpha=0.4):
    """
    Overlay the Grad-CAM heatmap on the original image.
    Returns a PIL Image with the heatmap overlaid.
    """
    try:
        if isinstance(original_image, Image.Image):
            img_array = np.array(original_image.resize((224, 224)))
        else:
            img_array = cv2.resize(original_image, (224, 224))

        # Resize heatmap to match image
        heatmap_resized = cv2.resize(heatmap, (img_array.shape[1], img_array.shape[0]))

        # Convert heatmap to RGB colormap (jet)
        heatmap_uint8   = np.uint8(255 * heatmap_resized)
        heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)

        # Blend
        if img_array.shape[-1] == 4:
            img_array = img_array[:, :, :3]

        superimposed = cv2.addWeighted(img_array, 1 - alpha, heatmap_colored, alpha, 0)
        return Image.fromarray(superimposed)

    except Exception:
        return original_image


def create_comparison_figure(original_image, heatmap_image):
    """
    Create a side-by-side comparison figure.
    Returns bytes of the figure.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(original_image)
    axes[0].set_title("Original Leaf Image", fontsize=13, fontweight="bold", color="#2E8B57")
    axes[0].axis("off")

    axes[1].imshow(heatmap_image)
    axes[1].set_title("Grad-CAM Heatmap\n(Red = AI Focus Area)", fontsize=13, fontweight="bold", color="#CC0000")
    axes[1].axis("off")

    plt.suptitle("AI Explainability Analysis", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return buf
