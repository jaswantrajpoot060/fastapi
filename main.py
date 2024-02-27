from fastapi import FastAPI, HTTPException, Depends
import pyodbc

import config
from employeeModel import Employee
from connection_db import connect_to_database
from employeeServices import getall_employee, get_employee

app = FastAPI()


@app.get("/employee")
async def get_all_employee(conn=Depends(connect_to_database)):
    return getall_employee(conn)


@app.get("/employee/{id}")
def getbyid_employee(id: int, conn=Depends(connect_to_database)):
    return get_employee(id, conn)


@app.post("/employee")
def create_employee(employee: Employee):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Call the stored procedure to insert data
        cursor.execute("EXEC [Usp_Insert_Employee] @Name = ?, @Email = ?, @Dob = ?, @Salary = ?, @EmpCode = ?",
                       (employee.Name, employee.Email, employee.Dob, employee.Salary, employee.EmpCode))
        # Commit the transaction
        conn.commit()

        return {"message": "Data inserted successfully"}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database insert error: {str(e)}")
    finally:
        cursor.close()
        conn.close()


@app.put("/employee/{id}")
def update_employee(id: int, employee: Employee):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # cursor.execute("EXEC UpdateData ?, ?, ?, ?, ?, ?",
        #                (data.id, data.name, data.email, data.dob, data.salary, data.emp_code))
        cursor.execute("EXEC [Usp_Update_Employee] @Id = ?, @Name = ?, @Email = ?, "
                       "@Dob = ?, @Salary = ?, @EmpCode = ?",
                       (id, employee.Name, employee.Email, employee.Dob, employee.Salary, employee.EmpCode))

        # Commit the transaction
        conn.commit()
        return {"message": "Data updated successfully"}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database update error: {str(e)}")
    finally:
        cursor.close()
        conn.close()


@app.delete("/employee/{id}")
def delete_employee(id: int):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC Usp_Delete_Employee ?", (id,))
        conn.commit()
        return {"message": "Data deleted successfully"}
    except pyodbc.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database delete error: {str(e)}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
