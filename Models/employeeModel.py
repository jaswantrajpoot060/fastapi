from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class Employee(BaseModel):
    id: Optional[int] = None
    Name: str
    Email: str
    Dob: datetime
    Salary: Decimal
    EmpCode: int
