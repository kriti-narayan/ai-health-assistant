import streamlit as st
import requests
import json
from datetime import datetime

# Setup the page
st.set_page_config(
    page_title="🤖 Free AI Health Assistant",
    layout="wide",
    menu_items={
        'About': "### 🍏 Your 24/7 Health Coach\nFree personalized health advice!"
    }
)
st.title("🤖 Free AI Health Assistant")
st.write("Get personalized health, diet, and fitness advice - completely free!")

# Comprehensive local knowledge base
HEALTH_KNOWLEDGE = {
    "Lose weight": {
        "diet": [
            "🥗 Eat more vegetables - fill half your plate with non-starchy veggies",
            "🍗 Increase protein intake (chicken, fish, tofu) to stay full longer",
            "🚫 Reduce added sugars - limit sweets, sodas, and processed foods",
            "💧 Drink water before meals - can help reduce calorie intake",
            "⏲️ Practice mindful eating - eat slowly and stop when 80% full"
        ],
        "exercise": [
            "🚶‍♂️ Walk 10,000 steps daily - use a pedometer or phone tracker",
            "🏋️‍♂️ Strength train 2-3x/week - preserves muscle while losing fat",
            "🔥 Add HIIT workouts 1-2x/week - burns calories efficiently",
            "🧘‍♀️ Try yoga - reduces stress eating and improves mindfulness",
            "🛑 Break up sitting time - stand/move every 30 minutes"
        ],
        "sleep": [
            "😴 Aim for 7-9 hours - sleep deprivation increases hunger hormones",
            "🌙 Consistent schedule - go to bed/wake up at same time daily",
            "📵 No screens 1 hour before bed - blue light disrupts sleep",
            "🛌 Cool, dark bedroom - ideal temperature is 18-22°C (65-72°F)",
            "☕ Limit caffeine after 2pm - can affect sleep 6-8 hours later"
        ]
    },
    "Gain muscle": {
        "diet": [
            "🍗 Eat 1.6-2.2g protein per kg body weight daily",
            "⚖️ Calorie surplus - eat 300-500 calories above maintenance",
            "⏰ Eat every 3-4 hours - 4-6 meals/snacks per day",
            "🥑 Include healthy fats - nuts, avocados, olive oil for calories",
            "🍚 Time carbs around workouts - fuels training and recovery"
        ],
        "exercise": [
            "🏋️ Focus on compound lifts - squats, deadlifts, bench press, rows",
            "📈 Progressive overload - gradually increase weight/reps",
            "🔄 Train each muscle 2-3x/week - optimal frequency for growth",
            "🛑 Stop 1-2 reps short of failure - reduces injury risk",
            "🧘 Include mobility work - prevents injuries from heavy lifting"
        ],
        "sleep": [
            "🛌 7-9 hours nightly - muscle repair happens during sleep",
            "🔄 Consistent schedule - regulates recovery hormones",
            "🍌 Pre-bed snack - casein protein or cottage cheese for slow digestion",
            "🚫 Limit alcohol - reduces protein synthesis and recovery",
            "🛁 Warm bath before bed - can improve sleep quality"
        ]
    },
    "Stay fit": {
        "diet": [
            "🌈 Eat the rainbow - variety of colorful fruits/vegetables",
            "⚖️ Balanced macros - 40% carbs, 30% protein, 30% fats (adjustable)",
            "🌾 Choose whole grains - more nutrients than refined grains",
            "💧 Stay hydrated - drink when thirsty, pale yellow urine is ideal",
            "🧂 Limit processed foods - cook fresh when possible"
        ],
        "exercise": [
            "🏃‍♂️ 150 mins moderate or 75 mins vigorous cardio weekly",
            "💪 Strength train 2x/week - full body workouts",
            "🧘‍♀️ Include flexibility/mobility - yoga or dynamic stretching",
            "🎯 Set SMART goals - Specific, Measurable, Achievable, Relevant, Time-bound",
            "🔄 Mix it up - try new activities to prevent boredom"
        ],
        "sleep": [
            "⏰ Consistent sleep schedule - even on weekends",
            "🌅 Morning sunlight - helps regulate circadian rhythm",
            "📵 Digital sunset - no screens 1 hour before bed",
            "📚 Relaxing routine - read, meditate, light stretches",
            "🌡️ Cool bedroom - 18-22°C (65-72°F) is ideal"
        ]
    },
    "Improve sleep": {
        "diet": [
            "🕒 Finish eating 2-3 hours before bed - digestion affects sleep",
            "🍵 Chamomile tea - contains apigenin that may promote sleep",
            "🥛 Warm milk - contains tryptophan (precursor to melatonin)",
            "🍌 Bananas - contain magnesium and potassium for muscle relaxation",
            "🚫 Avoid heavy/spicy meals - can cause discomfort at night"
        ],
        "exercise": [
            "☀️ Morning exercise - helps regulate circadian rhythm",
            "🚶‍♂️ Evening walk - gentle movement aids digestion",
            "🧘‍♀️ Yoga nidra - 'sleep yoga' promotes deep relaxation",
            "🤸‍♂️ Regular activity - people who exercise sleep better",
            "⏰ Finish intense workouts 3+ hours before bed"
        ],
        "sleep": [
            "🛌 Consistent schedule - even on weekends (+/- 1 hour max)",
            "🌑 Pitch black room - use blackout curtains if needed",
            "🔇 White noise - can mask disruptive sounds",
            "🌡️ Cool temperature - 18-22°C (65-72°F) is ideal",
            "📵 Remove electronics - no TV/phones in bedroom"
        ]
    }
}

