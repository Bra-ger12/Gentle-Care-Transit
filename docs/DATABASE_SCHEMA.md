# Database Schema - Gentle Care Transit (PostgreSQL)

## Entity Relationship Diagram (ERD)

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ email (UNIQUE)  │
│ phone           │
│ password_hash   │
│ role            │
│ is_active       │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
    ┌────┴──────────────────────┐
    │                           │
    ▼                           ▼
┌──────────────┐        ┌──────────────┐
│   Patient    │        │    Driver    │
├──────────────┤        ├──────────────┤
│ id (PK)      │        │ id (PK)      │
│ user_id (FK) │        │ user_id (FK) │
│ full_name    │        │ full_name    │
│ dob          │        │ license_num  │
│ blood_type   │        │ rating       │
│ allergies    │        │ availability │
│ medical_note │        │ document_url │
│ special_need │        └──────────────┘
│ verified_at  │              │
└──────────────┘              │
    │                         ▼
    │                    ┌──────────────┐
    │                    │   Vehicle    │
    │                    ├──────────────┤
    │                    │ id (PK)      │
    │                    │ driver_id(FK)│
    │                    │ plate_number │
    │                    │ type         │
    │                    │ capacity     │
    │                    │ color        │
    │                    │ insurance_no │
    │                    │ is_active    │
    │                    └──────────────┘
    │
    ▼
┌──────────────────┐
│ BookingRequest   │
├──────────────────┤
│ id (PK)          │
│ patient_id (FK)  │
│ pickup_lat       │
│ pickup_lng       │
│ pickup_address   │
│ dropoff_lat      │
│ dropoff_lng      │
│ dropoff_address  │
│ appointment_type │
│ appointment_date │
│ scheduled_time   │
│ special_needs    │
│ status           │
│ created_at       │
│ updated_at       │
└────────┬─────────┘
         │
         ▼
    ┌────────────┐
    │   Trip     │
    ├─────���──────┤
    │ id (PK)    │
    │ booking_id │
    │ driver_id  │
    │ vehicle_id │
    │ status     │
    │ started_at │
    │ ended_at   │
    │ distance_km│
    │ duration_min│
    └────┬───────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
    ┌────────────┐   ┌──────────┐
    │  Billing   │   │ Rating   │
    ├────────────┤   ├──────────┤
    │ id (PK)    │   │ id (PK)  │
    │ trip_id(FK)│   │ trip_id  │
    │ base_fare  │   │ patient_id│
    │ distance   │   │ driver_id│
    │ time_charge│   │ score    │
    │ total      │   │ comment  │
    │ payment_st │   │ created_at│
    │ paid_date  │   └──────────┘
    └────────────┘

┌────────────────────┐
│  Notification      │
├────────────────────┤
│ id (PK)            │
│ user_id (FK)       │
│ title              │
│ body               │
│ type               │
│ related_id         │
│ is_read            │
│ created_at         │
└────────────────────┘
```

## PostgreSQL Table Definitions

### 1. Create UUID Extension
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### 2. Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('patient', 'driver', 'admin')),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    otp_code VARCHAR(6),
    otp_expires_at TIMESTAMP WITH TIME ZONE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE NULL
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);
```

### 3. Patients Table
```sql
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    blood_type VARCHAR(10),
    allergies TEXT,
    medical_notes TEXT,
    special_needs TEXT,
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    verified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patients_user_id ON patients(user_id);
CREATE INDEX idx_patients_full_name ON patients(full_name);
```

### 4. Drivers Table
```sql
CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    license_expiry DATE,
    date_of_birth DATE,
    rating NUMERIC(3,2) DEFAULT 5.0,
    total_trips INTEGER DEFAULT 0,
    availability_status VARCHAR(20) DEFAULT 'offline' CHECK (availability_status IN ('online', 'offline', 'on_trip')),
    current_location_lat NUMERIC(10,8),
    current_location_lng NUMERIC(11,8),
    last_location_update TIMESTAMP WITH TIME ZONE,
    background_check_status VARCHAR(20) DEFAULT 'pending',
    document_url VARCHAR(500),
    verified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_drivers_user_id ON drivers(user_id);
CREATE INDEX idx_drivers_license_number ON drivers(license_number);
CREATE INDEX idx_drivers_availability ON drivers(availability_status);
CREATE INDEX idx_drivers_location ON drivers USING GIST (
    ll_to_earth(current_location_lat, current_location_lng)
);
```

