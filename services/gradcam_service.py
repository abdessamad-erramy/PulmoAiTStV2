"""
Grad-CAM Service Module
Generates Grad-CAM visualizations for model predictions
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.cm as cm


def make_gradcam_heatmap(img_array, model, last_conv_layer_name):
    """
    Generate Grad-CAM heatmap for a given image.

    Args:
        img_array:            preprocessed image, shape (1, H, W, 3), float [0, 1]
        model:                loaded Keras model
        last_conv_layer_name: e.g. 'mixed10'

    Returns:
        heatmap:   2D numpy array, values in [0, 1]
        top_index: int — predicted class index
    """

    # ── Split model into two parts ──────────────────────────────────────────
    # Part 1: input → last conv layer
    last_conv_layer  = model.get_layer(last_conv_layer_name)
    last_layer_model = keras.Model(model.inputs, last_conv_layer.output)

    # Part 2: last conv output → final predictions
    # This avoids the tape.watch ordering bug in the single-model approach
    classifier_input = keras.Input(shape=last_conv_layer.output.shape[1:])
    x = classifier_input
    
    # Walk all layers that come AFTER last_conv_layer
    found = False
    for layer in model.layers:
        if found:
            x = layer(x)
        if layer.name == last_conv_layer_name:
            found = True

    classifier_model = keras.Model(classifier_input, x)

    # ── Compute gradients (tape.watch BEFORE forward pass) ──────────────────
    with tf.GradientTape() as tape:
        # Run Part 1 first
        last_conv_output = last_layer_model(img_array)
        
        # NOW watch the tensor (inside the tape context, before Part 2)
        tape.watch(last_conv_output)
        
        # Run Part 2 on the watched tensor
        preds     = classifier_model(last_conv_output)
        top_index = tf.argmax(preds[0])
        top_class = preds[:, top_index]

    # ── Pool gradients ──────────────────────────────────────────────────────
    grads        = tape.gradient(top_class, last_conv_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # ── Weight activation maps ──────────────────────────────────────────────
    last_conv_output = last_conv_output.numpy()[0]   # (H, W, C)
    pooled_grads     = pooled_grads.numpy()          # (C,)

    for i in range(pooled_grads.shape[-1]):
        last_conv_output[:, :, i] *= pooled_grads[i]

    # ── Build & normalize heatmap ───────────────────────────────────────────
    heatmap = np.mean(last_conv_output, axis=-1)     # (H, W)
    heatmap = np.maximum(heatmap, 0)

    max_val = np.max(heatmap)
    if max_val > 0:
        heatmap /= max_val

    return heatmap, int(top_index.numpy())


def superimposed_img(image, heatmap, target_size=(224, 224), alpha=0.4):
    """
    Superimpose jet-colored heatmap on the original image.

    Args:
        image:       uint8 numpy array (H, W, 3), values 0–255
        heatmap:     2D float numpy array, values 0–1
        target_size: (W, H) to resize heatmap to
        alpha:       heatmap blend weight

    Returns:
        PIL Image
    """
    heatmap_uint8 = np.uint8(255 * heatmap)

    jet        = cm.get_cmap("jet")
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap_uint8]                         # (H, W, 3)

    jet_heatmap_img = keras.preprocessing.image.array_to_img(jet_heatmap)
    jet_heatmap_img = jet_heatmap_img.resize(target_size)
    jet_heatmap     = keras.preprocessing.image.img_to_array(jet_heatmap_img)

    superimposed = jet_heatmap * alpha + image
    superimposed = keras.preprocessing.image.array_to_img(superimposed)

    return superimposed


def generate_gradcam(model, img_array, last_conv_layer_name, image_original=None):
    heatmap, predicted_class = make_gradcam_heatmap(
        img_array, model, last_conv_layer_name
    )

    result = {
        'heatmap'         : heatmap,
        'predicted_class' : predicted_class,
        'superimposed_img': None
    }

    if image_original is not None:
        # image_original already uint8 (0-255) — NO multiplication
        result['superimposed_img'] = superimposed_img(image_original, heatmap)

    return result