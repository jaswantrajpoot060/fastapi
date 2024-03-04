from fastapi import APIRouter, Depends
from Configuration.connection_db import connect_to_database
from Models.employeeModel import Employee
from Services.employeeServices import createdata_employee, updatedata_employee, delete_data_employee, get_employee, \
    getall_employee

router = APIRouter()


# Employee crud Api
@router.get("/employee", tags=["employee"])
async def get_all_employee(conn=Depends(connect_to_database)):
    return getall_employee(conn)


@router.get("/employee/{id}", tags=["employee"])
def getbyid_employee(id: int, conn=Depends(connect_to_database)):
    return get_employee(id, conn)


@router.post("/employee", tags=["employee"])
def create_employee(employee: Employee):
    return createdata_employee(employee)


@router.put("/employee/{id}", tags=["employee"])
def update_employee(id: int, employee: Employee):
    return updatedata_employee(id, employee)


@router.delete("/employee/{id}", tags=["employee"])
def delete_employee(id: int):
    return delete_data_employee(id)