### 5. Vehicles Table
```sql
CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    plate_number VARCHAR(50) UNIQUE NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL CHECK (vehicle_type IN ('sedan', 'suv', 'minivan', 'wheelchair_accessible')),
    capacity INTEGER DEFAULT 4,
    color VARCHAR(50),
    make VARCHAR(100),
    model VARCHAR(100),
    year INTEGER,
    insurance_number VARCHAR(100),
    insurance_expiry DATE,
    is_active BOOLEAN DEFAULT TRUE,
    verification_status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vehicles_driver_id ON vehicles(driver_id);
CREATE INDEX idx_vehicles_plate_number ON vehicles(plate_number);
CREATE INDEX idx_vehicles_is_active ON vehicles(is_active);
```

### 6. Booking Requests Table
```sql
CREATE TABLE booking_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    pickup_latitude NUMERIC(10,8) NOT NULL,
    pickup_longitude NUMERIC(11,8) NOT NULL,
    pickup_address TEXT NOT NULL,
    pickup_place_id VARCHAR(255),
    dropoff_latitude NUMERIC(10,8) NOT NULL,
    dropoff_longitude NUMERIC(11,8) NOT NULL,
    dropoff_address TEXT NOT NULL,
    dropoff_place_id VARCHAR(255),
    appointment_type VARCHAR(100) NOT NULL CHECK (appointment_type IN ('dialysis', 'physiotherapy', 'antenatal', 'checkup', 'follow_up')),
    appointment_date DATE NOT NULL,
    appointment_time TIME,
    scheduled_datetime TIMESTAMP WITH TIME ZONE,
    special_needs TEXT,
    passenger_count INTEGER DEFAULT 1,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'assigned', 'cancelled', 'completed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    cancellation_reason TEXT
);

CREATE INDEX idx_booking_patient_id ON booking_requests(patient_id);
CREATE INDEX idx_booking_status ON booking_requests(status);
CREATE INDEX idx_booking_appointment_date ON booking_requests(appointment_date);
CREATE INDEX idx_booking_created_at ON booking_requests(created_at);
CREATE INDEX idx_booking_scheduled_datetime ON booking_requests(scheduled_datetime);
```

### 7. Trips Table
```sql
CREATE TABLE trips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_request_id UUID NOT NULL UNIQUE REFERENCES booking_requests(id) ON DELETE CASCADE,
    driver_id UUID REFERENCES drivers(id) ON DELETE SET NULL,
    vehicle_id UUID REFERENCES vehicles(id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'assigned' CHECK (status IN ('assigned', 'in_progress', 'arrived', 'completed', 'cancelled')),
    assigned_at TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE,
    arrived_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    distance_km NUMERIC(10,3),
    duration_minutes INTEGER,
    estimated_fare NUMERIC(10,2),
    actual_fare NUMERIC(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trips_driver_id ON trips(driver_id);
CREATE INDEX idx_trips_booking_id ON trips(booking_request_id);
CREATE INDEX idx_trips_status ON trips(status);
CREATE INDEX idx_trips_created_at ON trips(created_at);
```

### 8. Billing Table
```sql
CREATE TABLE billing (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trip_id UUID NOT NULL UNIQUE REFERENCES trips(id) ON DELETE CASCADE,
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    driver_id UUID REFERENCES drivers(id) ON DELETE SET NULL,
    base_fare NUMERIC(10,2) DEFAULT 0,
    distance_km NUMERIC(10,3),
    distance_rate NUMERIC(10,2),
    distance_charge NUMERIC(10,2) DEFAULT 0,
    duration_minutes INTEGER,
    time_rate NUMERIC(10,2),
    time_charge NUMERIC(10,2) DEFAULT 0,
    discount_amount NUMERIC(10,2) DEFAULT 0,
    discount_reason VARCHAR(255),
    tax_amount NUMERIC(10,2) DEFAULT 0,
    total_amount NUMERIC(10,2) NOT NULL,
    payment_method VARCHAR(50),
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded')),
    paid_at TIMESTAMP WITH TIME ZONE,
    invoice_number VARCHAR(50) UNIQUE,
    invoice_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_billing_trip_id ON billing(trip_id);
CREATE INDEX idx_billing_patient_id ON billing(patient_id);
CREATE INDEX idx_billing_payment_status ON billing(payment_status);
CREATE INDEX idx_billing_invoice_number ON billing(invoice_number);
```

