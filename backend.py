import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import random

class SmartLearningAssistant:
    def __init__(self, student_name="Student"):
        self.student_name = student_name
        self.data_file = "student_data.json"
        self.load_data()
        
    def load_data(self):
        """Load student data from file or initialize new"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.assignments = data.get('assignments', [])
                self.works = data.get('works', [])
                self.projects = data.get('projects', [])
                self.study_log = data.get('study_log', [])
                self.timetable = data.get('timetable', {})
                self.streak = data.get('streak', 0)
                self.total_study_hours = data.get('total_study_hours', 0.0)
        else:
            self.assignments = []
            self.works = []
            self.projects = []
            self.study_log = []
            self.timetable = {}
            self.streak = 0
            self.total_study_hours = 0.0
    
    def save_data(self):
        """Save all student data to file"""
        data = {
            'assignments': self.assignments,
            'works': self.works,
            'projects': self.projects,
            'study_log': self.study_log,
            'timetable': self.timetable,
            'streak': self.streak,
            'total_study_hours': self.total_study_hours
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_assignment(self, title, subject, deadline_days, difficulty="Medium"):
        """Add new assignment"""
        deadline = (datetime.now() + timedelta(days=deadline_days)).strftime("%Y-%m-%d")
        assignment = {
            'id': len(self.assignments) + 1,
            'title': title,
            'subject': subject,
            'deadline': deadline,
            'difficulty': difficulty,
            'status': 'Pending',
            'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.assignments.append(assignment)
        self.save_data()
        return f"Assignment '{title}' added successfully!"
    
    def add_work(self, title, subject, duration_hours, completed=False):
        """Add classwork/homework"""
        work = {
            'id': len(self.works) + 1,
            'title': title,
            'subject': subject,
            'duration_hours': duration_hours,
            'completed': completed,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.works.append(work)
        self.save_data()
        return f"Work '{title}' added successfully!"
    
    def add_project(self, title, description, deadline_days, status="In Progress"):
        """Add project"""
        deadline = (datetime.now() + timedelta(days=deadline_days)).strftime("%Y-%m-%d")
        project = {
            'id': len(self.projects) + 1,
            'title': title,
            'description': description,
            'deadline': deadline,
            'status': status,
            'progress': 0,
            'created_date': datetime.now().strftime("%Y-%m-%d")
        }
        self.projects.append(project)
        self.save_data()
        return f"Project '{title}' added successfully!"
    
    def log_study_session(self, subject, duration_hours, topics_covered):
        """Log study session"""
        session = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'subject': subject,
            'duration_hours': duration_hours,
            'topics': topics_covered
        }
        self.study_log.append(session)
        self.total_study_hours += duration_hours
        self.update_streak()
        self.save_data()
        return f"Study session logged: {duration_hours}h on {subject}"
    
    def add_timetable_entry(self, day, time, subject, duration):
        """Add timetable entry"""
        if day not in self.timetable:
            self.timetable[day] = []
        entry = {'time': time, 'subject': subject, 'duration': duration}
        self.timetable[day].append(entry)
        self.save_data()
        return f"Timetable updated for {day}"
    
    def update_streak(self):
        """Update study streak based on daily activity"""
        if not self.study_log:
            self.streak = 0
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        today_studied = any(log['date'] == today for log in self.study_log)
        
        if today_studied:
            self.streak += 1
        self.save_data()
    
    def complete_assignment(self, assignment_id, score):
        """Mark assignment complete"""
        for assignment in self.assignments:
            if assignment['id'] == assignment_id:
                assignment['status'] = 'Completed'
                assignment['score'] = score
                assignment['completion_date'] = datetime.now().strftime("%Y-%m-%d")
                self.save_data()
                return f"Assignment marked complete with score: {score}%"
        return "Assignment not found"
    
    def get_ai_suggestions(self):
        """Generate AI suggestions based on performance"""
        suggestions = []
        
        # Analyze study patterns
        if self.total_study_hours < 10:
            suggestions.append("💡 Increase daily study sessions to at least 2 hours")
        
        # Check pending assignments
        pending = [a for a in self.assignments if a['status'] == 'Pending']
        if pending:
            suggestions.append(f"⚠️  You have {len(pending)} pending assignments. Prioritize them!")
        
        # Analyze performance
        completed = [a for a in self.assignments if a['status'] == 'Completed']
        if completed:
            avg_score = sum(a.get('score', 0) for a in completed) / len(completed)
            if avg_score < 70:
                suggestions.append("📚 Your average score is below 70%. Focus on difficult topics")
            elif avg_score > 85:
                suggestions.append("⭐ Excellent performance! Keep it up!")
        
        # Streak motivation
        if self.streak >= 7:
            suggestions.append(f"🔥 Amazing streak of {self.streak} days! You're on fire!")
        elif self.streak == 0:
            suggestions.append("🚀 Start your learning journey today!")
        
        # Subject analysis
        subject_study = defaultdict(float)
        for log in self.study_log[-7:]:  # Last 7 days
            subject_study[log['subject']] += log['duration_hours']
        
        if subject_study:
            least_studied = min(subject_study, key=subject_study.get)
            suggestions.append(f"📖 Spend more time on {least_studied}")
        
        return suggestions
    
    def get_encouragement(self):
        """Get personalized encouragement"""
        encouragements = [
            f"🌟 Great job today, {self.student_name}! Keep pushing forward!",
            f"🎯 You're doing amazing, {self.student_name}! Stay focused!",
            f"💪 Proud of your effort, {self.student_name}! You got this!",
            f"🏆 Excellence is your path, {self.student_name}! Well done!",
            f"✨ You're crushing it, {self.student_name}! Never give up!",
            f"🚀 {self.student_name}, you're a star! Keep shining!",
        ]
        return random.choice(encouragements)
    
    def get_study_analytics(self):
        """Get analytics for visualization"""
        analytics = {
            'total_study_hours': self.total_study_hours,
            'current_streak': self.streak,
            'total_assignments': len(self.assignments),
            'completed_assignments': len([a for a in self.assignments if a['status'] == 'Completed']),
            'pending_assignments': len([a for a in self.assignments if a['status'] == 'Pending']),
            'total_projects': len(self.projects),
            'total_works': len(self.works),
            'completed_works': len([w for w in self.works if w['completed']]),
        }
        
        # Subject-wise breakdown
        subject_hours = defaultdict(float)
        for log in self.study_log:
            subject_hours[log['subject']] += log['duration_hours']
        analytics['subject_wise_hours'] = dict(subject_hours)
        
        # Daily study hours (last 7 days)
        daily_study = defaultdict(float)
        for log in self.study_log[-30:]:  # Last 30 entries
            daily_study[log['date']] += log['duration_hours']
        analytics['daily_study'] = dict(daily_study)
        
        # Performance scores
        scores = [a.get('score', 0) for a in self.assignments if a.get('score')]
        if scores:
            analytics['avg_score'] = sum(scores) / len(scores)
        else:
            analytics['avg_score'] = 0
        
        return analytics
    
    def get_dashboard_summary(self):
        """Get complete dashboard summary"""
        return {
            'student_name': self.student_name,
            'analytics': self.get_study_analytics(),
            'suggestions': self.get_ai_suggestions(),
            'encouragement': self.get_encouragement(),
            'assignments': self.assignments[-5:],  # Last 5
            'projects': self.projects,
            'timetable': self.timetable
        }