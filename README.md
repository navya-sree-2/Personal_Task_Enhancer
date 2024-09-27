📋 Personal Task Enhancer
Welcome to the Personal Task Enhancer, your ultimate productivity companion! This web-based tool is designed to simplify task management, boost productivity, and keep you organized with real-time notifications. With an intuitive interface and powerful features, managing your tasks and deadlines has never been easier.


🛠️ Technology Stack
Django: A high-level Python web framework for rapid development and clean, pragmatic design.
SQLite: A lightweight relational database for storing user and task data.
Bootstrap: For responsive and mobile-friendly front-end design.
Font Awesome: Stunning icons for a modern, professional user experience.
CAPTCHA Integration: Security mechanism to prevent bot attacks during user sign-up.


🚀 Installation and Setup
Prerequisites
Python 3.x
Django 3.x+
SQLite (built-in with Django)
Git (for version control)

📂 Project Structure

personal-task-enhancer/
│
├── tasks/                # Core app for managing tasks and notifications
│   ├── migrations/       # Database migrations
│   ├── templates/        # HTML templates for rendering pages
│   ├── static/           # CSS, JS, images
│   └── views.py          # Core views for task operations
│
├── personal_task_enhancer/
│   ├── settings.py       # Django project settings
│   ├── urls.py           # URL routing configuration
│   └── wsgi.py           # WSGI application
│
├── db.sqlite3            # SQLite database
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation (this file)


📦 Features in Detail
1. Task Management
Add new tasks with descriptions and deadlines.
Update or delete tasks based on changing priorities.
View all tasks on a clean, intuitive dashboard.
2. Overdue Task Notifications
Get notified instantly when any task is overdue.
Notifications appear with a bell icon and can be marked as read.
3. User Authentication
Secure registration and login functionality.
CAPTCHA integration to prevent bots and spammers.
Password reset functionality in case users forget their credentials.
4. Dashboard
A sleek, modern dashboard to manage all tasks, deadlines, and notifications in one place.


👩‍💻 Developer
Developed and maintained by Navya Sree. Feel free to reach out if you have any questions, feedback, or suggestions!

⭐ Don't forget to give this project a star if you found it helpful!
