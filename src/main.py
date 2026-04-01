from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv
from src.routes.todos import router
from src.database import init_db

load_dotenv()
port = int(os.environ.get("PORT", 8000))
app = FastAPI()

init_db()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
