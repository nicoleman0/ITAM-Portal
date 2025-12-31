# IT Asset Management System Online Portal

This is a simple Django-based IT Asset Management system for tracking and managing IT assets (laptops, desktops, etc.), users, and employees.

## Features

- **Asset Management**: Track IT assets with serial numbers, models, and categories
- **QR Code Generation**: Automatically generate QR codes for assets
- **Status Tracking**: Monitor asset status (Available, Deployed, Broken, Retired)
- **Warranty Management**: Track purchase dates and warranty expiry
- **Admin Interface**: Full-featured Django admin panel for asset management

## Requirements

- Python 3.8 or higher
- Django 5.0+
- PostgreSQL (or SQLite for development)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /home/nick/IT-django-project
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser account:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

## Running the Application

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the application:**
   - Open your browser and navigate to: `http://127.0.0.1:8000/`
   - The root URL automatically redirects to the admin panel
   - Or directly access: `http://127.0.0.1:8000/admin/`

3. **Login:**
   - Use the superuser credentials you created during installation

## Project Structure

```
IT-django-project/
├── assets/                 # Main app for asset management
│   ├── models.py          # Asset and Category models
│   ├── admin.py           # Admin interface configuration
│   ├── views.py           # View logic
│   ├── urls.py            # App URL routing
│   └── migrations/        # Database migrations
├── itam_project/          # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── db.sqlite3             # SQLite database (development)
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Key Models

### Category
- Organizes assets into categories (e.g., Laptop, Desktop, Server)
- Fields: name, description

### Asset
- Core model for tracking IT assets
- Fields:
  - Serial Number (unique identifier)
  - Model
  - Category (Foreign Key)
  - Purchase Date
  - Warranty Expiry
  - Status (Available, Deployed, Broken, Retired)
  - QR Code (auto-generated)

## Usage

1. **Add Categories:**
   - Navigate to Admin → Categories
   - Create categories like "Laptops", "Monitors", "Servers", etc.

2. **Add Assets:**
   - Navigate to Admin → Assets
   - Fill in asset details (serial number, model, category, dates)
   - QR codes are automatically generated for easy tracking

3. **Manage Assets:**
   - Update asset status as they are deployed or retired
   - Track warranty expiration dates
   - View and search assets through the admin interface

## Development

To make changes to the database schema:

1. Modify models in `assets/models.py`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`

## Dependencies

- **Django**: Web framework
- **psycopg2-binary**: PostgreSQL adapter
- **python-decouple**: Configuration management
- **qrcode[pil]**: QR code generation
- **Pillow**: Image processing

## License

MIT License.