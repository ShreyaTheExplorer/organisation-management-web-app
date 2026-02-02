📌 Employee & Project Management System with Collaboration

A full-stack web application designed to manage employees, departments, projects, tasks, and team collaboration inside an organization.

This system combines HR management + project tracking + team communication, similar to a mini version of Jira + Slack.

🚀 Features
👤 Employee Management

Add, update, and manage employees

Role-based access: Admin, Team Lead, Employee

Secure login using authentication

Employees linked to departments

🏢 Department Management

Create and manage departments

Assign department managers

View employees department-wise

📁 Project Management

Team Leads can create projects

Add employees to projects

Track project status and deadlines

🧩 Project Phases

Each project divided into phases

Phase timelines tracking

✅ Task Management

Tasks assigned to employees

Task status updates (Pending / Ongoing / Completed)

Task priority and deadlines

Project progress tracking

💬 Team Collaboration (Chat + Groups)

Employees can create groups

Add/remove members

Group chat system

Message history

📎 Resource Sharing

Upload and share files inside groups

Download shared resources

🔔 Notification System

Task assignments

Deadline reminders

Group messages

Project updates

🏗 System Architecture

Frontend: React.js
Backend: Flask (Python)
Database: MySQL / PostgreSQL
Authentication: JWT
ORM: SQLAlchemy

🧠 Database Entities

Employee

Department

Project

ProjectMembers (Many-to-Many)

Phase

Task

Group

GroupMembers

Message

Resource

Notification

🔐 User Roles
Role	Permissions
Admin	Manage employees, departments
Team Lead	Create projects, assign members, manage tasks
Employee	View tasks, update status, chat in groups
🌐 API Modules
Authentication

Login

Token verification

Employees

Add employee

View employee list

Projects

Create project

Add members

View project details

Tasks

Create task

Assign task

Update task status

Collaboration

Create group

Add members

Send messages

Upload resources

🎨 Frontend Pages

Login / Register

Dashboard

Employees Page

Departments Page

Projects Page

Project Detail Page

Task Board

Groups & Chat Page

Notifications Panel

⚙️ Installation (Backend)
git clone <repo_link>
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
flask run

⚙️ Installation (Frontend)
cd frontend
npm install
npm start

🔮 Future Enhancements

Real-time chat using WebSockets

Email notifications

File storage in cloud (AWS S3)

Analytics dashboard

Mobile responsive UI

🎯 Learning Outcomes

This project helps in understanding:

Full-stack development

REST API design

Database relationships (1-M, M-M)

Authentication & Authorization

Real-time systems

Team collaboration systems

📌 Conclusion

This project simulates a real-world enterprise workflow system where employees, teams, and projects are managed efficiently along with communication and resource sharing
