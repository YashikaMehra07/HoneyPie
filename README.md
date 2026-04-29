# 🍯 HoneyPie – Mood Detection Web App

HoneyPie is a Flask-based web application that detects a user’s mood in real time using a webcam and stores emotional trends for visualization.

The project integrates computer vision and deep learning to analyze facial expressions and generate insights about user emotions over time.

---

## 🚀 Features

* 🎥 Real-time mood detection using webcam
* 😊 Emotion analysis using DeepFace (pre-trained model)
* 📊 Mood data storage for each user
* 📈 Visualization of emotional trends (weekly/yearly)
* 🖥️ Interactive dashboard with camera toggle
* 🗃️ SQLite database integration

---

## 🧠 Tech Stack

**Backend**

* Python (Flask)
* OpenCV (video capture)
* DeepFace (emotion recognition)

**Frontend**

* HTML, CSS (Tailwind)
* JavaScript

**Database**

* SQLite

**Optional / Experimental**

* PyTorch (custom emotion model – not used in final pipeline)

---

## 📁 Project Structure

```
HONEYPIE/
│
├── app.py               # Main Flask app
├── mood_rec.py         # Emotion detection logic
├── dbfunc.py           # Database operations
├── pltit.py            # Visualization utilities
│
├── static/             # CSS, JS, assets
├── templates/          # HTML templates
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/your-username/honeypie.git
cd honeypie
```

### 2. Create virtual environment

```
python -m venv venv
```

Activate it:

**Windows**

```
venv\Scripts\activate
```

**Mac/Linux**

```
source venv/bin/activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Run the application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000/
```

---

## 📊 How It Works

1. Webcam captures real-time frames using OpenCV
2. Frames are passed to DeepFace for emotion analysis
3. Dominant + secondary emotions are extracted
4. Data is stored in SQLite database
5. Dashboard displays mood trends

---

## 🧪 Notes

* A custom PyTorch model (`Deep_Emotion`) was initially implemented using the FER2013 dataset
* Due to lower accuracy, the final system uses DeepFace instead
* The PyTorch model code is retained for reference and experimentation

---

## ⚠️ Limitations

* Emotion detection accuracy depends on lighting and camera quality
* DeepFace may produce inconsistent results in real-time scenarios
* No authentication/security layer implemented

---

## 🔮 Future Improvements

* Replace DeepFace with a fine-tuned lightweight model (MobileNet / EfficientNet)
* Improve UI/UX design of dashboard
* Add user authentication
* Deploy as a cloud-based service

---

## 👨‍💻 Author

Developed as part of a learning project exploring computer vision and emotion recognition.

---

## 👥 Contributors

* **Yashika Mehra** – Backend development, emotion detection, Flask integration
* **Priya Panchal** – Frontend design, UI/UX, dashboard implementation

This project was developed collaboratively as part of a learning initiative in computer vision and web development.

---

## 📜 License

This project is for educational purposes.
