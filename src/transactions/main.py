import os
from fastapi import FastAPI
from dotenv import load_dotenv
from routes.transactions import router

load_dotenv()

app = FastAPI()
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)