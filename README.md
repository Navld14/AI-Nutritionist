# 🥗 AI Nutritionist

Snap a photo of any meal and instantly get calories, macros, a health score, and personalized nutritional advice — powered by Google Gemini Vision AI.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Gemini](https://img.shields.io/badge/Google-Gemini_Vision-4285F4?style=flat-square&logo=google)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

🌐 **Live Demo:** [Try it here](https://ai-nutritionist-00.streamlit.app/)

---

## 🎯 What It Does

- 📷 **Upload or snap a photo** of any meal
- 🍽️ **Identifies all food items** in the image automatically
- 🔢 **Estimates calories & macros** — protein, carbs, fat, fiber
- 💯 **Health score** — 1 to 10 with label (Excellent → Very Unhealthy)
- 💡 **Personalized advice** — specific to what you ate
- 📅 **Daily food log** — tracks total calories across multiple meals
- 🔄 **Healthier alternatives** — simple swaps to improve the meal

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Google Gemini Vision API | Food recognition + nutrition analysis (free tier) |
| Pillow | Image processing |
| Streamlit | Web app UI + camera input |

---

## 🚀 Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/Navld14/AI-Nutritionist.git
cd AI-Nutritionist
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Gemini API key
- Go to [aistudio.google.com](https://aistudio.google.com)
- Click **Get API Key → Create API key**
- It's completely free

### 4. Set your API key
```bash
export GEMINI_API_KEY="AIzaSy..."
```

### 5. Run the app
```bash
streamlit run app.py
```

---

## 💡 How It Works

```
Meal Photo (upload or camera)
        ↓
Pillow → convert to JPEG bytes
        ↓
Gemini Vision API → identifies food + estimates nutrition
        ↓
Structured JSON response parsed
        ↓
Calories, macros, health score, advice displayed
        ↓
Meal added to daily food log
```

---

## 📁 Project Structure

```
AI-Nutritionist/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🙋 Author

**Naveen Ladha**
[GitHub](https://github.com/Navld14)

---

## 📄 License

MIT License — free to use and modify.
