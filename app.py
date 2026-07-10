import streamlit as st
import anthropic
import base64
import json
from PIL import Image
import io

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Nutritionist 🥗",
    page_icon="🥗",
    layout="wide"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero {
    text-align: center;
    padding: 1.5rem 0 0.5rem 0;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #22c55e, #84cc16, #f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p { color: #888; font-size: 1rem; margin-top: -6px; }

.food-card {
    background: #0a1a0a;
    border: 1px solid #22c55e33;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
}

.macro-box {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.macro-value { font-size: 1.8rem; font-weight: 700; }
.macro-label { font-size: 0.65rem; color: #555; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }

.health-score-ring {
    text-align: center;
    padding: 20px;
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 16px;
}
.score-number { font-size: 4rem; font-weight: 700; line-height: 1; }
.score-label { font-size: 0.75rem; color: #555; text-transform: uppercase; letter-spacing: 2px; margin-top: 6px; }

.advice-card {
    background: #0a1200;
    border: 1px solid #84cc1633;
    border-left: 3px solid #84cc16;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin-bottom: 10px;
    color: #d9f99d;
    font-size: 0.9rem;
    line-height: 1.6;
}

.food-item-tag {
    display: inline-block;
    background: #0a1a0a;
    border: 1px solid #22c55e44;
    color: #86efac;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.8rem;
    margin: 3px;
}

.warning-card {
    background: #1a0a00;
    border: 1px solid #f59e0b44;
    border-left: 3px solid #f59e0b;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    color: #fcd34d;
    font-size: 0.85rem;
    margin-bottom: 8px;
}

.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #555;
    margin-bottom: 10px;
}

.calorie-bar-bg {
    background: #1a1a1a;
    border-radius: 999px;
    height: 8px;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
def image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")


def analyze_food(image: Image.Image) -> dict:
    client = anthropic.Anthropic()
    img_b64 = image_to_base64(image)

    prompt = """You are an expert nutritionist and food scientist. Analyze this meal image carefully.

Respond ONLY with valid JSON (no markdown, no preamble):
{
  "meal_name": "<descriptive name of the overall meal>",
  "food_items": ["<item1>", "<item2>", "<item3>"],
  "calories": <estimated total calories as integer>,
  "protein_g": <protein in grams as integer>,
  "carbs_g": <carbohydrates in grams as integer>,
  "fat_g": <fat in grams as integer>,
  "fiber_g": <fiber in grams as integer>,
  "health_score": <integer 1-10, 10 being healthiest>,
  "health_label": "<one of: Excellent | Good | Moderate | Unhealthy | Very Unhealthy>",
  "health_color": "<one of: #22c55e | #86efac | #f59e0b | #ef4444 | #991b1b>",
  "positives": ["<health positive 1>", "<health positive 2>"],
  "warnings": ["<health concern 1>"],
  "advice": "<2-3 sentences of personalized nutritional advice for this specific meal>",
  "better_alternatives": "<one simple suggestion to make this meal healthier>"
}

If you cannot identify food in the image, set meal_name to "Unknown" and estimate conservatively."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": img_b64
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def calorie_context(calories: int) -> tuple:
    """Returns (percentage of daily intake, color)"""
    daily = 2000
    pct = min((calories / daily) * 100, 100)
    if pct < 20:
        return pct, "#22c55e", "Low calorie meal"
    elif pct < 40:
        return pct, "#86efac", "Moderate calories"
    elif pct < 60:
        return pct, "#f59e0b", "High calorie meal"
    else:
        return pct, "#ef4444", "Very high calorie meal"


# ── Session state ──────────────────────────────────────────────────────────────
if "daily_log" not in st.session_state:
    st.session_state.daily_log = []
if "total_calories" not in st.session_state:
    st.session_state.total_calories = 0


# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <h1>🥗 AI Nutritionist</h1>
    <p>Snap your meal — get instant calories, macros & health advice</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

left, right = st.columns([1, 1.2], gap="large")

with left:
    st.markdown("<div class='section-label'>📷 Upload or Take a Photo of Your Meal</div>", unsafe_allow_html=True)

    upload_tab, camera_tab = st.tabs(["📁 Upload Image", "📷 Take Photo"])

    image = None
    with upload_tab:
        uploaded = st.file_uploader("", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")
        if uploaded:
            image = Image.open(uploaded).convert("RGB")

    with camera_tab:
        camera = st.camera_input("", label_visibility="collapsed")
        if camera:
            image = Image.open(camera).convert("RGB")

    if image:
        st.image(image, caption="Your meal", use_column_width=True)

        if st.button("🔍 Analyze Nutrition", type="primary", use_container_width=True):
            with st.spinner("AI is analyzing your meal... 🧠🥗"):
                try:
                    result = st.session_state.get("last_result", None)
                    result = analyze_food(image)
                    st.session_state.last_result = result
                    st.session_state.daily_log.append(result)
                    st.session_state.total_calories += result["calories"]
                    st.rerun()
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
    else:
        st.markdown("""
        <div style='text-align:center; padding:3rem 0; color:#333'>
            <div style='font-size:4rem'>🍽️</div>
            <div style='margin-top:1rem; color:#555'>Upload a photo of your meal to get started</div>
        </div>
        """, unsafe_allow_html=True)

    # Daily tracker
    if st.session_state.daily_log:
        st.markdown("---")
        st.markdown("<div class='section-label'>📅 Today's Food Log</div>", unsafe_allow_html=True)
        daily_cal = st.session_state.total_calories
        daily_pct = min((daily_cal / 2000) * 100, 100)
        color = "#22c55e" if daily_pct < 50 else "#f59e0b" if daily_pct < 80 else "#ef4444"

        st.markdown(f"""
        <div style='background:#111; border:1px solid #222; border-radius:12px; padding:16px; margin-bottom:12px'>
            <div style='display:flex; justify-content:space-between; margin-bottom:6px'>
                <span style='color:#888; font-size:0.85rem'>Daily Calories</span>
                <span style='color:{color}; font-weight:700'>{daily_cal} / 2000 kcal</span>
            </div>
            <div class='calorie-bar-bg'>
                <div style='width:{daily_pct:.0f}%; background:{color}; height:8px; border-radius:999px'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for i, meal in enumerate(reversed(st.session_state.daily_log)):
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #1a1a1a'>
                <span style='color:#ccc; font-size:0.85rem'>🍽️ {meal['meal_name']}</span>
                <span style='color:#888; font-size:0.85rem'>{meal['calories']} kcal</span>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ Clear Log", use_container_width=True):
            st.session_state.daily_log = []
            st.session_state.total_calories = 0
            st.session_state.pop("last_result", None)
            st.rerun()

with right:
    result = st.session_state.get("last_result", None)

    if not result:
        st.markdown("""
        <div style='text-align:center; padding:4rem 0; color:#333'>
            <div style='font-size:4rem'>📊</div>
            <div style='margin-top:1rem; color:#555'>Nutrition analysis will appear here</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Meal name + food items
        st.markdown(f"### 🍽️ {result['meal_name']}")
        tags_html = "".join([f"<span class='food-item-tag'>{item}</span>" for item in result['food_items']])
        st.markdown(f"<div style='margin-bottom:16px'>{tags_html}</div>", unsafe_allow_html=True)

        # Health score + calories side by side
        h1, h2 = st.columns(2)
        with h1:
            st.markdown(f"""
            <div class='health-score-ring'>
                <div class='score-number' style='color:{result["health_color"]}'>{result["health_score"]}<span style='font-size:1.5rem'>/10</span></div>
                <div class='score-label'>Health Score</div>
                <div style='color:{result["health_color"]}; font-size:0.85rem; margin-top:6px; font-weight:600'>{result["health_label"]}</div>
            </div>
            """, unsafe_allow_html=True)

        with h2:
            cal_pct, cal_color, cal_ctx = calorie_context(result["calories"])
            st.markdown(f"""
            <div class='health-score-ring'>
                <div class='score-number' style='color:{cal_color}'>{result["calories"]}<span style='font-size:1rem'> kcal</span></div>
                <div class='score-label'>Calories</div>
                <div style='color:{cal_color}; font-size:0.85rem; margin-top:6px'>{cal_ctx}</div>
                <div class='calorie-bar-bg' style='margin-top:10px'>
                    <div style='width:{cal_pct:.0f}%; background:{cal_color}; height:8px; border-radius:999px'></div>
                </div>
                <div style='color:#555; font-size:0.7rem'>{cal_pct:.0f}% of daily intake</div>
            </div>
            """, unsafe_allow_html=True)

        # Macros
        st.markdown("<div class='section-label' style='margin-top:20px'>💪 Macronutrients</div>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        macros = [
            ("Protein", result["protein_g"], "g", "#3b82f6"),
            ("Carbs", result["carbs_g"], "g", "#f59e0b"),
            ("Fat", result["fat_g"], "g", "#ef4444"),
            ("Fiber", result["fiber_g"], "g", "#22c55e"),
        ]
        for col, (label, val, unit, color) in zip([m1, m2, m3, m4], macros):
            with col:
                st.markdown(f"""
                <div class='macro-box'>
                    <div class='macro-value' style='color:{color}'>{val}{unit}</div>
                    <div class='macro-label'>{label}</div>
                </div>
                """, unsafe_allow_html=True)

        # Positives
        if result.get("positives"):
            st.markdown("<div class='section-label' style='margin-top:20px'>✅ Health Positives</div>", unsafe_allow_html=True)
            for p in result["positives"]:
                st.markdown(f"<div class='advice-card'>✅ {p}</div>", unsafe_allow_html=True)

        # Warnings
        if result.get("warnings"):
            st.markdown("<div class='section-label' style='margin-top:4px'>⚠️ Watch Out</div>", unsafe_allow_html=True)
            for w in result["warnings"]:
                st.markdown(f"<div class='warning-card'>⚠️ {w}</div>", unsafe_allow_html=True)

        # Advice
        st.markdown("<div class='section-label' style='margin-top:4px'>💡 Nutritionist Advice</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background:#0a1020; border:1px solid #3b82f633; border-radius:12px; padding:16px; color:#93c5fd; font-size:0.9rem; line-height:1.7'>
            {result['advice']}
        </div>
        """, unsafe_allow_html=True)

        # Better alternative
        st.markdown(f"""
        <div style='background:#1a1200; border:1px solid #f59e0b44; border-radius:12px; padding:14px 16px; margin-top:12px; color:#fcd34d; font-size:0.85rem'>
            🔄 <b>Make it healthier:</b> {result['better_alternatives']}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#333; font-size:0.8rem'>Built with Python · Claude Vision API · Streamlit</p>", unsafe_allow_html=True)
