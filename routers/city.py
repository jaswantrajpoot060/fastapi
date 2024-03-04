from fastapi import APIRouter, Depends
from Configuration.connection_db import connect_to_database
from Models.cityModel import City
from Services.cityServices import createdata_city, updatedata_city, delete_data_city, get_city, getall_city

router = APIRouter()


# City crud Api
@router.get("/city", tags=["city"])
async def get_all_city(conn=Depends(connect_to_database)):
    return getall_city(conn)


@router.get("/city/{id}", tags=["city"])
def getbyid_city(id: int, conn=Depends(connect_to_database)):
    return get_city(id, conn)


@router.post("/city", tags=["city"])
def create_city(city: City):
    return createdata_city(city)


@router.put("/city/{id}", tags=["city"])
def update_city(id: int, city: City):
    return updatedata_city(id, city)


@router.delete("/city/{id}", tags=["city"])
def delete_city(id: int):
    return delete_data_city(id)
