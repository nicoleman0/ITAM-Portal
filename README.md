# IT Asset Management System (ITAM)

A Django-based IT Asset Management System for tracking IT assets, employees, and assignments.

## Features

- **Asset Management**: Track assets with serial numbers, models, categories, purchase dates, and warranty information
- **Employee Management**: Manage employee information including departments and contact details
- **Assignment Tracking**: Track which assets are assigned to which employees
- **Warranty Monitoring**: Automatic warranty expiry detection with visual indicators in admin panel

## Models

### Category
- Categorizes assets (e.g., Laptop, Desktop, Server, Peripherals)

### Asset
- Serial number, model, category
- Purchase date and warranty expiry
- Status: Available, Deployed, Broken, Retired
- Warranty expiry highlighting in admin

### Employee
- Full name, email, department, employee ID

### Assignment
- Tracks asset assignments to employees
- Assigned date and expected return date
- Active/returned status tracking

## Setup Instructions

### 1. Create PostgreSQL Database

```bash
sudo -u postgres psql
CREATE DATABASE itam_db;
CREATE USER itam_user WITH PASSWORD 'your_password_here';
ALTER ROLE itam_user SET client_encoding TO 'utf8';
ALTER ROLE itam_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE itam_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE itam_db TO itam_user;
\q
```

### 2. Configure Database Settings

Update the database credentials in `itam_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'itam_db',
        'USER': 'itam_user',
        'PASSWORD': 'your_password_here',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/admin to access the admin panel.

## Admin Features

- **Asset List View**: Shows status and warranty expiry with color-coded indicators
  - Red badge for expired warranties
  - Green badge for active warranties
- **Search and Filter**: Easily find assets, employees, and assignments
- **Assignment Tracking**: Visual indicators for active/returned assignments

## Technology Stack

- Django 6.0
- PostgreSQL
- Python 3.x

## Project Structure

```
IT-django-project/
├── assets/              # Main application
│   ├── models.py       # Database models
│   ├── admin.py        # Admin customization
│   └── ...
├── itam_project/       # Project settings
│   ├── settings.py
│   └── ...
├── manage.py
└── requirements.txt
```

## Next Steps

- Implement views and templates for front-end
- Add asset history tracking
- Implement notifications for warranty expiry
- Add reporting and analytics
- Implement asset maintenance scheduling
