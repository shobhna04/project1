
import streamlit as st
import pandas as pd
from google import genai
from dotenv import load_dotenv
import os
import urllib.parse
 
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
 
st.set_page_config(page_title="Life-OS", layout="wide")
st.title("👩‍🏫 SCREEN COACH 📵")
 
df = pd.read_csv("screentime.csv")
 
 
def summarize_day(day_data):
    category_totals = day_data.groupby("Category")["Minutes_Used"].sum()
    return category_totals.to_string()
 
 
df["Date"] = pd.to_datetime(df["Date"]).dt.date
 
# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.header("Controls")
 
all_dates = sorted(df["Date"].unique())
selected_date = st.sidebar.selectbox("Select a day", all_dates, index=len(all_dates) - 1)
 
daily_goals_minutes = st.sidebar.slider(
    "Daily Goal (minutes)", min_value=60, max_value=480, value=180, step=15
)
 
image_size = st.sidebar.slider(
    "Avatar Image Size (px)", min_value=256, max_value=1024, value=512, step=128
)
 
# ---------------- DATA FOR SELECTED DAY ----------------
day_data = df[df["Date"] == selected_date]
total_minutes = day_data["Minutes_Used"].sum()
most_used_app = day_data.loc[day_data["Minutes_Used"].idxmax(), "App_Name"]
delta = total_minutes - daily_goals_minutes
 
# ---------------- KPI ROW ----------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total screen time today", f"{total_minutes} min")
with col2:
    st.metric("Most used app", most_used_app)
with col3:
    st.metric(
        "vs. Daily goal",
        f"{total_minutes} min",
        delta=f"{delta:+d} min",
        delta_color="inverse",
    )
 
# ---------------- TREND CHART ----------------
st.subheader("14 Day Screen Time Trend")
daily_totals = df.groupby("Date")["Minutes_Used"].sum().reset_index()
daily_totals = daily_totals.set_index("Date")
st.bar_chart(daily_totals)
 
# ---------------- AI COACH ----------------
st.subheader("AI life coach 🤖😎")
 
if st.button("Get coaching feedback"):
    summary = summarize_day(day_data)
    prompt = f"""you are a holistic and a strict life coach, brutally honest and not generic.
Here is a user's screen time breakdown by category for one day (in minutes):
{summary}
 
Their daily screen time goal is {daily_goals_minutes} minutes. They spent {total_minutes} minutes today.
Analyze this data and give some real life solutions - not just "use your phone less". See each
category and talk about the apps with the maximum screentime. Be specific and caring, and motivate
them for tomorrow with a challenge.
 
Then, on a NEW final line starting exactly with "IMAGE_PROMPT:", write a specific visual
description (10-20 words) for an image generator. It MUST reference the SPECIFIC highest-usage
category from the data above by name (e.g. mention "social media scrolling" or "coding at a desk"
or "binge-watching shows" - whichever category had the most minutes). Describe a character and
a setting, not just an emotion. Example format: "an exhausted person scrolling social media in a
dark room, phone glow on their face" or "a focused person coding at a clean desk, morning light".
"""

 
    with st.spinner("Analyzing your day"):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        feedback = response.text
 
        if feedback is None:
            st.error("Gemini didn't return a response. Try again.")
            st.stop()
 
        if "IMAGE_PROMPT:" in feedback:
            coaching_text, image_prompt = feedback.split("IMAGE_PROMPT:")
            image_prompt = image_prompt.strip()
        else:
            coaching_text = feedback
            image_prompt = "a person looking at a glowing phone screen"
 
        # save results so slider moves don't wipe them
        st.session_state["coaching_text"] = coaching_text
        st.session_state["image_prompt"] = image_prompt
 
# ---------------- DISPLAY BLOCK (survives reruns / slider moves) ----------------
if "coaching_text" in st.session_state:
    if total_minutes > daily_goals_minutes:
        st.warning(st.session_state["coaching_text"])
    else:
        st.info(st.session_state["coaching_text"])
 
    st.subheader("Your Day, Visualized")
    encoded_prompt = urllib.parse.quote(st.session_state["image_prompt"])
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={image_size}&height={image_size}"
    st.image(image_url, caption=st.session_state["image_prompt"],width=image_size)
