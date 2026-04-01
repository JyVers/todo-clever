from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv
from routes.city import router
from database import init_db

load_dotenv()
port = os.environ["PORT"]
app = FastAPI()

init_db()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
