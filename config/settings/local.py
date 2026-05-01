# CAU HINH MOI TRUONG
from .base import *
from dotenv import load_dotenv
import os

# Nap bien moi truong tu file .env
load_dotenv()

# Khoa bi mat. Uu tien lay tu file .env neu khong co thi dung mac dinh
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-for-dev-only')

# Che do go loi (DEBUG)
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Danh sach cac dia chi duoc phep truy cap web
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '172.0.0.1, localhost').split(',')


# DATABASE
DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite3')

# SQL Server
if DB_ENGINE == 'mssql':
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': os.getenv('DB_NAME', 'QuanLyThuVien'),
            'USER': os.getenv('DB_USER', 'sa'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '1433'),
            'OPTIONS': {
                'driver': 'ODBC Driver 18 for SQL Server',
                'extra_params': 'TrustServerCertificate=yes',
            }
        }
    }

# SQLite
else: 
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
