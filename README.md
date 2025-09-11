# Anas Umar Portfolio

A modern, responsive portfolio website showcasing Anas Umar's graphic design and thumbnail creation services.

![Anas Umar Portfolio](https://assets.vercel.com/image/upload/v1669994241/random/django.png)

## Features

- **Responsive Design**: Fully responsive layout that works on all devices
- **Modern UI**: Clean and professional interface with animations
- **Portfolio Gallery**: Showcase of graphic design and thumbnail creation work
- **Contact Form**: Integrated contact form with email notifications
- **Skills & Tools Section**: Highlighting professional skills and tools used

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Django 4 (Python)
- **Animations**: CSS animations and Typed.js
- **Icons**: Boxicons
- **Deployment**: Vercel with Serverless Functions

## Project Structure

- **templates/**: Contains HTML templates
- **static/**: Contains CSS, JavaScript, and media files
  - **css/**: Stylesheet files
  - **js/**: JavaScript files
  - **images/**: Images and portfolio items
- **example/**: Django app with views and URL configurations
- **api/**: Django project settings and configurations

## Contact Form

The contact form is set up to send email notifications when users submit inquiries. Email configuration is handled through Django's email backend.

## Running Locally

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python manage.py runserver
   ```
4. Visit `http://localhost:8000` in your browser

## Deployment

This project is configured to deploy on Vercel with Django Serverless Functions.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fexamples%2Ftree%2Fmain%2Fpython%2Fdjango)

## Email Configuration

To enable email notifications from the contact form:

1. Update the email settings in `api/settings.py`:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'  # Or your email provider
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-app-password'  # Use app password for Gmail
   DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
   ```

2. For deployment on Vercel, you may need to use an alternative email service that supports serverless environments.

## License

All rights reserved 2025 Anas Umar
