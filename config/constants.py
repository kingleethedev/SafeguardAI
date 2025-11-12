# Application Constants

# Threat Level Thresholds
THREAT_THRESHOLDS = {
    'HIGH': 0.7,
    'MEDIUM': 0.4,
    'LOW': 0.0
}

# Social Media Sources
SOCIAL_MEDIA_SOURCES = {
    'TWITTER': 'twitter',
    'FACEBOOK': 'facebook',
    'INSTAGRAM': 'instagram',
    'REDDIT': 'reddit',
    'OTHER': 'other'
}

# Incident Types with Weights
INCIDENT_WEIGHTS = {
    'protest': 0.6,
    'violence': 0.9,
    'accident': 0.5,
    'natural_disaster': 0.8,
    'other': 0.3
}

# CCTV Analysis Settings
CCTV_SETTINGS = {
    'FRAME_INTERVAL': 30,  # Process every 30th frame
    'CONFIDENCE_THRESHOLD': 0.5,
    'MAX_FRAME_SIZE': (640, 640)
}

# API Settings (if using external APIs)
API_SETTINGS = {
    'TIMEOUT': 30,
    'RETRY_ATTEMPTS': 3,
    'RATE_LIMIT_DELAY': 1  # seconds
}

# File Upload Settings
UPLOAD_SETTINGS = {
    'MAX_FILE_SIZE': 50 * 1024 * 1024,  # 50MB
    'ALLOWED_VIDEO_EXTENSIONS': ['.mp4', '.avi', '.mov', '.mkv'],
    'ALLOWED_IMAGE_EXTENSIONS': ['.jpg', '.jpeg', '.png', '.gif']
}

# Database Settings
DB_SETTINGS = {
    'BATCH_SIZE': 1000,
    'QUERY_TIMEOUT': 30
}