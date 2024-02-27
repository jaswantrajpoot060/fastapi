from http.client import HTTPException

import pyodbc
from fastapi import Depends

from connection_db import connect_to_database
from employeeModel import Employee


def getall_employee(conn=Depends(connect_to_database)):
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC [Usp_Get_Employee]")
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return data
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
    finally:
        cursor.close()
def get_employee(id: int, conn=Depends(connect_to_database)):
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC [Usp_Get_EmployeeId] @id = ?", (id,))
        row = cursor.fetchone()
        if row is not None:
            # Convert the row to a dictionary
            columns = [column[0] for column in cursor.description]
            data = dict(zip(columns, row))
            return data
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
    finally:
        cursor.close()


def createdata_employee(employee: Employee):
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


def updatedata_employee(id: int, employee: Employee):
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


def delete_data_employee(id: int):
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
