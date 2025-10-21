import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers
import datetime
import os

# ===============================
# CONFIGURATION
# ===============================
IMG_SIZE = (128, 128)
BATCH_SIZE = 16
EPOCHS_FINE_TUNE = 20         # Number of fine-tune epochs
N_UNFREEZE = 20               # Unfreeze last N layers of MobileNetV2
MODEL_PATH = "<model-name>.h5"

train_dir = r"<path>"
val_dir   = r"<path>"

LOG_FILE = f"fine_tune_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# ===============================
# DATA LOADERS
# ===============================
datagen = ImageDataGenerator(rescale=1./255)
train_flow = datagen.flow_from_directory(train_dir, target_size=IMG_SIZE,
                                         batch_size=BATCH_SIZE, class_mode='binary')
val_flow = datagen.flow_from_directory(val_dir, target_size=IMG_SIZE,
                                       batch_size=BATCH_SIZE, class_mode='binary')

# ===============================
# LOAD & UNFREEZE MODEL
# ===============================
model = tf.keras.models.load_model(MODEL_PATH)
base_model = model.layers[0]  # MobileNetV2 backbone

# Freeze all except the last N layers
for layer in base_model.layers[:-N_UNFREEZE]:
    layer.trainable = False
for layer in base_model.layers[-N_UNFREEZE:]:
    layer.trainable = True

print(f"✅ Unfrozen last {N_UNFREEZE} layers of MobileNetV2 for fine-tuning.")

# ===============================
# COMPILE MODEL
# ===============================
model.compile(optimizer=optimizers.Adam(1e-5),  # Small LR for gentle fine-tuning
              loss='binary_crossentropy',
              metrics=['accuracy'])

# ===============================
# TRAIN & LOG RESULTS
# ===============================
with open(LOG_FILE, "w") as f:
    f.write("Epoch,Accuracy,Val_Accuracy,Loss,Val_Loss\n")

    for epoch in range(EPOCHS_FINE_TUNE):
        print(f"\n🚀 Starting epoch {epoch+1}/{EPOCHS_FINE_TUNE}")
        history = model.fit(train_flow,
                            validation_data=val_flow,
                            epochs=1,
                            verbose=1)

        acc = history.history['accuracy'][0]
        val_acc = history.history['val_accuracy'][0]
        loss = history.history['loss'][0]
        val_loss = history.history['val_loss'][0]

        log_line = f"{epoch+1},{acc:.4f},{val_acc:.4f},{loss:.4f},{val_loss:.4f}\n"
        f.write(log_line)
        f.flush()

        print(f"✅ Epoch {epoch+1}: acc={acc:.3f}, val_acc={val_acc:.3f}, loss={loss:.3f}, val_loss={val_loss:.3f}")

print(f"\n📘 Training log saved to: {LOG_FILE}")

# ===============================
# SAVE MODELS (.h5 + .tflite)
# ===============================
H5_PATH = "bird_detector_finetuned.h5"
TFLITE_PATH = "bird_detector_finetuned.tflite"

# Save .h5
model.save(H5_PATH)
print(f"💾 Saved fine-tuned Keras model as {H5_PATH}")

# Convert and save .tflite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # lightweight for BBB
tflite_model = converter.convert()
with open(TFLITE_PATH, "wb") as f:
    f.write(tflite_model)
print(f"💾 Saved quantized TFLite model as {TFLITE_PATH}")

print("\n🎯 Fine-tuning complete!")
print("📈 You can inspect training progress in:", LOG_FILE)
