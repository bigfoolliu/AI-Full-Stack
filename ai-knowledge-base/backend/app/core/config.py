import os

APP_NAME = "AI Knowledge Base Backend"
ALLOWED_ORIGINS = ["http://localhost:5173", "http://localhost:5174"]

MOCK_USERNAME = "admin"
MOCK_PASSWORD = "123456"
MOCK_TOKEN = "mock-token"
MOCK_USER = {
    "id": 1,
    "username": "admin",
    "nickname": "Admin",
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
