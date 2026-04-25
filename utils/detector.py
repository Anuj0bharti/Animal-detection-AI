from ultralytics import YOLO
import cv2
import numpy as np
import pandas as pd
import time

# Fast model
model = YOLO("yolov8n.pt")

ANIMAL_CLASSES = {
    "bird","cat","dog","horse","sheep","cow","elephant","bear",
    "zebra","giraffe","mouse","rabbit","snake","squirrel","fish",
    "person"
}

ALERT_CLASSES = {"person", "dog", "bear"}


# -------- IMAGE --------
def detect_animals_image(image, conf: float = 0.5):
    results = model(image, conf=conf, imgsz=320)[0]
    annotated = results.plot()

    rows = []
    for box in results.boxes:
        cls = int(box.cls[0])
        label = model.names.get(cls, str(cls))

        if label in ANIMAL_CLASSES:
            score = float(box.conf[0])
            rows.append({"Label": label, "Confidence": round(score, 3)})

    df = pd.DataFrame(rows)
    return annotated, df


# -------- VIDEO / WEBCAM --------
def detect_animals_frame(frame, conf: float = 0.5, alerts_on=True):
    try:
        results = model(frame, conf=conf, imgsz=320)[0]
        annotated = frame.copy()

        detected_labels = []

        for box in results.boxes:
            cls = int(box.cls[0])
            label = model.names.get(cls, str(cls))

            if label not in ANIMAL_CLASSES:
                continue

            detected_labels.append(label)

            score = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cv2.rectangle(annotated, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(
                annotated,
                f"{label} {score:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

        # 🔴 ALERT
        if alerts_on and any(label in ALERT_CLASSES for label in detected_labels):
            blink = int(time.time() * 2) % 2

            if blink == 0:
                cv2.rectangle(annotated, (0, 0), (annotated.shape[1], 60), (0, 0, 255), -1)
                cv2.putText(
                    annotated,
                    "⚠ ALERT DETECTED ⚠",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    3,
                )

        return annotated

    except Exception as e:
        print("Error:", e)
        return frame