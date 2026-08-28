# Task Manager – Django Web Application

**Codveda Technology**
**Python Development Internship — Level 3 (Advanced)**
**Task 1 — Django Web Application with Authentication**

---

## 1. Project Overview

Task Manager is a full-stack Django web application that lets users register, log in, and manage their own personal to-do list. It was built to satisfy the Level 3 (Advanced) internship requirement of producing a fully functional Django app with secure authentication, role-based permissions, and a clean, professional, responsive UI.

The app is deliberately scoped as a **Task Manager**: users can create tasks, set a priority and due date, mark them complete, and track their progress from a dashboard. Admins get an additional system-wide view via the built-in Django admin panel.

---

## 2. Task Requirements

This project implements every requirement of the internship brief:

- User registration, login, and logout
- Secure password storage via Django's built-in authentication system
- Two user roles — Admin and Regular User — with different permissions
- Password reset via email (console backend for local development)
- Task management (create / read / update / delete / complete)
- Responsive, professional frontend
- Proper error handling and Django messages for user feedback
- Clean, modular project structure

---

## 3. Features

- Modern responsive UI built with Bootstrap 5 + custom CSS
- Dashboard with live task statistics (total, pending, completed, high priority)
- Filterable task list (All / Pending / Completed)
- Flash messages for every success/error action
- Django admin panel for full data management (admins only)

---

## 4. Authentication Features

| Feature | Details |
|---|---|
| Registration | Username, email, password, confirm password, full server-side validation |
| Duplicate prevention | Duplicate usernames and emails are rejected with a clear error |
| Login | Username + password, invalid-credential errors shown clearly |
| Logout | Secure POST-based logout (CSRF protected) |
| Password Reset | Full Django password-reset workflow: request → email sent → confirm → complete |
| Password Storage | Never stored in plain text — handled entirely by Django's `PBKDF2` hasher |

---

## 5. User Roles

**Admin**
- Full access to the Django admin panel (`/admin/`)
- Can view, edit, and delete every user's tasks
- Can manage users and groups

**Regular User**
- Can register/login
- Has a personal dashboard
- Can create, view, edit, delete, and complete only **their own** tasks
- Cannot access the Django admin panel or another user's tasks (enforced at the view level, not just hidden in the UI)