# 1. User Input Form
with st.form("health_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your name")
        age = st.number_input("Age", 10, 100, 25)
        weight = st.number_input("Weight (kg)", 30, 200, 70)
        height = st.number_input("Height (cm)", 120, 250, 170)
    
    with col2:
        health_goal = st.selectbox("Your primary goal", ["Lose weight", "Gain muscle", "Stay fit", "Improve sleep"])
        activity_level = st.selectbox("Activity level", ["Sedentary", "Lightly active", "Moderately active", "Very active", "Extremely active"])
        dietary_pref = st.selectbox("Dietary preference", ["No restrictions", "Vegetarian", "Vegan", "Gluten-free", "Low-carb"])
    
    submitted = st.form_submit_button("Get My Health Plan!")

# AI Function using Hugging Face (free)
def get_ai_advice(prompt):
    try:
        API_URL = "https://api-inference.huggingface.co/models/google/gemma-2b-it"
        headers = {"Authorization": "Bearer hf_YOUR_NEW_TOKEN_HERE"}
        
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 400}
        }
        
        with st.spinner('🤖 Generating AI-powered advice...'):
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                return response.json()[0]['generated_text']
            elif response.status_code == 503:
                # Model is loading, wait and try again
                time.sleep(10)
                response = requests.post(API_URL, headers=headers, json=payload)
                if response.status_code == 200:
                    return response.json()[0]['generated_text']
                else:
                    return None
            else:
                return None
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Generate prompt for AI
def generate_prompt(context):
    return f"""
    Act as an expert health coach. Provide specific, actionable advice for:
    - Name: {context['name']}
    - Age: {context['age']}
    - Weight: {context['weight']}kg
    - Height: {context['height']}cm
    - Goal: {context['health_goal']}
    - Activity: {context['activity_level']}
    - Diet: {context['dietary_pref']}
    
    Provide concise recommendations for:
    1. Diet (consider dietary preference)
    2. Exercise (based on activity level)
    3. Sleep optimization
    4. Lifestyle tips
    
    Format with bullet points and keep it practical.
    """

# Display Results
if submitted:
    st.balloons()
    
    user_context = {
        'name': name,
        'age': age,
        'weight': weight,
        'height': height,
        'health_goal': health_goal,
        'activity_level': activity_level,
        'dietary_pref': dietary_pref
    }
    
    # Try to get AI response first
    ai_response = get_ai_advice(generate_prompt(user_context))
    
    if ai_response:
        st.success("✨ AI-Powered Health Plan")
        st.markdown(ai_response)
        
        # Download button
        health_plan = f"""
        {name}'s Personalized Health Plan
        Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}
        
        {ai_response}
        """
        st.download_button(
            "📥 Download Full Plan", 
            health_plan, 
            file_name=f"{name}_health_plan.txt",
            mime="text/plain"
        )
    else:
        st.info("💡 Expert-Curated Health Plan (AI service busy)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🍎 Diet Plan")
            for tip in HEALTH_KNOWLEDGE[health_goal]["diet"]:
                st.write(f"- {tip}")
        
        with col2:
            st.subheader("💪 Exercise Plan")
            for tip in HEALTH_KNOWLEDGE[health_goal]["exercise"]:
                st.write(f"- {tip}")
        
        with col3:
            st.subheader("😴 Sleep Tips")
            for tip in HEALTH_KNOWLEDGE[health_goal]["sleep"]:
                st.write(f"- {tip}")
        
        st.warning("For AI-personalized advice, please try again later when our service is less busy.")

# Health tips sidebar
with st.sidebar:
    st.header("💡 Daily Health Tips")
    tip = st.selectbox(
        "Random tip",
        [
            "Start meals with vegetables to eat fewer calories overall",
            "Stand up and move for 2-3 minutes every hour",
            "20 seconds of cold water at the end of your shower boosts immunity",
            "Chew food thoroughly - aids digestion and prevents overeating",
            "Morning sunlight exposure helps regulate your circadian rhythm"
        ]
    )
    st.info(tip)
    
    st.markdown("---")
    st.markdown("**Did You Know?**")
    st.markdown("- 🕒 Consistent sleep times improve sleep quality more than extra hours")
    st.markdown("- 🚰 Thirst is often mistaken for hunger - drink water first")
    st.markdown("- 🧘 5 minutes of deep breathing reduces stress hormones")

