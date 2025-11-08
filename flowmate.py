"""
FlowMate - AI-Powered Menstrual Health Companion 💕
A comprehensive cycle tracking app with AI chatbot, emotional support, and crisis detection
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

# Page configuration
st.set_page_config(
    page_title="FlowMate 💕 Your Cycle Companion",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra girly pink CSS theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Quicksand', sans-serif !important;
    }
    
    .main {
        background: linear-gradient(135deg, #FFE5EC 0%, #FFC2D4 25%, #FFB3C6 50%, #FF8FAB 75%, #FB6F92 100%);
        background-attachment: fixed;
    }
    
    /* Floating hearts animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(10deg); }
    }
    
    /* Sparkle animation */
    @keyframes sparkle {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #FF69B4 0%, #FF1493 50%, #C71585 100%);
        color: white;
        border-radius: 30px;
        border: 3px solid #FFB6C1;
        padding: 12px 28px;
        font-weight: 700;
        font-size: 1.1em;
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #FF1493 0%, #C71585 50%, #FF69B4 100%);
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(255, 105, 180, 0.6);
        border-color: #FF69B4;
    }
    
    /* Metric containers */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E9 100%);
        border: 3px solid #FFB6C1;
        padding: 20px;
        border-radius: 25px;
        box-shadow: 0 10px 25px rgba(255, 182, 193, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    div[data-testid="metric-container"]::before {
        content: '✨';
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 2em;
        animation: sparkle 2s infinite;
    }
    
    /* Affirmation cards */
    .affirmation-card {
        background: linear-gradient(135deg, #FFE5EC 0%, #FFC2D4 100%);
        border: 4px solid #FF69B4;
        border-radius: 25px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.3);
        position: relative;
        animation: float 3s ease-in-out infinite;
    }
    
    .affirmation-card::before {
        content: '💖';
        position: absolute;
        top: -15px;
        right: 20px;
        font-size: 2.5em;
    }
    
    /* Emergency alert */
    .emergency-alert {
        background: linear-gradient(135deg, #FFB6C1 0%, #FFE4E9 100%);
        border: 5px solid #FF1493;
        border-radius: 30px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 15px 40px rgba(255, 20, 147, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Chat messages */
    .chat-message-user {
        background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%);
        color: white;
        padding: 18px 25px;
        border-radius: 30px 30px 5px 30px;
        margin: 15px 0;
        text-align: right;
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.4);
        font-weight: 500;
        font-size: 1.1em;
    }
    
    .chat-message-bot {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E9 100%);
        color: #C71585;
        padding: 18px 25px;
        border-radius: 30px 30px 30px 5px;
        margin: 15px 0;
        border: 3px solid #FFB6C1;
        box-shadow: 0 8px 20px rgba(255, 182, 193, 0.3);
        font-weight: 500;
        font-size: 1.1em;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E9 100%);
        padding: 15px;
        border-radius: 25px;
        box-shadow: 0 8px 20px rgba(255, 182, 193, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 20px;
        color: #FF69B4;
        font-weight: 700;
        padding: 12px 24px;
        border: 3px solid #FFB6C1;
        font-size: 1.1em;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%);
        color: white;
        border-color: #FF1493;
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        border-radius: 20px;
        border: 3px solid #FFB6C1;
        padding: 15px;
        font-size: 1.1em;
        # background: linear-gradient(135deg, #FFF0F5 0%, #FFFFFF 100%);
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #FF69B4;
        box-shadow: 0 0 20px rgba(255, 105, 180, 0.4);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FF69B4 0%, #FF1493 50%, #C71585 100%);
        border-radius: 20px;
    }
    
    /* Headers */
    h1, h2, h3 {
        # color: #FF1493 !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(255, 182, 193, 0.3);
        font-weight: 700 !important;
    }
            
    #flow-mate{
        color: white !important;
        text-align: center;
        font-size: 3em;
        margin: 0px;
    }
    
    /* Card containers */
    .element-container {
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Emoji decorations */
    .decoration {
        position: fixed;
        font-size: 3em;
        animation: float 4s ease-in-out infinite;
        opacity: 0.3;
        z-index: -1;
    }
    
    /* Custom success/info boxes */
    .stSuccess {
        background: linear-gradient(135deg, #FFE5EC 0%, #FFC2D4 100%);
        border: 3px solid #FF69B4;
        border-radius: 20px;
        color: #C71585;
        font-weight: 600;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #E0BBE4 0%, #D291BC 100%);
        border: 3px solid #957DAD;
        border-radius: 20px;
        color: #6B5B8D;
        font-weight: 600;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFE5EC 0%, #FFC2D4 100%);
        border-right: 5px solid #FFB6C1;
    }
    
    /* Sparkles effect */
    .sparkle {
        position: absolute;
        font-size: 1.5em;
        animation: sparkle 1.5s infinite;
    }
    </style>
    
    <!-- Floating decorations -->
    <div class="decoration" style="top: 10%; left: 5%;">🌸</div>
    <div class="decoration" style="top: 20%; right: 8%;">💕</div>
    <div class="decoration" style="top: 40%; left: 10%;">🦋</div>
    <div class="decoration" style="top: 60%; right: 5%;">✨</div>
    <div class="decoration" style="top: 80%; left: 15%;">🌺</div>
    <div class="decoration" style="top: 30%; right: 15%;">💖</div>
    <div class="decoration" style="top: 70%; left: 8%;">🎀</div>
    <div class="decoration" style="top: 50%; right: 12%;">🌷</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'premium' not in st.session_state:
    st.session_state.premium = False
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"type": "bot", "text": "Hi gorgeous! 💕✨ I'm FlowMate, your AI bestie. How are you feeling today, beautiful? 🌸"}
    ]
if 'emotional_score' not in st.session_state:
    st.session_state.emotional_score = 75
if 'show_emergency' not in st.session_state:
    st.session_state.show_emergency = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Beautiful"
if 'cycle_day' not in st.session_state:
    st.session_state.cycle_day = 8
if 'cycle_phase' not in st.session_state:
    st.session_state.cycle_phase = 'follicular'

# Cycle phases data
CYCLE_PHASES = {
    'menstrual': {'name': '🌙 Menstrual Phase', 'days': '1-5', 'color': '#FF69B4', 'emoji': '🌸'},
    'follicular': {'name': '🦋 Follicular Phase', 'days': '6-14', 'color': '#FF1493', 'emoji': '💫'},
    'ovulation': {'name': '✨ Ovulation Phase', 'days': '15-17', 'color': '#C71585', 'emoji': '🌟'},
    'luteal': {'name': '🌺 Luteal Phase', 'days': '18-28', 'color': '#FF69B4', 'emoji': '💕'}
}

# Affirmations by phase
AFFIRMATIONS = {
    'menstrual': [
        "🌸 I honor my body's sacred need for rest and gentleness",
        "💝 This is my divine time to recharge and nurture my beautiful soul",
        "✨ I am a goddess, strong even in my softest moments"
    ],
    'follicular': [
        "🦋 I am bursting with creative energy and endless possibilities",
        "🌟 Today is absolutely perfect for magical new beginnings",
        "💫 I embrace this beautiful surge of vitality and pure joy"
    ],
    'ovulation': [
        "👑 I radiate confidence, power, and natural beauty",
        "✨ My energy is absolutely magnetic and beautifully powerful",
        "💖 I communicate with crystal clarity and feminine grace"
    ],
    'luteal': [
        "🌺 I listen to my body with deep love and compassion",
        "🏡 I create cozy, peaceful spaces for my precious wellbeing",
        "💕 It's perfectly okay to slow down and prioritize my beautiful self"
    ]
}

# Food recommendations
FOODS = {
    'menstrual': [
        {"name": "Dark Chocolate", "benefit": "Magnesium for cramp relief 💕", "icon": "🍫"},
        {"name": "Salmon & Omega-3s", "benefit": "Anti-inflammatory goodness", "icon": "🐟"},
        {"name": "Ginger Tea", "benefit": "Soothes nausea beautifully", "icon": "🫖"},
        {"name": "Leafy Greens", "benefit": "Iron replenishment magic", "icon": "🥬"}
    ],
    'follicular': [
        {"name": "Eggs", "benefit": "Protein power for energy", "icon": "🥚"},
        {"name": "Berries", "benefit": "Antioxidant boost", "icon": "🫐"},
        {"name": "Quinoa", "benefit": "Complex carb energy", "icon": "🌾"},
        {"name": "Nuts", "benefit": "Healthy fats for glow", "icon": "🥜"}
    ],
    'ovulation': [
        {"name": "Colorful Salads", "benefit": "Fiber & nutrient richness", "icon": "🥗"},
        {"name": "Lean Protein", "benefit": "Sustained energy all day", "icon": "🍗"},
        {"name": "Green Tea", "benefit": "Antioxidant queen", "icon": "🍵"},
        {"name": "Avocado", "benefit": "Healthy fats & glow", "icon": "🥑"}
    ],
    'luteal': [
        {"name": "Sweet Potato", "benefit": "Complex carb comfort", "icon": "🍠"},
        {"name": "Dark Leafy Greens", "benefit": "Calcium & magnesium love", "icon": "🥬"},
        {"name": "Whole Grains", "benefit": "Steady blood sugar", "icon": "🌾"},
        {"name": "Herbal Tea", "benefit": "Calming & soothing", "icon": "☕"}
    ]
}

# Activities by phase
ACTIVITIES = {
    'menstrual': [
        {"name": "Gentle Restorative Yoga", "icon": "🧘‍♀️", "duration": "20 min"},
        {"name": "Guided Meditation", "icon": "🕉️", "duration": "10 min"},
        {"name": "Journaling & Reflection", "icon": "📔", "duration": "15 min"},
        {"name": "Luxurious Warm Bath", "icon": "🛁", "duration": "30 min"}
    ],
    'follicular': [
        {"name": "HIIT Power Workout", "icon": "💪", "duration": "30 min"},
        {"name": "Dance Party Time", "icon": "💃", "duration": "45 min"},
        {"name": "Social Girl Time", "icon": "👭", "duration": "2 hours"},
        {"name": "Creative Art Project", "icon": "🎨", "duration": "1 hour"}
    ],
    'ovulation': [
        {"name": "Cardio Running", "icon": "🏃‍♀️", "duration": "40 min"},
        {"name": "Strength Training", "icon": "🏋️‍♀️", "duration": "45 min"},
        {"name": "Public Speaking", "icon": "🎤", "duration": "Varies"},
        {"name": "Networking Events", "icon": "🤝", "duration": "2 hours"}
    ],
    'luteal': [
        {"name": "Pilates Flow", "icon": "🤸‍♀️", "duration": "30 min"},
        {"name": "Nature Walks", "icon": "🌳", "duration": "45 min"},
        {"name": "Cozy Reading Time", "icon": "📖", "duration": "1 hour"},
        {"name": "Self-Care Spa Day", "icon": "💆‍♀️", "duration": "1 hour"}
    ]
}

def analyze_message_for_crisis(message):
    """Detect crisis keywords in user messages"""
    crisis_keywords = ['hurt', 'die', 'kill', 'suicide', 'end it', 'can\'t go on', 
                       'hopeless', 'worthless', 'want to die', 'harm myself']
    return any(keyword in message.lower() for keyword in crisis_keywords)

def get_ai_response(user_message):
    """Generate AI chatbot responses"""
    msg_lower = user_message.lower()
    
    if 'cramp' in msg_lower or 'pain' in msg_lower:
        return "💕 Oh sweetie, I understand cramps can be so tough! Try these loving remedies: apply a cozy heating pad, sip some warm ginger tea, do gentle stretches, or treat yourself to a warm bath. Would you like me to guide you through some soothing pain-relief exercises? 🌸"
    elif 'tired' in msg_lower or 'energy' in msg_lower:
        return "✨ Beautiful, it's totally normal to feel tired during your cycle! Make sure you're nourishing yourself with iron-rich foods, staying beautifully hydrated, and getting your beauty sleep (7-8 hours). Should I suggest some delicious energy-boosting snacks? 🦋"
    elif 'mood' in msg_lower or 'sad' in msg_lower or 'anxious' in msg_lower:
        return "🌸 Your emotions are so valid, gorgeous! Hormonal changes can absolutely affect mood. Try these: deep breathing exercises, talking to a friend who loves you, journaling your beautiful thoughts, or doing something that brings you joy. I'm here to listen always. Want to talk about what's on your heart? 💖"
    elif 'exercise' in msg_lower or 'workout' in msg_lower:
        phase = st.session_state.cycle_phase
        activities = ', '.join([a['name'] for a in ACTIVITIES[phase]])
        return f"💪 Great question, babe! During your {CYCLE_PHASES[phase]['name']}, I recommend these perfect activities: {activities}. Which one sounds amazing to you? ✨"
    else:
        return "💖 I'm totally here for you, beautiful! You can ask me about cramps, moods, nutrition, exercise, or absolutely anything else. What would help you feel your best right now? 🌸✨"

# Welcome/Login Screen
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center;'>
                <h1 style='font-size: 5em; background: linear-gradient(135deg, #FF69B4, #FF1493, #C71585); 
                            -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    💕✨ FlowMate ✨💕
                </h1>
                <h3 style='color: #FF69B4; font-weight: 600;'>Your AI-Powered Cycle Bestie 🦋</h3>
                <p style='color: #C71585; font-size: 1.2em; margin-top: 20px;'>Track, Support, Empower 🌸</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        name = st.text_input("✨ What's your beautiful name?", placeholder="Enter your name, gorgeous!", key="login_name")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔐 Log In", use_container_width=True):
                if name:
                    st.session_state.user_name = name
                    st.session_state.logged_in = True
                    st.rerun()
        with col_b:
            if st.button("✨ Create Account", use_container_width=True):
                if name:
                    st.session_state.user_name = name
                    st.session_state.logged_in = True
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("✨ AI-powered cycle predictions\n\n💕 24/7 emotional support chatbot\n\n🆘 Crisis detection & immediate support")
    
    st.stop()

# Main App (After Login)
# Header
st.markdown(f"""
    <div style='background: linear-gradient(135deg, #FF69B4 0%, #FF1493 50%, #C71585 100%); 
                padding: 30px; border-radius: 30px; margin-bottom: 20px;
                box-shadow: 0 15px 40px rgba(255, 105, 180, 0.4);'>
        <h1 style='color: white; text-align: center; font-size: 3em; margin: 0;'>
            💕✨ FlowMate ✨💕
        </h1>
        <p style='color: white; text-align: center; font-size: 1.5em; opacity: 0.9; margin-top: 10px;'>
            Hi {st.session_state.user_name}! You're absolutely glowing today! 🌸
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.metric("🌸 Cycle Day", f"{st.session_state.cycle_day} / 28")
with col2:
    phase = st.session_state.cycle_phase
    st.metric(CYCLE_PHASES[phase]['emoji'] + " Phase", CYCLE_PHASES[phase]['name'].split(' ', 1)[1])
