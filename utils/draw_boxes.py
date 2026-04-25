import cv2

def overlay_summary(img, df):
    if df is None or len(df) == 0:
        cv2.putText(img, "No animals detected", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return img

    total = len(df)
    txt = f"Animals detected: {total}"
    cv2.putText(img, txt, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    return img