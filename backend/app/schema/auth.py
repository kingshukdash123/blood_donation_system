from pydantic import BaseModel, Field
from typing import Annotated, Literal, Optional
from decimal import Decimal
from datetime import date


class BaseUser(BaseModel):
    name: Annotated[str, Field(description="Name of the user")]
    phone: Annotated[str, Field(description="Phone number of the user")]
    password: Annotated[str, Field(description="Password of the user")]

    role: Annotated[
        Literal["hospital", "blood_bank", "donor", "admin"],
        Field(description="Role of the user")
    ]

    isVerified: Annotated[
        bool,
        Field(default=False, description="Is the user verified or not")
    ]

    latitude: Annotated[
        Decimal,
        Field(max_digits=9, decimal_places=6, description="Latitude of the user")
    ]

    longitude: Annotated[
        Decimal,
        Field(max_digits=9, decimal_places=6, description="Longitude of the user")
    ]

    address: Annotated[str, Field(description="Address of the user")]


class CreateHospitalUser(BaseUser):
    role: Literal["hospital"]


class CreateBloodBankUser(BaseUser):
    role: Literal["blood_bank"]


class CreateDonorUser(BaseUser):
    role: Literal["donor"]

    bloodGroup: Annotated[
        Literal["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        Field(description="Blood group of the donor")
    ]

    lastDonationDate: Annotated[
        Optional[date],
        Field(default=None, description="Last donation date of the donor")
    ]

    isAvailable: Annotated[
        bool,
        Field(default=True, description="Is donor available for donation")
    ]


class UserLogIn(BaseModel):
    role: Annotated[Literal["hospital", "blood_bank", "donor", "admin"], Field(..., description="Role of the user")]
    phone: Annotated[str, Field(..., description='Phone number of the user')]
    password: Annotated[str, Field(..., description='Password of the user')]
