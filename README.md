# EstudIAntes Project

**EstudIAntes** is a web application developed using **Django** that allows students to manage their academic schedules, create availability blocks, and generate personalized study routines using an AI assistant.

## Prerequisites

To run this application, you need to have the following programs installed:

* **Python 3.8+** (it is recommended to use a virtual environment with `venv`)
* **Django 5.2.7+**
* **pip** (Python package manager)

## Installation

### 1. Clone the repository

First, clone the repository from GitHub:

```bash
git clone https://github.com/your_username/Proyecto-Integrador-1-EstudIAntes.git
cd Proyecto-Integrador-1-EstudIAntes
```

### 2. Create a virtual environment (optional, but recommended)

If you haven't already created a virtual environment for your project, you can do it using the following commands:

* For **Windows**:

```bash
python -m venv .venv
```

* For **macOS/Linux**:

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

* On **Windows**:

```bash
.venv\Scripts\Activate.ps1
```

* On **macOS/Linux**:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

Install all the necessary dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 5. Create the `.env` file with the required variables

Make sure to have an `.env` file at the root of your project with the following variables (you can get the API Key from OpenAI if you're using that feature):

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
OPENAI_API_KEY=your_openai_api_key
```

### 6. Run database migrations

To create the necessary tables in the database, run the migrations:

```bash
python manage.py migrate
```

### 7. Create a superuser (optional, for Django admin)

If you want to access the Django admin panel, create a superuser with:

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 8. Run the development server

To run the development server, use:

```bash
python manage.py runserver
```

You can now access the application in your browser at the URL:

```
http://127.0.0.1:8000/
```

### 9. Tests

Make sure all functionalities are correctly implemented:

* Adding schedules and available blocks.
* Viewing and applying AI-generated routines.
* Editing and deleting schedules and blocks.
* Displaying success/error messages.

---

## Project Structure

The project structure follows Django’s standard conventions. Below is a summary of the important files and directories:

```
/Proyecto-Integrador-1-EstudIAntes
│
├── busyschedule/            # Main logic for schedule management
│   ├── models.py            # Defines models for schedules and blocks
│   ├── views.py             # Views related to schedules
│   ├── forms.py             # Forms for creating and editing schedules
│   ├── urls.py              # Routes related to schedules
│   ├── templates/           # HTML templates
│   └── templatetags/        # Custom filters (if needed)
│
├── chat/                    # AI functionality
│   ├── views.py             # Views related to AI
│   ├── services.py          # Logic to interact with OpenAI API
│   └── templates/           # Templates to interact with AI
│
├── content/                 # Content (stories, challenges)
│   └── templates/           # Templates to display stories and challenges
│
├── manage.py                # Django management script
├── requirements.txt         # Project dependencies
└── .env                     # Configuration variables (including API keys)
```

---

## Known Issues

* The design is not fully responsive on mobile devices, but all functionalities are working.
* Some interactions with the AI may be slow depending on the internet connection.

---

### Final Note

This is the current state of the project. If more time is given, the goal is to further improve the frontend and perfect some functionalities, but the project is fully functional for submission.

## Authors

* Miguel Ángel Correa Piedrahita
* Valentina Zapata
* Laura Ortiz Usme
* Samuel Lenis Mira
* Julian Osorio Alturo
* EstudIAntes Team – Project Integrator 2025-2

