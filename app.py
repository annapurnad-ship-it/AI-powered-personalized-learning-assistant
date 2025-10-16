import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend import SmartLearningAssistant
from datetime import datetime

# Page config
st.set_page_config(page_title="Smart Learning AI Assistant", layout="wide", initial_sidebar_state="expanded")

# Initialize session state
if 'assistant' not in st.session_state:
    st.session_state.assistant = SmartLearningAssistant("Student")

assistant = st.session_state.assistant

# Sidebar
with st.sidebar:
    st.title("🎓 Smart Learning Assistant")
    student_name = st.text_input("Your Name:", value=assistant.student_name)
    if student_name != assistant.student_name:
        assistant.student_name = student_name
    
    st.divider()
    page = st.radio("Navigate:", [
        "📊 Dashboard",
        "✅ Assignments",
        "📝 Works",
        "🎯 Projects",
        "⏱️ Study Log",
        "📅 Timetable",
        "🤖 AI Suggestions"
    ])

# Main content
if page == "📊 Dashboard":
    st.title("📊 Your Learning Dashboard")
    
    # Get dashboard data
    summary = assistant.get_dashboard_summary()
    analytics = summary['analytics']
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Total Study Hours", f"{analytics['total_study_hours']:.1f}h")
    
    with col2:
        st.metric("🔥 Current Streak", f"{analytics['current_streak']} days")
    
    with col3:
        st.metric("✅ Completed Assignments", analytics['completed_assignments'])
    
    with col4:
        st.metric("⭐ Average Score", f"{analytics['avg_score']:.1f}%")
    
    st.divider()
    
    # Encouragement message
    if analytics['completed_assignments'] > 0:
        st.success(f"🎉 {summary['encouragement']}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📖 Study Hours by Subject")
        if analytics['subject_wise_hours']:
            df_subjects = pd.DataFrame(list(analytics['subject_wise_hours'].items()), 
                                      columns=['Subject', 'Hours'])
            fig = px.bar(df_subjects, x='Subject', y='Hours', color='Hours',
                        color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No study data yet. Start logging study sessions!")
    
    with col2:
        st.subheader("📈 Daily Study Progress (Last 7 Days)")
        if analytics['daily_study']:
            df_daily = pd.DataFrame(list(analytics['daily_study'].items()),
                                   columns=['Date', 'Hours']).sort_values('Date')
            fig = px.line(df_daily, x='Date', y='Hours', markers=True,
                         title="Daily Study Hours")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No daily data available yet.")
    
    # Summary cards
    st.subheader("📋 Quick Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Assignments", analytics['total_assignments'])
        st.metric("Pending", analytics['pending_assignments'])
    
    with col2:
        st.metric("Total Projects", analytics['total_projects'])
        completion_rate = (analytics['completed_works'] / max(analytics['total_works'], 1)) * 100
        st.metric("Works Completion", f"{completion_rate:.0f}%")
    
    with col3:
        st.metric("Study Streak", f"{analytics['current_streak']} days 🔥")

elif page == "✅ Assignments":
    st.title("✅ Assignments")
    
    tab1, tab2 = st.tabs(["View Assignments", "Add Assignment"])
    
    with tab1:
        if assistant.assignments:
            df = pd.DataFrame(assistant.assignments)
            st.dataframe(df, use_container_width=True)
            
            # Filter and update
            col1, col2 = st.columns(2)
            with col1:
                assignment_id = st.number_input("Assignment ID to Complete:", min_value=1)
            with col2:
                score = st.slider("Score (%):", 0, 100, 85)
            
            if st.button("✅ Mark as Complete"):
                result = assistant.complete_assignment(int(assignment_id), score)
                st.success(result)
                st.rerun()
        else:
            st.info("No assignments yet. Create your first one!")
    
    with tab2:
        st.subheader("Add New Assignment")
        title = st.text_input("Assignment Title:")
        subject = st.text_input("Subject:")
        deadline_days = st.number_input("Deadline (days):", min_value=1, value=7)
        difficulty = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard"])
        
        if st.button("➕ Add Assignment"):
            if title and subject:
                result = assistant.add_assignment(title, subject, deadline_days, difficulty)
                st.success(result)
                st.rerun()
            else:
                st.error("Please fill all fields!")

elif page == "📝 Works":
    st.title("📝 Classwork & Homework")
    
    tab1, tab2 = st.tabs(["View Works", "Add Work"])
    
    with tab1:
        if assistant.works:
            df = pd.DataFrame(assistant.works)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No works logged yet.")
    
    with tab2:
        st.subheader("Add New Work")
        title = st.text_input("Work Title:")
        subject = st.text_input("Subject:")
        duration = st.number_input("Duration (hours):", min_value=0.5, step=0.5, value=1.0)
        completed = st.checkbox("Mark as Completed")
        
        if st.button("➕ Add Work"):
            if title and subject:
                result = assistant.add_work(title, subject, duration, completed)
                st.success(result)
                st.rerun()
            else:
                st.error("Please fill all fields!")

elif page == "🎯 Projects":
    st.title("🎯 Projects")
    
    tab1, tab2 = st.tabs(["View Projects", "Add Project"])
    
    with tab1:
        if assistant.projects:
            df = pd.DataFrame(assistant.projects)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No projects yet.")
    
    with tab2:
        st.subheader("Add New Project")
        title = st.text_input("Project Title:")
        description = st.text_area("Description:")
        deadline_days = st.number_input("Deadline (days):", min_value=1, value=30)
        status = st.selectbox("Status:", ["In Progress", "Planning", "Review"])
        
        if st.button("➕ Add Project"):
            if title and description:
                result = assistant.add_project(title, description, deadline_days, status)
                st.success(result)
                st.rerun()
            else:
                st.error("Please fill all fields!")

elif page == "⏱️ Study Log":
    st.title("⏱️ Study Session Log")
    
    tab1, tab2 = st.tabs(["View Log", "Log Session"])
    
    with tab1:
        if assistant.study_log:
            df = pd.DataFrame(assistant.study_log)
            st.dataframe(df, use_container_width=True)
            
            # Statistics
            st.subheader("Session Statistics")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Sessions", len(assistant.study_log))
            with col2:
                st.metric("Total Hours", f"{assistant.total_study_hours:.1f}h")
        else:
            st.info("No study sessions logged yet.")
    
    with tab2:
        st.subheader("Log New Study Session")
        subject = st.text_input("Subject:")
        duration = st.number_input("Duration (hours):", min_value=0.25, step=0.25, value=1.0)
        topics = st.text_area("Topics Covered (comma-separated):")
        
        if st.button("📝 Log Session"):
            if subject and topics:
                result = assistant.log_study_session(subject, duration, topics)
                st.success(result)
                st.rerun()
            else:
                st.error("Please fill all fields!")

elif page == "📅 Timetable":
    st.title("📅 Study Timetable")
    
    tab1, tab2 = st.tabs(["View Timetable", "Add Entry"])
    
    with tab1:
        if assistant.timetable:
            for day, entries in assistant.timetable.items():
                st.subheader(f"📅 {day}")
                for entry in entries:
                    st.write(f"⏰ {entry['time']} - **{entry['subject']}** ({entry['duration']}h)")
        else:
            st.info("No timetable entries yet.")
    
    with tab2:
        st.subheader("Add Timetable Entry")
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day = st.selectbox("Day:", days)
        time = st.time_input("Time:")
        subject = st.text_input("Subject:")
        duration = st.number_input("Duration (hours):", min_value=0.5, step=0.5, value=1.0)
        
        if st.button("➕ Add Entry"):
            if subject:
                result = assistant.add_timetable_entry(day, time.strftime("%H:%M"), subject, duration)
                st.success(result)
                st.rerun()
            else:
                st.error("Please fill all fields!")

elif page == "🤖 AI Suggestions":
    st.title("🤖 AI-Powered Suggestions")
    
    suggestions = assistant.get_ai_suggestions()
    
    if suggestions:
        st.subheader("📌 Personalized Learning Methods:")
        for i, suggestion in enumerate(suggestions, 1):
            st.info(suggestion)
    else:
        st.info("Start your learning journey to get personalized suggestions!")
    
    st.divider()
    
    st.subheader("💡 Smart Learning Tips")
    tips = [
        "🎯 **Set Clear Goals**: Define what you want to achieve each week",
        "⏱️ **Use Pomodoro Technique**: Study 25 mins, then take a 5-min break",
        "📚 **Active Recall**: Test yourself instead of just re-reading",
        "🔄 **Spaced Repetition**: Review material at increasing intervals",
        "🎮 **Gamify Learning**: Create challenges and reward yourself",
        "😴 **Get Quality Sleep**: 7-9 hours helps consolidate learning",
        "🏃 **Exercise Daily**: Physical activity boosts cognitive function",
        "👥 **Study with Others**: Collaborative learning improves retention"
    ]
    
    for tip in tips:
        st.write(tip)

st.divider()
st.caption("🌟 Keep learning, keep growing! Your future self will thank you. 🌟")