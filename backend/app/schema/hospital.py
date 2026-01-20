from pydantic import BaseModel, Field
from typing import Annotated, Literal


class CreateBloodRequest(BaseModel):
    hospitalId: Annotated[int, Field(..., description='Id of the Hospital')]
    bloodGroup: Annotated[Literal['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], Field(..., description='Requested blood Group')]
    unitsRequired: Annotated[int, Field(..., description='How many units of blood are required')]
    status: Annotated[Literal['PENDING', 'FULFILLED', 'ALERTED'], Field(..., description='Status of request')]
    bloodBankId: Annotated[int, Field(..., description='Id of requested blood bank')]