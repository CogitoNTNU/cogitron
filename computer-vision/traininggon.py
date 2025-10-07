import cv2
import os
from datetime import datetime

# Define dataset paths
SAVE_DIR = "dataset"
GREEN_DIR = os.path.join(SAVE_DIR, "green_light")
NO_LIGHT_DIR = os.path.join(SAVE_DIR, "no_light")
RED_LIGHT_DIR = os.path.join(SAVE_DIR, "red_light")


# Create directories if they don't exist
os.makedirs(GREEN_DIR, exist_ok=True)
os.makedirs(NO_LIGHT_DIR, exist_ok=True)
os.makedirs(RED_LIGHT_DIR, exist_ok=True)


# Start webcam
cap = cv2.VideoCapture(0)

print("Press 'g' to save GREEN light image.")
print("Press 'n' to save NO light image.")
print("Press 'r' to save RED light image.")

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    # Display instructions
    cv2.putText(frame, "Press 'g' for GREEN, 'n' for NO light, 'q' to quit.",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Capture Dataset", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('g'):
        filename = os.path.join(GREEN_DIR, f"green_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.jpg")
        cv2.imwrite(filename, frame)
        print(f"[Saved] GREEN: {filename}")
    elif key == ord('n'):
        filename = os.path.join(NO_LIGHT_DIR, f"no_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.jpg")
        cv2.imwrite(filename, frame)
        print(f"[Saved] NO LIGHT: {filename}")
    elif key == ord('r'):
        filename = os.path.join(NO_LIGHT_DIR, f"no_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.jpg")
        cv2.imwrite(filename, frame)
        print(f"[Saved] RED: {filename}")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
