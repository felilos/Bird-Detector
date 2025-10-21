import tensorflow as tf
import os
import sys

# ----------------------------
# 1️⃣ Specify your model path
# ----------------------------
keras_model_file = r"<path>\<model_name>.h5"

# ----------------------------
# 2️⃣ Verify input file exists
# ----------------------------
if not os.path.exists(keras_model_file):
    print(f"❌ Model file not found: {keras_model_file}")
    input("Press Enter to exit...")
    sys.exit(1)

# ----------------------------
# 3️⃣ Specify output path
# ----------------------------
tflite_model_file = "bird_model_bbb.tflite"

# ----------------------------
# 4️⃣ Load and create converter
# ----------------------------
print("🔹 Loading Keras model...")
keras_model = tf.keras.models.load_model(keras_model_file)
converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)

# ----------------------------
# 5️⃣ Restrict to built-in ops only
# ----------------------------
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS]

# Optional: enable quantization (comment out if not needed)
# converter.optimizations = [tf.lite.Optimize.DEFAULT]
# converter.target_spec.supported_types = [tf.float16]

# ----------------------------
# 6️⃣ Convert
# ----------------------------
print("⚙️ Converting model...")
try:
    tflite_model = converter.convert()
except Exception as e:
    print(f"❌ Conversion failed: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

# ----------------------------
# 7️⃣ Save result
# ----------------------------
with open(tflite_model_file, "wb") as f:
    f.write(tflite_model)

abs_path = os.path.abspath(tflite_model_file)
print(f"✅ TFLite model successfully saved to:\n{abs_path}")

# ----------------------------
# 8️⃣ Keep window open
# ----------------------------
input("Press Enter to exit...")
