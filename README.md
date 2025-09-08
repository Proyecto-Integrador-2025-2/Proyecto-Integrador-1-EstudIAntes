# EstudIAntes

**EstudIAntes** is a web application developed with **Django** as part of the Integrative Project 2025-2.
The system allows students to manage their class schedules, available time blocks, and routines in a simple and intuitive way.

---

## Prerequisites

Before running the project, make sure you have installed:

* [Python 3.10+](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/)
* [Git](https://git-scm.com/)

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Proyecto-Integrador-2025-2/Proyecto-Integrador-1-EstudIAntes.git
   cd Proyecto-Integrador-1-EstudIAntes
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate     # On Linux/Mac
   venv\Scripts\activate        # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the project

1. Run database migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. (Optional) Create a superuser to access `/admin`:

   ```bash
   python manage.py createsuperuser
   ```

3. Start the development server:

   ```bash
   python manage.py runserver
   ```

4. Open in your browser:

   ```
   http://localhost:8000/
   ```

---

## Project structure

```
Proyecto-Integrador-1-EstudIAntes/
│── manage.py
│── schedule/                # Main project configuration
│   ├── settings.py
│   ├── urls.py
│   └── ...
│── busyschedule/            # Core app
│   ├── models.py            # Models (ClassSchedule, AvailableBlock, etc.)
│   ├── views.py             # Business logic
│   ├── forms.py             # Forms for schedules and blocks
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── routine.html
│   │   └── ...
│── requirements.txt         # Project dependencies
```

---

##  Main features

*  **Schedule management**: add and display classes.
*  **Available blocks**: register availability.
*  **Routines**: display occupied schedules.
*  **Web interface** powered by Django + Bootstrap.

---

## Authors

* Miguel Ángel Correa Piedrahita
* Valentina Zapata
* Laura Ortiz Usme
* Samuel Lenis Mira
* Julian Osorio Alturo
* EstudIAntes Team – Project Integrator 2025-2

