import cv2
import time

PREDATORS = {"dog", "bear", "wolf"}

def blinking_alert(frame, detected_labels):
    alert = any(label in PREDATORS for label in detected_labels)

    if alert:
        t = int(time.time() * 2) % 2
        if t == 0:
            cv2.rectangle(frame, (0, 0), (frame.shape[1], 60), (0, 0, 255), -1)
            cv2.putText(frame, "⚠ PREDATOR ALERT ⚠",
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2)

    return frame