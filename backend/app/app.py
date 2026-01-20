from fastapi import FastAPI

app = FastAPI(title='Blood Donation System')




@app.get("/")
def root():
    return {"status": "ok", "message": "Todo backend running"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "todo-backend"
    }