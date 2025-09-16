import cv2
import numpy as np
from tensorflow import keras
import serial
import time

# ----------------------------
# Load model
# ----------------------------
model = keras.models.load_model("model.h5")
classes = ["Hartija", "Plastika", "Staklo"]
class_to_number = {"Hartija": 1, "Plastika": 2, "Staklo": 3}

# ----------------------------
# Connect to Arduino
# ----------------------------
arduino = None
while arduino is None:
    try:
        arduino = serial.Serial("COM5", 9600, timeout=1)
        time.sleep(2)  # Wait for Arduino to initialize
        print("Connected to Arduino")
    except serial.SerialException:
        print("Could not connect. Retrying in 2 seconds...")
        time.sleep(2)

# ----------------------------
# Camera capture
# ----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

predicted_label = ""

print(">>> Press 's' to capture, 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Show last predicted label
    if predicted_label:
        number = class_to_number[predicted_label]
        cv2.putText(frame, f"{predicted_label} ({number})", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Kamera", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        # Capture current frame for prediction
        img = cv2.resize(frame, (224, 224))
        img = img.astype("float32") / 255.0
        img = np.expand_dims(img, axis=0)

        preds = model.predict(img)
        predicted_label = classes[np.argmax(preds)]
        number = class_to_number[predicted_label]
        print(f"Predicted: {predicted_label} -> {number}")

        # Sending prediction to Arduino
        arduino.write(f"{number}\n".encode())

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
