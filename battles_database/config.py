import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Настройки базы данных
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'battles_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

    # Секретный ключ для Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # 👇 ИСПРАВЛЕННЫЙ БЛОК ПОДКЛЮЧЕНИЯ К БД
    _db_url = os.getenv('DATABASE_URL')
    if _db_url:
        # Render дает ссылку, начинающуюся на postgres://, 
        # а SQLAlchemy 2.0 требует postgresql://
        if _db_url.startswith("postgres://"):
            _db_url = _db_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = _db_url
    else:
        # Локальный запуск
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 👇 Разрешение на редактирование (по умолчанию True)
    ALLOW_EDITING = os.getenv('ALLOW_EDITING', 'true').lower() == 'true'

class TestConfig(Config):
    TESTING = True
    DB_NAME = os.getenv('TEST_DB_NAME', 'battles_test_db')
