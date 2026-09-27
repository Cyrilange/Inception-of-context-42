from fastapi import FastAPI

app = FastAPI(
    title="Inception-of-Context",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ioc",
    }
