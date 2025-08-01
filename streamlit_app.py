## streamlit_app.py
# CycleSync Pro: Your Career Calendar as a Streamlit App with Interactive Calendar View
# Run locally: streamlit run streamlit_app.py
# Deploy: push this file + requirements.txt to GitHub, then connect to Streamlit Community Cloud

import streamlit as st
from datetime import date, timedelta
from typing import List, Dict
import calendar

# ----- Cycle Logic -----
PhaseInfo = Dict[str, any]

PHASES: List[PhaseInfo] = [
    {
        "phase": "Menstruation",
        "days": list(range(1, 6)),
        "hormonal_landscape": "Low estrogen and progesterone",
        "behavior_insights": "Lower energy, increased introspection, reduced cognitive flexibility",
        "professional_strategies": [
            "Prioritize low-stimulation, solo tasks like admin work, planning, or deep focus writing",
            "Reflect on recent achievements and set intentions for the cycle ahead",
            "Be gentle with energy output; consider blocking calendar time for rest or reduced workload",
            "Use journaling or voice memos to track pain, fatigue, or mood patterns"
        ]
    },
    {
        "phase": "Follicular",
        "days": list(range(6, 14)),
        "hormonal_landscape": "Rising estrogen, low progesterone",
        "behavior_insights": "Increased dopamine activity, improved motivation, verbal fluency, and creativity",
        "professional_strategies": [
            "Schedule brainstorming sessions, innovation meetings, and ambitious planning",
            "Tackle complex problem-solving and new project launches",
            "Take initiative on proposals, applications, and public speaking",
            "Learn new skills or tools; cognitive flexibility is high"
        ]
    },
    {
        "phase": "Ovulation",
        "days": [14, 15, 16],
        "hormonal_landscape": "Peak estrogen, LH surge, slight progesterone increase",
        "behavior_insights": "High verbal ability, social acuity, and confidence",
        "professional_strategies": [
            "Lead presentations, pitch ideas, network actively",
            "Organize team-building or client engagement activities",
            "Practice negotiation or interview skills—your communication is sharp",
            "Delegate or collaborate on shared goals; this is a peak energy window"
        ]
    },
    {
        "phase": "Luteal",
        "days": list(range(17, 29)),
        "hormonal_landscape": "High progesterone, moderate estrogen",
        "behavior_insights": "Increased attention to detail, sensitivity, and emotional depth. PMS symptoms may arise",
        "professional_strategies": [
            "Shift focus to execution, editing, and quality control",
            "Review contracts, budgets, and project deliverables",
            "Build in flexibility and buffer time as physical symptoms may increase",
            "Practice self-compassion; reduce meetings or confrontation-heavy tasks in late luteal days"
        ]
    }
]


def get_cycle_day(start: date, today: date, length: int) -> int:
    delta = (today - start).days + 1
    return ((delta - 1) % length) + 1


def get_phase_info(day: int) -> PhaseInfo:
    for info in PHASES:
        if day in info["days"]:
            return info
    return PHASES[0]

# ----- Streamlit UI -----
st.set_page_config(page_title="CycleSync Pro", layout="centered")
st.title("🔄 CycleSync Pro")
st.subheader("Your Career Calendar for Every Cycle Phase")

# Inputs: cycle start and length
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Day 1 of your cycle", date.today() - timedelta(days=1))
with col2:
    cycle_length = st.slider("Cycle length (days)", 20, 40, 28)

# Compute today's insights
today = date.today()
cycle_day = get_cycle_day(start_date, today, cycle_length)
phase = get_phase_info(cycle_day)

# Display Today's Insight card
st.markdown(f"**Today is Cycle Day {cycle_day}**")
st.markdown(f"**Phase:** {phase['phase']}")
st.markdown(f"**Hormonal Landscape:** {phase['hormonal_landscape']}")
st.write(phase['behavior_insights'])
st.markdown("**Professional Strategies:**")
for strat in phase['professional_strategies']:
    st.markdown(f"- {strat}")

# Journaling / Energy Log
st.markdown("---")
st.markdown("### 📝 Energy Log")
entry = st.text_area("Journal your energy/mood/work notes for today", height=150)
if st.button("Save Entry"):
    st.success("Entry saved! (In a real app, this would persist to a database)")

# Interactive Calendar View
st.markdown("---")
st.markdown("## 📅 Calendar View")

# Generate current month calendar matrix
cal_matrix = calendar.monthcalendar(today.year, today.month)

selected_day = None
for week in cal_matrix:
    cols = st.columns(7)
    for idx, day_num in enumerate(week):
        if day_num == 0:
            cols[idx].write(" ")  # empty cell
        else:
            if cols[idx].button(str(day_num), key=f"cal-{day_num}"):
                selected_day = day_num

# Show recommendations on date click
if selected_day:
    sel_date = date(today.year, today.month, selected_day)
    sel_cycle_day = get_cycle_day(start_date, sel_date, cycle_length)
    sel_phase = get_phase_info(sel_cycle_day)
    st.markdown(f"### Recommendations for {sel_date.strftime('%Y-%m-%d')}")
    st.markdown(f"- Cycle Day: {sel_cycle_day}")
    st.markdown(f"- Phase: {sel_phase['phase']}")
    st.markdown(f"- Hormonal Landscape: {sel_phase['hormonal_landscape']}")
    st.markdown("**Professional Strategies:**")
    for strat in sel_phase['professional_strategies']:
        st.markdown(f"  - {strat}")

# Deployment Instructions
st.markdown("---")
st.markdown("**To deploy:**")
st.markdown("1. Ensure `requirements.txt` lists `streamlit`.  ")
st.markdown("2. Push to GitHub and connect via https://share.streamlit.io.  ")
st.markdown("3. App will auto-deploy and be live.")
