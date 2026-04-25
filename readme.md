# 🐾 Animal Detection System

A real-time animal detection system built using YOLOv8, OpenCV, and Streamlit.
It detects animals (and optionally humans) from images, videos, and webcam.

---

## 🚀 Features

- Image detection
- Video detection
- Live webcam detection
- Real-time processing
- Object counting
- Blinking alert system
- Alert ON/OFF toggle
- Saves output images and videos

---

## 🧠 Technologies Used

- Python
- YOLOv8 (Ultralytics)
- OpenCV
- Streamlit
- NumPy
- Pandas

---

## 📁 Project Structure

Animal-Detection-AI/
│── main.py
│── requirements.txt
│── README.md
│── .gitignore
│
├── utils/
│   ├── detector.py
│   ├── helpers.py
│   ├── draw_boxes.py
│   ├── alerts.py
│   ├── drone_tracker.py
│
├── media/
│   ├── uploads/
│   ├── outputs/

---

## ⚙️ Installation

1. Clone repository
git clone https://github.com/Anuj0bharti/Animal-Detection-AI.git

2. Go to folder
cd Animal-Detection-AI

3. Create virtual environment
python -m venv venv

4. Activate
venv\Scripts\activate

5. Install dependencies
pip install -r requirements.txt

---

## ▶️ Run the app

streamlit run main.py

Open in browser:
http://localhost:8501

---

## 🚨 Alert System

- Shows blinking red alert when:
  - person
  - dog
  - bear

- Can be turned ON/OFF from sidebar

---

## ⚠️ Notes

- Runs on CPU
- Model downloads automatically on first run
- Made for learning and demo purposes

---

## 👨‍💻 Author

Anuj Bharti

---

## ⭐ Support

If you like this project, give it a star ⭐