with col3:
    if not st.session_state.premium:
        if st.button("👑 Go Premium ✨", key="premium_btn"):
            st.session_state.premium = True
            st.balloons()
            st.rerun()

st.markdown("---")

# Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Dashboard", 
    "📅 Calendar", 
    "💬 AI Bestie Chat", 
    "🍎 Wellness Guide", 
    "👑 Premium ✨"
])

# DASHBOARD TAB
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Current Phase Card
        phase = st.session_state.cycle_phase
        phase_info = CYCLE_PHASES[phase]
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, {phase_info["color"]} 0%, #FF1493 100%); 
                        padding: 40px; border-radius: 30px; color: white; margin-bottom: 30px;
                        box-shadow: 0 15px 40px rgba(255, 105, 180, 0.5);
                        border: 5px solid #FFB6C1;'>
                <h2 style='font-size: 2.5em; margin: 0;'>{phase_info['emoji']} {phase_info['name']}</h2>
                <p style='font-size: 1.5em; margin-top: 15px; opacity: 0.95;'>Days {phase_info['days']} of your beautiful cycle 🌸</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Today's Affirmations
        st.markdown("### ✨💖 Today's Affirmations for Your Beautiful Soul 💖✨")
        for affirmation in AFFIRMATIONS[phase]:
            st.markdown(f"""
                <div class='affirmation-card'>
                    <p style='font-size: 1.3em; font-weight: 600; color: #C71585;'>{affirmation}</p>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Emotional Wellbeing
        st.markdown("### 💗✨ Emotional Wellbeing")
        score = st.session_state.emotional_score
        st.metric("Today's Mood Score 🌸", f"{score}%")
        st.progress(score / 100)
        
        st.markdown("**How are you feeling, gorgeous? 💕**")
        cols = st.columns(5)
        emojis = [("😊", 90), ("😌", 75), ("😐", 50), ("😔", 35), ("😢", 20)]
        for i, (emoji, score_val) in enumerate(emojis):
            if cols[i].button(emoji, key=f"mood_{i}"):
                st.session_state.emotional_score = score_val
                if score_val < 40:
                    st.session_state.show_emergency = True
                st.rerun()
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### 🌸 Quick Actions")
        if st.button("💬 Chat with AI Bestie", use_container_width=True):
            pass
        if st.button("📞 Talk to Counselor 💕", use_container_width=True):
            st.success("💕 Connecting you with a caring professional counselor...")
        if st.button("🆘 Crisis Support Now", use_container_width=True):
            st.session_state.show_emergency = True
            st.rerun()

# Emergency Alert
if st.session_state.show_emergency:
    st.markdown("""
        <div class='emergency-alert'>
            <h2 style='color: #FF1493; text-align: center;'>🚨💕 We're Here For You, Beautiful 💕🚨</h2>
            <p style='font-size: 1.3em; text-align: center; color: #C71585; margin-top: 20px;'>
                Your wellbeing matters SO deeply to us. You're not alone. Please reach out immediately: 🌸
            </p>
            <br>
            <h3 style='text-align: center; color: #FF69B4;'>📞 Call 988 - Suicide & Crisis Lifeline</h3>
            <h3 style='text-align: center; color: #FF69B4;'>💬 Text HOME to 741741</h3>
            <h3 style='text-align: center; color: #FF69B4;'>🌐 www.988lifeline.org</h3>
            <p style='text-align: center; margin-top: 20px; font-size: 1.1em; color: #C71585;'>
                You are loved. You are valued. You are important. 💖✨
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Close Alert 🌸", key="close_emergency"):
        st.session_state.show_emergency = False
        st.rerun()

# CALENDAR TAB
with tab2:
    st.markdown("### 📅🌸 Your Beautiful Cycle Calendar")
    
    # Month selector
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        current_month = datetime.now()
        st.markdown(f"<h2 style='text-align: center; color: #FF69B4;'>✨ {current_month.strftime('%B %Y')} ✨</h2>", unsafe_allow_html=True)
    
    # Calendar grid
    cal = calendar.monthcalendar(current_month.year, current_month.month)
    
    st.markdown("**🌸 Sun | Mon | Tue | Wed | Thu | Fri | Sat 🌸**")
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day != 0:
                # Determine phase based on cycle day
                cycle_day = (day - 1) % 28 + 1
                if 1 <= cycle_day <= 5:
                    color = "#FF69B4"
                    emoji = "🌸"
                elif 6 <= cycle_day <= 14:
                    color = "#FF1493"
                    emoji = "🦋"
                elif 15 <= cycle_day <= 17:
                    color = "#C71585"
                    emoji = "✨"
                else:
                    color = "#FFB6C1"
                    emoji = "💕"
                
                cols[i].markdown(f"""
                    <div style='background: {color}; color: white; padding: 15px; 
                                border-radius: 15px; text-align: center; font-weight: bold;
                                box-shadow: 0 5px 15px rgba(255, 105, 180, 0.3);
                                border: 3px solid white;'>
                        {emoji}<br>{day}
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Legend
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown("🌸 **Menstrual**")
    col2.markdown("🦋 **Follicular**")
    col3.markdown("✨ **Ovulation**")
    col4.markdown("💕 **Luteal**")

# AI CHAT TAB
with tab3:
    st.markdown("### 💬✨ AI Bestie Chat - I'm Always Here For You! 💕")
    st.caption("Chat with me 24/7 - I'm your supportive friend who always listens 🌸")
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            if msg['type'] == 'user':
                st.markdown(f"<div class='chat-message-user'>{msg['text']} 💕</div>", unsafe_allow_html=True)
            else:
                emergency_class = " style='background: linear-gradient(135deg, #FFE5EC 0%, #FFB6C1 100%); border: 5px solid #FF1493;'" if msg.get('is_emergency') else ""
                st.markdown(f"<div class='chat-message-bot'{emergency_class}>{msg['text']}</div>", unsafe_allow_html=True)
    
    # Chat input
    st.markdown("<br>", unsafe_allow_html=True)
    user_input = st.text_input("💬 Type your message here, beautiful...", key="chat_input", placeholder="Tell me what's on your mind... 🌸")
    
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("Send 💕✨", key="send_chat", use_container_width=True):
            if user_input:
                # Add user message
                st.session_state.chat_messages.append({"type": "user", "text": user_input})
                
                # Check for crisis
                if analyze_message_for_crisis(user_input):
                    st.session_state.show_emergency = True
                    st.session_state.emotional_score = 20
                    st.session_state.chat_messages.append({
                        "type": "bot",
                        "text": "💗🌸 Beautiful, I'm really concerned about you. You're not alone, and your feelings matter SO much. I've connected you with immediate support resources. Would you like me to help you reach out to a caring crisis counselor right now? You deserve support and love. 💕✨",
                        "is_emergency": True
                    })
                else:
                    # Normal AI response
                    bot_response = get_ai_response(user_input)
                    st.session_state.chat_messages.append({"type": "bot", "text": bot_response})
                
                st.rerun()

# WELLNESS TAB
with tab4:
    st.markdown("### 🍎✨ Your Personalized Wellness Guide 💕")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🍓 Yummy Foods to Nourish Your Beautiful Body")
        phase = st.session_state.cycle_phase
        for food in FOODS[phase]:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #FFE5EC 0%, #FFC2D4 100%); 
                            border: 4px solid #FF69B4; border-radius: 20px; 
                            padding: 20px; margin: 15px 0;
                            box-shadow: 0 8px 20px rgba(255, 105, 180, 0.3);'>
                    <h3 style='color: #FF1493; margin: 0;'>{food['icon']} {food['name']}</h3>
                    <p style='color: #C71585; font-size: 1.1em; margin-top: 10px; font-weight: 500;'>
                        ✨ {food['benefit']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 💪 Perfect Activities Just For You")
        for activity in ACTIVITIES[phase]:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #E0BBE4 0%, #D291BC 100%); 
                            border: 4px solid #957DAD; border-radius: 20px; 
                            padding: 20px; margin: 15px 0;
                            box-shadow: 0 8px 20px rgba(149, 125, 173, 0.3);'>
                    <h3 style='color: #6B5B8D; margin: 0;'>{activity['icon']} {activity['name']}</h3>
                    <p style='color: #8B7A9E; font-size: 1.1em; margin-top: 10px; font-weight: 500;'>
                        ⏰ {activity['duration']}
                    </p>
                </div>
            """, unsafe_allow_html=True)

# PREMIUM TAB
with tab5:
    st.markdown("### 👑✨ Unlock Premium - Because You Deserve Everything! 💕")
    
    if not st.session_state.premium:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #FFFFFF 0%, #FFE5EC 100%); 
                            border: 4px solid #FFB6C1; 
                            border-radius: 25px; padding: 35px;
                            box-shadow: 0 10px 30px rgba(255, 182, 193, 0.3);'>
                    <h2 style='color: #FF69B4; text-align: center;'>🌸 Free Plan</h2>
                    <h1 style='color: #FF1493; text-align: center; font-size: 3em;'>
                        $0<span style='font-size: 0.4em; color: #C71585;'>/month</span>
                    </h1>
                    <br>
                    <p style='font-size: 1.2em; color: #C71585;'>✨ Basic cycle tracking</p>
                    <p style='font-size: 1.2em; color: #C71585;'>💕 Daily affirmations</p>
                    <p style='font-size: 1.2em; color: #C71585;'>💬 Basic AI chat</p>
                    <p style='font-size: 1.2em; color: #C71585;'>🍎 Food & activity tips</p>
                    <p style='font-size: 1.2em; color: #C71585;'>📅 Calendar view</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #FF69B4 0%, #FF1493 50%, #C71585 100%); 
                            border-radius: 25px; padding: 35px; color: white;
                            box-shadow: 0 15px 40px rgba(255, 105, 180, 0.5);
                            border: 5px solid #FFB6C1;
                            position: relative;'>
                    <div style='position: absolute; top: -15px; right: 20px; font-size: 3em;'>👑</div>
                    <h2 style='text-align: center;'>✨ Premium Goddess ✨</h2>
                    <h1 style='text-align: center; font-size: 3em;'>
                        $9.99<span style='font-size: 0.4em; opacity: 0.9;'>/month</span>
                    </h1>
                    <br>
                    <p style='font-size: 1.2em;'>💫 Advanced AI predictions</p>
                    <p style='font-size: 1.2em;'>💬 Unlimited AI bestie chat</p>
                    <p style='font-size: 1.2em;'>📞 24/7 crisis counselor access</p>
                    <p style='font-size: 1.2em;'>🍽️ Personalized meal plans</p>
                    <p style='font-size: 1.2em;'>🎥 Exclusive workout videos</p>
                    <p style='font-size: 1.2em;'>📊 Period pain tracker</p>
                    <p style='font-size: 1.2em;'>📥 Export health reports</p>
                    <p style='font-size: 1.2em;'>⚡ Priority VIP support</p>
                    <p style='font-size: 1.2em;'>🎁 Monthly surprise self-care tips</p>
                    <p style='font-size: 1.2em;'>💝 Ad-free experience</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💳✨ Upgrade to Premium Goddess - $9.99/month", use_container_width=True, key="upgrade_premium"):
                st.session_state.premium = True
                st.success("🎉💕 Welcome to Premium, Goddess! All features unlocked! ✨👑")
                st.balloons()
                st.rerun()
    else:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF69B4 100%); 
                        border-radius: 30px; padding: 50px; color: white; text-align: center;
                        box-shadow: 0 20px 50px rgba(255, 215, 0, 0.5);
                        border: 6px solid #FFFFFF;'>
                <h1 style='font-size: 4em; margin: 0;'>👑✨ Premium Goddess ✨👑</h1>
                <p style='font-size: 1.8em; margin-top: 20px;'>You have access to ALL FlowMate magic!</p>
                <p style='font-size: 1.3em; margin-top: 15px; opacity: 0.95;'>
                    You're absolutely glowing with all these premium features! 💕🌸
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Premium features showcase
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #FFE5EC 0%, #FFC2D4 100%);
                            border: 3px solid #FF69B4; border-radius: 20px; padding: 25px; text-align: center;'>
                    <div style='font-size: 3em;'>💫</div>
                    <h3 style='color: #FF1493;'>AI Predictions</h3>
                    <p style='color: #C71585;'>Advanced cycle forecasting</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #E0BBE4 0%, #D291BC 100%);
                            border: 3px solid #957DAD; border-radius: 20px; padding: 25px; text-align: center;'>
                    <div style='font-size: 3em;'>📞</div>
                    <h3 style='color: #6B5B8D;'>24/7 Support</h3>
                    <p style='color: #8B7A9E;'>Crisis counselor access</p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #FFDAB9 0%, #FFB6C1 100%);
                            border: 3px solid #FF69B4; border-radius: 20px; padding: 25px; text-align: center;'>
                    <div style='font-size: 3em;'>🎁</div>
                    <h3 style='color: #FF1493;'>Monthly Gifts</h3>
                    <p style='color: #C71585;'>Exclusive self-care tips</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 30px;
                background: linear-gradient(135deg, #FFE5EC 0%, #FFC2D4 100%);
                border-radius: 25px; border: 3px solid #FFB6C1;'>
        <h3 style='color: #FF1493;'>💕✨ Made with Love by FlowMate ✨💕</h3>
        <p style='color: #C71585; font-size: 1.2em; margin-top: 15px;'>
            Your health, happiness, and privacy matter deeply to us 🌸
        </p>
        <p style='color: #FF69B4; font-size: 1.1em; margin-top: 10px;'>
            🆘 If you're in crisis: Call 988 (US) or contact local emergency services
        </p>
        <p style='color: #FFB6C1; font-size: 0.95em; margin-top: 15px;'>
            You are loved 💖 You are valued 💕 You are important ✨
        </p>
    </div>
""", unsafe_allow_html=True)