import os
from dotenv import load_dotenv

load_dotenv()

# Helper for boolean environment variables
def get_bool_env(var_name: str, default: bool = False) -> bool:
    value = os.getenv(var_name, str(default)).lower()
    return value in ('true', '1', 'yes', 'on')

# Define standard Python classes for settings
class AppSettings:
    def __init__(self):
        self.APP_NAME: str = os.getenv('APP_NAME', 'API Manager')
        self.VERSION: str = os.getenv('APP_VERSION', '0.1.0')
        self.DEBUG: bool = get_bool_env('APP_DEBUG', False)
        self.DOCS_ENABLED: bool = get_bool_env('APP_DOCS_ENABLED', True)
        self.ENVIRONMENT: str = os.getenv('APP_ENVIRONMENT', 'development')

class UvicornSettings:
     def __init__(self):
        self.HOST: str = os.getenv('UVICORN_HOST', '0.0.0.0')
        self.PORT: int = int(os.getenv('UVICORN_PORT', '8000'))
        self.WORKERS: int = int(os.getenv('UVICORN_WORKERS', '1'))
        self.RELOAD: bool = get_bool_env('UVICORN_RELOAD', True)

class RedisSettings:
    def __init__(self):
        self.HOST: str = os.getenv('REDIS_HOST', 'redis-sigasiga')
        self.PORT: int = int(os.getenv('REDIS_PORT', '6379'))
        self.DB: int = int(os.getenv('REDIS_DB', '0'))
        # self.PASSWORD: str = os.getenv('REDIS_PASSWORD', None)

class ApiSigaSigaRestSettings:
    def __init__(self):
        self.HOST: str = os.getenv('URL_API-SIGASIGA-REST', 'http://api-sigasiga-rest')
        self.PORT: int = int(os.getenv('PORT_API-SIGASIGA-REST', '5000'))
        self.URL: str = f"{self.HOST}:{self.PORT}"

# Main settings class
class Settings:
    def __init__(self):

        # Instantiate nested settings
        self.app: AppSettings = AppSettings()
        self.uvicorn: UvicornSettings = UvicornSettings()
        self.redis: RedisSettings = RedisSettings()
        self.api_sigasiga_rest: ApiSigaSigaRestSettings = ApiSigaSigaRestSettings()


# Create the settings instance
settings = Settings()
