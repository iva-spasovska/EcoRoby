import cv2
import os
import random
import shutil

# ----------------------------
# Settings
# ----------------------------
classes = ["Hartija", "Plastika", "Staklo"]
num_images_per_class = 35   # how many images to capture per class
temp_dir = "dataset/temp"
final_dir = "dataset"

# ----------------------------
# Create temp folders
# ----------------------------
for c in classes:
    os.makedirs(os.path.join(temp_dir, c), exist_ok=True)

# ----------------------------
# Capture images
# ----------------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

print(">>> Press 's' to save, 'n' to switch class, 'q' to quit")

current_class = 0
img_counts = {c: 0 for c in classes}

while current_class < len(classes):
    ret, frame = cap.read()
    if not ret:
        print("Cannot read frame")
        break

    cv2.putText(frame, f"Class: {classes[current_class]}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        count = img_counts[classes[current_class]]
        save_path = os.path.join(temp_dir, classes[current_class], f"{count}.jpg")
        cv2.imwrite(save_path, frame)
        img_counts[classes[current_class]] += 1
        print(f"Saved: {save_path}")

        if img_counts[classes[current_class]] >= num_images_per_class:
            print(f"Done with class {classes[current_class]}")
            current_class += 1  # move to next class

    elif key == ord("n"):
        current_class = (current_class + 1) % len(classes)
        print(f"--- Now capturing: {classes[current_class]} ---")
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# ----------------------------
# Split dataset into train/val
# ----------------------------
for c in classes:
    class_temp_dir = os.path.join(temp_dir, c)
    files = os.listdir(class_temp_dir)
    random.shuffle(files)

    split = max(1, int(0.8 * len(files)))  # at least 1 image in train
    train_files = files[:split]
    val_files = files[split:]

    for t in train_files:
        train_path = os.path.join(final_dir, "train", c)
        os.makedirs(train_path, exist_ok=True)
        shutil.move(os.path.join(class_temp_dir, t), os.path.join(train_path, t))

    for v in val_files:
        val_path = os.path.join(final_dir, "val", c)
        os.makedirs(val_path, exist_ok=True)
        shutil.move(os.path.join(class_temp_dir, v), os.path.join(val_path, v))

# Remove temp
shutil.rmtree(temp_dir)

print("Dataset prepared in 'dataset/train' and 'dataset/val'")