### 9. Ratings Table
```sql
CREATE TABLE ratings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trip_id UUID NOT NULL UNIQUE REFERENCES trips(id) ON DELETE CASCADE,
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    score INTEGER NOT NULL CHECK (score >= 1 AND score <= 5),
    comment TEXT,
    categories JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ratings_trip_id ON ratings(trip_id);
CREATE INDEX idx_ratings_driver_id ON ratings(driver_id);
CREATE INDEX idx_ratings_patient_id ON ratings(patient_id);
```

### 10. Notifications Table
```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    related_model VARCHAR(50),
    related_id UUID,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP WITH TIME ZONE,
    data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
CREATE INDEX idx_notifications_type ON notifications(type);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);
```

### 11. Driver Locations Table (Real-time GPS Tracking)
```sql
CREATE TABLE driver_locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    trip_id UUID REFERENCES trips(id) ON DELETE SET NULL,
    latitude NUMERIC(10,8) NOT NULL,
    longitude NUMERIC(11,8) NOT NULL,
    accuracy NUMERIC(10,2),
    speed NUMERIC(10,2),
    heading NUMERIC(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- PostGIS Index for efficient geospatial queries
CREATE INDEX idx_driver_locations_geom ON driver_locations 
    USING GIST (ll_to_earth(latitude, longitude));
CREATE INDEX idx_driver_locations_driver_id ON driver_locations(driver_id);
CREATE INDEX idx_driver_locations_trip_id ON driver_locations(trip_id);
CREATE INDEX idx_driver_locations_created_at ON driver_locations(created_at);
```

### 12. Support for PostGIS (Optional but recommended)
```sql
-- Enable PostGIS extension for advanced geospatial queries
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS cube;
CREATE EXTENSION IF NOT EXISTS earthdistance;

-- Create a view for nearby drivers
CREATE OR REPLACE VIEW nearby_drivers AS
SELECT 
    d.id,
    d.user_id,
    d.full_name,
    d.current_location_lat,
    d.current_location_lng,
    d.availability_status,
    d.rating,
    v.vehicle_type,
    v.capacity
FROM drivers d
LEFT JOIN vehicles v ON d.id = v.driver_id
WHERE d.availability_status = 'online' AND v.is_active = TRUE;
```

## Constraints & Relationships

| Parent | Child | Type | Delete Action |
|--------|-------|------|---------------|
| users | patients | 1:1 | CASCADE |
| users | drivers | 1:1 | CASCADE |
| users | notifications | 1:N | CASCADE |
| drivers | vehicles | 1:N | CASCADE |
| drivers | trips | 1:N | SET NULL |
| patients | booking_requests | 1:N | CASCADE |
| booking_requests | trips | 1:1 | CASCADE |
| trips | billing | 1:1 | CASCADE |
| trips | ratings | 1:1 | CASCADE |
| drivers | driver_locations | 1:N | CASCADE |

## Migration Strategy

### 1. Create Database
```bash
createdb -U postgres gentle_care_transit
```

### 2. Run Migrations
```bash
# Using Django migrations
python manage.py migrate

# Or using raw SQL
psql -U postgres -d gentle_care_transit -f schema.sql
```

### 3. Create Views & Functions
```bash
psql -U postgres -d gentle_care_transit -f views.sql
psql -U postgres -d gentle_care_transit -f functions.sql
```

### 4. Backup Strategy
```bash
# Full backup
pg_dump -U postgres gentle_care_transit > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
psql -U postgres gentle_care_transit < backup_20260611_120000.sql

# Continuous archival (WAL)
```

## Performance Optimization

### Connection Pooling (pgBouncer)
```ini
[databases]
gentle_care_transit = host=localhost port=5432 dbname=gentle_care_transit

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
```

### Query Optimization
- All foreign keys are indexed
- Geospatial indexes for location queries
- Time-series data indexed by created_at
- Status fields indexed for filtering

## Maintenance Tasks

```sql
-- Vacuum and Analyze
VACUUM ANALYZE;

-- Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) 
FROM pg_tables 
WHERE schemaname != 'pg_catalog' 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Monitor slow queries
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();
```
