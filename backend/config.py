import os

# SecureVyapar Configuration
VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY', '')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'securevyapar-dev-key')

# API Configuration
VIRUSTOTAL_BASE_URL = 'https://www.virustotal.com/api/v3'
MAX_URL_LENGTH = 2048
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Security Settings
RATE_LIMIT per_minute = 60  # VirusTotal free tier limit
SCAN_PATTERNS_COUNT = 7  # Number of rule-based patterns

# Pricing Configuration
FREE_PLAN = 'free'
DETAILED_REPORT = 'detailed'  # ₹299 one-time
QUARTERLY_PLAN = 'quarterly'  # ₹999/quarter

# Assessment Configuration
TOTAL_QUESTIONS = 25
SCORE_RANGE = (0, 100)  # Min, Max
PASSING_SCORE = 80  # Score considered "mostly safe"

# Category Weights (for scoring)
CATEGORY_WEIGHTS = {
    'identity': 0.20,
    'backups': 0.15,
    'devices': 0.15,
    'upi': 0.25,
    'links': 0.25,
}