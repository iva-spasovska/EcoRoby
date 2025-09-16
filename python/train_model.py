import tensorflow as tf
from tensorflow import keras

# ----------------------------
# Paths
# ----------------------------
train_dir = "dataset/train"
val_dir = "dataset/val"

# ----------------------------
# Parameters
# ----------------------------
img_size = (224, 224)
batch_size = 16   # smaller batch for small dataset
epochs_stage1 = 15
epochs_stage2 = 8

# ----------------------------
# Data generators
# ----------------------------
train_datagen = keras.preprocessing.image.ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=25,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.3,
    horizontal_flip=True,
    brightness_range=[0.7, 1.3]
)

val_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)

train_gen = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical"
)

val_gen = val_datagen.flow_from_directory(
    val_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical"
)

# ----------------------------
# Base Model (Transfer Learning)
# ----------------------------
base_model = keras.applications.MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)
base_model.trainable = False  # Stage 1: freeze base

# ----------------------------
# Custom head
# ----------------------------
x = base_model.output
x = keras.layers.GlobalAveragePooling2D()(x)
x = keras.layers.Dropout(0.4)(x)   # dropout for regularization
x = keras.layers.Dense(64, activation="relu")(x)
x = keras.layers.Dropout(0.3)(x)
preds = keras.layers.Dense(3, activation="softmax")(x)

model = keras.Model(inputs=base_model.input, outputs=preds)

# ----------------------------
# Compile
# ----------------------------
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ----------------------------
# Callbacks for Stage 1
# ----------------------------
callbacks_stage1 = [
    keras.callbacks.EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=2, min_lr=1e-7),
    keras.callbacks.ModelCheckpoint("best_model_stage1.h5", save_best_only=True, monitor="val_loss")
]

# ----------------------------
# Stage 1 Training (head only)
# ----------------------------
print("Stage 1 training (frozen base)...")
history1 = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=epochs_stage1,
    callbacks=callbacks_stage1
)

# ----------------------------
# Stage 2 Training (fine-tune last 20 layers)
# ----------------------------
print("Fine-tuning last 20 layers...")
base_model.trainable = True
for layer in base_model.layers[:-20]:  # keep most frozen
    layer.trainable = False

model.compile(
    optimizer=keras.optimizers.Adam(1e-5),  # smaller learning rate
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

callbacks_stage2 = [
    keras.callbacks.EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=2, min_lr=1e-7),
    keras.callbacks.ModelCheckpoint("best_model_finetuned.h5", save_best_only=True, monitor="val_loss")
]

history2 = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=epochs_stage2,
    callbacks=callbacks_stage2
)

# ----------------------------
# Save final model
# ----------------------------
model.save("model.h5")
print("Training complete. Model saved as 'model.h5'")
