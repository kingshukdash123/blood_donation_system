from fastapi import APIRouter, Depends, HTTPException
from app.schema.hospital import CreateBloodRequest
from app.db.query.hospital import createBloodRequest

route = APIRouter(prefix="/hospital", tags=["Hospital"])


@route.post("/blood-requests")
def all_tasks(bloodRequestDetails: CreateBloodRequest):
    try:
        return createBloodRequest(bloodRequestDetails)
    # except HTTPException:
    #     raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error") 