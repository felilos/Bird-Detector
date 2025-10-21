import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models, optimizers
import traceback
import sys
import os

# ---------------------------
# Parameters
# ---------------------------
IMG_SIZE = (128, 128)
BATCH_SIZE = 16
EPOCHS = 10

dataset_dir = r"<path>"
train_dir = os.path.join(dataset_dir, "train")
val_dir   = os.path.join(dataset_dir, "val")

try:
    # ---------------------------
    # Data generators
    # ---------------------------
    train_gen = ImageDataGenerator(
        rescale=1./255,
        horizontal_flip=True,
        rotation_range=10,
        brightness_range=[0.8, 1.2]
    )

    val_gen = ImageDataGenerator(rescale=1./255)

    train_flow = train_gen.flow_from_directory(
        train_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    val_flow = val_gen.flow_from_directory(
        val_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    # ---------------------------
    # Model
    # ---------------------------
    base_model = MobileNetV2(input_shape=IMG_SIZE + (3,),
                             include_top=False,
                             weights='imagenet',
                             pooling='avg')
    base_model.trainable = False

    model = models.Sequential([
        base_model,
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer=optimizers.Adam(1e-4),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # ---------------------------
    # Training
    # ---------------------------
    history = model.fit(
        train_flow,
        validation_data=val_flow,
        epochs=EPOCHS,
        verbose=1  # show per-epoch output
    )

    # ---------------------------
    # Save models
    # ---------------------------
    keras_model_path = os.path.join(dataset_dir, "bird_detector.h5")
    tflite_model_path = os.path.join(dataset_dir, "bird_detector.tflite")

    model.save(keras_model_path)
    print(f"✅ Keras model saved as {keras_model_path}")

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()
    with open(tflite_model_path, "wb") as f:
        f.write(tflite_model)
    print(f"✅ TFLite model saved as {tflite_model_path}")

except Exception as e:
    print("❌ ERROR during training or saving model:")
    traceback.print_exc(file=sys.stdout)
    sys.exit(1)
