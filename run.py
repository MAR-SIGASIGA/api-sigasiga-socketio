from dotenv import load_dotenv

load_dotenv()

import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.uvicorn.HOST,
        port=settings.uvicorn.PORT,
        reload=settings.uvicorn.RELOAD,
        workers=settings.uvicorn.WORKERS,
    )
