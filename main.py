from fastapi import FastAPI

app = FastAPI(
    title="Dot AI",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "project": "Dot AI",
        "status": "running"
    }