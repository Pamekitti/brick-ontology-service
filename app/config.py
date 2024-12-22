from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# Define base directory path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Brick API"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Brick Graph Configuration
    ASSETS_DIR: str = os.path.join(BASE_DIR, '.assets')
    
    @property
    def BUILDING_TTL_FILES(self) -> List[str]:
        return [
            os.path.join(self.ASSETS_DIR, "building2.ttl"),
            os.path.join(self.ASSETS_DIR, "campus_lab_1.ttl"),
            os.path.join(self.ASSETS_DIR, "campus_office_1.ttl"),
            os.path.join(self.ASSETS_DIR, "custom_building_1.ttl"),
            os.path.join(self.ASSETS_DIR, "hospital_wing_east.ttl"),
            os.path.join(self.ASSETS_DIR, "lab_building_1.ttl"),
            os.path.join(self.ASSETS_DIR, "office_building_1.ttl"),
            os.path.join(self.ASSETS_DIR, "retail_store_1.ttl")
        ]
    
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()