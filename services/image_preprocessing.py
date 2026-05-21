"""
Enhanced Image Preprocessing for X-Ray Medical Images
Preserves important lung regions and handles aspect ratios correctly
"""

import numpy as np
import cv2
from tensorflow.keras.preprocessing import image as keras_image
from PIL import Image
import os


def preprocess_image_xray(img_path, target_size=(224, 224), preserve_aspect=True):
    """
    Preprocess X-ray image while preserving important lung regions
    
    Args:
        img_path: Path to image file
        target_size: Target size (height, width)
        preserve_aspect: If True, use padding instead of stretching
        
    Returns:
        np.array: Preprocessed image (1, H, W, 3) normalized 0-1
    """
    
    # 1. Load image with OpenCV (better for medical images)
    img = cv2.imread(img_path)
    
    if img is None:
        # Fallback to PIL if OpenCV fails
        img_pil = Image.open(img_path)
        img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    # 2. Convert to grayscale if needed (X-rays are often single channel)
    if len(img.shape) == 2:  # Grayscale
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif img.shape[2] == 4:  # RGBA
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    # 3. Enhance contrast for better lung visibility
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    img_lab[:, :, 0] = clahe.apply(img_lab[:, :, 0])
    img = cv2.cvtColor(img_lab, cv2.COLOR_LAB2BGR)
    
    # 4. Resize with aspect ratio preservation
    if preserve_aspect:
        img = resize_with_padding(img, target_size)
    else:
        img = cv2.resize(img, (target_size[1], target_size[0]))
    
    # 5. Convert to RGB (OpenCV uses BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 6. Normalize to 0-1
    img_array = img.astype('float32') / 255.0
    
    # 7. Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


def resize_with_padding(img, target_size=(224, 224), fill_color=0):
    """
    Resize image to target size while preserving aspect ratio
    Uses padding instead of stretching
    
    Args:
        img: Input image (OpenCV format)
        target_size: Target (height, width)
        fill_color: Color for padding (0=black)
        
    Returns:
        np.array: Resized image with padding
    """
    h, w = img.shape[:2]
    target_h, target_w = target_size
    
    # Calculate scaling factor to fit image in target box
    scale = min(target_w / w, target_h / h)
    
    # Resize image
    new_w = int(w * scale)
    new_h = int(h * scale)
    img_resized = cv2.resize(img, (new_w, new_h))
    
    # Create canvas
    canvas = np.full((target_h, target_w, 3), fill_color, dtype=img.dtype)
    
    # Center the image on canvas
    y_offset = (target_h - new_h) // 2
    x_offset = (target_w - new_w) // 2
    
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = img_resized
    
    return canvas


def preprocess_image_for_visualization(img_path, target_size=(224, 224)):
    """
    Load original image for Grad-CAM visualization (keeping uint8)
    
    Args:
        img_path: Path to image file
        target_size: Target size (height, width)
        
    Returns:
        np.array: Image array (H, W, 3) in uint8 (0-255)
    """
    
    img = cv2.imread(img_path)
    
    if img is None:
        img_pil = Image.open(img_path)
        img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale if needed
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    # Enhance contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    img_lab[:, :, 0] = clahe.apply(img_lab[:, :, 0])
    img = cv2.cvtColor(img_lab, cv2.COLOR_LAB2BGR)
    
    # Resize with padding
    img = resize_with_padding(img, target_size)
    
    # Convert to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Keep as uint8 (0-255)
    return np.uint8(img)


def save_gradcam_with_alpha(heatmap, original_img, output_path, alpha=0.4):
    """
    Save Grad-CAM with better blending
    
    Args:
        heatmap: Grad-CAM heatmap (0-1)
        original_img: Original image (uint8)
        output_path: Where to save
        alpha: Blend factor (0-1)
    """
    import matplotlib.cm as cm
    from tensorflow import keras
    
    # Scale heatmap to 0-255
    heatmap_uint8 = np.uint8(255 * heatmap)
    
    # Apply jet colormap
    jet = cm.get_cmap("jet")
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap_uint8]
    
    # Convert to PIL and resize
    jet_heatmap_img = keras.preprocessing.image.array_to_img(jet_heatmap)
    jet_heatmap_img = jet_heatmap_img.resize((original_img.shape[1], original_img.shape[0]))
    jet_heatmap_array = keras.preprocessing.image.img_to_array(jet_heatmap_img)
    
    # Blend: heatmap * alpha + original * (1-alpha)
    blended = jet_heatmap_array * alpha + original_img * (1 - alpha)
    blended = np.uint8(np.clip(blended, 0, 255))
    
    # Save
    result_img = keras.preprocessing.image.array_to_img(blended)
    result_img.save(output_path)
    
    return output_path