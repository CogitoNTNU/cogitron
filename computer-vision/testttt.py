import cv2
import tensorflow as tf
import numpy as np

# Load model
model = tf.keras.models.load_model("light_classifier.h5")

# Labels
class_names = ["green_light", "red_light"]  # Adjust order if needed

# Start webcam
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess frame
    img = cv2.resize(frame, (64, 64))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict
    preds = model.predict(img)
    class_id = np.argmax(preds)
    confidence = preds[0][class_id]

    # Show prediction
    label = f"{class_names[class_id]}: {confidence:.2f}"
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0) if class_id == 0 else (0, 0, 255), 2)

    cv2.imshow("Light Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
