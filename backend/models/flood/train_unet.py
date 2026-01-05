import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers, models

# -------------------------
# Paths
# -------------------------
processed_flood = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\processed\flood.npy"
model_save_path = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\ml_models\flood\model_unet_fast.h5"
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)

# -------------------------
# Parameters
# -------------------------
PATCH_SIZE = 64         # smaller = faster
BATCH_SIZE = 32         # larger batch fits in memory
EPOCHS = 5
SUBSET_SIZE = 10000     # train on subset each epoch

# -------------------------
# Load flood data
# -------------------------
flood_data = np.load(processed_flood)
if flood_data.ndim == 2:
    flood_data = flood_data[..., np.newaxis]

# -------------------------
# Extract patches
# -------------------------
def extract_patches(img, patch_size):
    H, W, C = img.shape
    patches = []
    # Added a stride to skip pixels and reduce the total number of patches
    stride = 4  
    for i in range(0, H - patch_size, patch_size * stride):
        for j in range(0, W - patch_size, patch_size * stride):
            patch = img[i:i+patch_size, j:j+patch_size]
            patches.append(patch)
    
    print(f"Memory-Safe: Created {len(patches)} patches.")
    return np.array(patches, dtype=np.float32)

print("Extracting patches...")
patches = extract_patches(flood_data, PATCH_SIZE)
print(f"Total patches: {len(patches)}")

X_full = patches
y_full = patches

# -------------------------
# Define small UNet (CPU-friendly)
# -------------------------
def unet_model(input_shape):
    inputs = layers.Input(shape=input_shape)

    # Encoder
    c1 = layers.Conv2D(8, 3, activation='relu', padding='same')(inputs)
    p1 = layers.MaxPooling2D(2)(c1)

    c2 = layers.Conv2D(16, 3, activation='relu', padding='same')(p1)
    p2 = layers.MaxPooling2D(2)(c2)

    # Bottleneck
    c3 = layers.Conv2D(32, 3, activation='relu', padding='same')(p2)

    # Decoder
    u2 = layers.Conv2DTranspose(16, 2, strides=2, padding='same')(c3)
    concat2 = layers.Concatenate()([u2, c2])
    c4 = layers.Conv2D(16, 3, activation='relu', padding='same')(concat2)

    u1 = layers.Conv2DTranspose(8, 2, strides=2, padding='same')(c4)
    concat1 = layers.Concatenate()([u1, c1])
    c5 = layers.Conv2D(8, 3, activation='relu', padding='same')(concat1)

    outputs = layers.Conv2D(1, 1, activation='sigmoid')(c5)
    return models.Model(inputs, outputs)

model = unet_model((PATCH_SIZE, PATCH_SIZE, 1))
model.compile(optimizer='adam', loss='mse')
model.summary()

# -------------------------
# Train on random subset per epoch
# -------------------------
for epoch in range(EPOCHS):
    print(f"\nEpoch {epoch+1}/{EPOCHS}")
    subset_indices = np.random.choice(len(X_full), size=SUBSET_SIZE, replace=False)
    X = X_full[subset_indices]
    y = y_full[subset_indices]

    dataset = tf.data.Dataset.from_tensor_slices((X, y))
    dataset = dataset.shuffle(buffer_size=SUBSET_SIZE)
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)

    model.fit(dataset, epochs=1, verbose=1)

# -------------------------
# Save model
# -------------------------
model.save(model_save_path)
print(f"Optimized Flood UNet model saved at {model_save_path}")
