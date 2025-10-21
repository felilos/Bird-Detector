import tensorflow as tf
import numpy as np
import os
import shutil
from tensorflow.keras.preprocessing import image
from tqdm import tqdm

# ===============================
# CONFIGURATION
# ===============================
MODEL_PATH = "<model_name>.h5"   # or bird_detector.h5
SOURCE_DIR = r"<path>"  # validation negatives
DEST_DIR   = r"<path>"      # where to copy misclassified images
IMG_SIZE   = (128, 128)
THRESHOLD  = 0.5  # predicted probability threshold for "bird"

os.makedirs(DEST_DIR, exist_ok=True)

# ===============================
# LOAD MODEL
# ===============================
model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Model loaded successfully.")

# ===============================
# LOOP THROUGH IMAGES & PREDICT
# ===============================
image_files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
print(f"🔍 Found {len(image_files)} images to test for hard negatives.")

hard_count = 0

for fname in tqdm(image_files, desc="Scanning for hard negatives"):
    path = os.path.join(SOURCE_DIR, fname)

    # Load and preprocess image
    img = image.load_img(path, target_size=IMG_SIZE)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0) / 255.0

    # Predict probability
    prob = model.predict(x, verbose=0)[0][0]

    if prob > THRESHOLD:  # model wrongly thinks there's a bird
        shutil.copy(path, os.path.join(DEST_DIR, fname))
        hard_count += 1

print(f"\n🚫 Hard negatives found: {hard_count}")
print(f"📁 Misclassified images copied to: {DEST_DIR}")
