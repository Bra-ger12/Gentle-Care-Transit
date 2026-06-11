"""
Utility helper functions.
"""

import uuid
from django.utils.text import slugify

def generate_invoice_number():
    """
    Generate a unique invoice number.
    Format: INV-YYYYMMDD-XXXX
    """
    from datetime import datetime
    return f"INV-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

def generate_otp(length=6):
    """
    Generate a random OTP.
    """
    import random
    return ''.join(random.choices('0123456789', k=length))

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula.
    Returns distance in kilometers.
    """
    from math import radians, cos, sin, asin, sqrt
    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r
