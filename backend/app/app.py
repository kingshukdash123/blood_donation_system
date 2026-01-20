from fastapi import FastAPI
from app.routes.hospital import route as hospital_route
from app.routes.auth import route as auth_route


app = FastAPI(title='Blood Donation System')

app.include_router(auth_route)
app.include_router(hospital_route)


@app.get("/")
def root():
    return {"status": "ok", "message": "Todo backend running"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "todo-backend"
    }