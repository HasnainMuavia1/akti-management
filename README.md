# Attendance Management Portal

A comprehensive Django application for managing attendance in educational institutions. This portal provides separate interfaces for administrators and trainers to manage courses, lectures, and student attendance.

## Features

### 🎯 Core Functionality
- **User Management**: Separate interfaces for administrators and trainers
- **Course Assignment**: Admin can assign multiple courses to trainers
- **Lecture Management**: Schedule and manage course lectures
- **Attendance Tracking**: Mark and track student attendance
- **Progress Monitoring**: Track course completion progress
- **Reporting**: Generate attendance reports in various formats

### 👨‍💼 Admin Features
- **Dashboard**: Overview of system statistics
- **Trainer Management**: Create and manage trainer accounts
- **Course Assignment**: Assign courses to trainers with multiple selection
- **Lecture Management**: Create and schedule lectures
- **Individual Attendance**: View individual student attendance records
- **Course Reports**: Generate attendance reports for specific courses
- **Batch Reports**: Generate attendance reports for entire batches

### 👨‍🏫 Trainer Features
- **Dashboard**: View assigned courses and progress
- **Course Progress**: Track lecture completion and student progress
- **Attendance Marking**: Mark student attendance for lectures
- **Reports**: Generate attendance reports for assigned courses

## Technical Details

### 🏗️ Architecture
- **Framework**: Django 4.x
- **Database**: PostgreSQL
- **Frontend**: Tailwind CSS v4 with modern design system
- **Authentication**: Django's built-in authentication system
- **Responsive Design**: Mobile-first approach with sidebar navigation

### 📁 Project Structure
```
portal/
├── models.py          # Database models
├── views.py           # View logic and business logic
├── forms.py           # Form definitions
├── admin.py           # Django admin configuration
├── urls.py            # URL routing
└── apps.py            # App configuration

templates/portal/
├── login.html         # Portal login page
├── base.html          # Base template with sidebar
├── admin/             # Admin-specific templates
│   ├── dashboard.html
│   ├── trainer_management.html
│   └── course_assignment.html
└── trainer/           # Trainer-specific templates
    └── dashboard.html
```

### 🗄️ Database Models

#### Trainer
- User account (OneToOne with Django User)
- Name, status, timestamps
- Properties for course count and student count

#### TrainerCourse
- Links trainers to courses
- Tracks assignment status and timestamps
- Calculates progress based on course duration

#### Lecture
- Individual lecture sessions
- Date, time, completion status
- Links to trainer-course assignments

#### Attendance
- Student attendance records
- Status (present, absent, late, excused)
- Remarks and marking information

#### AttendanceReport
- Generated attendance reports
- Multiple report types and formats

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- Django 4.x
- PostgreSQL database
- Existing Django project with 'example' app

### 2. Add to Project
```bash
# Add portal to INSTALLED_APPS in settings.py
INSTALLED_APPS = [
    # ... existing apps
    'portal',
]

# Add portal URLs to main urls.py
urlpatterns = [
    # ... existing patterns
    path('portal/', include('portal.urls')),
]
```

### 3. Database Migration
```bash
python manage.py makemigrations portal
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

## Usage

### 🚀 Getting Started

1. **Access Portal**: Navigate to `/portal/`
2. **Login**: Use admin credentials or trainer credentials
3. **Admin Setup**:
   - Create trainers using Trainer Management
   - Assign courses to trainers using Course Assignment
   - Schedule lectures using Lecture Management
4. **Trainer Usage**:
   - View assigned courses on dashboard
   - Mark attendance for scheduled lectures
   - Generate attendance reports

### 🔐 User Types

#### Administrator
- Full access to all features
- Can create and manage trainers
- Can assign courses and schedule lectures
- Can view all attendance data and reports

#### Trainer
- Access only to assigned courses
- Can mark attendance for their lectures
- Can generate reports for their courses
- Limited to their assigned responsibilities

### 📊 Course Duration Logic

The system automatically calculates lecture counts based on course duration:
- **1 Month Courses**: 12 lectures
- **Weekday/Weekend Courses**: 24 lectures

### 📈 Progress Tracking

- **Lecture Progress**: Tracks completed vs. total lectures
- **Attendance Statistics**: Present, absent, late, and excused counts
- **Course Completion**: Percentage-based progress indicators

## Customization

### 🎨 Styling
The portal uses Tailwind CSS v4 with a comprehensive design system:
- CSS custom properties for theming
- Dark/light mode support
- Responsive sidebar navigation
- Modern card-based layouts

### 🔧 Configuration
- Modify `portal/settings.py` for app-specific settings
- Customize forms in `portal/forms.py`
- Extend models in `portal/models.py` for additional fields

## API Endpoints

### Authentication
- `POST /portal/login/` - User login
- `GET /portal/logout/` - User logout

### Admin Routes
- `GET /portal/admin/dashboard/` - Admin dashboard
- `GET/POST /portal/admin/trainers/` - Trainer management
- `GET/POST /portal/admin/course-assignment/` - Course assignment
- `GET /portal/admin/lectures/` - Lecture management

### Trainer Routes
- `GET /portal/trainer/dashboard/` - Trainer dashboard
- `GET /portal/trainer/course/<id>/` - Course details
- `GET/POST /portal/trainer/lecture/<id>/attendance/` - Mark attendance

### AJAX Endpoints
- `POST /portal/ajax/mark-attendance/` - Mark attendance via AJAX

## Security Features

- **Authentication Required**: All views require login
- **Permission Checks**: Role-based access control
- **CSRF Protection**: Built-in Django CSRF protection
- **Input Validation**: Form validation and sanitization

## Browser Support

- **Modern Browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- **Mobile**: Responsive design for mobile devices
- **JavaScript**: Required for interactive features

## Contributing

1. Follow Django coding standards
2. Add tests for new features
3. Update documentation for changes
4. Use meaningful commit messages

## License

This project is part of the School Management System and follows the same licensing terms.

## Support

For technical support or questions:
- Check the Django documentation
- Review the code comments
- Contact the development team

---

**Note**: This portal app is designed to work with the existing 'example' app models (Course, Student, Batch). Ensure these models exist and are properly configured before using the portal.
