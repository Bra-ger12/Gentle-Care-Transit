# Gentle Care Transit - Non-Emergency Medical Transportation Platform

A production-ready NEMT platform providing transportation services for patients attending medical appointments (Dialysis, Physiotherapy, Antenatal Visits, Checkups, Follow-up Appointments).

## 📋 Project Architecture

### Tech Stack

**Frontend:**
- Flutter (Patient App, Driver App, Admin Web)
- Riverpod (State Management)
- GoRouter (Navigation)
- Google Maps SDK
- Firebase Cloud Messaging

**Backend:**
- Django 4.2+
- Django REST Framework
- PostgreSQL 14+
- Redis (Caching & Real-time)
- Django Channels (WebSockets)
- Celery (Async Tasks)

**Infrastructure:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- AWS/GCP Ready

## 📁 Project Structure

```
Gentle-Care-Transit/
├── backend/                          # Django Backend
│   ├── config/                       # Django Settings
│   ├── apps/
│   │   ├── accounts/                # User Authentication
│   │   ├── patients/                # Patient Management
│   │   ├── drivers/                 # Driver Management
│   │   ├── vehicles/                # Vehicle Management
│   │   ├── bookings/                # Booking Management
│   │   ├── trips/                   # Trip Management
│   │   ├── billing/                 # Billing & Invoicing
│   │   ├── notifications/           # Notification System
│   │   ├── ratings/                 # Ratings & Reviews
│   │   ├── reports/                 # Analytics & Reports
│   │   └── websockets/              # WebSocket Handlers
│   ├── utils/                       # Shared Utilities
│   ├── middleware/                  # Custom Middleware
│   ├── requirements.txt
│   ├── manage.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── Dockerfile
│
├── patient_app/                      # Flutter Patient App
│   ├── lib/
│   │   ├── core/                    # Core Logic
│   │   ├── data/                    # Data Layer
│   │   ├── domain/                  # Business Logic
│   │   ├── presentation/            # UI Screens
│   │   ├── services/                # External Services
│   │   ├── widgets/                 # Reusable Widgets
│   │   ├── config/                  # App Config
│   │   └── main.dart
│   ├── pubspec.yaml
│   ├── Dockerfile
│   └── build/
│
├── driver_app/                       # Flutter Driver App
│   ├── lib/
│   │   ├── core/
│   │   ├── data/
│   │   ├── domain/
│   │   ├── presentation/
│   │   ├── services/
│   │   ├── widgets/
│   │   ├── config/
│   │   └── main.dart
│   ├── pubspec.yaml
│   └── Dockerfile
│
├── admin_portal/                     # Flutter Web Admin
│   ├── lib/
│   │   ├── core/
│   │   ├── data/
│   │   ├── domain/
│   │   ├── presentation/
│   │   ├── services/
│   │   ├── widgets/
│   │   ├── config/
│   │   └── main.dart
│   ├── pubspec.yaml
│   └── Dockerfile
│
├── docs/                             # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── DATABASE_SCHEMA.md
│   ├── DEPLOYMENT.md
│   ├── ARCHITECTURE.md
│   └── ERD.md
│
├── docker-compose.yml                # Multi-container Setup
├── .github/
│   └── workflows/                    # CI/CD Pipelines
│       ├── backend-tests.yml
│       ├── flutter-build.yml
│       └── deploy.yml
├── .env.example
├── .gitignore
└── LICENSE
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Flutter SDK 3.0+
- Python 3.10+
- PostgreSQL 14+

### Backend Setup
```bash
cd backend
cp .env.example .env
docker-compose up -d
python manage.py migrate
python manage.py createsuperuser
```

### Patient App
```bash
cd patient_app
flutter pub get
flutter run
```

### Driver App
```bash
cd driver_app
flutter pub get
flutter run
```

### Admin Portal
```bash
cd admin_portal
flutter pub get
flutter run -d chrome
```

## 📚 Documentation

- [API Documentation](./docs/API_DOCUMENTATION.md)
- [Database Schema](./docs/DATABASE_SCHEMA.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)

## 🔐 Features

### Patient App
- ✅ Register/Login with OTP Verification
- ✅ Book & Schedule Rides
- ✅ Live Driver Tracking
- ✅ Trip History & Billing
- ✅ Rating & Reviews
- ✅ Push Notifications

### Driver App
- ✅ Document Upload & Verification
- ✅ Vehicle Management
- ✅ Trip Accept/Reject
- ✅ Live GPS Broadcasting
- ✅ Earnings Dashboard
- ✅ Real-time Notifications

### Admin Portal
- ✅ Analytics Dashboard
- ✅ User & Vehicle Management
- ✅ Booking & Trip Management
- ✅ Driver Assignment
- ✅ Billing & Reports
- ✅ Real-time Monitoring

## 🎨 Design System

**Color Palette:**
- Primary: `#1A6B8A` (Medical Blue)
- Secondary: `#4CAF82` (Healthcare Green)
- Background: `#F8FAFB` (Light Gray)
- Success: `#4CAF82`
- Error: `#F44336`
- Warning: `#FF9800`

**Design Principles:**
- Modern & Professional
- Elder-Friendly (Large Text, High Contrast)
- Medical Grade UI
- Accessible (WCAG 2.1 AA)

## 📞 Support

For issues and questions, please create an issue in the repository.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- Senior Software Architect
- Senior Flutter Developer
- Senior Django Developer
- UI/UX Designer
- DevOps Engineer
- Database Architect

---

**Last Updated:** June 2026
