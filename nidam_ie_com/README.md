# nidam-ie-com

A complete ecommerce web application built with Python Flask for a single merchant with multilingual support (Arabic RTL and English).

## Features

- **Multilingual Support**: Full Arabic (RTL) and English support with dynamic UI adaptation
- **Product Management**: Display products with dedicated pages, images, pricing, and attributes
- **Admin Dashboard**: Secure admin panel for managing products, categories, and index parameters
- **Ecommerce Development Index**: Customizable scoring system to measure product performance
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Easy Deployment**: Compatible with VPS and cPanel hosting environments

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: Jinja2 Templates, HTML, CSS, JavaScript
- **Database**: SQLite (default) with MySQL compatibility
- **Deployment**: Gunicorn + Nginx for VPS, Passenger for cPanel

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd nidam-ie-com
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python init_db.py
   ```

5. Run the development server:
   ```bash
   python app.py
   ```

6. Access the application:
   - Public site: http://localhost:5000
   - Admin panel: http://localhost:5000/admin
   - Default admin credentials: username: `admin`, password: `admin123`

## Deployment

### VPS Deployment (Gunicorn + Nginx)

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Create a Gunicorn configuration file (`gunicorn.conf.py`):
   ```python
   bind = "0.0.0.0:8000"
   workers = 4
   timeout = 120
   ```

3. Run Gunicorn:
   ```bash
   gunicorn -c gunicorn.conf.py app:create_app()
   ```

4. Configure Nginx with the following server block:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }

       location /static {
           alias /path/to/nidam-ie-com/static;
       }
   }
   ```

### cPanel Deployment (Passenger)

1. Upload the application files to your cPanel account

2. Create a Passenger configuration file (`passenger_wsgi.py`):
   ```python
   import sys
   import os

   sys.path.insert(0, os.path.dirname(__file__))

   from app import create_app

   application = create_app()
   ```

3. In cPanel:
   - Go to "Setup Python App"
   - Create a new application
   - Select Python version (3.8 or higher)
   - Set application root to your app directory
   - Set application URL to your desired path
   - Set application startup file to `passenger_wsgi.py`
   - Click "Create"

4. After the application is created, install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Initialize the database:
   ```bash
   python init_db.py
   ```

## Project Structure

```
nidam-ie-com/
├── app.py                 # Main application file
├── config/
│   ├── __init__.py
│   └── settings.py        # Configuration settings
├── models/                # Database models
│   ├── __init__.py
│   ├── product.py
│   ├── category.py
│   ├── admin_user.py
│   ├── attribute.py
│   ├── index_parameter.py
│   └── index_result.py
├── views/                 # Flask blueprints
│   ├── __init__.py
│   ├── public.py
│   ├── admin.py
│   └── auth.py
├── templates/             # HTML templates
│   ├── base.html
│   ├── ar/                # Arabic templates
│   ├── en/                # English templates
│   └── admin/             # Admin templates
├── static/                # Static assets
│   ├── css/
│   ├── js/
│   ├── uploads/
│   └── fonts/
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── auth.py
│   ├── file_upload.py
│   └── index_calculator.py
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── init_db.py            # Database initialization
└── README.md             # This file
```

## Customization

### Adding New Languages

To add a new language:

1. Create a new directory in `templates/` with the language code (e.g., `templates/fr/`)
2. Copy templates from `templates/en/` to the new directory and translate content
3. Add language-specific CSS if needed in `static/css/`
4. Update the language switcher in the base templates

### Modifying the Ecommerce Index

The Ecommerce Development Index can be customized through the admin panel:

1. Navigate to "Index Parameters" in the admin dashboard
2. Add new parameters with custom formulas (e.g., "sales * 0.1", "views / 100")
3. Assign weights to each parameter to determine importance
4. The system will automatically calculate scores based on your parameters

## Security Considerations

- Change the default admin password immediately after installation
- Use a strong SECRET_KEY in production
- Regularly update dependencies
- Implement proper backup procedures for the database
- Consider using HTTPS in production

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on the repository or contact the development team.