from http.client import HTTPException
import pyodbc
from fastapi import Depends
from Configuration.connection_db import connect_to_database
from Models.cityModel import City


def getall_city(conn=Depends(connect_to_database)):
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC [Usp_City_Get]")
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return data
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
    finally:
        cursor.close()


def get_city(id: int, conn=Depends(connect_to_database)):
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC [Usp_City_Get] @id = ?", (id,))
        row = cursor.fetchone()
        if row is not None:
            # Convert the row to a dictionary
            columns = [column[0] for column in cursor.description]
            data = dict(zip(columns, row))
            return data
        else:
            raise HTTPException(status_code=404, detail="City not found")
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
    finally:
        cursor.close()


def createdata_city(city: City):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Call the stored procedure to insert data
        cursor.execute("EXEC [Usp_City_Insert] @StateId = ?, @Name = ?, @CityCode = ?, @CreatedBy = ?",
                       (city.StateId, city.Name, city.CityCode, 1))
        # Commit the transaction
        conn.commit()

        return {"message": "Data inserted successfully"}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database insert error: {str(e)}")
    finally:
        cursor.close()
        conn.close()


def updatedata_city(id: int, city: City):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # cursor.execute("EXEC UpdateData ?, ?, ?, ?, ?, ?",
        #                (data.id, data.name, data.email, data.dob, data.salary, data.emp_code))
        cursor.execute("EXEC [Usp_City_Update] @Id = ?, @StateId = ?, @Name = ?, @CityCode = ?, @CreatedBy = ?",
                       (id, city.StateId, city.Name, city.CityCode, 1))

        # Commit the transaction
        conn.commit()
        return {"message": "Data updated successfully"}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database update error: {str(e)}")
    finally:
        cursor.close()
        conn.close()


def delete_data_city(id: int):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC Usp_City_Delete ?", (id,))
        conn.commit()
        return {"message": "Data deleted successfully"}
    except pyodbc.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database delete error: {str(e)}")
    finally:
        cursor.close()
        conn.close()