Roles are stored on a `Profile` model (one-to-one with Django's `User`) and are automatically created via a `post_save` signal. Superusers created with `createsuperuser` are automatically given the Admin role.

---

## 6. Task Management Features

Each task has: title, description, created_by, created_at, updated_at, due_date, completed, priority (Low / Medium / High).

Users can:
- Add a task
- View their tasks (with filtering by status)
- Edit a task
- Delete a task (with a confirmation screen)
- Mark a task as completed / pending
- See pending vs. completed tasks separately

---

## 7. Technologies Used

- **Backend:** Python 3, Django 5
- **Database:** SQLite (development)
- **Frontend:** HTML5, CSS3, Bootstrap 5 (CDN), Bootstrap Icons, vanilla JS
- **Auth:** Django's built-in `django.contrib.auth`

---

## 8. Project Structure

```
Task-1-Django-Web-App/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── taskmanager/            # Project settings, root URLs, WSGI/ASGI
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                # Registration, login, profile, roles
│   ├── models.py            # Profile model (admin / regular user)
│   ├── forms.py              # RegisterForm, ProfileUpdateForm
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── tasks/                   # Task CRUD + dashboard
│   ├── models.py             # Task model
│   ├── forms.py               # TaskForm
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
│   ├── base.html
│   ├── registration/         # login, register, password reset templates
│   ├── tasks/                 # dashboard, task list/form/delete
│   └── accounts/              # profile page
│
└── static/
    ├── css/style.css
    └── js/script.js
```

> Note: `db.sqlite3` and `__pycache__/` are intentionally excluded from the repository (see `.gitignore`) and will be generated automatically the first time you run migrations.

---

## 9. Installation

```bash
git clone <your-repo-url>
cd Task-1-Django-Web-App
```

---

## 10. Virtual Environment Setup

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

---

## 11. Installing Dependencies

```bash
pip install -r requirements.txt
```

---

## 12. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 13. Creating a Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password. This account will automatically be given the **Admin** role.

---

## 14. Running the Development Server

```bash
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser.

---

## 15. How to Register

1. Go to `/accounts/register/` (or click "Register" in the navbar).
2. Fill in a username, email, and password (twice, to confirm).
3. On success you are logged in automatically and redirected to your dashboard.

---

## 16. How to Login

1. Go to `/accounts/login/`.
2. Enter your username and password.
3. Invalid credentials show a clear inline error message.

---

## 17. How to Reset Your Password

1. On the login page, click **"Forgot password?"**.
2. Enter your account's email address.
3. **In development**, the reset email is printed directly to the terminal where `runserver` is running (no real email is sent) — copy the reset link from there and open it in your browser.
4. Enter and confirm your new password.

### Configuring Gmail SMTP for real emails (optional / production)

By default the project uses Django's **console email backend**, so nothing is actually sent. To send real emails via Gmail:

1. Create a Gmail **App Password** (Google Account → Security → 2-Step Verification → App Passwords).
2. Set the following environment variables before running the server:

```bash
export DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
export DJANGO_EMAIL_HOST_USER=your_email@gmail.com
export DJANGO_EMAIL_HOST_PASSWORD=your_app_password
export DJANGO_DEFAULT_FROM_EMAIL=your_email@gmail.com
```

(On Windows, use `set` instead of `export`.)

`EMAIL_HOST`, `EMAIL_PORT`, and `EMAIL_USE_TLS` already default to Gmail's SMTP settings (`smtp.gmail.com`, `587`, TLS enabled) in `settings.py`, so no further changes are needed.

---

## 18. Admin Usage

1. Log in with a superuser/admin account.
2. An **"Admin Panel"** link appears in the navbar — click it to open `/admin/`.
3. From there you can view/manage all Users, Groups, Profiles, and Tasks across every account.
4. Admins also see **every user's tasks** (not just their own) in the regular Task Manager UI.

---

## 19. Regular User Usage

1. Register or log in as a normal user.
2. Use the navbar to reach **Dashboard**, **My Tasks**, **Add Task**, and **Profile**.
3. Create tasks, set a priority/due date, mark them complete, edit or delete them.
4. You will only ever see and be able to modify tasks you created — attempting to access another user's task directly returns a permission error.

---

## 20. Testing

The following was manually and programmatically verified before packaging:

1. ✅ User registration
2. ✅ Duplicate registration (username/email) rejected
3. ✅ Valid login
4. ✅ Invalid login shows an error
5. ✅ Logout
6. ✅ Password reset flow (email printed to console with working link)
7. ✅ Admin panel access for admins
8. ✅ Admin panel blocked for regular users
9. ✅ Task creation
10. ✅ Task editing
11. ✅ Task deletion (with confirmation)
12. ✅ Marking a task completed / pending
13. ✅ A regular user cannot edit or delete another user's task (returns HTTP 403)
14. ✅ CSRF protection active on all forms (login, register, tasks, logout)
15. ✅ Form validation (empty title, invalid email, weak/mismatched passwords, etc.)

To run Django's own test runner (once you add test cases under each app's `tests.py`):

```bash
python manage.py test
```

---

## 21. Screenshots

_Add screenshots of the login page, register page, dashboard, and task list here before submitting/publishing._

- `screenshots/login.png`
- `screenshots/register.png`
- `screenshots/dashboard.png`
- `screenshots/task_list.png`

---

## 22. Security Notes

- Passwords are **never** stored or handled in plain text — Django's `PBKDF2` password hasher is used automatically.
- All forms use Django's CSRF protection (`{% csrf_token %}`).
- All task and dashboard views are protected with `@login_required`.
- Task edit/delete/toggle views explicitly check that the requesting user owns the task (or is an admin) before allowing any change — this is enforced in the view logic, not just hidden in the template.
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and email credentials are all configurable via environment variables so no secrets need to be hardcoded or committed.
- `.gitignore` excludes `db.sqlite3`, `.env`, and all virtual-environment/cache files from version control.
- Before deploying to production: set `DJANGO_DEBUG=False`, set a strong random `DJANGO_SECRET_KEY`, configure `DJANGO_ALLOWED_HOSTS`, and switch to a production-grade database and email backend.

---

## 23. Future Improvements

- Add task categories/tags and search
- Add pagination to the task list for users with many tasks
- Add unit/integration tests using Django's `TestCase` framework
- Add REST API endpoints (Django REST Framework) for a future mobile/SPA frontend
- Add email verification on registration
- Deploy to a production host (e.g. Render, Railway, or Heroku) with PostgreSQL

---

## 24. Author

Built as part of the **Codveda Technology — Python Development Internship**, Level 3 (Advanced), Task 1.
