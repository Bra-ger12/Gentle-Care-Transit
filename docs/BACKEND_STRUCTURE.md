# Backend Project Structure

```
backend/
├── manage.py
├── requirements.txt
├── .env.example
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── wsgi.py
├── asgi.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py              # Main Django settings
│   ├── urls.py                  # Root URL configuration
│   ├── asgi.py                  # ASGI for WebSockets
│   ├── middleware.py            # Custom middleware
│   ├── celery.py                # Celery configuration
│   ├── redis_config.py          # Redis configuration
│   └── constants.py             # App-wide constants
│
├── apps/
│   │
│   ├── accounts/                # User Authentication & Management
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── permissions.py
│   │   ├── authentication.py    # JWT Auth
│   │   ├── otp.py               # OTP logic
│   │   └── tests.py
│   │
│   ├── patients/                # Patient Management
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── signals.py
│   │   └── tests.py
│   │
│   ├── drivers/                 # Driver Management
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── signals.py
│   │   └── tests.py
│   │
│   ├── vehicles/                # Vehicle Management
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests.py
│   │
│   ├── bookings/                # Booking Management
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── filters.py
│   │   ├── signals.py
│   │   └── tests.py
│   │
│   ├── trips/                   # Trip Management
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── signals.py
│   │   ├── websocket_handlers.py
│   │   └── tests.py
│   │
│   ├── billing/                 # Billing & Invoicing
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── invoice_generator.py # PDF Generation
│   │   ├── tasks.py             # Celery tasks
│   │   └── tests.py
│   │
│   ├── ratings/                 # Ratings & Reviews
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests.py
│   │
│   ├── notifications/           # Notification System
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── signals.py
│   │   ├── firebase_service.py  # Firebase FCM
│   │   ├── tasks.py
│   │   └── tests.py
│   │
│   ├── reports/                 # Analytics & Reports
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── analytics.py
│   │   └── tests.py
│   │
│   ├── websockets/              # WebSocket Handlers
│   │   ├── __init__.py
│   │   ├── consumers.py         # Channel consumers
│   │   ├── routing.py           # WebSocket routing
│   │   ├── auth.py              # WebSocket auth
│   │   └── handlers.py
│   │
│   └── __init__.py
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py               # Utility functions
│   ├── validators.py            # Custom validators
│   ├── pagination.py            # Custom pagination
│   ├── filters.py               # DRF filters
│   ├── exceptions.py            # Custom exceptions
│   ├── response.py              # Response formatting
│   ├── logger.py                # Logging setup
│   ├── decorators.py            # Custom decorators
│   ├── caching.py               # Caching utilities
│   └── storage.py               # File storage config
│
├── middleware/
│   ├── __init__.py
│   ├── request_logging.py
│   ├── error_handler.py
│   ├── cors_middleware.py
│   └── rate_limiting.py
│
├── static/
│   └── .gitkeep
│
├── media/
│   ├── documents/
│   ├── invoices/
│   └── .gitkeep
│
└── tests/
    ├── __init__.py
    ├── test_accounts.py
    ├── test_bookings.py
    ├── test_trips.py
    ├── test_billing.py
    └── factories.py
```

## Key Configuration Files

### requirements.txt
```
Django==4.2.0
djangorestframework==3.14.0
django-cors-headers==4.0.0
django-filter==23.1
django-celery-beat==2.5.0
django-celery-results==2.5.0
django-environ==0.10.0
psycopg2-binary==2.9.6
psycopg2==2.9.6
celery==5.3.1
redis==4.5.5
channels==4.0.0
channels-redis==4.1.0
daphne==4.0.0
djangorestframework-simplejwt==5.2.2
django-filter==23.1
Pillow==9.5.0
requests==2.31.0
googlemaps==4.10.0
firebase-admin==6.2.0
reportlab==4.0.4
PyPDF2==3.0.1
gunicorn==20.1.0
python-decouple==3.8
```

## Django Apps Configuration

All apps follow this structure:
- Models (Database layer)
- Serializers (Data validation & transformation)
- Views (Business logic)
- URLs (Routing)
- Admin (Django admin registration)
- Tests (Unit tests)
- Signals (Event handlers)
- Tasks (Async tasks for Celery)

## Middleware Stack

1. CORS Middleware
2. Request Logging Middleware
3. Error Handler Middleware
4. Rate Limiting Middleware
5. Custom Authentication Middleware

## Database Models

All models located in `apps/*/models.py`:
- User model with role-based access
- Patient profile with medical info
- Driver profile with ratings
- Vehicle management
- Booking requests with status tracking
- Trip management with real-time tracking
- Billing with invoice generation
- Ratings with feedback
- Notifications system
- Driver location tracking
