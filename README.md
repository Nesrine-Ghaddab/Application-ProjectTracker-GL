# 🎓 Personal Study & Project Tracker

## 📌 Overview

The **Personal Study & Project Tracker** is a web application developed using **Python (Django)** that helps students and individuals:

- 📚 Organize their study sessions  
- 📊 Manage projects and tasks  
- 📈 Track productivity and progress  
- 🧠 Improve focus and consistency  

This application combines **time management**, **project tracking**, and **analytics** into one intelligent platform.

---

## 🚀 Features

### 🔹 Study Session Management
- ⏱️ Smart Pomodoro timer (focus / break)
- 📊 Daily & weekly statistics
- 🎯 Focus mode (minimal distractions)
- 🧠 Smart duration suggestion (based on history)
- 👀 Tab detection → lowers productivity score if user leaves

---

### 🔹 Project & Task Management
- 📁 Create / edit / delete projects
- ✅ Add tasks with deadlines
- 📌 Track completion percentage
- ⏳ Time tracking per task
- 🤖 Smart prioritization (suggest what to do first)

---

### 🔹 Planner & Calendar
- 📅 Daily & weekly planning
- 🗓️ Calendar view
- 🔔 Optional reminders & scheduling

---

### 🔹 Analytics & Reports
- 📊 Charts (weekly productivity, time per project)
- 🔥 Streak tracking (consistency)
- ⭐ Productivity score system

---

### 🔹 Extra Modules
- 📖 Notes linked to projects
- 🔁 Habit tracker with streaks
- 🏆 Gamification (badges & rewards)

---

## 🧠 AI Integration

- 🤖 Smart chatbot assistant (guidance & productivity tips)
- 📈 Predict project completion (based on past behavior)
- 🧠 Adaptive study suggestions
- ⚡ Intelligent task prioritization

---

## 🏗️ System Architecture

### 📐 MVC Structure (Django)

#### 🟢 Models
- `User` → profile & preferences  
- `Project` → title, description, deadline  
- `Task` → deadline, status, time tracking  
- `StudySession` → duration, timestamps  
- `Habit` → frequency, streak  
- `Note` → content linked to project  

---

#### 🔵 Views (Frontend)
- Dashboard (global overview)
- Study Timer page
- Project & Task manager
- Analytics dashboard
- Planner / Calendar

---

#### 🟡 Controllers (Backend Logic)
- Authentication (login/register)
- CRUD operations
- Timer management
- Notifications & reminders
- Data analytics (statistics & trends)

---

## ⚙️ Technologies

### 🖥️ Backend
- Python (Django)

### 🗄️ Database
- SQLite (development)
- PostgreSQL / MySQL (production)

### 🎨 Frontend
- HTML / CSS / JavaScript
- TailwindCSS / Bootstrap
- Chart.js (analytics)


---

## 👥 Project Structure (Team Work)

| Module | Description | Responsible |
|------|------------|------------|
| 👤 User | Authentication & profile | MOTAZ |
| ⏱️ Study Sessions | Timer + analytics | HOUSSEM |
| 📁 Projects | Project management | NESRINE |
| ✅ Tasks | Task management & priority | AHMED |
| 📅 Meetings | Meeting management | ILYES |
| 📖 Habits & Notes | Notes + streak system | ISMAIL |
| 🤖 AI Chatbot | Smart assistant | TEAM |

---

## 🔄 User Flow

1. 🔐 User logs in  
2. 📊 Dashboard shows overview  
3. ⏱️ Start study session (timer begins)  
4. 📁 Create project → add tasks  
5. 📅 Plan activities via calendar  
6. 📈 Track progress & analytics  
7. 🧠 Get AI recommendations  

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-repo-link.git

# Go to project folder
cd PersonalTracker

# Create virtual environment
python -m venv env

# Activate environment
env\Scripts\activate   # Windows
source env/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run server
python manage.py runserver
