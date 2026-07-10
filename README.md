# 🥗 AI Nutritionist

Snap a photo of any meal and instantly get calories, macros, a health score, and personalized nutritional advice — powered by Claude's vision AI.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Claude Vision](https://img.shields.io/badge/Claude-Vision_API-orange?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

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
| Claude Vision API | Food recognition + nutrition analysis |
| Pillow | Image processing + base64 encoding |
| Streamlit | Web app UI + camera input |

---

## 🚀 Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/Navld14/ai-nutritionist.git
cd ai-nutritionist
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
```bash
export ANTHROPIC_API_KEY=your_key_here
```

Get your free API key at [console.anthropic.com](https://console.anthropic.com)

### 4. Run the app
```bash
streamlit run app.py
```

---

## 💡 How It Works

```
Meal Photo (upload or camera)
        ↓
Pillow → convert to JPEG → base64 encode
        ↓
Claude Vision API → identifies food + estimates nutrition
        ↓
Structured JSON response parsed
        ↓
Calories, macros, health score, advice displayed
        ↓
Meal added to daily food log
```

Claude's multimodal vision model analyzes the image and returns structured nutritional data — no food database needed, works with any meal from any cuisine.

---

## 📊 Output Example

```
Meal: Grilled Chicken with Rice and Vegetables
Food Items: [grilled chicken breast, brown rice, broccoli, carrots]
Calories: 520 kcal
Protein: 45g | Carbs: 48g | Fat: 12g | Fiber: 8g
Health Score: 9/10 — Excellent
```

---

## 📁 Project Structure

```
ai-nutritionist/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore
└── README.md
```

---

## 🙋 Author

**Naveen Ladha**
[GitHub](https://github.com/Navld14)

---

## 📄 License

MIT License — free to use and modify.
