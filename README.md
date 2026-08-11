# Life-OS Screen Coach 📱⛔

An AI-powered dashboard that analyzes your daily screen time and gives you personalized coaching to build healthier digital habits — powered by Google's Gemini AI.

## What it does

- Reads and summarizes daily screen time data by category (social media, work, entertainment, etc.)
- Uses Gemini AI to generate personalized feedback and suggestions based on usage patterns
- Clean, wide-layout dashboard built with Streamlit

## Tech Stack

- **Streamlit** — dashboard UI
- **Pandas** — data processing
- **Google Gemini API** — AI-generated coaching insights
- **python-dotenv** — environment variable management

## Setup & Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/shobhna04/project1.git
   cd project1
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your own Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   (Get a free key at [Google AI Studio](https://aistudio.google.com/))

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Notes

This project reads sample screen time data from `screentime.csv`. You can replace it with your own data in the same format (Date, Category, Minutes_Used) to get personalized insights.
